from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
)
from brownie.network.state import Chain
from brownie import web3
from web3 import Web3

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])

def get_web3():
    # this looks terrible...
    return Web3(web3.provider)

def deploy_with_bytecode(abi, bytecode, deployer_account):
    w3 = get_web3()
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(str(deployer_account))
    # Submit the transaction that deploys the contract
    transaction = contract.constructor().buildTransaction(
        {
            "chainId": Chain().id,
            "gasPrice": w3.seth.gas_price,
            "from": str(deployer_account),
            "nonce": nonce,
        }
    )
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=str(deployer_account.private_key))
    # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def get_contract_address(name):
    return config["networks"]['ropsten'][name]

def check_solution(challenge_address):
    if interface.IChallenge(challenge_address).isComplete():
        print("Challenge completed!")
    else:
        print("Challenge not completed...")
    print()