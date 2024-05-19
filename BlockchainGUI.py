import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyperclip

class BlockchainGUI:
    """
    A simple GUI interface for interacting with a blockchain.

    Attributes:
        root (Tk): The root Tkinter window.
        label (Label): Label widget displaying the title.
        image (PIL.Image.Image): Image object for the logo.
        photo (ImageTk.PhotoImage): PhotoImage object for displaying the logo.
        image_label (Label): Label widget for displaying the logo.
        mine_button (Button): Button widget for mining a new block.
        view_chain_button (Button): Button widget for viewing the blockchain.
        new_transaction_button (Button): Button widget for creating a new transaction.
        view_wallet_button (Button): Button widget for viewing the wallet information.
    """

    def __init__(self, root):
        """
        Initializes the BlockchainGUI.

        Args:
            root (Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("BRC Trader")

        # Title label
        self.label = tk.Label(root, text="Boar Coin (BRC)", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Logo
        self.image = Image.open("BoarCoin.png")
        self.image = self.image.resize((250, 250), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(root, image=self.photo)
        self.image_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Buttons
        self.mine_button = tk.Button(root, text="Mine block", command=self.mine)
        self.mine_button.grid(row=2, column=0, padx=10, pady=5)

        self.view_chain_button = tk.Button(root, text="View Chain", command=self.view_chain)
        self.view_chain_button.grid(row=2, column=1, padx=10, pady=5)

        self.new_transaction_button = tk.Button(root, text="New Transaction", command=self.new_transaction)
        self.new_transaction_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.view_wallet_button = tk.Button(root, text="My Wallet", command=self.view_wallet)
        self.view_wallet_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def mine(self):
        """
        Sends a request to the server to mine a new block.
        Displays a success or error message box based on the response.
        """
        response = requests.get('http://localhost:5000/mine')
        if response.status_code == 200:
            messagebox.showinfo("Success", "New Block Forged")
        else:
            messagebox.showerror("Error", "Failed to mine block")

    def view_chain(self):
        """
        Sends a request to the server to retrieve the blockchain.
        Displays the blockchain information in a message box.
        """
        response = requests.get('http://localhost:5000/chain')
        if response.status_code == 200:
            chain = response.json()['chain']
            length = response.json()['length']
            chain_str = "\n".join([f"Block {block['index']}: {block['transactions']}" for block in chain])
            messagebox.showinfo("Blockchain", f"Chain Length: {length}\n\n{chain_str}")
        else:
            messagebox.showerror("Error", "Failed to retrieve blockchain")

    def new_transaction(self):
        """
        Opens a new window for creating a new transaction.
        Sends transaction data to the server upon submission.
        Displays success or error message box based on the response.
        """
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("New Transaction")

        sender_label = tk.Label(transaction_window, text="Sender:")
        sender_label.grid(row=0, column=0, padx=10, pady=5)
        sender_entry = tk.Entry(transaction_window)
        sender_entry.grid(row=0, column=1, padx=10, pady=5)

        recipient_label = tk.Label(transaction_window, text="Recipient:")
        recipient_label.grid(row=1, column=0, padx=10, pady=5)
        recipient_entry = tk.Entry(transaction_window)
        recipient_entry.grid(row=1, column=1, padx=10, pady=5)

        amount_label = tk.Label(transaction_window, text="Amount:")
        amount_label.grid(row=2, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(transaction_window)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)

        def submit_transaction():
            sender = sender_entry.get()
            recipient = recipient_entry.get()
            amount = amount_entry.get()

            if not sender or not recipient or not amount:
                messagebox.showerror("Error", "All fields are required")
                return

            response = requests.post('http://localhost:5000/transactions/new', json={
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            })

            if response.status_code == 201:
                messagebox.showinfo("Success", "Transaction created successfully")
                transaction_window.destroy()
            elif response.status_code == 403:
                messagebox.showinfo("Success", "Insufficient balance for transaction")
                transaction_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to create transaction")

        submit_button = tk.Button(transaction_window, text="Submit", command=submit_transaction)
        submit_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def view_wallet(self):
        """
        Sends a request to the server to retrieve wallet information.
        Displays the wallet address and balance in a new window.
        """
        response = requests.get('http://localhost:5000/balance')
        if response.status_code == 200:
            data = response.json()
            address = data['address']
            balance = data['balance']
            wallet_info = f"Address: {address}\nBalance: {balance}BRC"

            wallet_window = tk.Toplevel(self.root)
            wallet_window.title("Wallet Info")

            wallet_label = tk.Label(wallet_window, text=wallet_info, justify=tk.LEFT)
            wallet_label.grid(row=0, column=0, padx=10, pady=10)

            def copy_address():
                """
                Copies the wallet address to the clipboard.
                Displays a message box confirming the copy operation.
                """
                pyperclip.copy(address)
                messagebox.showinfo("Copied", "Wallet address copied to clipboard")

            copy_button = tk.Button(wallet_window, text="Copy Address", command=copy_address)
            copy_button.grid(row=1, column=0, padx=10, pady=5)
        else:
            messagebox.showerror("Error", "Failed to retrieve wallet information")

if __name__ == "__main__":
    root = tk.Tk()
    blockchain_gui = BlockchainGUI(root)
    root.mainloop()