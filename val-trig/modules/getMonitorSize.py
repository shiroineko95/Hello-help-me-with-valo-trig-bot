import ctypes

def get_monitor_size_function1():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_monitor_size_function2():
    # Alternatif bir monitör boyutu alma yöntemi
    pass