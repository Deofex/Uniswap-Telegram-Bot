import logging
import bin.settings as settings
from bin.get_json_from_url import get_json_from_url

# Configure logging
logger = logging.getLogger(__name__)

class UniswapTransactionBatch():
    def __init__(self,startblock):
        self.startblock = startblock
        self.json = None
        self.transactionhashes = []

        logger.info(("Initializing Uniswap transaction batch object. "
            "Startblock: {}").format(startblock))

        self.get_uniswaptransactions()
        self.extracttransactionhashes()


    def get_uniswaptransactions(self):
        esurl = ("https://api.etherscan.io/api"
            "?module=account"
            "&action=tokentx"
            "&startblock={}"
            "&address={}"
            "&contractaddress={}"
            "&apikey={}".format(
                self.startblock,
                settings.config.uniswapaddress,
                settings.config.primarytokencontractaddress,
                settings.config.etherscanapikey
             ))

        logger.info("The Etherscan Uniswap transaction batch URL is: {}".format(
            esurl))
        try:
            self.json = get_json_from_url(esurl)
            logger.info("The JSON file is succesfully retrieved")
        except:
            logger.error("Can't retrieve the JSON file from the url")

    def extracttransactionhashes(self):
        logger.info("Extracting transaction hashes")
        for transaction in self.json['result']:
            if transaction['hash'] not in self.transactionhashes:
                self.transactionhashes.append(transaction['hash'])



