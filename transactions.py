import time
import json
import hashlib
from model import Model
from database import TransactionDB, UnTransactionDB

class Transaction():
    def __init__(self, sender, recipient, amount):
        self.timestamp = int(time.time())
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.hash = self.gen_hash()

    def gen_hash(self):
        return hashlib.sha256((str(self.timestamp) + str(self.vin) + str(self.vout)).encode('utf-8')).hexdigest()

    def addToLocalDB(self):

    	ldb = LocalTransactionDB()

		transaction = {
		    'timestamp': self.timestamp,
		    'details': [
		        'sender': self.sender,
		        'recipient': self.recipient,
		        'amount': self.amount
		    ],
		    'hash': self.hash
		    'localIndex': ldb.getIndex()
		}

		ldb.insert(transaction)

        return ldb.getIndex()

def addToTransferQueue(hash):
	
	# TO DO: Call to function which automatically sync local chain with true chain
	ldb = LocalTransactionDB()
	trs = ldb.find(hash)

	f = open('data/queue', 'r')
	lines = f.readlines()
	f.close()

	lines.append(trs)

	f = open('data/queue', 'w')
	f.write(lines)
	f.close()
