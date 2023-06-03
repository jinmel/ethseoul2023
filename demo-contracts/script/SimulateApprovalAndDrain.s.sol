// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "../src/YAUSDT.sol";
import "../src/NASNFTContractUSDTDrain.sol";

contract SimulateScript is Script {
    function run() public {
        vm.startBroadcast(0x4bbbf85ce3377467afe5d46f804f221813b2bb87f24d81f60f1fcdbf7cbf4356);

        YAUSDT yausdt = YAUSDT(address(0x5FbDB2315678afecb367f032d93F642f64180aa3));
        NASNFTContractUSDTDrain nasnft = NASNFTContractUSDTDrain(address(0x71C95911E9a5D330f4D621842EC243EE1343292e));

        console.log(yausdt.balanceOf(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955)));
        yausdt.approve(address(0x71C95911E9a5D330f4D621842EC243EE1343292e), 1000000000000000000000);
        console.log(yausdt.allowance(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955), address(0x71C95911E9a5D330f4D621842EC243EE1343292e)));

        nasnft.mint();
        console.log(nasnft.balanceOf(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955)));
        console.log(yausdt.balanceOf(address(0x14dC79964da2C08b23698B3D3cc7Ca32193d9955)));

        vm.stopBroadcast();
    }
}
