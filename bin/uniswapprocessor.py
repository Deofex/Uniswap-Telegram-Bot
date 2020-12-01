import logging
import time
import bin.settings as settings
from api.etherscan.uniswaptransactionbatch import UniswapTransactionBatch
from api.etherscan.uniswaptransaction import UniswapTransaction
from api.telegram.telegramsendmessage import TelegramSendMessage

# Configure logging
logger = logging.getLogger(__name__)

class UniswapProcessor():
    def __init__(self):
        logger.info("Start Uniswap Processor")

    def process_uniswaptransactionbatch(self):
        logger.info("Start looking for a new Uniswap transaction batch")
        utb = UniswapTransactionBatch(settings.config.lastprocessedblocknumber)

        logger.info("Processing Uniswap transaction batch")
        for transactionhash in utb.transactionhashes:
            try:
                ut = UniswapTransaction(transactionhash)
            except:
                logger.warning("Transaction {} can't be processed".format(
                    transactionhash))
                continue

            ut = UniswapTransaction(transactionhash)

            if ut.action == "Bought":
                msg = (
                "<b>{primarytokenname} {action} in block {blocknumber}</b>\n"
                "{pairtokenamount} {tokenname} "
                "swapped for: {primarytokenamount} {primarytokensymbol}\n"
                "<b>Fiat worth:</b> {fiatpricetotal} {fiatsymbol} "
                "<i>(Price per token: {fiatpricepertoken} {fiatsymbol})</i>\n"
                "<b>TX here:</b> "
                "<a href=\"https://etherscan.io/tx/{txhash}\">link</a> - "
                "<b>Wallet:</b> "
                "<a href=\"https://etherscan.io/address/{wallet}\">link</a>\n"
                ).format(
                    action = ut.action,
                    primarytokenamount = round(ut.primarytokenamount,2),
                    primarytokenname = settings.config.primarytokenname,
                    primarytokensymbol = settings.config.primarytokensymbol,
                    pairtokenamount = round(ut.pairtokenamount,2),
                    tokenname = ut.pairtoken.tokenname,
                    fiatpricetotal = round(ut.fiatpricetotal,2),
                    fiatsymbol = settings.config.fiatsymbol.upper(),
                    txhash = ut.txhash,
                    blocknumber = ut.blocknumber,
                    fiatpricepertoken= round(ut.fiatpricepertoken,2),
                    wallet = "{0:#0{1}x}".format(int(ut.wallet,16),1)
                )
            elif ut.action == "Sold":
                msg = (
                "<b>{primarytokenname} {action} in block {blocknumber}</b>\n"
                "{primarytokenamount} {primarytokensymbol} "
                "swapped for: {pairtokenamount} {tokenname}\n"
                "<b>Fiat worth:</b> {fiatpricetotal} {fiatsymbol} "
                "<i>(Price per token: {fiatpricepertoken} {fiatsymbol})</i>\n"
                "<b>TX here:</b> "
                "<a href=\"https://etherscan.io/tx/{txhash}\">link</a> - "
                "<b>Wallet:</b> "
                "<a href=\"https://etherscan.io/address/{wallet}\">link</a>\n"
                ).format(
                    action = ut.action,
                    primarytokenamount = round(ut.primarytokenamount,2),
                    primarytokenname = settings.config.primarytokenname,
                    primarytokensymbol = settings.config.primarytokensymbol,
                    pairtokenamount = round(ut.pairtokenamount,2),
                    tokenname = ut.pairtoken.tokenname,
                    fiatpricetotal = round(ut.fiatpricetotal,2),
                    fiatsymbol = settings.config.fiatsymbol.upper(),
                    txhash = ut.txhash,
                    blocknumber = ut.blocknumber,
                    fiatpricepertoken= round(ut.fiatpricepertoken,2),
                    wallet = "{0:#0{1}x}".format(int(ut.wallet,16),1)
                )
            else:
                msg = (
                "<b>{action} in block {blocknumber}</b>\n"
                "{pairtokenamount} {tokenname} and "
                "{primarytokenamount} {primarytokensymbol}\n"
                "<b>Combined value:</b> {fiatpricetotal} {fiatsymbol}\n"
                "<b>TX here:</b> "
                "<a href=\"https://etherscan.io/tx/{txhash}\">link</a> - "
                "<b>Wallet:</b> "
                "<a href=\"https://etherscan.io/address/{wallet}\">link</a>\n"
                ).format(
                    action = ut.action,
                    primarytokenamount = round(ut.primarytokenamount,2),
                    primarytokensymbol = settings.config.primarytokensymbol,
                    pairtokenamount = round(ut.pairtokenamount,2),
                    tokenname = ut.pairtoken.tokenname,
                    fiatpricetotal = round(ut.fiatpricetotal,2) * 2,
                    fiatsymbol = settings.config.fiatsymbol.upper(),
                    txhash = ut.txhash,
                    blocknumber = ut.blocknumber,
                    wallet = "{0:#0{1}x}".format(int(ut.wallet,16),1)
                )

            for channel in settings.config.telegramactivatedchannels:
                TelegramSendMessage(channel,msg)

            # Change last blocknumber in settings file to last processed block
            # number + 1
            nextblocknumber = str((int(ut.blocknumber) + 1))
            settings.config.updateblocknumber(nextblocknumber)

    def start(self,pollinterval=60):
        logger.info("Starting Uniswap processor cycle "
        " with a poll interval of: {} seconds".format(pollinterval))
        while True:
            self.process_uniswaptransactionbatch()
            logger.info(
                "Uniswap processor cycle finished, waiting {} seconds".format(
                    pollinterval))
            time.sleep(pollinterval)