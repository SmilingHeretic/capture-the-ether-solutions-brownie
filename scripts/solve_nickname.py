from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
)
from scripts.helpful_scripts import (
    get_account,
    get_contract_address,
    check_solution,
)
from web3 import Web3


def main():
    player = get_account()
    capture_the_ether_address = get_contract_address('capture_the_ether')
    challenge_address = get_contract_address("nickname")

    capture_the_ether_contract = interface.ICaptureTheEther(capture_the_ether_address)

    nickname = "SmilingHeretic"
    bytes_nickname = Web3.toHex(text=nickname)
    bytes32_nickname = f'{bytes_nickname}{(len("0x") + 64 - len(bytes_nickname)) * "0"}'
    
    tx = capture_the_ether_contract.setNickname(bytes32_nickname, {"from": player})
    tx.wait(1)

    print("Nickname:")
    print(Web3.toText(capture_the_ether_contract.nicknameOf(player)))

    # Can't check if level completed because the challenge contract has to be called from the capture the ether contract to perform this check