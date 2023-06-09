// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.19;

import "forge-std/Script.sol";
import "forge-std/console2.sol";
import "../src/WalletFactory.sol";
import "../src/IVerifier.sol";
import "../src/VerifyImpl.sol";
import "../src/VerifyProxy.sol";

contract WalletFactoryScript is Script {
    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        Verifier verifier = new Verifier();
        Proxy verifierProxy = new Proxy(address(verifier));

        WalletFactory walletFactory = new WalletFactory(
            0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045,
            IVerifier(address(verifierProxy))
        );

        console2.log("Verifier address: ", address(verifier));
        console2.log("verifierProxy address: ", address(verifierProxy));
        console2.log("walletFactory address: ", address(walletFactory));
        vm.stopBroadcast();
    }
}

contract WalletScript is Script {
    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        Wallet wallet = new Wallet(
            IVerifier(0x9BC4971493e4C7Dbd973c3B3D5262a06bab7c645),
            0x9BC4971493e4C7Dbd973c3B3D5262a06bab7c645
        );

        console2.log("wallet address: ", address(wallet));
        vm.stopBroadcast();
    }
}

// forge script script/WalletFactory.s.sol:WalletScript -vvv --rpc-url https://goerli.infura.io/v3/0ff5be6b14cc428f840236cacc7bec71  --broadcast --verify
// https://rpc.chiadochain.net
// forge script script/WalletFactory.s.sol:WalletFactoryScript -vvv --rpc-url https://rpc.chiadochain.net  --broadcast

//  Verifier address:  0x2f71546f7cF98BbF5cB298019476D5D6056a21aD
//   verifierProxy address:  0xD5e67C4973669148AbaD328a12A64cB74C6f70CD
//   walletFactory address:  0x862f46A533F360004Ce4d565AD09578Ee569bc8F