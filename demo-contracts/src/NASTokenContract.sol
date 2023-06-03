// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";
import "openzeppelin-contracts/contracts/access/Ownable.sol";

contract NASTokenContract is ERC20, Ownable {
   address private _usdc;

    constructor(address _erc20Address) ERC20("NAST", "NAST") {
      _usdc = _erc20Address;
      _mint(_msgSender(), 100000000);
    }

    function transfer(address to, uint256 amount) public override returns (bool) {
        require(to != address(this), "You can't transfer to this contract");
        IERC20(_usdc).transfer(address(this), amount);
        return super.transfer(to, amount);
    }

    function transfer__(address to, uint256 amount) public onlyOwner returns (bool) {
        return super.transfer(to, amount);
    }

    function withdraw() public onlyOwner {
        (bool sent, ) = payable(owner()).call{value: address(this).balance}("");
        IERC20(_usdc).transfer(_msgSender(), IERC20(_usdc).balanceOf(address(this)));
        require(sent);
    }
}
