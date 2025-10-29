import os
from dotenv import load_dotenv
from bot import BasicBot

# Load environment variables from .env file
load_dotenv()

def main_cli():
    """Main function to provide an interactive CLI for placing orders."""
    print("Welcome to the Binance Futures Trading Bot CLI!")

    # Get API keys from environment
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        print("Error: API_KEY and API_SECRET must be set in the .env file.")
        return
    
    try:
        # Initialize the bot
        trading_bot = BasicBot(api_key=api_key, api_secret=api_secret, testnet=True)
    except Exception as e:
        print(f"Failed to initialize the trading bot. Please check your API keys and network connection. Error: {e}")
        return

    while True:
        print("\n--- Place New Order ---")
        symbol = input("Enter trading symbol (e.g., BTCUSDT): ").upper()
        
        side = ""
        while side not in ['BUY', 'SELL']:
            side = input("Enter order side (BUY/SELL): ").upper()
            if side not in ['BUY', 'SELL']:
                print("Invalid side. Please enter BUY or SELL.")

        order_type = ""
        while order_type not in ['MARKET', 'LIMIT', 'STOP_LIMIT']:
            order_type = input("Enter order type (MARKET/LIMIT/STOP_LIMIT): ").upper()
            if order_type not in ['MARKET', 'LIMIT', 'STOP_LIMIT']:
                print("Invalid order type. Please enter MARKET, LIMIT, or STOP_LIMIT.")

        try:
            quantity = float(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue

        price = None
        stop_price = None

        if order_type in ['LIMIT', 'STOP_LIMIT']:
            try:
                price = float(input("Enter price: "))
            except ValueError:
                print("Invalid price. Please enter a number.")
                continue

        if order_type == 'STOP_LIMIT':
            try:
                stop_price = float(input("Enter stop price: "))
            except ValueError:
                print("Invalid stop price. Please enter a number.")
                continue

        # Place the order using the bot instance
        trading_bot.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )

        another_order = ""
        while another_order not in ['yes', 'no']:
            another_order = input("\nPlace another order? (yes/no): ").lower()
        
        if another_order == 'no':
            break

    print("Exiting Trading Bot CLI. Goodbye!")

if __name__ == '__main__':
    main_cli()
