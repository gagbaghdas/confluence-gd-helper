import os

class Config(object):
    CLIENT_ID = os.environ.get("CONFLUENCE_CLIENT_ID")
    CLIENT_ID = os.environ.get("CONFLUENCE_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CONFLUENCE_CLIENT_SECRET")
    REDIRECT_URI = os.environ.get("CONFLUENCE_REDIRECT_URI")
    AUTH_URL = os.environ.get("CONFLUENCE_AUTH_URL")
    TOKEN_URL = os.environ.get("CONFLUENCE_TOKEN_URL")
    CONFLUENCE_ACCESSIBLE_RESOURCES_URL = os.environ.get(
        "CONFLUENCE_ACCESSIBLE_RESOURCES_URL"
    )
