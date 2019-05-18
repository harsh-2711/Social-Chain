from textwrap import dedent
from uuid import uuid4
import json

from flask import Flask, jsonify, request

from Blockchain import Blockchain
from database import TransactionDB, LocalTransactionDB
from transactions import Transaction

import account
import transactions

import time

import hashlib

# Instantiates the node
app = Flask(__name__)

# Generates a globally unique address for this node
miner = str(uuid4()).replace('-','')

# Initiates the Blockchain
blockchain = Blockchain()

# Percentage cut from total amount
perc_cut = 0.1

@app.route('/')
def index():
    return "App is deployed"

@app.route('/new_account', methods=['GET'])
def new_account():
    private_key, public_key, address = account.new_account()
    response = {
        'Private Key': private_key,
        'Public Key': public_key,
        'Address': address
    }
    return jsonify(response), 200

@app.route('/get_account', methods=['GET'])
def get_account():
    latest_account = account.get_account()
    return jsonify(latest_account), 200

@app.route('/mine', methods=['GET'])
def mine():
    # TO DO: Sync current chain with true chain

    # Running proof of work algorithm to get the next proof...
    tdb = TransactionDB()
    try:
        lastIndex = tdb.getIndex()
    except:
        lastIndex = 1
    last_block = tdb.find_with_index(lastIndex)
    #print(last_block)
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Get all transactions from transaction queue
    allTransactions = transactions.getTransferQueue()
    print(allTransactions)
    totalAmount = 0

    for trans in allTransactions:
        totalAmount += trans['amount']

    # Provide a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        timestamp=int(time.time()),
        sender="0",
        recipient=miner,
        amount=(totalAmount*perc_cut)/100,
        hash_key=hashlib.sha256((str(int(time.time()))).encode('utf-8')).hexdigest(),
        localIndex=0
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    transaction = Transaction(values['sender'], values['recipient'], values['amount'])
    index = transaction.addToLocalDB()
    
    #index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index-1}'}
    return jsonify(response), 201

@app.route('/transactions/add/queue', methods=['POST'])
def addTransactionToQueue():
    values = request.get_json()

    required = ['hash', 'index']
    if not any(k in values for k in required):
        return 'Missing values', 400

    ldb = LocalTransactionDB()

    err_hash_resp = {'message': f'Incorrect Hash'}
    err_index_resp = {'message': f'Incorrect Index'}
    succ_resp = {'message': f'Transaction added to queue successfully'}

    if 'hash' in values:
        item = ldb.find(values['hash'])
        if len(item) < 1:
            return jsonify(err_hash_resp), 401
        else:
            transactions.addToTransferQueue_Hash(values['hash'])
            return jsonify(succ_resp), 200
    else:
        item = ldb.find_with_index(values['index'])
        if not item:
            return jsonify(err_index_resp), 401
        else:
            transactions.addToTransferQueue_Index(values['index'])
            return jsonify(succ_resp), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
