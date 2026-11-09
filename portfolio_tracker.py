"""
================================================================================
                    STOCK PORTFOLIO TRACKER
================================================================================
A beginner-friendly, interactive Python application to track your stock
investments using predefined market prices, basic arithmetic, dictionaries,
and file handling (TXT and CSV export).

Key Concepts Used:
- Dictionaries: Key-value pairs for market prices and user holdings
- Input/Output: Interactive command-line prompts and formatted output
- Basic Arithmetic: Total value calculations, percentage allocation
- File Handling: Exporting reports to .txt and .csv using context managers
- Error Handling: Handling invalid symbols, negative/non-numeric inputs, and file errors
================================================================================
"""

import os
from datetime import datetime

# ------------------------------------------------------------------------------
# 1. PREDEFINED STOCK MARKET PRICES (Dictionary)
# ------------------------------------------------------------------------------
# Dictionary mapping stock ticker symbols (keys) to their current price in USD (values).
STOCK_PRICES = {
    "AAPL": 180.00,   # Apple Inc.
    "TSLA": 250.00,   # Tesla Inc.
    "GOOGL": 140.00,  # Alphabet Inc. (Google)
    "MSFT": 420.00,   # Microsoft Corp.
    "AMZN": 175.00,   # Amazon.com Inc.
    "NVDA": 120.00,   # NVIDIA Corp.
    "META": 500.00,   # Meta Platforms Inc.
    "NFLX": 630.00,   # Netflix Inc.
}


def print_header(title: str):
    """Prints a styled visual header for different sections."""
    print("\n" + "=" * 65)
    print(f" {title.upper()} ".center(65, "-"))
    print("=" * 65)


def display_market_prices():
    """Displays the list of predefined stocks and their current prices."""
    print_header("Current Market Prices")
    print(f"{'Ticker Symbol':<18} | {'Price Per Share ($)':<20}")
    print("-" * 42)
    for ticker, price in sorted(STOCK_PRICES.items()):
        print(f"{ticker:<18} | ${price:>18.2f}")
    print("-" * 42)


def get_positive_quantity() -> float:
    """
    Prompts the user for a valid positive number for stock quantity.
    Demonstrates input validation and exception handling with try-except.
    """
    while True:
        user_input = input(" Enter quantity of shares: ").strip()
        try:
            quantity = float(user_input)
            if quantity <= 0:
                print(" [!] Error: Quantity must be greater than zero. Please try again.")
                continue
            # Return integer if it's a whole number (e.g. 5.0 -> 5)
            return int(quantity) if quantity.is_integer() else quantity
        except ValueError:
            print(" [!] Error: Invalid input! Please enter a valid number (e.g., 10 or 2.5).")


def add_or_update_stock(portfolio: dict):
    """
    Allows user to add a new stock or update an existing stock in their portfolio.
    Validates stock symbol against the predefined STOCK_PRICES dictionary.
    """
    print_header("Add / Update Stock")
    display_market_prices()

    while True:
        ticker = input("\nEnter stock symbol from list above (or 'C' to cancel): ").strip().upper()

        if ticker == "C":
            print(" [*] Action cancelled. Returning to main menu.")
            return

        # Validate if ticker is present in predefined dictionary
        if ticker not in STOCK_PRICES:
            print(f" [X] Error: '{ticker}' is not a valid stock in our price list.")
            print("     Available stocks: " + ", ".join(STOCK_PRICES.keys()))
            continue
        
        break

    # If stock is already in portfolio, ask whether to add or replace shares
    if ticker in portfolio:
        current_qty = portfolio[ticker]
        print(f"\n [*] Notice: You currently own {current_qty} share(s) of {ticker}.")
        print("     1. Add to existing shares")
        print("     2. Replace / Overwrite existing shares")
        choice = input("     Choose an option (1 or 2, default is 1): ").strip()
        
        qty_input = get_positive_quantity()
        if choice == "2":
            portfolio[ticker] = qty_input
            print(f"\n [✓] Success: Updated {ticker} total shares to {portfolio[ticker]}.")
        else:
            portfolio[ticker] += qty_input
            print(f"\n [✓] Success: Added {qty_input} share(s). New total for {ticker}: {portfolio[ticker]}.")
    else:
        quantity = get_positive_quantity()
        portfolio[ticker] = quantity
        print(f"\n [✓] Success: Added {quantity} share(s) of {ticker} to your portfolio.")


def remove_stock(portfolio: dict):
    """Allows user to remove a stock from their portfolio."""
    print_header("Remove Stock from Portfolio")
    if not portfolio:
        print(" [!] Your portfolio is currently empty. Nothing to remove.")
        return

    print("Currently owned stocks:", ", ".join(portfolio.keys()))
    ticker = input("Enter stock symbol to remove (or 'C' to cancel): ").strip().upper()

    if ticker == "C":
        print(" [*] Action cancelled.")
        return

    if ticker in portfolio:
        del portfolio[ticker]
        print(f" [✓] Success: {ticker} has been removed from your portfolio.")
    else:
        print(f" [X] Error: '{ticker}' is not in your portfolio.")


def calculate_portfolio_totals(portfolio: dict):
    """
    Computes total investment value for each stock and the overall portfolio total.
    Returns:
        details: list of dicts with calculated metrics
        grand_total: overall portfolio value
    """
    details = []
    grand_total = 0.0

    # Arithmetic calculation for individual and total values
    for ticker, qty in portfolio.items():
        price = STOCK_PRICES[ticker]
        stock_total = qty * price
        grand_total += stock_total
        details.append({
            "ticker": ticker,
            "price": price,
            "quantity": qty,
            "total_value": stock_total,
        })

    # Calculate portfolio percentage allocation for each stock
    for item in details:
        item["percentage"] = (item["total_value"] / grand_total * 100) if grand_total > 0 else 0.0

    return details, grand_total


