import configparser

# Konfigürasyon dosyasını yükleyen global değişken
config = configparser.ConfigParser()
config.read('config.ini')

# Varsayılan ayarlar
variables = {
    "key": "default_key",
    "fovx": 90,
    "fovy": 90,
    "mode": "Toggle",
    "shootdelay": 100,
    # Diğer değişkenler
}

def loadConfig():
    """
    Konfigürasyon dosyasını yükler ve geçerli ayarları döner.
    
    Returns:
        configparser.ConfigParser: Yüklenen konfigürasyon dosyasını temsil eden nesne.
    """
    if not config.sections():
        print("Config file is empty or not loaded.")
    else:
        print("Config file loaded successfully.")
    return config

def getVar(var_name, section):
    """
    Konfigürasyon dosyasından belirli bir ayarı alır.
    
    Args:
        var_name (str): Alınacak ayarın adı.
        section (str): Ayarın bulunduğu bölüm.

    Returns:
        str|int: Ayarın değeri, veri türüne göre string veya int.
    """
    if config.has_option(section, var_name):
        value = config.get(section, var_name)
        if var_name in ["fovx", "fovy", "shootdelay"]:
            try:
                return int(value)
            except ValueError:
                print(f"Invalid value for {var_name}: {value}. Expected an integer.")
                return variables.get(var_name, None)
        return value
    else:
        print(f"{var_name} not found in section {section}. Returning default value.")
        return variables.get(var_name, None)

def setVar(var_name, value, section):
    """
    Konfigürasyon dosyasındaki bir ayarı günceller veya ekler.

    Args:
        var_name (str): Ayarın adı.
        value (str|int): Güncellenmiş değer.
        section (str): Ayarın bulunduğu bölüm.
    """
    variables[var_name] = value
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, var_name, str(value))
    saveConfig()

def saveConfig(config_file='config.ini'):
    """
    Konfigürasyon dosyasını kaydeder.
    
    Args:
        config_file (str): Konfigürasyon dosyasının yolu.
    """
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print("Configuration saved successfully.")
