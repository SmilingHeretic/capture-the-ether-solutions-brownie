from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from brownie import (
    network,
    accounts,
    config,
    interface,
    chain,
    Contract,
    PublicKeyChallenge,
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
    challenge_contract = get_challenge_contract(PublicKeyChallenge, "public_key", [], {"from": player})
    w3 = get_web3()

    # Found on etherscan. The only transacion sent from address 0x92b28647ae1f3264661f72fb2eb9625a89d88a31
    tx = w3.eth.get_transaction("0xabc467bedd1d17462fcc7942d0af7874d6f8bdefee2b299c9168a216d3ff0edb")

    public_key = recover_public_key(tx, w3)
    print("Confirm recovered address:", public_key.to_address())
    print()

    tx = challenge_contract.authenticate(Web3.toHex(hexstr=str(public_key)), {"from": player})
    tx.wait(1)

    check_solution(challenge_contract.address)


def recover_public_key(tx, w3):
    # Based on https://gist.github.com/CrackerHax/ec6964ea030d4b31d47b7d412036c623
    s = w3.eth.account._keys.Signature(vrs=(
        to_standard_v(extract_chain_id(tx.v)[1]),
        w3.toInt(tx.r),
        w3.toInt(tx.s)
    ))
    tt = {k: tx[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId', 'data'}}
    tt['data'] = tx.input
    tt['chainId'] = extract_chain_id(tx.v)[0]
    ut = serializable_unsigned_transaction_from_dict(tt)
    public_key = s.recover_public_key_from_msg_hash(ut.hash())
    return public_key
