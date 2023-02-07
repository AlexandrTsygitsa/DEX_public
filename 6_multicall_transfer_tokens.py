import json
import random

from eth_account.messages import encode_defunct
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Step 6. Generates random MicroTXs and call multiCall function of Executor smart contract.
# Change TX_NUMBER to generate expected number of MicroTX
TX_NUMBER = 70

node_url = "http://127.0.0.1:8575"

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print("chain ID: ", w3.eth.chain_id)

DEX_OWNER_PK = "52e93cac3de0aee3a39a805cdad5956d572934e5d123f35893b1dd9d45f5ad28"
# get wallet address of sender
PA = w3.eth.account.from_key(DEX_OWNER_PK)
DEX_OWNER = PA.address

# Load deployed contracts addresses
with open('deployed_contracts.json') as f:
    deployed_contracts = json.load(f)
# Load subaccounts
with open('user_subaccounts.json') as f:
    user_subaccounts = json.load(f)

# Load users
with open('users.json') as f:
    users = json.load(f)

# Load compiled contracts
with open('./bin/contracts/Executor.abi') as f:
    EXECUTOR_ABI = json.load(f)

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

# Initialize contracts
EXECUTOR = w3.eth.contract(address=deployed_contracts['executor'], abi=EXECUTOR_ABI)
CAT = w3.eth.contract(address=deployed_contracts['cat_token'], abi=CAT_ABI)
LION = w3.eth.contract(address=deployed_contracts['lion_token'], abi=LION_ABI)
OWL = w3.eth.contract(address=deployed_contracts['owl_token'], abi=OWL_ABI)
PENGUIN = w3.eth.contract(address=deployed_contracts['penguin_token'], abi=PENGUIN_ABI)
WOLF = w3.eth.contract(address=deployed_contracts['wolf_token'], abi=WOLF_ABI)

CAT_ADDR = deployed_contracts['cat_token']
LION_ADDR = deployed_contracts['lion_token']
OWL_ADDR = deployed_contracts['owl_token']
PENGUIN_ADDR = deployed_contracts['penguin_token']
CAT_ADDR = deployed_contracts['wolf_token']


tokens = [CAT, LION, OWL, PENGUIN, CAT]
subaccounts = list(user_subaccounts.values())
users = list(users.keys())

ADDRESS_ARRAY = []
SIGN_ARRAY = []
MICROTX_ARRAY = []

value = 10

for _ in range(TX_NUMBER):
    if TX_NUMBER == 0:
        break

    sender_is_recipient = True

    # owner of subaccount parameters
    owner_privkey = random.choice(users)
    owner_account = w3.eth.account.from_key(owner_privkey)
    owner_address = owner_account.address

    # subaccount sender parameters
    subacc_sender_address = user_subaccounts.get(owner_privkey)
    SUBACCOUNT = w3.eth.contract(address=subacc_sender_address, abi=SUBACC_ABI)
    
    # subaccount recipient parameters
    subacc_recipient_address = random.choice(subaccounts)

    # token parameters
    token = random.choice(tokens)
    token_address = token.address

    # sender must not be the recipient 
    while sender_is_recipient:
        if subacc_sender_address == subacc_recipient_address:
            print("\nSENDER AND RECIPIENT GENERATED THE SAME!!\n")
            subacc_recipient_address = random.choice(subaccounts)
        else:
            sender_is_recipient = False

    print("#"*60)
    print("owners private key: ", owner_privkey)
    print("owners public address: ", owner_address)
    print("#"*60)

    print("subacc_sender: ", subacc_sender_address)
    print("subacc_recipient: ", subacc_recipient_address)
    print("token_addr: ", token_address)
    print("#"*60)

    ### CREATING LOCAL SIGNATURE
    msg = Web3.soliditySha3(['address', 'address', 'uint256'], [Web3.toChecksumAddress(token_address), Web3.toChecksumAddress(subacc_recipient_address), value])
    encoded_message = encode_defunct(msg)
    signed_messageLocal = w3.eth.account.sign_message(encoded_message, private_key=owner_privkey)

    ### EXTRACTING SIGNATURE PARAMETERS
    message_hash = w3.toHex(signed_messageLocal['messageHash'])
    signature = signed_messageLocal['signature']
    v = signed_messageLocal['v']
    r = w3.toBytes(signed_messageLocal['r'])
    if len(r) == 31:
        r = w3.toBytes(hexstr=("0x00" + w3.toHex(r)[2:]))
    s = w3.toBytes(signed_messageLocal['s'])
    if len(s) == 31:
        s = w3.toBytes(hexstr=("0x00" + w3.toHex(s)[2:]))


    print("message hash: ", message_hash)
    print("R: ", w3.toHex(r), len(r))
    print("S: ", w3.toHex(s), len(s))
    print("V: ", w3.toHex(v))
    print("signature: ", w3.toHex(signature))

    ### CHECK IF SIGNATURE IS VALID FOR MULTICALL
    python_web3_recovered_address = w3.eth.account.recoverHash(message_hash=message_hash, vrs=(v,r,s))
    solidity_recovered_address = SUBACCOUNT.functions.VerifyMessage(_hashedMessage=message_hash, _v=v, _r=r, _s=s).call()

    print("web3 py address recover: ", python_web3_recovered_address)
    print("smart contract address recover: ", solidity_recovered_address)

    recover_owner_passed = (owner_address == solidity_recovered_address)

    print("recovered address from signature and subAccount address is equal : ", recover_owner_passed)

    if not recover_owner_passed:
        exit("Address is generated incorrectly")
    
    ### CREATE ARRAY PARAMS FOR MULTICALL
    MicroTX = (token_address, subacc_recipient_address, value, message_hash)
    sign = (v, r, s)

    MICROTX_ARRAY.append(MicroTX)
    SIGN_ARRAY.append(sign)
    ADDRESS_ARRAY.append(subacc_sender_address)

### EXECUTOR MULTICALL PARAMS
_from=list(map(lambda x: str(x), ADDRESS_ARRAY))
_MicroTX = MICROTX_ARRAY
_Sign = SIGN_ARRAY


build_tx = {
    "chainId": w3.eth.chain_id,
    "gasPrice": w3.eth.gasPrice,
    "from": DEX_OWNER,
    "nonce": w3.eth.getTransactionCount(DEX_OWNER),
}

tx = EXECUTOR.functions.multiCall(_from, _MicroTX, _Sign).buildTransaction(build_tx)
signed_tx = w3.eth.account.sign_transaction(tx, private_key = DEX_OWNER_PK)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt, "\n")
print("MULTICALL GAS USED: ", tx_receipt['gasUsed'], "\n")
print("SUCCESS")
