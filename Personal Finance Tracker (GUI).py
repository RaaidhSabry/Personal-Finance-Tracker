import tkinter as tk
from tkinter import ttk, messagebox
import json

#import python modules


# Global dictionary to store transactions
transactions = {}

# File handling functions

#Load Transactions
def load_transactions():
    try:
        with open('transactions.json', 'r') as file:
            data = json.load(file)
            transactions.update(data)
    except:
        TypeError

#save transactions
def save_transactions():

    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)

#read bulk transactions

def read_bulk_transactions_from_file(filename):

    try:
        with open(filename, 'r') as file:
            transaction = [json.loads(line.strip()) for line in file]
            read_bulk = {}

            for data in transaction:
                read_bulk.update(data)
            return read_bulk
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{filename}': {str(e)}")

    except Exception as e:
        print(f"Error occurred while reading transactions: {str(e)}")

#Extracted data from file location

filename = 'text.txt'

#Save bulk transactions

def save_bulk_transactions(read_transactions, dictionary_file):

    try:
        with open(dictionary_file, 'w') as json_file:
            json.dump(read_transactions, json_file, indent=4)
            print(f"Dictionary saved to '{dictionary_file}' successfully.")

    except Exception as e:
        print(f"Error occurred while saving JSON to '{dictionary_file}': {str(e)}")

#data extracted pushed to new file location      

dictionary_file = "transactions.json"

# Feature implementations

#Get a Transaction ID

transaction_id_counter = 1

#add a transaction

def add_transaction(type_of_expense, amount, date):
    
    #global is used to create a variable inside a function
    global transaction_id_counter

    if type_of_expense not in transactions:
        transactions[type_of_expense] = []
        type_of_expense.lower()
        transaction_id_counter = 0

    transaction_id = transaction_id_counter
    transaction_id_counter += 1

    transactions[type_of_expense].append({"amount": amount, "date": date})
    pass


# Validate amount

def validate_float_input(amount):

    try:
        float_value = float(amount)
        return float_value
    
    except ValueError:
        raise ValueError("Invalid input. Please enter a numerical value.")
    
# Validate date

from datetime import datetime

def validate_date_input(date):

    while True:

        try:
            date = datetime.strptime(date, '%Y-%m-%d')
            date_input = date.strftime('%Y-%m-%d')
            return date_input
        
        except ValueError:
            raise ValueError('Invalid input, the date should be in the format YYYY-MM-DD')



#Validate Transaction ID

def validate_Transaction_id(transaction_id):

    try:
        transaction_id = int(transaction_id)

        for transactions_list in transactions.values():
            if any(transaction.get("ID") == transaction_id for transaction in transactions_list):
                return transaction_id
        raise ValueError("Transaction ID not found.")
    
    except ValueError:
        raise ValueError("Invalid input. Transaction ID must be an integer.")
    
#view transactions

def view_transactions():

    for expense_type, transactions_list in transactions.items():
        print(expense_type)
        for transaction in transactions_list:
            print(transaction)
    return

#update a transaction

def update_transaction(type_of_expense, transaction_id, amount, date):
    
    transactions_list = transactions.get(type_of_expense, [])
    transaction_id = validate_Transaction_id(transaction_id)

    #Locating transaction ID
    for transaction in transactions:
        if transaction[0] == transaction_id:
            print("Current Transaction:", transaction)


    # Update the transaction
    for transaction in transactions_list:
        if transaction["ID"] == transaction_id:
            transaction["amount"] = amount
            transaction["date"] = date
            save_transactions()
            return


#delete a transaction

def delete_transaction(type_of_expense, transaction_id):
    
    transactions_list = transactions.get(type_of_expense, [])

    #validation for transaction ID

    try:
        transaction_id = validate_Transaction_id(transaction_id)

    except ValueError as ve:
        print(ve)
        return
    
    #locating transaction ID
    for transaction in transactions_list:
        if transaction["ID"] == transaction_id:
            print("Transaction to delete:", transactions_list)

        #Confirmation of deletion
            confirmation = input("Confirm deletion (yes/no): ").lower()

            #for yes
            if confirmation == "yes":
                transactions_list.remove(transaction)
                print("Transaction deleted successfully!")
                save_transactions()
                return
                    
            #for no
            elif confirmation == "no":
                print("Deletion cancelled.")
                return
            
            #for invalid input
            else:
                print('Invalid Input')
                break
                
    print("Transaction with ID {} not found for type of expense {}.".format(transaction_id, type_of_expense))

                
#summary of transactions
def display_summary():

    for expense_type, transactions_list in transactions.items():
        total_amount = sum(int(transaction["amount"]) for transaction in transactions_list)
        print(f"{expense_type}: Total Amount - {int(total_amount)}")

