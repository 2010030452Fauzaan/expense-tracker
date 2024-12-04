import sqlite3
from tabulate import tabulate

# Database setup
def setup_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount REAL,
            date TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add an expense
def add_expense(category, amount, date, description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (category, amount, date, description)
        VALUES (?, ?, ?, ?)
    """, (category, amount, date, description))
    conn.commit()
    conn.close()

# View all expenses
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows

# View total expenses by category
def total_by_category():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Delete an expense by ID
def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

# Main menu
def main_menu():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total by Category")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter category (e.g., Food, Transport): ")
            amount = float(input("Enter amount: "))
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            add_expense(category, amount, date, description)
            print("Expense added successfully!")

        elif choice == "2":
            expenses = view_expenses()
            if expenses:
                print("\nExpenses:")
                print(tabulate(expenses, headers=["ID", "Category", "Amount", "Date", "Description"], tablefmt="pretty"))
            else:
                print("No expenses recorded.")

        elif choice == "3":
            totals = total_by_category()
            if totals:
                print("\nTotal by Category:")
                print(tabulate(totals, headers=["Category", "Total Amount"], tablefmt="pretty"))
            else:
                print("No expenses recorded.")

        elif choice == "4":
            expense_id = int(input("Enter the ID of the expense to delete: "))
            delete_expense(expense_id)
            print("Expense deleted successfully!")

        elif choice == "5":
            print("Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the app
if __name__ == "__main__":
    setup_database()
    main_menu()
