import logging
import bin.settings as settings
from bin.get_json_from_url import get_json_from_url
from api.telegram.telegrambaseobject import TelegramBaseObject

# Configure logging
logger = logging.getLogger(__name__)

class TelegramUpdates(TelegramBaseObject):
    def __init__(self, timeout=300):
        self.json = None
        self.timeout = timeout
        method = "getUpdates"
        # Offset = last update id + 1 (imported from settings file)
        offset = str(int(settings.config.telegramlastprocessedupdateid) + 1)
        parameters = {
            "timeout":timeout,
            "offset":offset
        }
        self.apiurl = super().apiurl(
            method = method,
            parameters = parameters
        )
        logger.info("Get new updates for the bot via the Telegram API")
        self.json = get_json_from_url(self.apiurl)


