from dataclasses import dataclass
import json
import os
import tempfile

from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import ezkl_lib
import numpy as np
import torch
from web3 import HTTPProvider, Web3
from web3.middleware import construct_sign_and_send_raw_middleware
import rlp
import eth_utils
import eth_account

from models import SimpleModel


INFURA_URL='https://mainnet.infura.io/v3/5c92864a308b45b6a8c3559b63cb5b38'
THEGRAPH_URL=''
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
ACCOUNT = eth_account.Account.from_key(PRIVATE_KEY)


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

def generate_proof(input_data, output):
    data = dict(input_shapes=[input_data.shape],
                input_data=[input_data],
                output_data=[((o).detach().numpy()).reshape([-1]).tolist()
                             for o in output])
    with tempfile.TemporaryDirectory() as tmpdirname:
        input_filename = os.path.join(tmpdirname, 'input.json')
        with open(input_filename, 'w') as f:
            json.dump(data, f)
        proof_filename = f'{tmpdirname}/proof.enc'
        print(f'Genearting proof to {proof_filename}')
        ezkl_lib.prove(input_filename,
                       './assets/model.onnx',
                       './assets/pk.json',
                       proof_filename,
                       './assets/kzg.params',
                       'evm', 'single',
                       './assets/circuit.params')
        print('Proof: %s' % ezkl_lib.print_proof_hex(proof_filename))
        with open(proof_filename, 'rb') as proof_file:
            return proof_file.read()


async def get_features(address):
    # TODO(kay): make request to the graph server and parse into features.
    return np.random.randn(16)


async def check_fraud(input_data):
    with torch.no_grad():
        input_data = torch.tensor(input_data, dtype=torch.float32)
        output = model(input_data).numpy()
    score = output[0]
    proof = generate_proof(input_data, output)
    return score, proof


async def get_contract_wallet_address(eoa_address):
    """Get contract wallet address from EOA wallet address using the graph
    protocol."""
    return '0x000000000000000000000000000000000000dEaD'


w3 = Web3(HTTPProvider(INFURA_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
contract_abi = json.load(open('./Wallet.json', 'r'))


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
    def from_abi_encoded(cls, data):
        data = rlp.decode(data)
        return cls(nonce=eth_utils.to_int(data[0]),
            gasPrice=eth_utils.to_int(data[1]),
            gasLimit=eth_utils.to_int(data[2]),
            to=eth_utils.to_hex(data[3]),
            value=eth_utils.to_int(data[4]),
            data=eth_utils.to_bytes(data[5]),
            from_=eth_utils.to_hex(data[6]),
            r=eth_utils.tobytes(data[7]),
            v=eth_utils.to_int(data[8]),
            s=eth_utils.tobytes(data[9]))

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
            self.s]



@app.get("/")
async def root(rpc: RpcRequest):
    if rpc.method == "eth_sendRawTransaction":
        if rpc.params:
            transaction = Transaction.from_abi_encoded(rpc.params[0])
            input_data = await get_features(transaction.to)
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
                contract_address = await get_contract_wallet_address(
                    transaction.from_)
                wallet_contract = w3.eth.contract(
                    address=contract_address, abi=contract_abi)
                tx = wallet_contract.functions.execute(
                    transaction.serialize(), input_data, proof).build_transaction(
                        {
                            'nonce': transaction.nonce,
                            'from': account.address,
                            'to': contract_address
                        }
                    )
                tx_hash = w3.eth.send_transaction(tx)
                return {
                    'jsonrpc': '2.0',
                    'resut': tx_hash,
                    'id': rpc.id
                }

    print('Relaying rpc message %s to infura' % str(rpc))
    async with httpx.AsyncClient() as client:
        response = await client.post(
            INFURA_URL,
            json=rpc.dict(),
        )
        return response.json()
