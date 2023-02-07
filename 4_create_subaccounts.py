import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Step 4. Creates user SubAccounts via Factory contract. Stores data in user_subaccounts.json
# user_subaccounts.json : {owners_private_key: subacc_public_address}

node_url = "http://127.0.0.1:8575"

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
chainID = w3.eth.chain_id
print("chain ID: ", chainID)

# Load deployed contracts addresses
with open('deployed_contracts.json') as f:
    deployed_contracts = json.load(f)

# Load users
with open('users.json') as f:
    users = json.load(f)

# Load compiled contracts
with open('./bin/contracts/SubAccountFactory.abi') as f:
    FACTORY_ABI = json.load(f)

# Get factory contract address
factory_address = deployed_contracts['sub_account_factory']


# Create subaccounts
subaccounts = {}
factory = w3.eth.contract(address=factory_address, abi=FACTORY_ABI)
get_address_event = factory.events.SubAccountCreated()

for user in users:
    user_addr = users.get(user)

    build_tx = {
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gasPrice,
            "from": user_addr,
            "nonce": w3.eth.getTransactionCount(user_addr),
        }

    tx = factory.functions.createSubAccount().buildTransaction(build_tx)
    signed_tx = w3.eth.account.sign_transaction(tx, private_key = user)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    get_address_event = factory.events.SubAccountCreated()

    raw_logs = tx_receipt.logs[0]
    
    receipt = w3.eth.waitForTransactionReceipt(raw_logs['transactionHash'])
    logs = get_address_event.processReceipt(receipt)
    
    address_raw = logs[0]['args']
    address = address_raw['newSubAccountAddress']

    subaccounts[user] = address

    print(f"Created subaccount @ {address} \nOwner: {user_addr}")

# Save subaccounts addresses to json file
with open('user_subaccounts.json', 'w') as f:
    json.dump(subaccounts, f)
