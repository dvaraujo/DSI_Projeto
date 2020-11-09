"""Variáveis de configuração do Flask."""
from os import environ, path
from dotenv import load_dotenv
from oauthlib.oauth2 import WebApplicationClient
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Configura o Flask com o arquivo .env"""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Google Login
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Stripe
    STRIPE_PUBLIC_KEY = environ.get("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = environ.get("STRIPE_SECRET_KEY")
    
    #Rapid Api
    RAPID_API_KEY = environ.get("RAPID_API_KEY")
