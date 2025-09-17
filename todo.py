import csv
import os
import datetime
from collections import defaultdict

# --- File and Data Configuration ---
# Use a CSV file to store expenses.
FILE_NAME = 'expenses.csv'
FIELD_NAMES = ['Date', 'Category', 'Amount', 'Description']

def init_file():
    """Initializes the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
            writer.writeheader()
        print(f"Initialized new expense file: {FILE_NAME}")

# --- Core Functionalities ---

def add_expense():
    """Prompts the user to add a new expense entry."""
    print("\n--- Add New Expense ---")
    
    # Error handling for Date
    while True:
        try:
            date_str = input("Enter date (YYYY-MM-DD): ")
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            
    # Error handling for Amount
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be a positive number.")
            else:
                break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    category = input("Enter category (e.g., Food, Transport, Bills): ")
    description = input("Enter a brief description: ")

    new_expense = {
        'Date': date_str,
        'Category': category.capitalize(),  # Capitalize for consistency
        'Amount': amount,
        'Description': description
    }

    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writerow(new_expense)
    print("Expense added successfully!")

def view_expenses():
    """Displays all recorded expenses."""
    print("\n--- All Expenses ---")
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        print("No expenses recorded yet.")
        return
        
    with open(FILE_NAME, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        if not data:
            print("No expenses found.")
            return

        for expense in data:
            print(f"Date: {expense['Date']}, Category: {expense['Category']}, "
                  f"Amount: ${float(expense['Amount']):.2f}, Description: {expense['Description']}")

def search_expenses():
    """Allows the user to search expenses by date or category."""
    print("\n--- Search Expenses ---")
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        print("No expenses recorded yet.")
        return

    search_by = input("Search by 'date' or 'category'? ").lower()
    search_term = input(f"Enter the {search_by} to search for: ")
    
    found_expenses = []
    with open(FILE_NAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if search_by == 'date' and row['Date'] == search_term:
                found_expenses.append(row)
            elif search_by == 'category' and row['Category'].lower() == search_term.lower():
                found_expenses.append(row)
    
    if found_expenses:
        print("\n--- Search Results ---")
        for expense in found_expenses:
            print(f"Date: {expense['Date']}, Category: {expense['Category']}, "
                  f"Amount: ${float(expense['Amount']):.2f}, Description: {expense['Description']}")
    else:
        print("No matching expenses found.")

def get_monthly_summary():
    """Calculates and displays a monthly summary of expenses."""
    print("\n--- Monthly Expense Summary ---")
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        print("No expenses recorded yet.")
        return
    
    month_year_str = input("Enter month and year to summarize (e.g., 2025-09): ")
    try:
        datetime.datetime.strptime(month_year_str, '%Y-%m')
    except ValueError:
        print("Invalid month/year format. Please use YYYY-MM.")
        return

    monthly_total = 0.0
    category_totals = defaultdict(float)
    
    with open(FILE_NAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Date'].startswith(month_year_str):
                amount = float(row['Amount'])
                category = row['Category']
                
                monthly_total += amount
                category_totals[category] += amount

    if monthly_total == 0:
        print(f"No expenses found for {month_year_str}.")
        return

    print(f"\nSummary for {month_year_str}:")
    print(f"Total Expenses: ${monthly_total:.2f}")

    print("\n--- Summary by Category ---")
    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")

    # --- Data Analysis: Top 3 Categories ---
    sorted_categories = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
    
    print("\n--- Top 3 Expense Categories ---")
    if len(sorted_categories) < 3:
        print("Not enough data to determine top 3 categories.")
    for i, (cat, total) in enumerate(sorted_categories[:3]):
        print(f"{i+1}. {cat}: ${total:.2f}")

# --- Main Application Loop ---

def main():
    """Main function to run the expense tracker application."""
    init_file()

    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Search expenses")
        print("4. Get monthly summary & analysis")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            search_expenses()
        elif choice == '4':
            get_monthly_summary()
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
