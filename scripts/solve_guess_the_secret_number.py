from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    GuessTheSecretNumberChallenge
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
    # I'm deploying my own challenge contract instead of getting instance from https://capturetheether.com/challenges/
    # to avoid someone interacting with my challenge contract and stealing my scarce Ropsten ETH... (it happened!)
    challenge_contract = GuessTheSecretNumberChallenge.deploy({"from": player, "value": Web3.toWei(1.0, "ether")})
    w3 = get_web3()
    answerHash = w3.eth.get_storage_at(challenge_contract.address, 0)
    print('answerHash recovered from storage:', Web3.toHex(answerHash))

    for guess in range(2 ** 8):
        if (Web3.solidityKeccak(['uint8'], [guess]) == answerHash):
            answer = guess
            break
    print("Answer:", answer)
    
    tx = challenge_contract.guess(answer, {"from": player, "value": Web3.toWei(1.0, "ether")})
    tx.wait(1)

    check_solution(challenge_contract.address)