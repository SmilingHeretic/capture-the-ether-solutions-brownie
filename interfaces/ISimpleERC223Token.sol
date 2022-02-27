pragma solidity ^0.6.0;

interface ISimpleERC223Token {
    function balanceOf(address) external view returns (uint256);

    function transfer(address to, uint256 value)
        external
        returns (bool success);
}
