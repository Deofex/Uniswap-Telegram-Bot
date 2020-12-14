import logging
import bin.settings as settings
from decimal import Decimal
from bin.get_json_from_url import get_json_from_url
from api.coingecko.tokeninformation import TokenInformation

# Configure logging
logger = logging.getLogger(__name__)

class UniswapTransaction():
    """
    Base class of an UniSwap transactions. Need the tx hash to collect data.
    """
    def __init__(
        self,
        txhash
    ):
        logger.info(("Initializing Uniswap transaction object for "
            "txhash: {}").format(txhash))

        self.txhash = txhash
        self.json = None
        self.action = None
        self.blocknumber = None
        self.primarytokenamount = None
        self.pairtoken = None
        self.pairtokenamount = None
        self.eurpricetotal = None
        self.eurpricepertoken = None
        self.usdpricetotal = None
        self.usdpricepertoken = None
        self.wallet = None

        # Get content from EtherScan
        self.get_content()

        # Process the information found in Etherscan
        self.process_tx()

        # Calculate the price involved in the tranasaction
        self.calculate_price()

    def get_content(self):
        esurl = ("https://api.etherscan.io/api"
            "?module=proxy"
            "&action=eth_getTransactionReceipt"
            "&txhash={}"
            "&apikey={}").format(self.txhash,settings.config.etherscanapikey)
        logger.info("The Etherscan Uniswap transaction URL is: {}".format(
            esurl))
        try:
            self.json = get_json_from_url(esurl)
            logger.info("The JSON file is succesfully retrieved")
        except:
            logger.error("Can't retrieve the JSON file from the url")


    def process_tx(self):
        # Transfer topic for ETH transactions =
        # 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        t = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        # Mint topic for ETH transactions =
        # 0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f
        m = "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f"
        # Butn topic for ETH transactions =
        # 0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496

        b = "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496"
        logger.info("Processing logs for Uniswap Transaction: {}".format(
            self.txhash))
        self.blocknumber = int(self.json['result']["blockNumber"],0)
        # Configure uniswap address with additional 0's
        uniswapaddress = "{0:#0{1}x}".format(int(
            settings.config.uniswapaddress,16),66)
        for logentry in self.json['result']['logs']:
            # If log entry is a transaction, process transfer
            # If log entry = mint. Set action on Liquidity Added.
            # If log entry = burn. Set action to Liquidity Removed
            if logentry['topics'][0] == t:
                if logentry['topics'][1] == uniswapaddress or \
                    logentry['topics'][2] == uniswapaddress:
                    self.process_transfer(logentry)
            elif logentry['topics'][0] == m:
                self.action = 'Liquidity Added'
            elif logentry['topics'][0] == b:
                self.action = 'Liquidity Removed'

    def process_transfer(self,logentry):
        if logentry['address'] == settings.config.primarytokencontractaddress:
            logger.info("Primary token transactions found")

            # Configure uniswap address with additional 0's
            uniswapaddress = "{0:#0{1}x}".format(int(
            settings.config.uniswapaddress,16),66)

            if logentry['topics'][1] == uniswapaddress and self.action == None:
                logger.info(
                    "The Primary token in this transaction has been bought")
                self.action = "Bought"
                self.wallet = logentry['topics'][2]
                logger.info(
                    "The wallet which bought the primary token is: {}".format(
                    self.wallet))
            if logentry['topics'][2] == uniswapaddress and self.action == None:
                logger.info(
                    "The Primary token in this transaction has been sold")
                self.action = "Sold"

                self.wallet = logentry['topics'][1]
                logger.info(
                    "The wallet which sold the primary token is: {}".format(
                    self.wallet))

            # Processing the amount of tokens which has been send
            data = logentry["data"]
            self.primarytokenamount = Decimal(
                str(int(data,16))) / 1000000000000000000
            logger.info(("Amount of primary tokens involved in the "
                "transaction: {}").format(self.primarytokenamount))
        elif logentry['address'] == settings.config.uniswapaddress:
            pass
        else:
            logger.info(
                "Secondary transaction contract address found: {}".format(
                    logentry['address']))
            # looking up information about the token which has been used
            self.pairtoken = TokenInformation(logentry['address'])

            # Processing the amount of tokens which has been send
            data = logentry["data"]
            self.pairtokenamount = Decimal(
                str(int(data,16))) / int(str(
                    "1" + int(settings.config.pairtokendecimals) *"0"))
            logger.info("{} amount involved in transactions: {}".format(
                self.pairtoken.tokenname, self.pairtokenamount))

    def calculate_price(self):
        self.eurpricetotal = self.pairtokenamount * self.pairtoken.eurprice
        logger.info("Calculated Euro price total transaction: €{}".format(
            self.eurpricetotal
        ))

        self.usdpricetotal = self.pairtokenamount * self.pairtoken.usdprice
        logger.info("Calculated Dollar price total transaction: ${}".format(
            self.usdpricetotal
        ))

        self.eurpricepertoken = self.eurpricetotal / self.primarytokenamount
        logger.info("Calculated Euro price per token: €{}".format(
            self.eurpricepertoken
        ))

        self.usdpricepertoken = self.usdpricetotal / self.primarytokenamount
        logger.info("Calculated Dollar price per token: ${}".format(
            self.usdpricepertoken
        ))


        # Calculte the price compared to the paired token
        self.pairtokenpricept = self.pairtokenamount / self.primarytokenamount
        logger.info("Calculated the paired price per token: {} {}".format(
            self.pairtokenpricept, self.pairtoken.tokenname
        ))


    def __str__(self):
        return "Uniswap transactionobject for txhash: {}".format(self.txhash)

