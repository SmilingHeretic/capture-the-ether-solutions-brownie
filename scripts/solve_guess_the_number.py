from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    GuessTheNumberChallenge
)
from scripts.helpful_scripts import (
    get_account,
    get_contract_address,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account()
    # I'm deploying my own challenge contract instead of getting instance from https://capturetheether.com/challenges/
    # to avoid someone interacting with my challenge contract and stealing my scarce Ropsten ETH... (it happened!)
    challenge_contract = GuessTheNumberChallenge.deploy({"from": player, "value": Web3.toWei(1.0, "ether")})
    
    tx = challenge_contract.guess(42, {"from": player, "value": Web3.toWei(1.0, "ether")})
    tx.wait(1)

    check_solution(challenge_contract.address)