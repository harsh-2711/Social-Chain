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

def writeToFile(trs):

	with open('data/queue', 'r+') as f:
	    raw = f.readline()
	    if len(raw) > 0:
	    	data = json.loads(raw)
	    else:
	    	data = []

	if isinstance(trs,list):
	    data = data + trs
	else:
	    data.append(trs)

	with open('data/queue', 'w+') as f:
	    f.write(json.dumps(data))

def addToTransferQueue_Hash(hash):
	
	ldb = LocalTransactionDB()
	trs = ldb.find(hash)

	writeToFile(trs)

def addToTransferQueue_Index(localIndex):
	
	ldb = LocalTransactionDB()
	trs = ldb.find_with_index(localIndex)

	writeToFile(trs)

def getTransferQueue():

	f = open('data/queue', 'r+')
	raw = f.readline()
	f.close()

	try:
		data = json.loads(raw)
	except:
		data = []

	return data

def getA():
	f = open('data/queue', 'r+')
	raw = f.readline()
	f.close()

	data = json.loads(raw)
	return data

def emptyQueue():

	f = open('data/queue', 'w')
	f.write("")
	f.close()
