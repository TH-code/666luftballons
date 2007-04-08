import ConfigParser

def load_data_configuration(data_dir):
    configuration = ConfigParser.ConfigParser()
    configuration.read([data_dir])
    return configuration
