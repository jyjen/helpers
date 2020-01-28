from general_utils import path_checker
import configparser

class ConfigWriter:

    """Class for writing and updating config files.

    Arguments:
        config_fp {str} -- Path of config file to write/append to

    Keyword Arguments:
        config_details {dict} -- kwarg keywords will become sections; keys and values from
            arguments (dictionaries) will populate the sections.

    Returns:
        Success message {str} -- Message indicating save type and location"""

    def __init__(self,
                 config_fp: str,
                 **config_details):

        self.check_config_details(config_details)
        self.config_fp = config_fp
        self.config_details = config_details

    @staticmethod
    def check_config_details(config_details):
        # TODO: need to validate the dict of dict type
        pass

    def write_config(self):

        exists = path_checker(path=self.config_fp,
                        check_type='file',
                        to_raise = False)

        out_phrase = 'appended' if exists else 'written'
        print (exists)
        print (out_phrase)

        config = configparser.ConfigParser()
        for key, value in self.config_details.items():
            config[key] = value
        with open(self.config_fp, 'a') as configfile:
            config.write(configfile)


        return "Config file has been {} to '{}'".format(out_phrase,
                                                        self.config_fp)


class ConfigReader:

    def __init__(self,
                 config_fp: str):

        self.exists = path_checker(path=config_fp,
                                   check_type='file',
                                   to_raise = True)
        self.config_fp = config_fp

    def read_config(self):
        pass

    def validate(self):
        pass