from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    GuessTheRandomNumberChallenge
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
        GuessTheRandomNumberChallenge, "guess_the_random_number", [], {"from": player, "value": Web3.toWei(1.0, "ether")}
    )
    w3 = get_web3()
    answer = w3.eth.get_storage_at(challenge_contract.address, 0)
    print("Answer:", Web3.toInt(answer))
    
    tx = challenge_contract.guess(answer, {"from": player, "value": Web3.toWei(1.0, "ether")})
    tx.wait(1)

    check_solution(challenge_contract.address)