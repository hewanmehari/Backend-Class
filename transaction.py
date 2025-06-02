from datetime import datetime

class Transaction:
    def __init__(self, narration, amount, transaction_type):
        self.date_time = datetime.now()
        self.narration = narration
        self.amount = amount
        self.transaction_type = transaction_type

    def __str__(self):
        return f"{self.date_time.strftime('%Y-%m-%d %H:%M:%S')} | {self.transaction_type.upper()} | {self.amount} | {self.narration}"



class Account:
    def __init__(self, owner, account_number):
        self.__owner = owner
        self.__account_number = account_number
        self.__transactions = []
        self.__loan = 0
        self.__frozen = False
        self.__minimum_balance = 0
        self.__closed = False

    def deposit(self, amount, narration="Deposit"):
        if self.__closed:
            return "Account is closed."
        if self.__frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Amount must be positive."
        self.__transactions.append(Transaction(narration, amount, "deposit"))
        return f"Deposited {amount}. New balance: {self.get_balance()}"

    def withdraw(self, amount, narration="Withdrawal"):
        if self.__closed:
            return "Account is closed."
        if self.__frozen:
            return "Account is frozen."
        if amount <= 0:
            return "Amount must be positive."
        if self.get_balance() - amount < self.__minimum_balance:
            return "Insufficient balance (considering minimum balance requirement)."
        self.__transactions.append(Transaction(narration, -amount, "withdrawal"))
        return f"Withdrew {amount}. New balance: {self.get_balance()}"

    def transfer(self, amount, target_account):
        if self.__closed or target_account.__closed:
            return "One of the accounts is closed."
        if self.__frozen or target_account.__frozen:
            return "One of the accounts is frozen."
        if amount <= 0:
            return "Amount must be positive."
        if self.get_balance() - amount < self.__minimum_balance:
            return "Insufficient funds for transfer."
        self.__transactions.append(Transaction("Transfer to " + target_account.get_owner(), -amount, "transfer"))
        target_account.__transactions.append(Transaction("Transfer from " + self.__owner, amount, "transfer"))
        return f"Transferred {amount} to {target_account.get_owner()}. Your new balance: {self.get_balance()}"

    def request_loan(self, amount):
        if self.__closed:
            return "Account is closed."
        if amount <= 0:
            return "Loan amount must be positive."
        self.__loan += amount
        self.__transactions.append(Transaction("Loan granted", amount, "loan"))
        return f"Loan of {amount} approved. Total loan: {self.__loan}"

    def repay_loan(self, amount):
        if self.__closed:
            return "Account is closed."
        if amount <= 0:
            return "Repayment must be positive."
        repayment = min(amount, self.__loan)
        self.__loan -= repayment
        self.__transactions.append(Transaction("Loan repayment", -repayment, "loan_repayment"))
        return f"Loan repayment of {repayment} accepted. Remaining loan: {self.__loan}"

    def get_balance(self):
        return sum(t.amount for t in self.__transactions)

    def view_account_details(self):
        return f"Owner: {self.__owner}\nAccount Number: {self.__account_number}\nBalance: {self.get_balance()}"

    def change_owner(self, new_name):
        if self.__closed:
            return "Account is closed."
        self.__owner = new_name
        return f"Account owner changed to {self.__owner}"

    def account_statement(self):
        print("ACCOUNT STATEMENT")
        for txn in self.__transactions:
            print(txn)
        print(f"Current balance: {self.get_balance()}")

    def apply_interest(self):
        if self.__closed:
            return "Account is closed."
        interest = self.get_balance() * 0.05
        self.__transactions.append(Transaction("Interest added", interest, "interest"))
        return f"Interest of {interest:.2f} applied. New balance: {self.get_balance()}"

    def freeze_account(self):
        self.__frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.__frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.__minimum_balance = amount
        return f"Minimum balance set to {amount}."

    def close_account(self):
        self.__transactions.append(Transaction("Account closed", -self.get_balance(), "closure"))
        self.__closed = True
        return "Account has been closed. Balance set to zero and all transactions stopped."

    def get_owner(self):
        return self.__owner

    def get_account_number(self):
        return self.__account_number



accounts = {}


def find_account(account_number):
    return accounts.get(account_number)



