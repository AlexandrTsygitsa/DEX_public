import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
import time

# Step 1. Sends 1 Eth from system dev account to each generated user

node_url = "http://127.0.0.1:8575"

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print("chain ID: ", w3.eth.chain_id)

ETH_SENDER_PK = "52e93cac3de0aee3a39a805cdad5956d572934e5d123f35893b1dd9d45f5ad28"

# get wallet address of sender
PA = w3.eth.account.from_key(ETH_SENDER_PK)

# Get public address of sender
ETH_SENDER = PA.address
print("ETH SENDER ADDRESS: ", ETH_SENDER)
print("Wei balance: ", w3.eth.getBalance(ETH_SENDER))
balance = w3.eth.getBalance(ETH_SENDER)
print("ETH balance: ", w3.fromWei(balance, "ether"))


with open('users.json') as f:
    users = json.load(f)

for user in users:
    print("\n======================================================\n")
    recipient_addr = users.get(user)
    print("recipient address: ", recipient_addr, "\n")
    print("ETH balance before transaction: ", w3.fromWei(w3.eth.getBalance(ETH_SENDER), "ether"))

    nonce = w3.eth.getTransactionCount(ETH_SENDER)
    print("nonce of ETH_SENDER address: ", nonce, "\n")


    tx = {
    'nonce': nonce,
    'to': recipient_addr,
    'value': w3.toWei(1, 'ether'),
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei'),
    'chainId': w3.eth.chain_id
    }

    #sign the transaction
    signed_tx = Account.sign_transaction(tx, ETH_SENDER_PK)

    #send transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    #get transaction hash
    print("transaction hash: \n", w3.toHex(tx_hash), "\n")
    time.sleep(6)

for user in users:
    print(f"ETH balance of address {users.get(user)} after transaction: ", w3.fromWei(w3.eth.getBalance(users.get(user)), "ether"))