def display_portfolio(portfolio: dict):
    """Displays the user's current portfolio summary in a formatted table."""
    print_header("Portfolio Summary")
    if not portfolio:
        print(" Your portfolio is currently empty!")
        print(" Select option 1 from the main menu to add stocks.")
        return

    details, grand_total = calculate_portfolio_totals(portfolio)

    print(f"{'Stock':<8} | {'Unit Price ($)':<14} | {'Quantity':<10} | {'Total Value ($)':<16} | {'Portfolio %':<12}")
    print("-" * 70)
    for item in details:
        print(
            f"{item['ticker']:<8} | "
            f"${item['price']:>12.2f} | "
            f"{item['quantity']:>10} | "
            f"${item['total_value']:>14.2f} | "
            f"{item['percentage']:>10.2f}%"
        )
    print("-" * 70)
    print(f"OVERALL PORTFOLIO VALUE: ${grand_total:>14.2f}")
    print(f"TOTAL UNIQUE HOLDINGS : {len(portfolio):>14}")
    print("-" * 70)


def save_portfolio_to_file(portfolio: dict):
    """
    Optionally allows user to save the portfolio summary to a .txt or .csv file.
    Demonstrates file handling (creation, writing, closing, and exception handling).
    """
    print_header("Save Portfolio To File")
    if not portfolio:
        print(" [!] Your portfolio is empty. Add stocks first before exporting.")
        return

    print("Select file export format:")
    print("  1. Plain Text File (.txt)")
    print("  2. CSV Spreadsheet File (.csv)")
    print("  3. Cancel and return to menu")

    format_choice = input("Enter your choice (1, 2, or 3): ").strip()

    if format_choice == "1":
        ext = ".txt"
        default_filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    elif format_choice == "2":
        ext = ".csv"
        default_filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    elif format_choice == "3":
        print(" [*] Export cancelled.")
        return
    else:
        print(" [X] Invalid choice. Export cancelled.")
        return

    filename = input(f"Enter filename (Press Enter for default '{default_filename}'): ").strip()
    if not filename:
        filename = default_filename
    elif not filename.lower().endswith(ext):
        filename += ext

    details, grand_total = calculate_portfolio_totals(portfolio)

    try:
        if ext == ".txt":
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("STOCK PORTFOLIO SUMMARY REPORT\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"{'Stock':<8} | {'Unit Price ($)':<14} | {'Quantity':<10} | {'Total Value ($)':<16} | {'Portfolio %':<12}\n")
                f.write("-" * 70 + "\n")
                for item in details:
                    f.write(
                        f"{item['ticker']:<8} | "
                        f"${item['price']:>12.2f} | "
                        f"{item['quantity']:>10} | "
                        f"${item['total_value']:>14.2f} | "
                        f"{item['percentage']:>10.2f}%\n"
                    )
                f.write("-" * 70 + "\n")
                f.write(f"OVERALL PORTFOLIO VALUE: ${grand_total:>14.2f}\n")
                f.write(f"TOTAL UNIQUE HOLDINGS : {len(portfolio):>14}\n")
                f.write("=" * 70 + "\n")

        elif ext == ".csv":
            with open(filename, "w", encoding="utf-8") as f:
                # CSV Headers
                f.write("Stock,Unit Price ($),Quantity,Total Value ($),Portfolio Percentage (%)\n")
                for item in details:
                    f.write(
                        f"{item['ticker']},{item['price']:.2f},{item['quantity']},"
                        f"{item['total_value']:.2f},{item['percentage']:.2f}\n"
                    )
                f.write(f"OVERALL TOTAL,,,{grand_total:.2f},100.00\n")

        absolute_path = os.path.abspath(filename)
        print(f"\n [✓] File saved successfully!")
        print(f"     File path: {absolute_path}")

    except OSError as e:
        print(f"\n [X] An error occurred while saving the file: {e}")


def main():
    """Main function containing the interactive user loop."""
    # User portfolio dictionary: maps ticker (str) -> quantity (int/float)
    portfolio = {}

    print("\n" + "#" * 65)
    print("        WELCOME TO THE PYTHON STOCK PORTFOLIO TRACKER        ")
    print("#" * 65)

    while True:
        print("\n" + "=" * 65)
        print("                          MAIN MENU                          ")
        print("=" * 65)
        print("  1. Add / Update a Stock in Portfolio")
        print("  2. View Current Portfolio Summary & Total Investment")
        print("  3. View Predefined Market Stock Prices")
        print("  4. Remove a Stock from Portfolio")
        print("  5. Save Portfolio to File (.txt or .csv)")
        print("  6. Reset / Clear Entire Portfolio")
        print("  7. Exit Program")
        print("-" * 65)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_or_update_stock(portfolio)
        elif choice == "2":
            display_portfolio(portfolio)
        elif choice == "3":
            display_market_prices()
        elif choice == "4":
            remove_stock(portfolio)
        elif choice == "5":
            save_portfolio_to_file(portfolio)
        elif choice == "6":
            if not portfolio:
                print("\n [!] Portfolio is already empty.")
            else:
                confirm = input("\n Are you sure you want to clear your entire portfolio? (y/n): ").strip().lower()
                if confirm == "y":
                    portfolio.clear()
                    print(" [✓] Portfolio has been cleared.")
                else:
                    print(" [*] Reset cancelled.")
        elif choice == "7":
            print("\n" + "=" * 65)
            print(" Thank you for using the Stock Portfolio Tracker. Happy Investing!")
            print("=" * 65 + "\n")
            break
        else:
            print("\n [!] Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
