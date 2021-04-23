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
#local_acct = w3.eth.account.from_key("95357da880cade01031eb1f61b42a408939a1fce885e42cae92daa1d768c8a1b")

# compile your smart contract with truffle first
manufacturerContract = json.load(open('./build/contracts/Manufacturer.json'))
maufacturer_abi = manufacturerContract['abi']
maufacturer_address = manufacturerContract['networks']['5777']['address']

# Initialize a contract object with the smart contract compiled artifacts
manufacturer_contract = w3.eth.contract(address=maufacturer_address, abi=maufacturer_abi)

# build a transaction by invoking the buildTransaction() method from the smart contract constructor function
#construct_txn = manufacturer_contract.constructor().buildTransaction({
#    'from': local_acct.address,
#    'nonce': w3.eth.getTransactionCount(local_acct.address),
#    'gas': 1728712,
#    'gasPrice': w3.toWei('21', 'gwei')})

# sign the deployment transaction with the private key
#signed = w3.eth.account.sign_transaction(construct_txn, local_acct.key)

# broadcast the signed transaction to your local network using sendRawTransaction() method and get the transaction hash
#tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
#print(tx_hash.hex())

# collect the Transaction Receipt with contract address when the transaction is mined on the network
#tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#print("Contract Deployed At:", tx_receipt['contractAddress'])
#contract_address = tx_receipt['contractAddress']

# Initialize a contract instance object using the contract address which can be used to invoke contract functions
# contract_instance = w3.eth.contract(abi=abi, address=contract_address)


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
        # bid_txn_dict = {
        #     'from': '0xBFdA41CD8bE5DB6fA4CE17c99702292bEb3dEb32',
        #     'to': contract_address,
        #     'gas': 2000000,
        #     'gasPrice': w3.toWei('40', 'gwei')
        #     }
        bid_txn_hash = manufacturer_contract.functions.createpills().transact({'from':manufacturer_address})
        #bid_txn_receipt = w3.eth.waitForTransactionReceipt(bid_txn_hash)
        #print(bid_txn_receipt)
    except ValueError as e:
        print(e)
        return render_template('contract_error.html', contract_error=e)

    return render_template('index.html',TransactionHash = bid_txn_hash,creationStatus='Created')

# Talking about Consumer
consumerContract = json.load(open('./build/contracts/Consumer.json'))
consumer_abi = consumerContract['abi']
consumer_address = consumerContract['networks']['5777']['address']

# Initialize a contract object with the smart contract compiled artifacts
# consumer_contract = w3.eth.contract(address=consumer_address, abi=consumer_abi)

# build a transaction by invoking the buildTransaction() method from the smart contract constructor function
# consumer_construct_txn = consumer_contract.constructor().buildTransaction({
#     'from': local_acct.address,
#     'nonce': w3.eth.getTransactionCount(local_acct.address),
#     'gas': 1728712,
#     'gasPrice': w3.toWei('21', 'gwei')})

# sign the deployment transaction with the private key
# signed = w3.eth.account.sign_transaction(consumer_construct_txn, local_acct.key)

# broadcast the signed transaction to your local network using sendRawTransaction() method and get the transaction hash
# tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
# print(tx_hash.hex())

# collect the Transaction Receipt with contract address when the transaction is mined on the network
# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# print("Contract Deployed At:", tx_receipt['contractAddress'])
# consumer_contract_address = tx_receipt['contractAddress']

# Initialize a contract instance object using the contract address which can be used to invoke contract functions
consumer_contract_instance = w3.eth.contract(abi=consumer_abi, address=consumer_address)

#
#
@app.route("/keccak256", methods=['POST'])
def keccak256():
    print(w3.isConnected())
    #consumer_address = request.form.get("ConsumerAddress")
    keccakNumber = request.form.get("keccakNumber")

    # print(consumer_address)
    #
    # if not w3.isAddress(consumer_address):
    #     print("Invalid address", file=sys.stderr)
    #     return render_template('validation_error.html', val_err1="Invalid Address")
    #
    # try:
    #     keccakNum = keccakNumber
    #     if keccakNum < 0:
    #         print("Invalid Amount")
    #         return render_template('validation_error.html', val_err2="Bid amount must be an unsigned integer")
    #
    # except ValueError:
    #     print("Invalid amount")
    #     return render_template('validation_error.html', val_err3="Bid amount must be an unsigned integer")

    try:
        # bid_amt_wei = w3.toWei(int_bid_amt, "ether")
        #print(consumer_address, keccakNumber)
        # bid_txn_dict = {
        #     'from': consumer_address,
        #     'to': contract_address,
        #     'gas': 2000000,
        #     'gasPrice': w3.toWei('40', 'gwei')
        #     }
        KeccakReturn = consumer_contract_instance.functions.keccakOfNumber(int(keccakNumber)).call() #Not important from where you call!

    except ValueError as e:
        print(e)
        return render_template('contract_error.html', contract_error=e)

    return render_template('index.html',keccak256= '0x'+KeccakReturn.hex())


@app.route("/consumePill", methods=['POST'])
def consumePill():
    print(w3.isConnected())

    consumer_address = request.form.get("ConsumerAddress")
    secrete_key = request.form.get("KeccakSecret")

    consumed = consumer_contract_instance.functions.consumeThePill(int(secrete_key)).transact({'from':consumer_address})
    print(consumer_contract_instance)
    return render_template('index.html', Status=consumed)


if __name__ == '__main__':
    app.run(debug=True)
