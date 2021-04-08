# Store credentials (user, password) in local_config.py
from os.path import isfile, abspath, expanduser


class BaseConfig:
    USER = None
    PASSWORD = None
    SERVER = ''
    DATABASE = 'postgresql'
    SCHEMA = ''

    @property
    def GP_CONNECTION_STRING(self):
        return f'{self.DATABASE}://{self.USER}:{self.PASSWORD}@{self.SERVER}/{self.SCHEMA}'


LOCAL_CONFIG = 'local_config.py'
LOCAL_CONFIG = abspath(expanduser(LOCAL_CONFIG))

if isfile(LOCAL_CONFIG):
    import importlib.util

    local_config_spec = importlib.util.spec_from_file_location('local_config', LOCAL_CONFIG)
    local_config_module = importlib.util.module_from_spec(local_config_spec)
    local_config_spec.loader.exec_module(local_config_module)
    for k in dir(local_config_module):
        if k.startswith('__'): continue
        v = getattr(local_config_module, k)
        setattr(BaseConfig, k, v)
else:
    print(f'Warning: Local config not found!')
