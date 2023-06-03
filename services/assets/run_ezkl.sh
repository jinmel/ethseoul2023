#!/bin/sh

set -ex

echo "Starting to generate verifier contract"

ezkl setup -D input.json -M model.onnx --params-path=kzg.params --vk-path=vk.key --pk-path=pk.key --circuit-params-path=circuit.params

# gen proof
ezkl prove --transcript=evm -M model.onnx -D input.json --proof-path model.pf --pk-path pk.key --params-path=kzg.params --circuit-params-path=circuit.params

# gen evm verifier
ezkl create-evm-verifier --deployment-code-path model.code --params-path=kzg.params --vk-path vk.key --sol-code-path verifier.sol --circuit-params-path=circuit.params

# Verify (EVM)
ezkl verify-evm --proof-path model.pf --deployment-code-path model.code

echo "Verifier solidity code at verifier.sol"
