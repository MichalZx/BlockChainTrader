import hashlib
import json
from time import time

class Blockchain(object):
    """
    A simple blockchain implementation.

    This class represents a basic blockchain with methods for adding blocks,
    performing proof of work, creating new transactions, and calculating wallet balances.

    Attributes:
        chain (list): A list to store blocks in the blockchain.
        pending_transactions (list): A list to store pending transactions.
    """

    def __init__(self):
        """
        Initializes the blockchain with a genesis block.

        Args:
            self: The Blockchain object.
        """
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="BoarCoin Entertainment", proof=100)

    def proof_of_work(self, last_proof):
        """
        Performs proof of work to find a valid proof.

        Args:
            last_proof (int): The proof of the previous block.

        Returns:
            int: The valid proof found through proof of work.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof.

        Args:
            last_proof (int): The proof of the previous block.
            proof (int): The proof to be validated.

        Returns:
            bool: True if the proof is valid, False otherwise.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block in the blockchain.

        Args:
            proof (int): The proof of the new block.
            previous_hash (str): The hash of the previous block.

        Returns:
            dict: The newly created block.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        """
        Retrieves the last block in the blockchain.

        Returns:
            dict: The last block in the blockchain.
        """
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction.

        Args:
            sender (str): The sender's address.
            recipient (str): The recipient's address.
            amount (float): The amount to be transferred.

        Returns:
            int: The index of the block that will contain the transaction.
        """
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self, block):
        """
        Generates the SHA-256 hash of a block.

        Args:
            block (dict): The block to be hashed.

        Returns:
            str: The SHA-256 hash of the block.
        """
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash

    def get_balance(self, address):
        """
        Calculates the balance of a wallet address.

        Args:
            address (str): The wallet address.

        Returns:
            float: The balance of the wallet address.
        """
        balance = 0
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                if transaction['recipient'] == address:
                    balance += transaction['amount']
        return balance
