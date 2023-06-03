// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../src/YAUSDT.sol";

contract CheckMoneyScript is Script {
    function run() public {
        vm.startBroadcast();

        YAUSDT yausdt = YAUSDT(address(0x5FbDB2315678afecb367f032d93F642f64180aa3));

        console.log(yausdt.balanceOf(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955)));
        console.log(yausdt.allowance(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955), address(0x71C95911E9a5D330f4D621842EC243EE1343292e)));

        vm.stopBroadcast();
    }
}
