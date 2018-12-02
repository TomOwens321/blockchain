from blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4
from textwrap import dedent
import json
import hashlib


# Instantiate our node
app = Flask(__name__)

# Generate a unique id for this node
node_identifier = str(uuid4()).replace('-','')

# Instantiate the blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check for required values
    required = ['sender', 'recipient', 'amount']
    # if not all(k in values for k in required):
    #     return 'Missing Values', 400

    # Create the new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to block {}'.format(index)}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
