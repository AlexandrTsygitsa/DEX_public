import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Step 3. Deploys smart contracts (SubAccount Factory, Executor, test tokens) and stores addresses in deployed_contracts.json
# deployed_contracts.json : {"{contract_name}": public_address}


node_url = "http://127.0.0.1:8575"

w3 = Web3(Web3.HTTPProvider(node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
chainID = w3.eth.chain_id
print("chain ID: ", chainID)

TX_SENDER_PK = "52e93cac3de0aee3a39a805cdad5956d572934e5d123f35893b1dd9d45f5ad28"
PA = w3.eth.account.from_key(TX_SENDER_PK)
TX_SENDER = PA.address
print("TX SENDER: ", TX_SENDER)

## Load compiled contracts
# SubAccount Contract
with open("./bin/contracts/SubAccount.abi") as f:
    SUB_ACC_ABI = json.load(f)
with open("./bin/contracts/SubAccount.bin") as f:
    SUB_ACC_BIN = f.read()
# SubAccount Factory Contract
with open("./bin/contracts/SubAccountFactory.abi") as f:
    FACTORY_ABI = json.load(f)
with open("./bin/contracts/SubAccountFactory.bin") as f:
    FACTORY_BIN = f.read()
# Executor Contract
with open("./bin/contracts/Executor.abi") as f:
    EXECUTOR_ABI = json.load(f)
with open("./bin/contracts/Executor.bin") as f:
    EXECUTOR_BIN = f.read()

# CatToken Contract
with open("./bin/contracts/test_tokens/Cat.abi") as f:
    CAT_ABI = json.load(f)
with open("./bin/contracts/test_tokens/Cat.bin") as f:
    CAT_BIN = f.read()
# LionToken Contract
with open("./bin/contracts/test_tokens/Lion.abi") as f:
    LION_ABI = json.load(f)
with open("./bin/contracts/test_tokens/Lion.bin") as f:
    LION_BIN = f.read()
# OwlToken Contract
with open("./bin/contracts/test_tokens/Owl.abi") as f:
    OWL_ABI = json.load(f)
with open("./bin/contracts/test_tokens/Owl.bin") as f:
    OWL_BIN = f.read()
# PenguinToken Contract
with open("./bin/contracts/test_tokens/Penguin.abi") as f:
    PENGUIN_ABI = json.load(f)
with open("./bin/contracts/test_tokens/Penguin.bin") as f:
    PENGUIN_BIN = f.read()
# WolfToken Contract
with open("./bin/contracts/test_tokens/Wolf.abi") as f:
    WOLF_ABI = json.load(f)
with open("./bin/contracts/test_tokens/Wolf.bin") as f:
    WOLF_BIN = f.read()


def deploy_contract(contract_name: str, abi, bytecode, owner=None):

    print(f"{contract_name}: deploying contract...")
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    build_tx = {
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gasPrice,
            "from": TX_SENDER,
            "nonce": w3.eth.getTransactionCount(TX_SENDER),
        }

    if owner:
        tx = contract.constructor(owner).buildTransaction(build_tx)
    else:
        tx = contract.constructor().buildTransaction(build_tx)

    print(f"{contract_name}: signing transaction...")
    signed_tx = w3.eth.account.sign_transaction(tx, private_key = TX_SENDER_PK)

    print(f"{contract_name}: sending first transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"{contract_name}: waiting for Txn receipt...")
    txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    ADDRESS = txn_receipt.contractAddress
    print(f"{contract_name} contract deployed @ {ADDRESS}")

    return ADDRESS

## DEX contract addresses
SUBACCOUNT_ADDRESS = deploy_contract("SubAccount", SUB_ACC_ABI, SUB_ACC_BIN, owner = TX_SENDER)
SUBACCOUNT_FACTORY_ADDRESS = deploy_contract("SubAccountFactory", FACTORY_ABI, FACTORY_BIN)
EXECUTOR_ADDRESS = deploy_contract("Executor", EXECUTOR_ABI, EXECUTOR_BIN)

#ERC-20 test token contract addresses
CAT_ADDRESS = deploy_contract("CatToken", CAT_ABI, CAT_BIN)
LION_ADDRESS = deploy_contract("LionToken", LION_ABI, LION_BIN)
OWL_ADDRESS = deploy_contract("OwlToken", OWL_ABI, OWL_BIN)
PENGUIN_ADDRESS = deploy_contract("PenguinToken", PENGUIN_ABI, PENGUIN_BIN)
WOLF_ADDRESS = deploy_contract("WolfToken", WOLF_ABI, WOLF_BIN)

# Save deployed contracts addresses to json file
with open('deployed_contracts.json', 'w') as f:
    json.dump({
        'sub_account': SUBACCOUNT_ADDRESS,
        'sub_account_factory': SUBACCOUNT_FACTORY_ADDRESS,
        'executor': EXECUTOR_ADDRESS,
        'cat_token': CAT_ADDRESS,
        'lion_token': LION_ADDRESS,
        'owl_token': OWL_ADDRESS,
        'penguin_token': PENGUIN_ADDRESS,
        'wolf_token': WOLF_ADDRESS,
    }, f)
