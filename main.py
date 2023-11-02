import json
import os

class Account:

    account_type = {1: "Asset", 2: "Liability",
                    3: "Equity", 4: "Revenue", 5: "Expense"}

    def __init__(self, title):
        self.title = title

    def create_account(self, type, normal_balance, accrual):
        acc = {"title": self.title, "type": self.account_type[type],
               "normal_balance": normal_balance, "is_accrual": accrual}

        accounts = []

        # Check if the accounts_chart.json file exists
        if os.path.exists("accounts_chart.json"):
            # Read existing accounts from the file
            with open("accounts_chart.json", "r") as chart:
                accounts = json.load(chart)

            # Check if the account with the given title already exists
            for existing_acc in accounts:
                if existing_acc["title"] == self.title:
                    print("Account already exists.")
                    break
            else:
                # If the loop completes without a break, add the new account
                accounts.append(acc)
                with open("accounts_chart.json", "w") as chart:
                    json.dump(accounts, chart)
                print("Account enlistment successful")
        else:
            # If the file doesn't exist, create a new one and add the account
            with open("accounts_chart.json", "w") as chart:
                json.dump([acc], chart)
            print("Account enlistment successful")



acc = Account("Cash")
acc.create_account(1, "Dr", False)
