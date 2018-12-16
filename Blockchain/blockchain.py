import hashlib
import json
import requests
from time import time
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self, testing=False):
        self.testing = testing
        self.chain = []
        self.current_transactions = []
        self.nodes = set({'localhost:5000'})

        if testing:
            # Create the genesis block
            self.genesis_block()
        else:
            self._read_chain()
            self.resolve_conflicts()
            if len(self.chain) == 0:
                self.genesis_block()
            self._write_chain()

    def genesis_block(self):
        self.chain = []
        self.new_block( previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """ 
        Create a new block and add it to the chain
          :param proof: <int> The proof given by the Proof of Work algorithm
          :param previous_hash: (optional) <str> Hash of previous block
          :return: <dict> New Block
        """
        block = {
            'index': len( self.chain ) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'merkle': self.hash(self.current_transactions),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Add the block to the chain
        self.chain.append( block )
        self._write_chain()

        return block

    def new_transaction(self, sender, recipient, amount):
        """ 
        Creates a new transaction to go into the next mined Block
          :param sender: <str> Address of the Sender
          :param recipient: <str> Address of the Recipient
          :param amount: <int> Amount
          :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0

        # Incrementally test numbers until a valid proof is reached
        while self.valid_proof( last_proof, proof ) is False:
            proof += 1
        return proof

    def register_node(self, address):
        """
        Add a new node to the list of nodes
          :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
          :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
          :param chain: <list> A blockchain
          :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            # Check that the hash of block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check the Proof of Work
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
          :return: <bool> True if our chain was replaced, False if not
        """
        neighbors = self.nodes
        print(neighbors)
        new_chain = None

        # We only care about chains longer than our own
        max_length = len(self.chain)

        # Get and verify all neighbors chains
        for node in neighbors:
            try:
                url = 'http://{}/chain'.format(node)
                response = requests.get(url)
                if response.status_code == 200:
                    length = response.json()['length']
                    chain  = response.json()['chain']

                    # Check if longer and chain is valid
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except:
                return False
        # Replace our chain if necessary
        if new_chain:
            self.chain = new_chain
            self._write_chain()
            return True

        return False

    def _read_chain(self, file='chain.json'):
        try:
            with open(file) as json_data:
                self.chain = json.load(json_data)
        except:
            return False
        return True

    def _write_chain(self, file='chain.json'):
        if self.testing:
            return True

        with open(file, 'w') as outfile:
            json.dump(self.chain, outfile)
        return True

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
          :param last_proof: <int> Previous Proof
          :param proof: <int> Current Proof
          :return: <bool> True if correct, False if not.
        """

        guess = '{}{}'.format(last_proof,proof).encode()
        guess_hash = hashlib.sha256( guess ).hexdigest()
        return guess_hash[:5] == "00000"

    @staticmethod
    def hash(block):
        """ 
        Hashes a block
          :param block: <dict> Block
          :return: <str> The hash of the block
        """
        block_string = json.dumps( block, sort_keys=True ).encode()
        return hashlib.sha256( block_string ).hexdigest()

    @property
    def last_block(self):
        """ Returns the last block in the chain """
        return self.chain[-1]
