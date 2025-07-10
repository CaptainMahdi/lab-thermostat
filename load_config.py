import yaml
import os
from dataclasses import dataclass
from typing import List, Dict, Any

CONFIG_PATH = "config.yaml"

@dataclass
class SmartThermo:
    name: str
    version: str
    features: List[str]
    mode: str
    set_point: int

    def change_mode(self, new_mode: str):
        self.mode = new_mode
        print(f"Mode changed to {new_mode}")

    def update_set_point(self, new_temp: int):
        self.set_point = new_temp
        print(f"Set point changed to {new_temp}")

    def to_dict(self, logging: dict) -> dict:
        return {
            'app': {
                'name': self.name,
                'version': self.version,
                'features': self.features,
                'mode': self.mode,
                'set_point': self.set_point,
            },
            'logging': logging
        }

    def save(self, path: str, logging: dict):
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(logging), f)

def load_config(path: str) -> tuple[SmartThermo, dict]:
    if not os.path.exists(path):
        config = {
            'app': {
                'name': 'SmartThermo',
                'version': '1.0.0',
                'features': ['temperature_control'],
                'mode': 'off',
                'set_point': 70
            },
            'logging': {
                'level': 'info',
                'file': 'logs/output.log'
            }
        }
        with open(path, 'w') as f:
            yaml.dump(config, f)
    else:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)

    app = config.get('app', {})
    logging = config.get('logging', {})

    required = ['name', 'version', 'features', 'mode', 'set_point']
    if not all(k in app for k in required):
        raise ValueError("Missing required fields in 'app' config")

    thermo = SmartThermo(
        name=app['name'],
        version=app['version'],
        features=app['features'],
        mode=app['mode'],
        set_point=app['set_point']
    )
    return thermo, logging

def print_summary(thermo: SmartThermo, logging: dict):
    print(f"""Loading config from {CONFIG_PATH}...
Application: {thermo.name} (v{thermo.version})
Enabled Features: {', '.join(thermo.features)}
Mode: {thermo.mode}
Set Point: {thermo.set_point}
Logging: {logging.get('level')} -> {logging.get('file')}""")

if __name__ == "__main__":
    thermo, logging = load_config(CONFIG_PATH)
    print_summary(thermo, logging)

    print("\nUpdating thermostat state...\n")
    thermo.change_mode("cool")
    thermo.update_set_point(67)
    thermo.save(CONFIG_PATH, logging)

    print("Updated and saved new config:") 
