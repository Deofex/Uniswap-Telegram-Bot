import logging
import urllib.parse
from bin.get_json_from_url import get_json_from_url
from api.telegram.telegrambaseobject import TelegramBaseObject

# Configure logging
logger = logging.getLogger(__name__)

class TelegramSendMessage(TelegramBaseObject):
    def __init__(self,chat_id,text,formatstyle="HTML",disablewebpreview="True"):
        self.json = None
        method = "sendMessage"
        formattedtext = urllib.parse.quote_plus(text)
        parameters = {
            "chat_id":chat_id,
            "text":formattedtext,
            "parse_mode":formatstyle,
            "disable_web_page_preview":disablewebpreview
        }
        self.apiurl = super().apiurl(
            method = method,
            parameters = parameters
        )

        logger.info("Sending message: {} to: {}".format(text,chat_id))
        self.json = get_json_from_url(self.apiurl)