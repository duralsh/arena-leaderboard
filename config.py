import json

def get_db_config(filename='configs.json', section='postgresql'):
    return _get_config(filename, section)

def get_weight_config(filename='configs.json', section='weights'):
    return _get_config(filename, section)

def _get_config(filename, section):
    # Read the JSON config file
    with open(filename, 'r') as file:
        config_data = json.load(file)
    # Extract the section containing the database parameters
    if section in config_data:
        db_params = config_data[section]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db_params
