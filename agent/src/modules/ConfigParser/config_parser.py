import configparser

class ConfigParser():
    def __init__(self, path: str = "config.ini"):
        config = configparser.ConfigParser()
        config.read(path)
        self.config = config
        self.logger = None
        
    def setLogger(self, logger):
        self.logger = logger

    def __getattr__(self, section):
        if not self.config.has_section(section):
            if self.logger != None:
                self.logger.debug("Config section \"%s\" does not exist", section)
            else:
                print(f"Config section {section} does not exist")
            return False
        option = Option(self.config, section)
        if not option.exists:
            if self.logger != None:
                self.logger.debug("Config option \"%s\" in section \"%s\" does not exist", option, section)
            else:
                print(f"Config section {section} does not exist")
            return False
        return option


class Option():
    def __init__(self, config, section):
        self.config = config
        self.section = section

    def __getattr__(self, option):
        if not self.config.has_option(self.section, option):
            if self.logger != None:
                self.logger.debug("Config option \"%s\" does not exist", option)
            else:
                print(f"Config option {option} does not exist")
        return self.config.get(self.section, option)

    def exists(self, option):
        return self.config.has_option(self.section, option)