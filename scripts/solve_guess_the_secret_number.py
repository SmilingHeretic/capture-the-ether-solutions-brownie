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
    get_challenge_contract,
    check_solution,
    get_web3
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(
        GuessTheSecretNumberChallenge, "guess_the_secret_number", [], {"from": player, "value": Web3.toWei(1.0, "ether")}
    )
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