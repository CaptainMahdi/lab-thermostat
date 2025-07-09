import yaml
from dataclasses import dataclass
from typing import List, Dict, Any
import os

config_dict = {}

# Step 1: Define your data class
@dataclass
class ThemeConfig:
    background: str
    font_size: int

@dataclass
class AppConfig:
    app_name: str
    version: float
    author: str
    theme: ThemeConfig
    settings: Dict[str, Any]
    
unit = "None"

@dataclass
class SmartThermo:
    name: str
    version: str
    features: List[str]
    mode: str
    set_point: int

    def change_mode(self, new_mode: str):
        self.mode = new_mode

    def update_set_point(self, new_temp: int):
        self.set_point = new_temp
    def save_to_file(self, path: str, logging_config: dict):
        with open(path, 'w') as f:
            yaml.dump({
                'app': {
                    'name': self.name,
                    'version': self.version,
                    'features': self.features,
                    'mode': self.mode,
                    'set_point': self.set_point
                },
                'logging': logging_config
            }, f)


# Step 2: Load YAML config file

def load_config(file_path: str) -> tuple[SmartThermo, dict]:
    if not os.path.exists(file_path):
        # Create a default config if file is missing
        default_config = {
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
        with open(file_path, 'w') as f:
            yaml.dump(default_config, f)
        config = default_config
    else:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)

    # Validate presence of required fields
    if 'app' not in config or 'logging' not in config:
        raise ValueError("Missing required sections: 'app' or 'logging'")

    app = config['app']
    required_fields = ['name', 'version', 'features', 'mode', 'set_point']
    for field in required_fields:
        if field not in app:
            raise ValueError(f"Missing required config field: {field}")

    # Create the SmartThermo object
    thermo = SmartThermo(
        name=app['name'],
        version=app['version'],
        features=app['features'],
        mode=app['mode'],
        set_point=app['set_point']
    )

    return thermo, config['logging']


def print_summary(thermo: SmartThermo, logging: dict):
    print("Loading config from config.yaml...")
    print(f"Application: {thermo.name} (v{thermo.version})")
    print("Enabled Features:")
    for feature in thermo.features:
        print(f"- {feature}")
    print(f"Mode: {thermo.mode}")
    print(f"Set Point: {thermo.set_point}")
    print(f"Logging: {logging['level']} -> {logging['file']}")


# Step 3: Use the config
if __name__ == "__main__":
    thermo, logging = load_config("config.yaml")
    print_summary(thermo, logging)
    
    # Simulate runtime state changes
    print("\nUpdating thermostat state...\n")
    thermo.change_mode("heat")
    thermo.update_set_point(70)

    # Save the updated state
    thermo.save_to_file("config.yaml", logging_config)

    print("Updated and saved new config:")
    print_summary(thermo, logging_config)

    
