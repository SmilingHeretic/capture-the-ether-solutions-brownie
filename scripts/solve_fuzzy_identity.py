import rlp
from eth_utils import (
    keccak, 
    to_checksum_address, 
    to_bytes
)
from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
    FuzzyIdentityChallenge,
    FuzzyIdentityAttack,
)
from scripts.helpful_scripts import (
    get_account,
    get_challenge_contract,
    check_solution,
)
from web3 import Web3
from eth_account import Account


def main():
    player = get_account("player")
    challenge_contract = get_challenge_contract(FuzzyIdentityChallenge, "fuzzy_identity", [], {"from": player})

    nonce = 5
    deployer = find_bad_code_account(start=3463400, nonce=nonce)
    print("Deployer account address:", deployer)
    print()

    player.transfer(deployer, "0.1 ether")
    while deployer.nonce < nonce:
        deployer.transfer(deployer, "0 wei")

    attack_contract = FuzzyIdentityAttack.deploy({"from": deployer})

    tx = attack_contract.attack(challenge_contract, {"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)

def find_bad_code_account(start=0, nonce=5):
    is_bad_code = False
    nonce_available = False
    i = start - 1

    while not (is_bad_code and nonce_available):
        i += 1
        deployer = generate_account(i)
        attack_contract_address = mk_contract_address(deployer.address, nonce)
        is_bad_code = "badc0de" in attack_contract_address.lower()

        if i % 10_000 == 0:
            print("Attempt id:", i)
            print("Testing private key:", Web3.toHex(deployer.key))
            print("Address of deployed contract would be:", attack_contract_address)

        if is_bad_code:
            print(f"Found bad code! Checking if nonce {nonce} available...")
            print("Attempt id:", i)
            print("Private key:", Web3.toHex(deployer.key))
            print("Attack contract address:", attack_contract_address)

            deployer = accounts.add(deployer.key)
            nonce_available = deployer.nonce <= nonce
            print(f"Nonce {nonce} availabe!" if nonce_available else f"Nonce {nonce} not availabe...")

    print()
    print("Found bad code deployer private key!")
    print("Attempt id:", i)
    print("Private key:", deployer.private_key)
    print("Attack contract address:", attack_contract_address)
    print()
    return deployer

def generate_account(number):
    short_hex_str = Web3.toHex(number)
    private_key = f'0x{"0"* (66 - len(short_hex_str))}{short_hex_str[2:]}'
    return Account.from_key(private_key)

def mk_contract_address(sender: str, nonce: int) -> str:
    """Create a contract address using eth-utils.

    # https://ethereum.stackexchange.com/a/761/620
    """
    sender_bytes = to_bytes(hexstr=sender)
    raw = rlp.encode([sender_bytes, nonce])
    h = keccak(raw)
    address_bytes = h[12:]
    return to_checksum_address(address_bytes)

def test_is_bad_code_function(base_address, player):
    attack_contract = FuzzyIdentityAttack.deploy({"from": player})
    base_address = '0x5C51457EF556e6ff9446A0251157a891B511464B'
    print(base_address)
    print(attack_contract.isBadCode(base_address))
    for i in range(2, 43 - 7):
        address = base_address[:i] + 'badc0de' + base_address[i+7:]
        print(address)
        print(attack_contract.isBadCode(address))
    print()
