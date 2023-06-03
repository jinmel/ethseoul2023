// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "../src/YAUSDT.sol";

contract DeployMoneyScript is Script {
    function run() public {
        vm.startBroadcast(0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80);

        YAUSDT yausdt = new YAUSDT();

        yausdt.mint(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955), 1000000000000000000000);
        vm.stopBroadcast();
    }
}
