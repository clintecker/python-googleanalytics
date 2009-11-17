import ConfigParser
import os.path

def get_configuration():
    home_directory = os.path.expanduser('~')
    config_file = os.path.join(home_directory, '.pythongoogleanalytics')
    if not os.path.exists(config_file):
        return None
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    return config


def get_google_credentials():
    config = get_configuration()
    if not config:
        return None, None
    google_account_email = config.get('Credentials', 'google_account_email')
    google_account_password = config.get('Credentials', 'google_account_password')
    return google_account_email, google_account_password


def get_valid_profiles():
    config = get_configuration()
    if not config:
        return None
    profile_ids = config.get('Accounts', 'test_profile_ids').split(' ')
    return profile_ids
