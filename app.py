import json
import sys
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request

w3 = Web3(HTTPProvider("http://localhost:7545"))

print(w3.isConnected())


# compile your smart contract with truffle first
manufacturerContract = json.load(open('./build/contracts/Manufacturer.json'))
maufacturer_abi = manufacturerContract['abi']
maufacturer_address = manufacturerContract['networks']['5777']['address']

# Initialize a contract object with the smart contract compiled artifacts
manufacturer_contract = w3.eth.contract(address=maufacturer_address, abi=maufacturer_abi)


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    print(w3.isConnected())
    return render_template('index.html')

@app.route("/createPills", methods=['POST'])
def createPills():

    print(w3.isConnected())
    manufacturer_address = request.form.get("ManufacturerAddress")

    print(manufacturer_address)

    if not w3.isAddress(manufacturer_address):
        print("Invalid address", file=sys.stderr)
        return render_template('validation_error.html', val_err1="Invalid Address")

    try:

        bid_txn_hash = manufacturer_contract.functions.createpills().transact({'from':manufacturer_address})
        tx_receipt = w3.eth.waitForTransactionReceipt(bid_txn_hash.hex())
        print(tx_receipt)
        logs = manufacturer_contract.events.PillCreated().processReceipt(tx_receipt)
    except ValueError as e:
        print(e)
        return render_template('contract_error.html', contract_error=e)

    return render_template('index.html',TransactionHash = bid_txn_hash.hex(),creationStatus='Created', EmitedMessage1 = logs[0]['args']['message'],EmitedMessage2 = logs[0]['args']['description'])

# Talking about Consumer
consumerContract = json.load(open('./build/contracts/Consumer.json'))
consumer_abi = consumerContract['abi']
consumer_address = consumerContract['networks']['5777']['address']

consumer_contract_instance = w3.eth.contract(abi=consumer_abi, address=consumer_address)

@app.route("/keccak256", methods=['POST'])
def keccak256():
    print(w3.isConnected())
    keccakNumber = request.form.get("keccakNumber")

    try:
        KeccakReturn = consumer_contract_instance.functions.keccakOfNumber(int(keccakNumber)).call() #Not important from where you call!

    except ValueError as e:
        print(e)
        return render_template('contract_error.html', contract_error=e)

    return render_template('index.html',keccak256= '0x'+KeccakReturn.hex())


@app.route("/consumePill", methods=['POST'])
def consumePill():
    print(w3.isConnected())

    consumer_address = request.form.get("ConsumerAddress")

    print(consumer_address)

    if not w3.isAddress(consumer_address):
        print("Invalid address", file=sys.stderr)
        return render_template('validation_error.html', val_err1="Invalid Address")

    try:
        secrete_key = request.form.get("KeccakSecret")

        consumed = consumer_contract_instance.functions.consumeThePill(int(secrete_key)).transact({'from':consumer_address})
        print(consumer_contract_instance)
        tx_receipt = w3.eth.waitForTransactionReceipt(consumed.hex())
        print(tx_receipt)
        logs = consumer_contract_instance.events.EatPill().processReceipt(tx_receipt)

    except ValueError as e:
        print(e)
        return render_template('contract_error.html', contract_error=e)

    print(logs)

    return render_template('index.html', TxH=consumed.hex(),Status = 'Consumed', EmitedMessageConsume1 = logs[0]['args']['_indexed'],EmitedMessageConsume2 = logs[0]['args']['consumer'])


if __name__ == '__main__':
    app.run(debug=True)
