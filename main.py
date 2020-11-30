import logging
import threading
import bin.settings as settings
from concurrent.futures import ThreadPoolExecutor
from bin.uniswapprocessor import UniswapProcessor
from bin.telegramprocessor import TelegramProcessor
from api.etherscan.lastblock import lastblock

# Configure the logger
logging.basicConfig(
    format=('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    datefmt="%a %d/%m/%Y %H:%M:%S",
    level=logging.INFO)

# Initialize Settings
settings.init()

# Update settings file with last blocknumber, if the blocknumber is None
if settings.config.lastprocessedblocknumber == "0":
    lastblock = lastblock()
    settings.config.updateblocknumber(lastblock)

# Initialize Telegram Processor
tgp = TelegramProcessor()

# Initialize Uniswap Processor
usp = UniswapProcessor()


with ThreadPoolExecutor(max_workers=3) as executor:
    tgpprocessor = executor.submit(tgp.start)
    uspprocessor = executor.submit(usp.start)



