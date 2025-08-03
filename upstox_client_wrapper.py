import logging
from upstox_client import ApiClient, Configuration
from upstox_client.rest import ApiException
from upstox_client.api import OrderApiV3
from upstox_client.api import MarketQuoteV3Api
from upstox_client.apiV3 import SessionApiV3

logger = logging.getLogger(__name__)

class UpstoxClientWrapper:
    def __init__(self, access_token: str, api_key: str):
        """
        Initializes the Upstox API client

        :param access_token: Your Upstox OAuth 2.0 access token (string)
        :param api_key: Your Upstox API key (string)
        """
        self.access_token = access_token
        self.api_key = api_key

        # Configure the API client
        self.configuration = Configuration()
        self.configuration.access_token = self.access_token
        self.api_client = ApiClient(self.configuration)

        # API endpoints
        self.order_api = OrderApiV3(self.api_client)
        self.market_api = MarketQuoteV3Api(self.api_client)
        self.session_api = SessionApiV3(self.api_client)

    def get_profile(self):
        """
        Fetches logged-in user's profile details (example)
        """
        try:
            profile = self.session_api.get_profile()
            logger.info(f"Profile fetched: {profile}")
            return profile
        except ApiException as e:
            logger.error(f"Error fetching profile: {e}")
            return None

    def get_ltp(self, instrument_token: int):
        """
        Get last traded price (LTP) for an instrument token

        :param instrument_token: Integer instrument token for the product
        :return: Last traded price as float or None if error
        """
        try:
            quote = self.market_api.get_quote(instrument_token)
            ltp = quote.last_price
            logger.debug(f"LTP for token {instrument_token}: {ltp}")
            return ltp
        except ApiException as e:
            logger.error(f"Error fetching LTP for {instrument_token}: {e}")
            return None

    def place_order(self, instrument_token: int, quantity: int, transaction_type: str,
                    order_type: str = "MARKET", product: str = "D", price: float = None,
                    trigger_price: float = None, validity: str = "DAY", is_amo: bool = False):
        """
        Place an order to buy/sell instruments

        :param instrument_token: Instrument token integer
        :param quantity: Quantity to buy/sell
        :param transaction_type: "BUY" or "SELL"
        :param order_type: "MARKET" or "LIMIT" etc.
        :param product: Product type string, e.g., "D" for Delivery, "I" for Intraday
        :param price: Price for limit order (float), optional
        :param trigger_price: Trigger price for stop loss orders (float), optional
        :param validity: Order validity, e.g., "DAY"
        :param is_amo: After Market Order (bool)
        :return: Order response object or None
        """
        order = upstox_client.PlaceOrderV3Request(
            instrument_token=instrument_token,
            quantity=quantity,
            transaction_type=transaction_type,
            order_type=order_type,
            product=product,
            price=price,
            trigger_price=trigger_price,
            validity=validity,
            is_amo=is_amo
        )

        try:
            response = self.order_api.place_order(order)
            logger.info(f"Order placed: {response}")
            return response
        except ApiException as e:
            logger.error(f"Failed to place order: {e}")
            return None

    def get_positions(self):
        """
        Get current open positions (example utility)

        :return: List of positions or empty list
        """
        try:
            positions = self.order_api.get_positions()
            logger.info(f"Positions fetched: {positions}")
            return positions
        except ApiException as e:
            logger.error(f"Error fetching positions: {e}")
            return []

    # Add more methods as necessary (cancel_orders, get_order_book etc.)

if __name__ == "__main__":
    import os

    # For manual test/example usage:
    logging.basicConfig(level=logging.DEBUG)

    access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
    api_key = os.getenv("UPSTOX_API_KEY")

    if not access_token or not api_key:
        print("Set UPSTOX_ACCESS_TOKEN and UPSTOX_API_KEY in your environment!")
        exit(1)

    client = UpstoxClientWrapper(access_token=access_token, api_key=api_key)
    profile = client.get_profile()
    print(profile)

    # Place a test order - Be VERY careful running real orders:
    # Example: client.place_order(instrument_token=12345, quantity=1, transaction_type="BUY")


