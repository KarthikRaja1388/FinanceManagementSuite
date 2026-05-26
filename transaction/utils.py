from decimal import Decimal

def apply_transaction_effect(account,transaction_type, amount):
    amount = Decimal(amount)

    if transaction_type == 'INC':
        account.current_balance += amount
    else:
        account.current_balance -= amount

    account.save()

def reverse_transaction_effect(account,transaction_type, amount):
    amount = Decimal(amount)

    if transaction_type == 'INC':
        account.current_balance -= amount
    else:
        account.current_balance += amount

    account.save()