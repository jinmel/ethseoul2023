// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "../src/YAUSDT.sol";

contract GiveMoneyScript is Script {
    function run() public {
        vm.startBroadcast(0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80);

        YAUSDT yausdt = new YAUSDT();

        yausdt.mint(address(0xa0Ee7A142d267C1f36714E4a8F75612F20a79720), 10000);
        vm.stopBroadcast();
    }
}
