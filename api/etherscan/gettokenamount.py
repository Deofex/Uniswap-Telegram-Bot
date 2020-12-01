import logging
import bin.settings as settings
from decimal import Decimal
from bin.get_json_from_url import get_json_from_url

# Configure logging
logger = logging.getLogger(__name__)

def gettokenamount(walletaddress, contractaddress):
    logger.info(("Initializing object to easilty get the token amount for "
        "address: {} and contract {}").format(walletaddress,contractaddress))
    esurl = ("https://api.etherscan.io/api"
        "?module=account"
        "&action=tokenbalance"
        "&contractaddress={}"
        "&address={}"
        "&apikey={}").format(
            contractaddress,
            walletaddress,
            settings.config.etherscanapikey
            )

    logger.info("The Etherscan get balance URL is: {}".format(esurl))
    try:
        json = get_json_from_url(esurl)
        logger.info("The JSON file is succesfully retrieved")
        amount = Decimal(json["result"]) / 1000000000000000000
        logger.info("The amount of tokens found is {}".format(amount))

    except:
        logger.error("Can't retrieve the JSON file from the url")
        raise Exception("Can't retrieve the JSON file from the get balance url")

    return amount
