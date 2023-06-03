// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.19;

interface IVerifier {
    function verify(
        uint256[] memory pubInputs,
        bytes memory proof
    ) external view returns (bool);
}
