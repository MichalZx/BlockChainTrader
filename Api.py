"""
A simple blockchain application with a Flask-based GUI.

This application allows users to interact with a blockchain through a graphical user interface (GUI).
Users can mine new blocks, view the blockchain, create new transactions, and view their wallet information.

Attributes:
    app (Flask): The Flask application instance.
    node_identifier (str): Globally unique identifier for the node.
    blockchain (Blockchain): Instance of the Blockchain class.

"""

from uuid import uuid4
from flask import Flask, jsonify, request
from Blockchain import Blockchain

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    """
    Mines a new block in the blockchain.

    Returns:
        JSON: A JSON response indicating the status of the mining operation and the details of the new block.
    """
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Creates a new transaction in the blockchain.

    Returns:
        JSON: A JSON response indicating the status of the transaction creation.
    """
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    try:
        amount = int(values['amount'])
    except ValueError:
        amount = 0

    sender_balance = blockchain.get_balance(values['sender'])
    if sender_balance < amount:
        return jsonify({'message': 'Insufficient balance for transaction'}), 403

    index = blockchain.new_transaction(values['sender'], values['recipient'], amount)

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    """
    Retrieves the full blockchain.

    Returns:
        JSON: A JSON response containing the full blockchain and its length.
    """
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/balance', methods=['GET'])
def get_balance():
    """
    Retrieves the balance of the current node.

    Returns:
        JSON: A JSON response containing the wallet address and balance of the node.
    """
    balance = blockchain.get_balance(node_identifier)
    response = {'address': node_identifier, 'balance': balance}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
