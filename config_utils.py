from general_utils import path_checker
import configparser

class ConfigWriter:

    """Class for writing and updating config files.

    Arguments:
        config_fp {str} -- Path of config file to write/append to

    Keyword Arguments:
        config_details {dict} -- kwarg keywords will become sections; keys and values from
            arguments (dictionaries) will populate the sections.
    """

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
            is_valid {bool} -- Indication of whether the config details are in a valid format.
        """

        # TODO: need to validate the dict of dict type
        raise NotImplementedError ('This method has not been implemented yet.')

    def write_config(self):

        """Method which writes or appends to the specified config_fp.

        Arguments:
            None

        Returns:
            out_string {string} -- Success message indicating save type and location
        """

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
        config_fp {str} -- Path of config file to read
    """

    def __init__(self,
                 config_fp: str):

        self.exists = path_checker(path=config_fp,
                                   check_type='file',
                                   to_raise = True)
        self.config = configparser.ConfigParser()
        self.config.read(config_fp)

    def get_all(self) -> dict:

        """Returns all sections and options in the specified config file.

        Returns:
            all_sections {dict} -- All sections and options in the config file
                e.g. {section1: {options1},
                      section2: {options2}}
        """

        all_sections = {section: dict(self.config[section])
                        for section in self.config.sections()}

        return all_sections

    @staticmethod
    def validate_section(section_dict: dict,
                         validation_options: set) -> bool:

        """Validates if all options expected are present in a section.

        Arguments:
            section_dict {dict} -- Dict of config options to validate
            validation_options {set} -- Names of options to be present in the section_dict

        Returns:
            is_valid {bool} -- Whether all expected fields are present in the section_dict
        """

        is_valid = set(section_dict.keys()) == validation_options

        if is_valid:
            return is_valid
        else:
            raise ValueError ("Config file is not valid. `section_dict` fields do not match\
                 `validation_options` specified.")

    def get_section(self,
                    section_name: str,
                    validate: bool = False,
                    validation_options: set = None) -> dict:

        """Returns a section of the specified config file.

        Arguments:
            section_name {str} -- Name of section to return
            validate {bool} -- Whether or not to validate the options
                in the section (default: {False})
            validation_options {set} -- Names of options to be present in the section_dict

        Returns:
            section_dict {dict} -- Dictionary of config options from the specified section
        """

        section_dict = dict(self.config[section_name])

        if not validate:
            return section_dict

        if not validation_options:
            raise ValueError ("'{}' is an invalid input. Please specify a valid set of \
                `expected_fields` for validation.".format(validation_options))

        is_valid = self.validate_section(section_dict,
                                         validation_options=validation_options)

        if is_valid:
            return section_dict

    def get_option(self,
                   section_name: str,
                   option_name: str) -> str:

        """Returns an option from a section of the specified config file.

        Arguments:
            section_name {str} -- Name of section to return
            validate {bool} -- Whether or not to validate the options
                in the section (default: {False})
            validation_options {set} -- Names of options to be present in the section_dict

        Returns:
            section_dict {dict} -- Dictionary of config options from the specified section
        """

        return self.config.get(section_name, option_name)
