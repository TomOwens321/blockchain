from blockchain import Blockchain
from flask import Flask, jsonify
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
    return "We'll create a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
