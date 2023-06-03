// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../src/YAUSDT.sol";

contract GiveMoneyScript is Script {
    function run() public {
        vm.startBroadcast();

        YAUSDT yausdt = YAUSDT(address(0xdBB0d62e8aBa9c0d9aA1F5d2aB295Be9E96c2006));

        yausdt.mint(address(0x7F558B326d7c696434Fe569bE4a305a46581D902), 100000000000000000000000); // 100k

        console.log(yausdt.balanceOf(address(0x7F558B326d7c696434Fe569bE4a305a46581D902)));

        vm.stopBroadcast();
    }
}
