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
    get_challenge_contract,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(GuessTheNumberChallenge, "guess_the_number", [], {"from": player, "value": Web3.toWei(1.0, "ether")})
    
    tx = challenge_contract.guess(42, {"from": player, "value": Web3.toWei(1.0, "ether")})
    tx.wait(1)

    check_solution(challenge_contract.address)