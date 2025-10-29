import unittest
from unittest.mock import patch, MagicMock
from bot import BasicBot

class TestOrderPlacement(unittest.TestCase):

    @patch('bot.Client')
    def test_init(self, mock_client):
        """Tests that the bot initializes the client correctly."""
        mock_instance = MagicMock()
        mock_instance.get_server_time.return_value = {'serverTime': 1234567890}
        mock_client.return_value = mock_instance

        bot = BasicBot(api_key='test_key', api_secret='test_secret', testnet=True)
        
        mock_client.assert_called_once_with('test_key', 'test_secret', testnet=True)
        self.assertEqual(bot.client.API_URL, 'https://testnet.binancefuture.com/fapi')
        mock_instance.get_server_time.assert_called_once()

    @patch('bot.Client')
    def test_place_market_order_success(self, mock_client):
        """Tests successful placement of a MARKET order."""
        mock_instance = MagicMock()
        mock_instance.get_server_time.return_value = {'serverTime': 1234567890}
        mock_instance.futures_create_order.return_value = {'orderId': 123, 'status': 'NEW'}
        mock_client.return_value = mock_instance

        bot = BasicBot(api_key='test_key', api_secret='test_secret')
        order = bot.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='MARKET',
            quantity=0.001
        )

        self.assertIsNotNone(order)
        self.assertEqual(order['orderId'], 123)
        mock_instance.futures_create_order.assert_called_once_with(
            symbol='BTCUSDT',
            side='BUY',
            type='MARKET',
            quantity=0.001
        )

    @patch('bot.Client')
    def test_place_limit_order_success(self, mock_client):
        """Tests successful placement of a LIMIT order."""
        mock_instance = MagicMock()
        mock_instance.get_server_time.return_value = {'serverTime': 1234567890}
        mock_instance.futures_create_order.return_value = {'orderId': 456, 'status': 'NEW'}
        mock_client.return_value = mock_instance

        bot = BasicBot(api_key='test_key', api_secret='test_secret')
        order = bot.place_order(
            symbol='BTCUSDT',
            side='SELL',
            order_type='LIMIT',
            quantity=0.002,
            price=50000.0
        )

        self.assertIsNotNone(order)
        self.assertEqual(order['orderId'], 456)
        mock_instance.futures_create_order.assert_called_once_with(
            symbol='BTCUSDT',
            side='SELL',
            type='LIMIT',
            timeInForce='GTC',
            quantity=0.002,
            price=50000.0
        )

    @patch('bot.Client')
    def test_limit_order_missing_price(self, mock_client):
        """Tests that a LIMIT order logs an error if the price is missing."""
        mock_instance = MagicMock()
        mock_instance.get_server_time.return_value = {'serverTime': 1234567890}
        mock_client.return_value = mock_instance
        
        bot = BasicBot(api_key='test_key', api_secret='test_secret')
        order = bot.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='LIMIT',
            quantity=0.001
        )
        self.assertIsNone(order) # Should return None on failure

    @patch('bot.Client')
    def test_unsupported_order_type(self, mock_client):
        """Tests that an unsupported order type logs an error."""
        mock_instance = MagicMock()
        mock_instance.get_server_time.return_value = {'serverTime': 1234567890}
        mock_client.return_value = mock_instance

        bot = BasicBot(api_key='test_key', api_secret='test_secret')
        order = bot.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='STOP_LOSS', # Unsupported
            quantity=0.001
        )
        self.assertIsNone(order) # Should return None on failure

    @patch('bot.Client')
    def test_place_stop_limit_order_success(self, mock_client):
        """Tests successful placement of a STOP_LIMIT order."""
        mock_instance = MagicMock()
        mock_instance.get_server_time.return_value = {'serverTime': 1234567890}
        mock_instance.futures_create_order.return_value = {'orderId': 789, 'status': 'NEW'}
        mock_client.return_value = mock_instance

        bot = BasicBot(api_key='test_key', api_secret='test_secret')
        order = bot.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='STOP_LIMIT',
            quantity=0.001,
            price=51000.0,
            stop_price=50000.0
        )

        self.assertIsNotNone(order)
        self.assertEqual(order['orderId'], 789)
        mock_instance.futures_create_order.assert_called_once_with(
            symbol='BTCUSDT',
            side='BUY',
            type='STOP_LIMIT',
            timeInForce='GTC',
            quantity=0.001,
            price=51000.0,
            stopPrice=50000.0
        )

    @patch('bot.Client')
    def test_stop_limit_order_missing_price(self, mock_client):
        """Tests that a STOP_LIMIT order logs an error if price is missing."""
        mock_instance = MagicMock()
        mock_instance.get_server_time.return_value = {'serverTime': 1234567890}
        mock_client.return_value = mock_instance

        bot = BasicBot(api_key='test_key', api_secret='test_secret')
        order = bot.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='STOP_LIMIT',
            quantity=0.001,
            stop_price=50000.0
        )
        self.assertIsNone(order) # Should return None on failure

if __name__ == '__main__':
    unittest.main()