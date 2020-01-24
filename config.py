import os

# Application Configurations
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CanYouGuess?'