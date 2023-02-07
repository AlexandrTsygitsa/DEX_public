import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
import random
import time

# Step 5. Add each test tokens on each subaccount, created in step 4.
# Generates random amount and send tokens using `transfer` ERC-20 function.

node_url = "http://127.0.0.1:8575"

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print("chain ID: ", w3.eth.chain_id)

TOKENS_OWNER_PK = "52e93cac3de0aee3a39a805cdad5956d572934e5d123f35893b1dd9d45f5ad28"
# get wallet address of sender
PA = w3.eth.account.from_key(TOKENS_OWNER_PK)
TOKENS_OWNER = PA.address

# Load deployed contracts addresses
with open('deployed_contracts.json') as f:
    deployed_contracts = json.load(f)

# Load users
with open('users.json') as f:
    users = json.load(f)

# Load subaccounts
with open('user_subaccounts.json') as f:
    user_subaccounts = json.load(f)

# Load compiled contracts
with open('./bin/contracts/SubAccount.abi') as f:
    SUBACC_ABI = json.load(f)

# CatToken Contract
with open("./bin/contracts/test_tokens/Cat.abi") as f:
    CAT_ABI = json.load(f)
# LionToken Contract
with open("./bin/contracts/test_tokens/Lion.abi") as f:
    LION_ABI = json.load(f)
# OwlToken Contract
with open("./bin/contracts/test_tokens/Owl.abi") as f:
    OWL_ABI = json.load(f)
# PenguinToken Contract
with open("./bin/contracts/test_tokens/Penguin.abi") as f:
    PENGUIN_ABI = json.load(f)
# WolfToken Contract
with open("./bin/contracts/test_tokens/Wolf.abi") as f:
    WOLF_ABI = json.load(f)

# Initialize token contracts
CAT_TOKEN = w3.eth.contract(address=deployed_contracts['cat_token'], abi=CAT_ABI)
LION_TOKEN = w3.eth.contract(address=deployed_contracts['lion_token'], abi=LION_ABI)
OWL_TOKEN = w3.eth.contract(address=deployed_contracts['owl_token'], abi=OWL_ABI)
PENGUIN_TOKEN = w3.eth.contract(address=deployed_contracts['penguin_token'], abi=PENGUIN_ABI)
WOLF_TOKEN = w3.eth.contract(address=deployed_contracts['wolf_token'], abi=WOLF_ABI)

tokens = [CAT_TOKEN, LION_TOKEN, OWL_TOKEN, PENGUIN_TOKEN, WOLF_TOKEN]
subaccounts = list(user_subaccounts.values())
subaccounts_pk = list(user_subaccounts.keys())

## Add tokens to subaccounts
for token in tokens:
    print(f'Token: {token.functions.name().call()}')
    for addr in subaccounts:

        SUBACCOUNT = w3.eth.contract(address=addr, abi=SUBACC_ABI)

        value = random.randint(16000, 20000)

        build_tx = {
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gasPrice,
            "from": TOKENS_OWNER,
            "nonce": w3.eth.getTransactionCount(TOKENS_OWNER),
        }

        tx = token.functions.transfer(SUBACCOUNT.address, value).buildTransaction(build_tx)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key = TOKENS_OWNER_PK)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"Sent {value} on subAccount @ {addr}")
        time.sleep(8)
