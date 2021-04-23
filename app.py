import json
import sys
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request

# create a web3.py instance w3 by connecting to the local Ethereum node
# memonics: current echo clock afford over beach fluid enroll birth lobster clay square
w3 = Web3(HTTPProvider("http://localhost:7545"))

print(w3.isConnected())

# Initialize a local account object from the private key of a valid Ethereum node address
# Initializing local account at index 0 to deploy
local_acct = w3.eth.account.from_key("95357da880cade01031eb1f61b42a408939a1fce885e42cae92daa1d768c8a1b")

# compile your smart contract with truffle first
manufacturerContract = json.load(open('./build/contracts/Manufacturer.json'))
abi = manufacturerContract['abi']
bytecode = manufacturerContract['bytecode']

# Initialize a contract object with the smart contract compiled artifacts
manufacturer_contract = w3.eth.contract(bytecode=bytecode, abi=abi)

# build a transaction by invoking the buildTransaction() method from the smart contract constructor function
construct_txn = manufacturer_contract.constructor().buildTransaction({
    'from': local_acct.address,
    'nonce': w3.eth.getTransactionCount(local_acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})

# sign the deployment transaction with the private key
signed = w3.eth.account.sign_transaction(construct_txn, local_acct.key)

# broadcast the signed transaction to your local network using sendRawTransaction() method and get the transaction hash
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())

# collect the Transaction Receipt with contract address when the transaction is mined on the network
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed At:", tx_receipt['contractAddress'])
contract_address = tx_receipt['contractAddress']

# Initialize a contract instance object using the contract address which can be used to invoke contract functions
contract_instance = w3.eth.contract(abi=abi, address=contract_address)


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    print(w3.isConnected())
    return render_template('index.html')

#
# @app.route("/error")
# def error():
#     return render_template('error.html')
#
#
@app.route("/createPills", methods=['POST'])
def createPills():

    print(w3.isConnected())
    manufacturer_address = request.form.get("ManufacturerAddress")
    # bid_amount = request.form.get("bid_amount")

    print(manufacturer_address)

    if not w3.isAddress(manufacturer_address):
        print("Invalid address", file=sys.stderr)
        return render_template('validation_error.html', val_err1="Invalid Address")

    # try:
    #     int_bid_amt = int(bid_amount)
    #     if int_bid_amt < 0:
    #         print("Invalid Amount")
    #         return render_template('validation_error.html', val_err2="Bid amount must be an unsigned integer")
    #
    # except ValueError:
    #     print("Invalid amount")
    #     return render_template('validation_error.html', val_err3="Bid amount must be an unsigned integer")
    try:
        # bid_amt_wei = w3.toWei(int_bid_amt, "ether")
        # print(bidder_address, bid_amt_wei)
        bid_txn_dict = {
            'from': '0xBFdA41CD8bE5DB6fA4CE17c99702292bEb3dEb32',
            'to': contract_address,
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei')
            }
        bid_txn_hash = contract_instance.functions.createpills().transact(bid_txn_dict)
        bid_txn_receipt = w3.eth.waitForTransactionReceipt(bid_txn_hash)
        print(bid_txn_receipt)
    except ValueError as e:
        print(e)
        return render_template('contract_error.html', contract_error=e)

    return render_template('index.html',creationStatus='Created')
#
#
# @app.route("/highestbidder", methods=['POST'])
# def highestbidder():
#     print(w3.isConnected())
#     highest_bidder = contract_instance.functions.highestBidder().call()
#     print(highest_bidder)
#     return render_template('index.html', highest_bidder=highest_bidder)
#
#
# @app.route("/highestbid", methods=['POST'])
# def highestbid():
#     print(w3.isConnected())
#     highest_bid = contract_instance.functions.highestBid().call()
#     print(highest_bid)
#     return render_template('index.html', highest_bid=highest_bid)
# @app.route("/highestbid", methods=['POST'])
# def highestbid():
#     print(w3.isConnected())
#     highest_bid = contract_instance.functions.highestBid().call()
#     print(highest_bid)
#     return render_template('index.html', highest_bid=highest_bid)

if __name__ == '__main__':
    app.run(debug=True)
