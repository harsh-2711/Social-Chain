import hashlib
import json

from time import time
from uuid import uuid4

from urllib.parse import urlparse
import requests

import transactions
from database import TransactionDB

class Blockchain(object):

    def __init__(self):
        # Initiates the blockchain
        self.chain = []
        self.current_transactions = []

        # Creating a genesis block
        self.new_block(previous_hash=1, proof=100)

        # Unique nodes
        self.nodes = set()

    def new_block(self, proof, previous_hash=None):
        '''
        Adds new block to the chain

        :param proof: <int> The proof provided by Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous block

        :return: <dict> New block
        '''

        # Get all transactions from transaction queue
        allTransactions = transactions.getTransferQueue()

        for trans in allTransactions:
            self.current_transactions.append(trans)

        tdb = TransactionDB()
        try:
            lastIndex = tdb.getIndex()
        except:
            lastIndex = 0
        #print(lastIndex)

        block = {
            'index': lastIndex + 1,
            'timestamp': int(time()),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Resetting the current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        tdb.insert(block)

        transactions.emptyQueue()

        return block

    def new_transaction(self, timestamp, sender, recipient, amount, hash_key, localIndex):
        '''
        Creates a new transaction to move to the newly mined block

        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount transfered

        :return: <int> Index of the block that will hold this transaction (New block)
        '''

        self.current_transactions.append({
            'timestamp': timestamp,
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'hash': hash_key,
            'localIndex': localIndex
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        '''
        Adds hashing to the newly added block (SHA-256 hashing alogrithm)

        :param block: <dict> Newly created block to which hashing needs to be added

        :return: <str>
        '''

        # Sorting keys to prevent inconsistent hashing
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        '''
        Proof of Work Algorithm to check the validity of provided solution by miner to mine new block
        - Find a number p' such that hash(pp') contains leading numbers as 2711, where p is the previous p'
        - p is the previous proof and p' is the new proof

        :param last_proof: <int>
        :return: <int>
        '''

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        Validates the proof: Does hash(last_proof,proof) contains leading digits as 2711 or not?

        :param last_proof: <int> Previous proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, Fasle if algorithm isn't satisfied
        '''

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '2711'

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
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is the Consensus Algorithm, it resolves conflicts
        by replacing the user's chain with the longest one in the network.
        
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than the main
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in the network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace main chain if new valid longer chain is discovered
        if new_chain:
            self.chain = new_chain
            return True

        return False
