import eth_account
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
    AccountTakeoverChallenge,
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
    challenge_contract = get_challenge_contract(AccountTakeoverChallenge, "account_takeover", [], {"from": player})
    w3 = get_web3()

    # Details of this attack (together with ECDSA) are described here:
    # https://www.instructables.com/Understanding-how-ECDSA-protects-your-data/ and here:
    # https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/

    # Found on etherscan. First two transactions of address 0x6B477781b0e68031109f21887e6B5afEAaEB002b
    # They have the same r in signature, so the private key can be recovered
    tx_0 = w3.eth.get_transaction("0xd79fc80e7b787802602f3317b7fe67765c14a7d40c3e0dcb266e63657f881396")
    tx_1 = w3.eth.get_transaction("0x061bf0b4b5fdb64ac475795e9bc5a3978f985919ce6747ce2cfbbcaccaf51009")

    z_0 = Web3.toInt(get_hash(tx_0, w3))
    z_1 = Web3.toInt(get_hash(tx_1, w3))
    s_0 = Web3.toInt(tx_0['s'])
    s_1 = Web3.toInt(tx_1['s'])
    r_0 = Web3.toInt(tx_0['r'])
    r_1 = Web3.toInt(tx_1['r'])

    assert r_0 == r_1

    # prime number used for ecdsa in ethereum (SECP256k1)
    p = 115792089237316195423570985008687907852837564279074904382605163141518161494337

    k = ((z_0 - z_1) * pow((s_0 - s_1), -1, p)) % p
    private_key = ((s_0 * k - z_0) * pow(r_0, -1, p)) % p

    hacked_account = accounts.add(Web3.toHex(private_key))
    print("Confirming address of hacked account:", hacked_account)
    print()
    tx = challenge_contract.authenticate({"from": hacked_account})
    tx.wait(1)

    check_solution(challenge_contract.address)


def get_hash(tx, w3):
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
    return ut.hash()