def display_graphic():
    class PersonalFinanceTrackerApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Personal Finance Tracker")

            # Create a frame for category buttons
            self.category_frame = ttk.Frame(self.root)
            self.category_frame.pack(padx=10, pady=10)

            # Create buttons for each category
            self.category_buttons = {}
            self.create_category_buttons()

            # Create a frame for the transaction display table
            self.table_frame = ttk.Frame(self.root)
            self.table_frame.pack(padx=10, pady=10)

            # Create a widget for displaying transactions
            self.transaction_tree = ttk.Treeview(self.table_frame, columns=("Date", "Amount", "Category"))
            self.transaction_tree.heading("#0", text="ID")
            self.transaction_tree.heading("Date", text="Date", command=lambda: self.sort_by_column("Date", False))
            self.transaction_tree.heading("Amount", text="Amount", command=lambda: self.sort_by_column("Amount", False))
            self.transaction_tree.heading("Category", text="Category")
            self.transaction_tree.pack()

            # Search bar and button
            self.search_var = tk.StringVar()
            self.search_entry = ttk.Entry(self.root, textvariable=self.search_var)
            self.search_entry.pack(pady=5)
            self.search_button = ttk.Button(self.root, text="Search", command=self.search_transactions)
            self.search_button.pack()

        # Create buttons for category
        def create_category_buttons(self):
            categories = ["groceries", "salary", "shopping"] 
            for idx, category in enumerate(categories):
                button = ttk.Button(self.category_frame, text=category, command=lambda c=category: self.show_transactions(c))
                button.grid(row=0, column=idx, padx=10, pady=10)
                self.category_buttons[category] = button

        # Show transactions for the selected category
        def show_transactions(self, category):
            self.transaction_tree.delete(*self.transaction_tree.get_children())
            try:
                with open("transactions.json", "r") as file:
                    data = json.load(file)
                    transactions = data.get(category, [])
                    for idx, transaction_data in enumerate(transactions):
                        try:
                            self.transaction_tree.insert("", "end", text=int(idx), values=(transaction_data["date"], transaction_data["amount"], category))
                        except KeyError:
                            messagebox.showerror("Error", f"Transaction in category '{category}' at index {idx} is missing required fields.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Transactions file not found!")


        # Search transactions by keyword
        def search_transactions(self):
            query = self.search_var.get().lower()
            self.transaction_tree.delete(*self.transaction_tree.get_children())
            try:
                with open("transactions.json", "r") as file:
                    data = json.load(file)
                    for category, transactions in data.items():
                        for idx, transaction_data in enumerate(transactions):
                            try:
                                if query in transaction_data["date"].lower() or query in str(transaction_data["amount"]).lower() or query in category.lower():
                                    self.transaction_tree.insert("", "end", text=int(idx), values=(transaction_data["date"], transaction_data["amount"], category))
                            except KeyError:
                                messagebox.showerror("Error", f"Transaction in category '{category}' at index {idx} is missing required fields.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Transactions file not found!")

    def main():
        root = tk.Tk()
        app = PersonalFinanceTrackerApp(root)
        root.mainloop()

    if __name__ == "__main__":
        main()
#Main Menu

def main():

    while True:
        load_transactions()
        print("\n1. Create Transaction")
        print("2. Read Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Bulk Read Transactions from File")
        print("6. Display summary")
        print("7. GUI Model")
        print("8. Exit")

        #input values for choices in main menu
        choice = input("Enter your choice: ")


        #choice to create a transaction
        if choice == '1':
            type_of_expense = input("Enter type of expense: ")
            
            #validation for amount

            while True:

                try:
                    amount= input("Enter amount :")
                    float_value = validate_float_input(amount)
                    print("Valid float value:", float_value)

                except ValueError as ve:
                    print(ve)
                else:

                    break

            #validation for date

            while True:

                try:    
                    date = input("Enter date (YYYY-MM-DD) : ")
                    date_input = validate_date_input(date)
                    print("valid date:", date_input)

                except ValueError as ve:
                    print(ve)

                else:
                    break


            add_transaction(type_of_expense, amount, date)
            print("Transaction created successfully.")
            save_transactions()


        #choice to view transactions
        elif choice == '2':
            print(view_transactions(),"of the transactions are left without being read")


        #choice to update a transaction
        elif choice == '3':

            type_of_expense = input("Enter type of expense: ")

            #Validation for transaction ID

            while True:

                try:
                    transaction_id = str(input("Enter transaction ID of transaction to update: "))
                    ID_input = validate_Transaction_id(transaction_id)
                    print("The transaction ID selected is ",ID_input)

                except ValueError as ve:
                    print(ve)

                else:
                    break
            
            #validation for amount

            while True:

                try:
                    amount= input("Enter amount :")
                    float_value = validate_float_input(amount)
                    print("Amount:", float_value)

                except ValueError as ve:
                    print(ve)

                else:
                    break

            #validation for date

            while True:

                try:    
                    date = input("Enter date (YYYY-MM-DD) : ")
                    date_input = validate_date_input(date)
                    print("Date:", date_input)

                except ValueError as ve:
                    print(ve)

                else:
                    break

            update_transaction(type_of_expense, transaction_id, amount, date)
            print("Transaction updated successfully.")
            save_transactions()


        #choice to delete a transaction
        elif choice == '4':

            type_of_expense = input("Enter type of expense: ")

            #Validations for transaction ID

            while True:
                try:

                    transaction_id = str(input("Enter transaction ID of transaction to delete: "))
                    ID_input = validate_Transaction_id(transaction_id)
                    print("The transaction ID selected is ",ID_input)

                except ValueError as ve:
                    print(ve)
                    
                else:
                    break

            delete_transaction(type_of_expense, transaction_id)
            save_transactions()


        #choice to read and save bulk transactions
        elif choice == '5':
                read_transactions = read_bulk_transactions_from_file(filename)
                print(read_transactions)
                save_bulk_transactions(read_transactions, dictionary_file)

        #choice to display the summary
        elif choice == '6':
            display_summary()

        #choice to open GUI model
        elif choice == '7':
            display_graphic()

        #choice to exit the program   
        elif choice == '8':
            print("Exiting program.")
            break
        
        #Error raised if invalid choice is selected
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
