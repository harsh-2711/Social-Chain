import time
import json
import hashlib
from model import Model
from database import TransactionDB, LocalTransactionDB

class Transaction():
    def __init__(self, sender, recipient, amount):
        self.timestamp = int(time.time())
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.hash = self.gen_hash()

    def gen_hash(self):
        return hashlib.sha256((str(self.timestamp)).encode('utf-8')).hexdigest()

    def addToLocalDB(self):

    	ldb = LocalTransactionDB()

    	transaction = {
		    'timestamp': self.timestamp,
			'sender': self.sender,
			'recipient': self.recipient,
			'amount': self.amount,
		    'hash': self.hash,
		    'localIndex': ldb.getIndex()
	    }

    	ldb.insert(transaction)

    	return ldb.getIndex()

def addToTransferQueue(hash):
	
	ldb = LocalTransactionDB()
	trs = ldb.find(hash)

	f = open('data/queue', 'r')
	lines = f.readlines()
	f.close()

	lines.append(trs)

	f = open('data/queue', 'w')

	for line in lines:
		f.write(str(line))

	f.close()
