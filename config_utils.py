from general_utils import path_checker
import configparser

class ConfigWriter:

    """Class for writing and updating config files.

    Arguments:
        config_fp {str} -- Path of config file to write/append to

    Keyword Arguments:
        config_details {dict} -- kwarg keywords will become sections; keys and values from
            arguments (dictionaries) will populate the sections."""

    def __init__(self,
                 config_fp: str,
                 **config_details):

        # self.check_config_details(config_details)
        self.config_fp = config_fp
        self.config_details = config_details

    @staticmethod
    def check_config_details(config_details):

        """Method which checks the format of config details passed.

        Arguments:
            config_details {dict} -- dict of dicts containing config details

        Returns:
            is_valid {bool} -- Indication of whether the config details are in a valid format."""

        # TODO: need to validate the dict of dict type
        raise NotImplementedError ('This method has not been implemented yet.')

    def write_config(self):

        """Method which writes or appends to the specified config_fp.

        Arguments:
            None

        Returns:
            out_string {string} -- Success message indicating save type and location"""

        exists = path_checker(path=self.config_fp,
                              check_type='file',
                              to_raise = False)
        out_phrase = 'appended' if exists else 'written'

        config = configparser.ConfigParser()
        for key, value in self.config_details.items():
            config[key] = value
        with open(self.config_fp, 'a') as configfile:
            config.write(configfile)

        out_string = "Config file has been {} to '{}'".format(out_phrase,
                                                              self.config_fp)

        return out_string

class ConfigReader:

    """Class for reading config files.

    Arguments:
        config_fp {str} -- Path of config file to read"""

    def __init__(self,
                 config_fp: str):

        self.exists = path_checker(path=config_fp,
                                   check_type='file',
                                   to_raise = True)
        self.config_fp = config_fp

    @staticmethod
    def validate(config_dict: dict,
                 validation_fields: set) -> bool:

        """Validates if all config params expected are present.

        Arguments:
            config_dict {dict} -- Dict of config params to validate
            validation_fields {set} -- Names of fields to be present in the config_dict

        Returns:
            is_valid {bool} -- Whether all expected fields are present in the config_dict"""

        is_valid = set(config_dict.keys()) == validation_fields

        if is_valid:
            return is_valid
        else:
            raise ValueError ("Config file is not valid. Please check either the specified config \
                file or the `validation_fields` specified.")

    def read_config(self,
                    section_name: str,
                    validate: bool = False,
                    expected_fields: set = None) -> dict:

        """Method which reads the config file from the config_fp passed.

        Arguments:
            section_name {str} -- Name of section containing config details to return
            validate {bool} -- Whether or not to validate the config details
            expected_fields {set} -- Expected fields expected in the config file

        Returns:
            config_dict {dict} -- Dict of config params"""

        config = configparser.ConfigParser()
        config.read(self.config_fp)
        config_dict = dict(config.items(section_name))

        if not validate:
            return config_dict

        if not expected_fields:
            raise ValueError ("'{}' is an invalid input. Please specify a valid list of \
                `expected_fields` for validation.".format(expected_fields))

        is_valid = self.validate(config_dict=config_dict,
                                 validation_fields=expected_fields)

        if is_valid:
            return config_dict


