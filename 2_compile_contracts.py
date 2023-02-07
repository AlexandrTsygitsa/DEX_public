from json import dump
from solcx import compile_standard

# Step 2. Optional. Compiles smart contracts.
# It doesn't work now.

solc_version = "0.8.4"

with open("./contracts/SubAccount.sol") as f:
	source = f.read()

print("Compiling SubAccount....")
try:
	# Solidity source code
	compiled = compile_standard(
	    {
	        "language": "Solidity",
	        "sources": {"SubAccount.sol": {"content": source}},
	        "settings": {
	            "outputSelection": {
	                "*": {
	                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
	                }
	            }
	        },
	    },
	    solc_version = solc_version,
	)
except Exception as e:
	print(f"An error occurred during compilation. Error: {e}")

print("Dumping to SubAccount.json")
dump(compiled, open("../artifacts/SubAccount.json", "w"))
