#!/usr/bin/env python3
"""
Config File Parser for Minecraft Modpack Rebalancing
Extracts configuration data from .cfg, .json, and .prop files
"""

import os
import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Union


class ConfigParser:
    """Parse various Minecraft mod configuration formats"""

    def __init__(self, config_root: str):
        self.config_root = Path(config_root)
        self.data = {
            'items': [],
            'mobs': [],
            'biomes': [],
            'structures': [],
            'general_settings': []
        }

    def parse_cfg_file(self, filepath: Path) -> Dict[str, Any]:
        """Parse Forge-style .cfg files"""
        result = {}
        current_section = None

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Section headers
                if line.endswith('{'):
                    section_name = line.replace('{', '').strip()
                    current_section = section_name
                    result[current_section] = {}
                    continue

                # End of section
                if line == '}':
                    current_section = None
                    continue

                # Parse key-value pairs
                if '=' in line and current_section:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Parse value type
                    parsed_value = self._parse_value(value)
                    result[current_section][key] = parsed_value

        return result

    def _parse_value(self, value: str) -> Union[bool, int, float, str, list]:
        """Parse config value to appropriate Python type"""
        # Remove comments
        if '#' in value:
            value = value.split('#')[0].strip()

        # Boolean
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'

        # List/Array (format: <value1, value2>)
        if value.startswith('<') and value.endswith('>'):
            content = value[1:-1].strip()
            if not content:
                return []
            return [item.strip() for item in content.split('\n') if item.strip()]

        # Try integer
        if value.startswith('I:'):
            try:
                return int(value[2:])
            except ValueError:
                pass

        # Try float
        if value.startswith('D:') or value.startswith('S:'):
            try:
                return float(value[2:])
            except ValueError:
                return value[2:]

        # Try boolean
        if value.startswith('B:'):
            return value[2:].lower() == 'true'

        # Try numeric without prefix
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass

        # String
        return value

    def parse_json_file(self, filepath: Path) -> Dict[str, Any]:
        """Parse JSON configuration files"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse_prop_file(self, filepath: Path) -> Dict[str, str]:
        """Parse .prop files (Java properties format)"""
        result = {}

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    result[key.strip()] = value.strip()

        return result

    def scan_all_configs(self) -> Dict[str, Dict]:
        """Scan all configuration files in the config directory"""
        all_configs = {}

        # Scan .cfg files
        for cfg_file in self.config_root.rglob('*.cfg'):
            relative_path = cfg_file.relative_to(self.config_root)
            print(f"Parsing: {relative_path}")
            try:
                all_configs[str(relative_path)] = {
                    'type': 'cfg',
                    'data': self.parse_cfg_file(cfg_file)
                }
            except Exception as e:
                print(f"  Error: {e}")

        # Scan .json files
        for json_file in self.config_root.rglob('*.json'):
            relative_path = json_file.relative_to(self.config_root)
            print(f"Parsing: {relative_path}")
            try:
                all_configs[str(relative_path)] = {
                    'type': 'json',
                    'data': self.parse_json_file(json_file)
                }
            except Exception as e:
                print(f"  Error: {e}")

        # Scan .prop files
        for prop_file in self.config_root.rglob('*.prop'):
            relative_path = prop_file.relative_to(self.config_root)
            print(f"Parsing: {relative_path}")
            try:
                all_configs[str(relative_path)] = {
                    'type': 'prop',
                    'data': self.parse_prop_file(prop_file)
                }
            except Exception as e:
                print(f"  Error: {e}")

        return all_configs

    def export_to_json(self, output_path: str, data: Dict):
        """Export parsed data to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def export_to_csv(self, output_path: str, data: Dict):
        """Export flattened data to CSV"""
        rows = []

        for filepath, content in data.items():
            self._flatten_dict(content['data'], filepath, '', rows)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['File', 'Category', 'Key', 'Value', 'Type'])
            writer.writerows(rows)

    def _flatten_dict(self, d: Dict, filepath: str, parent_key: str, rows: List):
        """Recursively flatten nested dictionaries for CSV export"""
        for key, value in d.items():
            full_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                self._flatten_dict(value, filepath, full_key, rows)
            elif isinstance(value, list):
                rows.append([filepath, parent_key, key, ', '.join(map(str, value)), 'list'])
            else:
                rows.append([filepath, parent_key, key, value, type(value).__name__])


def main():
    """Main execution"""
    import sys

    # Get config directory from command line or use default
    if len(sys.argv) > 1:
        config_dir = sys.argv[1]
    else:
        config_dir = '../config'

    parser = ConfigParser(config_dir)

    print("Scanning configuration files...")
    all_data = parser.scan_all_configs()

    print(f"\nFound {len(all_data)} configuration files")

    # Export to JSON
    json_output = '../../database/parsed_configs.json'
    print(f"\nExporting to {json_output}...")
    parser.export_to_json(json_output, all_data)

    # Export to CSV
    csv_output = '../../database/parsed_configs.csv'
    print(f"Exporting to {csv_output}...")
    parser.export_to_csv(csv_output, all_data)

    print("\nParsing complete!")


if __name__ == '__main__':
    main()
