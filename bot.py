
import logging
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("trading_bot.log"),
                        logging.StreamHandler()
                    ])

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initializes the bot with API credentials and sets up the client."""
        self.client = Client(api_key, api_secret, testnet=testnet)
        if testnet:
            self.client.API_URL = 'https://testnet.binancefuture.com/fapi'
        
        # Sync time with server
        self._sync_time()

    def _sync_time(self):
        """Syncs the client time with the server time."""
        try:
            server_time = self.client.get_server_time()
            timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
            self.client.timestamp_offset = timestamp_offset
            logging.info("Client time synced with server.")
        except Exception as e:
            logging.error(f"Failed to sync time with server: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """Places an order on Binance Futures."""
        logging.info(f"Attempting to place {side} {order_type} order for {quantity} {symbol}...")
        try:
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity,
            }

            if order_type.upper() == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders.")
                params.update({
                    'timeInForce': 'GTC',  # Good Till Cancel
                    'price': price
                })
            elif order_type.upper() == 'STOP_LIMIT':
                if price is None or stop_price is None:
                    raise ValueError("Price and stop_price are required for STOP_LIMIT orders.")
                params.update({
                    'timeInForce': 'GTC',
                    'price': price,
                    'stopPrice': stop_price
                })
            elif order_type.upper() != 'MARKET':
                raise ValueError(f"Unsupported order type: {order_type}")

            order = self.client.futures_create_order(**params)
            
            logging.info("Order placed successfully:")
            print(order)
            return order

        except BinanceAPIException as e:
            logging.error(f"Binance API Exception: {e}")
            return None
        except ValueError as e:
            logging.error(f"Input Error: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise e
