import configparser
import logging
import sys

# Configure logging
logger = logging.getLogger(__name__)

class Config():
    def __init__(self,configfile="settings.config"):

        logger.info('Initializing config')
        self.config = configparser.ConfigParser()
        self.configfile = configfile
        self.etherscanapikey = None
        self.primarytokenname = None
        self.primarytokensymbol = None
        self.primarytokencontractaddress = None
        self.uniswapaddress = None
        self.lastprocessedblocknumber = None
        self.telegramapitoken = None
        self.telegramlastprocessedupdateid = None
        self.telegramactivatedchannels = []

        # Read the config file and throw an error if this is failing
        try:
            self.readconfigfile()
        except:
            logger.error("Can't load the setting file correctly")
            raise Exception(
                "Can't load the setting file correctly. Error: {}".format(
                    sys.exc_info()[0]))

    def readconfigfile(self):
        logger.info('Importing settings file: {}'.format(self.configfile))
        self.config.read(self.configfile)
        # Import PrimaryToken info
        self.primarytokenname = \
            self.config['PrimaryToken']['primarytokenname']
        logger.info('Primary Token Name: {}'.format(self.primarytokenname))
        self.primarytokensymbol = \
            self.config['PrimaryToken']['primarytokensymbol']
        logger.info('Primary Token Symbol: {}'.format(self.primarytokensymbol))
        self.primarytokencontractaddress = \
            self.config['PrimaryToken']['primarytokencontractaddress']
        logger.info('Primary Token Address: {}'.format(
            self.primarytokencontractaddress))
        # Import EtherScan info
        self.etherscanapikey = \
            self.config['EtherScanAPI']['etherscanapikey']
        logger.info('EtherScan API Key: {}'.format(self.etherscanapikey))
        # Import Uniswap address
        self.uniswapaddress = \
            self.config['Uniswap']['uniswapaddress']
        logger.info('Uniswap Address: {}'.format(self.uniswapaddress))
        # Import Telegram information
        self.telegramapitoken = \
            self.config['Telegram']['telegramapitoken']
        logger.info('Telegram Api Token: {}'.format(self.telegramapitoken))

        self.telegramlastprocessedupdateid = \
            self.config['Telegram']['telegramlastprocessedupdateid']
        logger.info('Last processed Telegram update ID: {}'.format(
            self.telegramlastprocessedupdateid
        ))
        if self.config['Telegram']['telegramactivatedchannels'] != "None":
            self.telegramactivatedchannels = \
                self.config['Telegram']['telegramactivatedchannels'].split(",")
            logger.info('Telegram activated channels found: {}'.format(
                self.config['Telegram']['telegramactivatedchannels']))
        # Import processing information
        if self.config['Process']['lastprocessedblocknumber'] != "None":
            self.lastprocessedblocknumber = \
                self.config['Process']['lastprocessedblocknumber']
            logger.info('Last processed blocknumber: {}'.format(
                self.lastprocessedblocknumber))
        else:
            logger.info('No last processed blocknumber found in config')
        # Import advanced info
        self.pairtokendecimals = \
            self.config['Advanced']['pairtokendecimals']
        logger.info('Pair token decimals: {}'.format(
            self.pairtokendecimals
        ))

    def writetofile(self):
        logger.info('Writing config file')

        # Write config file.
        with open(self.configfile, 'w') as configfile:
            self.config.write(configfile)

    def updateblocknumber(self,blocknumber):
        if int(self.lastprocessedblocknumber) <= int(blocknumber):
            self.config['Process'] = {
                "lastprocessedblocknumber" : str(blocknumber)
            }
            self.writetofile()
            self.lastprocessedblocknumber = str(blocknumber)

    def update_telegramsettings(self,telegramchannel=None,updateid=None):
        if telegramchannel != None:
            self.telegramactivatedchannels.append(telegramchannel)
            logger.info("Telegram channels updated with: {}".format(
                telegramchannel))

        if updateid != None:
            self.telegramlastprocessedupdateid = updateid
            logger.info("Telegram update ID updated to: {}".format(updateid))

        self.config['Telegram'] = {
            "telegramapitoken" : self.telegramapitoken ,
            "telegramactivatedchannels" : ",".join(
                self.telegramactivatedchannels),
            "telegramlastprocessedupdateid" : self.telegramlastprocessedupdateid
        }
        self.writetofile()

def init():
    # Initilize config
    global config
    config = Config()