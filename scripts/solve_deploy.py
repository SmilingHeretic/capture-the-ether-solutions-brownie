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
    challenge_address = get_challenge_address("deploy")
    check_solution(challenge_address)