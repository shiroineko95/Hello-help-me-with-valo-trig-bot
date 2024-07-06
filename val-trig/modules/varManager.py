import configparser

# Önceden yüklenen config dosyasını bir global değişken olarak tanımlayalım
config = configparser.ConfigParser()
config.read('config.ini')

variables = {
    "key": "default_key",
    "fovx": 90,
    "fovy": 90,
    "mode": "Toggle",
    "shootdelay": 100,
    # Diğer değişkenler
}

def getVar(var_name, section):
    if config.has_option(section, var_name):
        value = config.get(section, var_name)
        if var_name in ["fovx", "fovy", "shootdelay"]:
            return int(value)
        return value
    return variables.get(var_name, None)

def setVar(var_name, value, section):
    variables[var_name] = value
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, var_name, str(value))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)