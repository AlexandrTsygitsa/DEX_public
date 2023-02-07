import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
import secrets
from eth_account import Account

# Step 0. Creates EOA's and stores private keys with public addresses in users.json 
# users.json : {private_key: public_address}

node_url = "http://127.0.0.1:8575"

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print("chain ID: ", w3.eth.chain_id, "\n")

users = {}

def wallet_generator():
    priv = secrets.token_hex(32)
    private_key = f"0x{priv}"
    acct = Account.from_key(private_key)
    public_address = acct.address

    return private_key, public_address

# Generate 10 users
for i in range(10):
    keys = wallet_generator()
    users.update({keys[0]: keys[1]})

# Save user info to json file
with open('users.json', 'w') as f:
    json.dump(users, f)

print("Users: ", list(users.keys()), "\n")
print("generated wallet addresses: ")
for user in users:
    print(users.get(user), "\n")
