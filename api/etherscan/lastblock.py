import logging
import bin.settings as settings
import sys
from bin.get_json_from_url import get_json_from_url

# Configure logging
logger = logging.getLogger(__name__)

def lastblock():
    esurl = ("https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&"
        "apikey={}".format(settings.config.etherscanapikey))
    logger.info("Get last blocknumber from EtherScan url {}".format(esurl))
    try:
        json = get_json_from_url(esurl)
        blocknumber = int(json["result"],16)
    except:
        logger.error("Can't retrieve blocknumber from URL")
        raise Exception("Can't retrieve blocknumber from url. Error: {}".format(
            sys.exc_info()[0]))

    return blocknumber