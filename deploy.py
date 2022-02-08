import os
from dotenv import load_dotenv
from solcx import compile_standard, install_solc
import json
from web3 import Web3

load_dotenv()

with open("./SimpleStorage.sol", "r") as file: simple_storage_file = file.read()
# print(simple_storage_file)

install_solc("0.8.0")
# COMPILE OUR SOLIDITY
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            },
        }
    },
    solc_version="0.8.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# GET BYTECODE
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# GET ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# print(abi)
# CONNECTING TO GANACHE
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x06CD833E9EE7F93063382f973B279F41fA7de4e0"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode = bytecode)
print(SimpleStorage)

# WHENEVER WE DO A STATE CHANGE OR DEPLOY A NEW CONTRACT

# GET THE LATESTEST TRANSACTION
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# 1) Build the contract deploy transaction
# 2) Sign the Transaction
# 3) Send the Transaction
transaction = SimpleStorage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price,"chainId": chain_id, "from": my_address, "nonce": nonce})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)

# SEND THIS SIGNED TRANSACTION
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# WORKING WITH THE CONTRACT, YOU ALWAYS NEED
# CONTRACT ADDRESS
# CONTRACT API
