from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_address,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account()
    challenge_address = get_challenge_address("call_me")

    challenge_contract = interface.ICallMeChallenge(challenge_address)
    tx = challenge_contract.callme({"from": player})
    tx.wait(1)

    check_solution(challenge_address)