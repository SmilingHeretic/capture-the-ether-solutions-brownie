pragma solidity ^0.6.0;

interface ITokenBankChallenge {
    function balanceOf(address) external view returns (uint256);

    function withdraw(uint256 amount) external;
}
