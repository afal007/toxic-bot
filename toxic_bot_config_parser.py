import yaml


class Config:
    def __init__(self, path: str):
        self.config = self.load(path)

    def load(self, path: str):
        pass

    def get_property(self, name: str, default: str = None) -> str:
        pass

    def get_boolean(self, name: str, default: bool = None) -> bool:
        try:
            return self.get_property(name) == 'true'
        except KeyError:
            if default is not None:
                return default
            else:
                raise

    def get_int(self, name: str, default: int = None) -> int:
        try:
            return int(self.get_property(name))
        except KeyError:
            if default is not None:
                return default
            else:
                raise
        except ValueError:
            raise Exception('Не удалось привести к типу int значение настройки ' + name)


class YamlConfig(Config):
    def load(self, path: str):
        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError:
                print('Не удалось загрузить конфигурационный файл')
                raise

    def get_property(self, name: str, default: str = None) -> str:
        res = self.config
        for s in name.split("."):
            if s not in self.config and default is not None:
                res = default
                break
            res = res[s]
        return res


class PropertiesConfig(Config):
    def load(self, path: str):
        with open(path, "r") as stream:
            lines = [line.split("=") for line in stream.readlines()]
            return {key.strip(): value.strip() for key, value in lines}

    def get_property(self, name: str, default: str = None) -> str:
        if name not in self.config and default is not None:
            return default
        return self.config.get(name)


def get_config(path: str) -> Config:
    if path.endswith('.yml') or path.endswith('.yaml'):
        return YamlConfig(path)
    elif path.endswith('.properties'):
        return PropertiesConfig(path)
    else:
        raise Exception('Конфигурационный файл должен быть в формате YAML или properties')
