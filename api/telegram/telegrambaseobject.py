import logging
import bin.settings as settings

# Configure logging
logger = logging.getLogger(__name__)


class TelegramBaseObject():
    def apiurl(self,method,parameters={}):
        # Define api url
        apiurl = "https://api.telegram.org/bot{}/{}".format(
            settings.config.telegramapitoken,method)

        # Add parameters to the api url
        if len(parameters.keys()) != 0:
            apiurl = apiurl + "?"
            for parameter in parameters.keys():
                apiurl = apiurl + parameter + "="
                apiurl = apiurl + str(parameters[parameter]) + "&"

        # Remove last &
        apiurl = apiurl[:-1]

        logger.info("Telegram API url: {}".format(apiurl))
        return apiurl