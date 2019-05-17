# coding:utf-8
import json
import os

BASEDBPATH = 'data'
BLOCKFILE = 'block'
TXFILE = 'tx'
LTXFILE = 'ltx'
ACCOUNTFILE = 'account'
NODEFILE = 'node'

class BaseDB():

    filepath = ''

    def __init__(self):
        self.set_path()
        self.filepath = '/'.join((BASEDBPATH, self.filepath))

    def set_path(self):
        pass

    def find_all(self):
        return self.read()

    def insert(self, item):
        self.write(item)  

    def read(self):
        raw = ''
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath,'r+') as f:
            raw = f.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []
        return data

    def write(self, item):
        data = self.read()
        if isinstance(item,list):
            data = data + item
        else:
            data.append(item)
        with open(self.filepath,'w+') as f:
            f.write(json.dumps(data))
        return True

    def clear(self):
        with open(self.filepath,'w+') as f:
            f.write('')

    def hash_insert(self, item):
        exists = False
        for i in self.find_all():
            if item['hash'] == i['hash']:
                exists = True
                break
        if not exists:
            self.write(item)  

class NodeDB(BaseDB):

    def set_path(self):
        self.filepath = NODEFILE  


class AccountDB(BaseDB):
    def set_path(self):
        self.filepath = ACCOUNTFILE  

    def find_one(self):
        ac = self.read()
        return ac[0]


class BlockChainDB(BaseDB):

    def set_path(self):
        self.filepath = BLOCKFILE

    def last(self):
        bc = self.read()
        if len(bc) > 0:
            return bc[-1]
        else:
            return []

    def find(self, hash):
        one = {}
        for item in self.find_all():
            if item['hash'] == hash:
                one = item
                break
        return one

    def insert(self, item):
        self.hash_insert(item)

class TransactionDB(BaseDB):
    '''
    True Transactions of blockchain.
    '''
    def set_path(self):
        self.filepath = TXFILE

    def find(self, hash):
        one = {}
        for item in self.find_all():
            if item['hash'] == hash:
                one = item
                break
        return one

    def insert(self, txs):
        if not isinstance(txs,list):
            txs = [txs]
        for tx in txs:
            self.hash_insert(tx)

    def getIndex(self):
        counter = 0
        for item in self.find_all():
            counter += 1
        counter +=1
        return counter

class LocalTransactionDB(BaseDB):
    '''
    Local Transactions.
    '''
    def set_path(self):
        self.filepath = LTXFILE

    def find(self, hash):
        one = {}
        for item in self.find_all():
            if item['hash'] == hash:
                one = item
                break
        return one

    def insert(self, txs):
        if not isinstance(txs,list):
            txs = [txs]
        for tx in txs:
            self.hash_insert(tx)

    def getIndex(self):
        counter = 0
        for item in self.find_all():
            counter += 1
        counter +=1
        return counter

    def find_with_index(self, local_index):
        one = {}
        for item in self.find_all():
            if item['localIndex'] == local_index:
                one = item
                break
        return one