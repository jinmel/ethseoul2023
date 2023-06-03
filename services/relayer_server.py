from dataclasses import dataclass
import json
import os
from string import Template
import tempfile

from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import ezkl_lib
import torch
from web3 import HTTPProvider, Web3
from web3.middleware import construct_sign_and_send_raw_middleware
import rlp
import eth_utils
import eth_account
from eth.vm.forks.arrow_glacier.transactions import ArrowGlacierTransactionBuilder as TransactionBuilder

from models import SimpleModel
from transaction_features import EtherScan


INFURA_URL='https://goerli.infura.io/v3/5c92864a308b45b6a8c3559b63cb5b38'
THEGRAPH_URL='https://api.thegraph.com/subgraphs/name/chee-chyuan/walletfactory'
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
ACCOUNT = eth_account.Account.from_key(PRIVATE_KEY)
WALLET_FACTORY_CONTRACT = '0xe652a8E383F55cB8D5c4fD2fD31849065231147F'


w3 = Web3(HTTPProvider(INFURA_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
contract_abi = json.load(open('./Wallet.json', 'r'))
factory_contract_abi = json.load(open('./WalletFactory.json', 'r'))


class RpcRequest(BaseModel):
    jsonrpc: str
    method: str
    params: list | None = None
    id: str | int | None = None


def load_model(model_path):
    ckpt = torch.load(model_path)
    model = SimpleModel()
    model.load_state_dict(ckpt)
    model.eval()
    return model


model = load_model('./assets/model.pt')

app = FastAPI()


def ezkl_prove(input_filename, proof_filename):
    cmd = (f'ezkl prove -D {input_filename} -M ./assets/model.onnx --pk-path ./assets/pk.key --proof-path {proof_filename} --params-path ./assets/kzg.params --transcript=evm --circuit-params-path ./assets/circuit.params')
    print('Running %s' % cmd)
    os.system(cmd)


def generate_proof(input_data, output):
    data = dict(input_shapes=[list(input_data.shape)],
                input_data=[input_data.tolist()],
                output_data=[o.reshape([-1]).tolist() for o in output])
    with tempfile.TemporaryDirectory() as tmpdirname:
        input_filename = os.path.join(tmpdirname, 'input.json')
        proof_filename = os.path.join(tmpdirname, 'proof.enc')
        print(f'Dumping input {data} to {input_filename}')
        with open(input_filename, 'w') as f:
            json.dump(data, f)
        print(f'Genearting proof to {proof_filename}')
        ezkl_prove(input_filename, proof_filename)
        # ezkl_lib.prove(input_filename,
        #                './assets/model.onnx',
        #                './assets/pk.key',
        #                proof_filename,
        #                './assets/kzg.params',
        #                'evm',
        #                'single',
        #                './assets/circuit.params')
        print('Proof: %s' % ezkl_lib.print_proof_hex(proof_filename))
        with open(proof_filename, 'rb') as proof_file:
            return proof_file.read()


async def get_features(address):
    etherscan = EtherScan(address, base_url='https://api-goerli.etherscan.io/api')
    features = await etherscan.get_features_list()
    assert len(features) == 16, 'Expect 16 features'
    return features


async def check_fraud(input_data):
    with torch.no_grad():
        input_data = torch.tensor(input_data, dtype=torch.float32)
        output = model(input_data).cpu().numpy()
    proof = generate_proof(input_data, output)
    score = output[0]
    return score, proof


query_template = Template("""
query MyQuery {
    deployedWallets(where: {owner: "$address"}) {
        owner
        transactionHash
        walletAddress
        blockTimestamp
        id
        blockNumber
    }
}
""")


async def get_contract_wallet_address(eoa_address):
    """Get contract wallet address from EOA wallet address using the graph
    protocol."""
    async with httpx.AsyncClient() as client:
        response = await client.post(THEGRAPH_URL, json={
            "query": query_template.substitute(address=eoa_address),
            "variables":{}})
    return response.json()['data']['deployedWallets'][0]['walletAddress']


class SerializedTransaction(rlp.Serializable):
    fields = [
        ('nonce', rlp.sedes.big_endian_int),
        ('gasPrice', rlp.sedes.big_endian_int),
        ('gasLimit', rlp.sedes.big_endian_int),
        ('to', rlp.sedes.Text.fixed_length(20, allow_empty=True)),
        ('value', rlp.sedes.big_endian_int),
        ('data', rlp.sedes.Binary(allow_empty=True)),
        ('from', rlp.sedes.Text.fixed_length(20, allow_empty=True)),
        ('r', rlp.sedes.binary),
        ('v', rlp.sedes.big_endian_int),
        ('s', rlp.sedes.binary)
    ]


@dataclass
class Transaction:
    nonce: int
    gasPrice: int
    gasLimit: int
    to: str
    value: int
    data: bytes
    from_: str
    r: bytes
    v: int
    s: bytes

    @classmethod
    def from_hexstring(cls, data):
        data = eth_utils.to_bytes(hexstr=data)
        print(data)
        data = rlp.decode(data, SerializedTransaction)
        print(data)
        return cls(nonce=eth_utils.to_int(data[0]),
            gasPrice=eth_utils.to_int(data[1]),
            gasLimit=eth_utils.to_int(data[2]),
            to=eth_utils.to_hex(data[3]),
            value=eth_utils.to_int(data[4]),
            data=eth_utils.to_bytes(data[5]),
            from_=eth_utils.to_hex(data[6]),
            r=eth_utils.to_bytes(data[7]),
            v=eth_utils.to_int(data[8]),
            s=eth_utils.to_bytes(data[9]))

    def serialize(self):
        return [
            self.nonce,
            self.gasPrice,
            self.gasLimit,
            self.to,
            self.value,
            self.data,
            self.from_,
            self.r,
            self.v,
            self.s
        ]


@app.post("/")
async def root(rpc: RpcRequest):
    if rpc.method == "eth_sendRawTransaction":
        if rpc.params:
            signed_tx_bytes = eth_utils.to_bytes(hexstr=rpc.params[0])
            decoded_tx = TransactionBuilder().decode(signed_tx_bytes)
            sender = eth_utils.encode_hex(decoded_tx.sender)
            to = eth_utils.to_hex(decoded_tx.to)
            input_data = await get_features(to)
            score, proof = await check_fraud(input_data)
            if score > 0.5:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32600,
                        'message': 'Detected a fraud wallet',
                        'data': {
                            'score': score,
                            'proof': proof
                        }
                    },
                    'id': rpc.id
                }
            else:
                contract_address = await get_contract_wallet_address(sender)
                wallet_contract = w3.eth.contract(
                    address=contract_address, abi=contract_abi)
                tx = wallet_contract.functions.execute(
                    decoded_tx.data, input_data, proof).build_transaction(
                        {
                            'nonce': decoded_tx.nonce,
                            'from': account.address,
                            'to': contract_address
                        }
                    )
                tx_hash = w3.eth.send_transaction(tx)
                return {
                    'jsonrpc': '2.0',
                    'result': tx_hash,
                    'id': rpc.id
                }
    print('Relaying rpc %s to infura' % str(rpc.method))
    async with httpx.AsyncClient() as client:
        response = await client.post(
            INFURA_URL,
            json=rpc.dict(),
        )
        return response.json()
