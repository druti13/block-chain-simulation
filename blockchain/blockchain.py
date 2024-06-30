# blockchain/blockchain.py

import hashlib
import time
from blockchain.transaction import Transaction

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash})"

class EnhancedBlockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.pending_smart_contracts = []
        self.file_storage = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), [])
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def create_new_block(self, nonce, previous_hash):
        block = Block(len(self.chain), previous_hash, time.time(), self.current_transactions, nonce)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, transaction):
        self.current_transactions.append(transaction)

    def add_smart_contract(self, contract):
        self.pending_smart_contracts.append(contract)

    def execute_smart_contracts(self):
        for contract in self.pending_smart_contracts:
            print(f"Executing smart contract: {contract}")
            # Add logic to execute the smart contract here

    def store_file(self, file_data):
        file_hash = hashlib.sha256(file_data.encode()).hexdigest()
        self.file_storage[file_hash] = file_data
        return file_hash

    def get_file(self, file_hash):
        return self.file_storage.get(file_hash, None)

    def proof_of_work(self, last_block):
        last_hash = last_block.hash
        nonce = 0
        while True:
            new_block = Block(len(self.chain), last_hash, time.time(), self.current_transactions, nonce)
            if new_block.hash.startswith('0000'):  # Adjust difficulty as needed
                return nonce
            nonce += 1

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
