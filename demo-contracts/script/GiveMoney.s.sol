// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../src/YAUSDT.sol";

contract GiveMoneyScript is Script {
    function run() public {
        vm.startBroadcast(0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80);

        YAUSDT yausdt = YAUSDT(address(0x5FbDB2315678afecb367f032d93F642f64180aa3));

        yausdt.mint(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955), 1000000000000000000000);

        console.log(yausdt.balanceOf(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955)));

        vm.stopBroadcast();
    }
}
