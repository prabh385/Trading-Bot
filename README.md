# Binance Futures Trading Bot

This is a simple trading bot that allows you to place market, limit, and stop-limit orders on the Binance Futures Testnet via an interactive command-line interface.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/trading-bot.git
    cd trading-bot
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your API keys:**
    -   Create a copy of the `.env.example` file and name it `.env`.
    -   Open the new `.env` file and add your Binance Testnet API key and secret.
        ```env
        API_KEY="YOUR_API_KEY_HERE"
        API_SECRET="YOUR_API_SECRET_HERE"
        ```
    -   **Important:** The `.env` file is included in `.gitignore` to ensure your keys are never committed to version control.
## Usage

To start the interactive trading bot CLI, simply run:

```bash
python main.py
```

The bot will then prompt you for the necessary order details (symbol, side, order type, quantity, price, and stop price if applicable). You can place multiple orders and choose to exit when done.