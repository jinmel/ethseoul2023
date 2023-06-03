import json
import os
import tempfile

from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import ezkl_lib
import numpy as np
import torch
from web3 import AsyncHTTPProvider, AsyncWeb3
import rlp
import eth_utils

from models import SimpleModel


INFURA_URL='https://mainnet.infura.io/v3/5c92864a308b45b6a8c3559b63cb5b38'
THEGRAPH_URL=''


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


async def check_fraud_address(address):
    input_data = get_features(address)
    input_data = torch.tensor(input_data, dtype=torch.float32)
    output = model(input_data).numpy()
    score = output[0]
    proof = generate_proof(input_data, output)
    return score, proof


@app.get("/")
async def root(rpc: RpcRequest):
    if rpc.method == "eth_sendRawTransaction":
        if rpc.params:
            data = rpc.params[0]
            data = rlp.decode(data)
            address = eth_utils.to_hex(data[3])
            score, proof = await check_fraud_address(address)
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
                w3 = AsyncWeb3(AsyncHTTPProvider(INFURA_URL))
                # TODO: Send transaction to the pre-defined contract.

                result = await w3.eth.send_transaction(proof)
                return result
        else:
            print('Error in message')

    async with httpx.AsyncClient() as client:
        response = await client.post(
            INFURA_URL,
            json=rpc.dict(),
        )
        return response.json()
