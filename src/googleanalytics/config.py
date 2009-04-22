import ConfigParser
import os.path

def get_google_credentials():
  home_directory = os.path.expanduser("~")
  config_file = os.path.join(home_directory,'.pythongoogleanalytics')
  if not os.path.exists(config_file):
    return None, None
  config = ConfigParser.RawConfigParser()
  config.read(config_file)
  google_account_email = config.get('Credentials', 'google_account_email')
  google_account_password = config.get('Credentials', 'google_account_password')
  return google_account_email, google_account_password