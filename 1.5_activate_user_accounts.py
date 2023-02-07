import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Step 1.5. Activates user accounts that generated in step 1

node_url = "http://127.0.0.1:8575"

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print("chain ID: ", w3.eth.chain_id)

# Load users
with open('users.json') as f:
    users = json.load(f)

# Load compiled fee contract
with open('./bin/contracts/graphite/FeeContract.abi') as f:
    FEE_ABI = json.load(f)

# Graphite fee contract address
fee_contract_address = "0x0000000000000000000000000000000000001000"
fee = w3.eth.contract(address=fee_contract_address, abi=FEE_ABI)

for user in users:

    user_addr = users.get(user)

    build_tx = {
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gasPrice,
            "from": user_addr,
            "nonce": w3.eth.getTransactionCount(user_addr),
            'value': w3.toWei(0.1, 'ether')
        }

    tx = fee.functions.pay().buildTransaction(build_tx)
    signed_tx = w3.eth.account.sign_transaction(tx, private_key = user)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Activated user account @ {user_addr}")
