import logging
import time
import bin.settings as settings
from bin.formatnumber import formatnumber
from bin.wallettostring import wallettostring
from api.etherscan.uniswaptransactionbatch import UniswapTransactionBatch
from api.etherscan.uniswaptransaction import UniswapTransaction
from api.etherscan.gettokenamount import gettokenamount
from api.telegram.telegramsendmessage import TelegramSendMessage

# Configure logging
logger = logging.getLogger(__name__)

class UniswapProcessor():
    def __init__(self):
        logger.info("Start Uniswap Processor")

    def process_uniswaptransactionbatch(self):
        # Get all transaction for the UniSwap address from the last processed
        # blocknumber
        logger.info("Start looking for a new Uniswap transaction batch")
        utb = UniswapTransactionBatch(settings.config.lastprocessedblocknumber)

        logger.info("Processing Uniswap transaction batch")
        # Foreach transaction has in the batch, get the information from the
        # transaction (amount, pair token, price etc. will be returned)
        for transactionhash in utb.transactionhashes:
            try:
                ut = UniswapTransaction(transactionhash)
            except:
                logger.warning("Transaction {} can't be processed".format(
                    transactionhash))
                continue

            # Send message to active Telegram channels with the information
            # gathered earlier
            if ut.action == "Sold" or ut.action == "Bought":
                if ut.action == "Bought":
                    actionicon = "\U0001f7e2"
                if ut.action == "Sold":
                    actionicon = "\U0001f534"
                msg = (
                "<b>{primarytokenname} {action} {actionicon}</b>\n"
                "Block: {blocknumber}\n\n"
                "<b>{primarytokenamount} {primarytokensymbol}</b> "
                "{laction} for <b>{pairtokenamount} {pairtokenname}</b>\n"
                "<b>{primarytokensymbol} Value:</b> "
                "{eurpricetotal} EUR / {usdpricetotal} USD\n"
                "<i>(Price per {primarytokensymbol}: "
                "{eurpricepertoken} EUR / "
                "{usdpricepertoken} USD / "
                "{pairtokenpricept} {pairtokenname})</i>\n\n"
                "1 {pairtokenname} = {pairtokeneurprice} EUR / "
                "{pairtokenusdprice} USD \n\n"
                "<b>TX here:</b> "
                "<a href=\"https://etherscan.io/tx/{txhash}\">link</a>\n"
                "<b>Wallet:</b> "
                "<a href=\"https://etherscan.io/address/{wallet}\">"
                "{wallet}</a>\n"
                "<b>Uniswap pair:</b> "
                "<a href=\"https://info.uniswap.org/pair/{uniswapaddress}\">"
                "link</a>"
                ).format(
                    action = ut.action,
                    laction = ut.action.lower(),
                    actionicon = actionicon,
                    primarytokenamount = formatnumber(ut.primarytokenamount),
                    primarytokenname = settings.config.primarytokenname,
                    primarytokensymbol = settings.config.primarytokensymbol,
                    pairtokenamount = formatnumber(ut.pairtokenamount),
                    pairtokenname = ut.pairtoken.tokenname,
                    pairtokeneurprice = formatnumber(ut.pairtoken.eurprice),
                    pairtokenusdprice = formatnumber(ut.pairtoken.usdprice),
                    eurpricetotal = formatnumber(ut.eurpricetotal),
                    usdpricetotal = formatnumber(ut.usdpricetotal),
                    txhash = ut.txhash,
                    blocknumber = ut.blocknumber,
                    eurpricepertoken= formatnumber(ut.eurpricepertoken),
                    usdpricepertoken= formatnumber(ut.usdpricepertoken),
                    pairtokenpricept = formatnumber(ut.pairtokenpricept,8),
                    wallet = wallettostring(ut.wallet),
                    uniswapaddress = settings.config.uniswapaddress
                )
            elif ut.action == 'Liquidity Added' or \
                ut.action == 'Liquidity Removed':

                if ut.action == 'Liquidity Added':
                    actionicon = '\U0001f7e9'
                if ut.action == 'Liquidity Removed':
                    actionicon = '\U0001f7e5'

                pairtokenatuniswap = gettokenamount(
                    settings.config.uniswapaddress,
                    ut.pairtoken.contractaddress
                )
                primarytokenatuniswap = gettokenamount(
                    settings.config.uniswapaddress,
                    settings.config.primarytokencontractaddress
                )
                msg = (
                "<b>{action}</b> {actionicon}\n"
                "Block: {blocknumber}\n\n"
                "<b>{pairtokenamount} {pairtokenname}</b> and "
                "<b>{primarytokenamount} {primarytokensymbol}</b>\n"
                "<b>Combined value:</b> {eurpricetotal} EUR / "
                "{usdpricetotal} USD\n\n"
                "<b>TX here:</b> "
                "<a href=\"https://etherscan.io/tx/{txhash}\">link</a>\n"
                "<b>Wallet:</b> "
                "<a href=\"https://etherscan.io/address/{wallet}\">{wallet}</a>\n"
                "<b>Uniswap pair:</b> "
                "<a href=\"https://info.uniswap.org/pair/{uniswapaddress}\">"
                "link</a>"
                "\n\n<b>New pooled token amounts:</b>\n"
                "Pooled {pairtokenname}: {pairtokenatuniswap}\n"
                "Pooled {primarytokensymbol}: {primarytokenatuniswap}"
                ).format(
                    action = ut.action,
                    actionicon = actionicon,
                    primarytokenamount = formatnumber(ut.primarytokenamount),
                    primarytokensymbol = settings.config.primarytokensymbol,
                    pairtokenamount = formatnumber(ut.pairtokenamount),
                    pairtokenname = ut.pairtoken.tokenname,
                    eurpricetotal = formatnumber(ut.eurpricetotal * 2),
                    usdpricetotal = formatnumber(ut.usdpricetotal * 2),
                    txhash = ut.txhash,
                    blocknumber = ut.blocknumber,
                    wallet = wallettostring(ut.wallet),
                    pairtokenatuniswap = formatnumber(pairtokenatuniswap),
                    primarytokenatuniswap = formatnumber(primarytokenatuniswap),
                    uniswapaddress = settings.config.uniswapaddress
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
            try:
                self.process_uniswaptransactionbatch()
                logger.info(("Uniswap processor cycle finished, waiting {} "
                "seconds").format(
                        pollinterval))
                time.sleep(pollinterval)
            except:
                logger.error("Uniswap Processor run failed")
                time.sleep(10)
