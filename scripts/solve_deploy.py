from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    DeployChallenge,
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(DeployChallenge, "deploy", [], {"from": player})

    check_solution(challenge_contract)