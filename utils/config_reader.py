import yaml

def load_config(env):
    # Load the configuration from a YAML file based on the specified environment.
    config_file = open("config/config.yaml", "r") #  with open("config/config.yaml","r") as config_file:
    config = yaml.safe_load(config_file)
    return config[env]