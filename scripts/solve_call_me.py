from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    CallMeChallenge,
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(CallMeChallenge, "call_me", [], {"from": player})

    tx = challenge_contract.callme({"from": player})
    tx.wait(1)

    check_solution(challenge_contract)