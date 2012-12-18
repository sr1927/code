import sys
import urllib
sys.path.append("mashape")

from mashape.http.http_client import HttpClient
from mashape.http.content_type import ContentType
from mashape.auth.mashape_auth import MashapeAuth
from mashape.auth.basic_auth import BasicAuth
from mashape.auth.query_auth import QueryAuth
from mashape.auth.custom_header_auth import CustomHeaderAuth
from mashape.auth.oauth_auth import OAuthAuth
from mashape.auth.oauth10a_auth import OAuth10aAuth
from mashape.auth.oauth2_auth import OAuth2Auth


class WordCloudMaker:

    auth_handlers = []
    PUBLIC_DNS = "gatheringpoint-word-cloud-maker.p.mashape.com"

    def __init__(self, public_key, private_key):
        self.auth_handlers.append(MashapeAuth(public_key, private_key))

    def makeWordCloud(self, height, textblock, width, config=None, mashape_callback=None):
        parameters = {
                "height": height,
                "textblock": textblock,
                "width": width,
                "config": config}

        mashape_client = HttpClient()
        response = mashape_client.do_call(
                "POST",
                "https://" + self.PUBLIC_DNS + "/index.php",
                parameters,
                self.auth_handlers,
                ContentType.FORM,
                mashape_callback,
                True)
        return response


