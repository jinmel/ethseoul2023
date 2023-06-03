// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";
import "openzeppelin-contracts/contracts/access/Ownable.sol";

contract NASNFTContractPayable is ERC721, Ownable {
    string public baseURI;
    uint256 public cost = 0.05 ether;
    uint256 public currentMintId = 0;

    constructor(string memory _initialBaseURI) ERC721("NASNFT", "NASNFT") {
        baseURI = _initialBaseURI;
    }

    function _baseURI() internal view override returns (string memory) {
        return baseURI;
    }

    function mint() public payable {
        require(balanceOf(_msgSender()) == 0, "You already have a token");
        require(msg.value >= cost, "Insufficient funds");
        currentMintId = currentMintId + 1;
        _safeMint(_msgSender(), currentMintId + 1);
    }

    function withdraw() public onlyOwner {
        (bool sent, ) = payable(owner()).call{value: address(this).balance}("");
        require(sent);
    }
}
