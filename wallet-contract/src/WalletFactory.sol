// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.19;

import "./Wallet.sol";
import "./IVerifier.sol";

contract WalletFactory {
    address owner;
    IVerifier verifier;

    constructor(address _owner, IVerifier _verifier) {
        owner = _owner;
        verifier = _verifier;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    event DeployedWallet(address indexed owner, address indexed walletAddress);

    function deploy(address walletOwner) external { // onlyOwner should be used here in a production setting
        address walletAddress = address(new Wallet(verifier, owner));

        emit DeployedWallet(walletOwner, walletAddress);
    }
}
