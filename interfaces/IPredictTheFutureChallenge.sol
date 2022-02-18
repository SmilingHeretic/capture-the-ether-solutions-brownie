pragma solidity ^0.6.0;

interface IPredictTheFutureChallenge {
    function guess() external view returns (uint8);

    function lockInGuess(uint8 n) external payable;

    function settle() external;
}
