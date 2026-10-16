#!/usr/bin/env python3
"""
SQLite Database Builder for Modpack Rebalancing
Creates and populates database with parsed configuration data
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any


class ModpackDatabase:
    """Manage modpack rebalancing database"""

    def __init__(self, db_path: str = '../../database/modpack.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def create_schema(self):
        """Create database schema"""

        # Items/Blocks Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT,
                name TEXT,
                mod_id TEXT,
                damage INTEGER,
                durability INTEGER,
                enchantability INTEGER,
                stack_size INTEGER,
                harvest_level INTEGER,
                mining_speed REAL,
                attack_damage REAL,
                armor_value INTEGER,
                toughness REAL,
                rarity TEXT,
                config_source TEXT,
                notes TEXT
            )
        ''')

        # Mobs/Entities Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT,
                name TEXT,
                mod_id TEXT,
                health REAL,
                attack_damage REAL,
                armor REAL,
                movement_speed REAL,
                knockback_resistance REAL,
                follow_range REAL,
                xp_drop INTEGER,
                is_boss BOOLEAN,
                spawn_weight INTEGER,
                min_group_size INTEGER,
                max_group_size INTEGER,
                config_source TEXT,
                notes TEXT
            )
        ''')

        # Biomes Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS biomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                biome_id INTEGER,
                name TEXT,
                mod_id TEXT,
                temperature REAL,
                rainfall REAL,
                spawn_weight INTEGER,
                village_spawn BOOLEAN,
                stronghold_spawn BOOLEAN,
                config_source TEXT,
                notes TEXT
            )
        ''')

        # Structures/Dungeons Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS structures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id TEXT,
                name TEXT,
                mod_id TEXT,
                spawn_chance INTEGER,
                separation_chunks INTEGER,
                allowed_biomes TEXT,
                mob_type TEXT,
                mob_count INTEGER,
                floor_count INTEGER,
                room_count INTEGER,
                instant_build BOOLEAN,
                config_source TEXT,
                notes TEXT
            )
        ''')

        # Loot Tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS loot_tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                structure_type TEXT,
                item_id TEXT,
                min_quantity INTEGER,
                max_quantity INTEGER,
                weight INTEGER,
                config_source TEXT
            )
        ''')

        # Recipes Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_type TEXT,
                output_item TEXT,
                output_quantity INTEGER,
                input_items TEXT,
                mod_id TEXT,
                crafting_station TEXT,
                config_source TEXT,
                notes TEXT
            )
        ''')

        # Configuration Settings Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS config_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mod_id TEXT,
                category TEXT,
                setting_key TEXT,
                setting_value TEXT,
                value_type TEXT,
                file_path TEXT,
                description TEXT
            )
        ''')

        # Balance Metrics Table (calculated values)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS balance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT,
                entity_id TEXT,
                entity_name TEXT,
                calculated_dps REAL,
                calculated_defense REAL,
                calculated_efficiency REAL,
                progression_tier INTEGER,
                power_score REAL,
                is_outlier BOOLEAN,
                notes TEXT
            )
        ''')

        # Changes Log Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS change_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                change_type TEXT,
                target_type TEXT,
                target_id TEXT,
                field_changed TEXT,
                old_value TEXT,
                new_value TEXT,
                reason TEXT,
                implementation_method TEXT
            )
        ''')

        self.conn.commit()
        print("Database schema created successfully")

    def import_parsed_configs(self, json_path: str):
        """Import parsed configuration data from JSON"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for filepath, content in data.items():
            file_type = content['type']
            config_data = content['data']

            # Extract mod ID from filepath
            mod_id = self._extract_mod_id(filepath)

            # Process based on file type and content
            self._process_config_data(filepath, mod_id, config_data)
            count += 1

        self.conn.commit()
        print(f"Imported {count} configuration files")

    def _extract_mod_id(self, filepath: str) -> str:
        """Extract mod ID from filepath"""
        parts = Path(filepath).parts
        if len(parts) > 0:
            # First part is usually the mod config file name
            return parts[0].replace('.cfg', '').replace('.json', '')
        return 'unknown'

    def _process_config_data(self, filepath: str, mod_id: str, data: Dict):
        """Process configuration data and insert into appropriate tables"""

        # Insert all key-value pairs into config_settings table
        for category, settings in data.items():
            if isinstance(settings, dict):
                for key, value in settings.items():
                    self.cursor.execute('''
                        INSERT INTO config_settings
                        (mod_id, category, setting_key, setting_value, value_type, file_path)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        mod_id,
                        category,
                        key,
                        str(value),
                        type(value).__name__,
                        filepath
                    ))

        # Special processing for known config patterns
        self._process_structure_configs(filepath, mod_id, data)
        self._process_mob_configs(filepath, mod_id, data)
        self._process_biome_configs(filepath, mod_id, data)

    def _process_structure_configs(self, filepath: str, mod_id: str, data: Dict):
        """Process structure/dungeon configuration"""
        if 'DungeonConfig' in filepath or 'stronghold' in filepath.lower():
            # Extract structure data
            structure_data = {
                'structure_id': f"{mod_id}_{Path(filepath).stem}",
                'name': Path(filepath).stem,
                'mod_id': mod_id,
                'config_source': filepath
            }

            # Extract specific values if they exist
            for category, settings in data.items():
                if isinstance(settings, dict):
                    if 'chance' in settings:
                        structure_data['spawn_chance'] = settings['chance']
                    if 'dungeonSeparation' in settings:
                        structure_data['separation_chunks'] = settings['dungeonSeparation']
                    if 'mob' in settings:
                        structure_data['mob_type'] = str(settings['mob'])
                    if 'mobs' in settings:
                        structure_data['mob_count'] = settings['mobs']
                    if 'floors' in settings:
                        structure_data['floor_count'] = settings['floors']
                    if 'rooms' in settings:
                        structure_data['room_count'] = settings['rooms']

            # Insert if we have meaningful data
            if 'spawn_chance' in structure_data or 'mob_type' in structure_data:
                fields = ', '.join(structure_data.keys())
                placeholders = ', '.join(['?'] * len(structure_data))
                self.cursor.execute(f'''
                    INSERT INTO structures ({fields})
                    VALUES ({placeholders})
                ''', tuple(structure_data.values()))

    def _process_mob_configs(self, filepath: str, mod_id: str, data: Dict):
        """Process mob/entity configuration"""
        # Add logic to extract mob data from configs
        # This would be implemented based on specific mod config patterns
        pass

    def _process_biome_configs(self, filepath: str, mod_id: str, data: Dict):
        """Process biome configuration"""
        if 'biome' in filepath.lower():
            for category, settings in data.items():
                if isinstance(settings, dict):
                    # Look for biome ID patterns
                    for key, value in settings.items():
                        if 'biome' in key.lower() and isinstance(value, int):
                            self.cursor.execute('''
                                INSERT INTO biomes (biome_id, name, mod_id, config_source)
                                VALUES (?, ?, ?, ?)
                            ''', (value, key, mod_id, filepath))

    def query_all_structures(self):
        """Query all structures"""
        self.cursor.execute('SELECT * FROM structures')
        return self.cursor.fetchall()

    def query_config_by_mod(self, mod_id: str):
        """Get all config settings for a specific mod"""
        self.cursor.execute('''
            SELECT category, setting_key, setting_value, value_type
            FROM config_settings
            WHERE mod_id = ?
            ORDER BY category, setting_key
        ''', (mod_id,))
        return self.cursor.fetchall()

    def export_summary_report(self, output_path: str):
        """Export summary report of database contents"""
        report = []

        # Count by table
        tables = ['items', 'mobs', 'biomes', 'structures', 'loot_tables', 'recipes', 'config_settings']
        for table in tables:
            self.cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = self.cursor.fetchone()[0]
            report.append(f"{table}: {count} entries")

        # List all mods
        self.cursor.execute('SELECT DISTINCT mod_id FROM config_settings ORDER BY mod_id')
        mods = [row[0] for row in self.cursor.fetchall()]
        report.append(f"\nMods found: {len(mods)}")
        report.extend([f"  - {mod}" for mod in mods])

        with open(output_path, 'w') as f:
            f.write('\n'.join(report))

        print(f"Summary report written to {output_path}")


def main():
    """Main execution"""
    db = ModpackDatabase()

    print("Connecting to database...")
    db.connect()

    print("Creating schema...")
    db.create_schema()

    print("\nImporting parsed configuration data...")
    json_path = '../../database/parsed_configs.json'
    if Path(json_path).exists():
        db.import_parsed_configs(json_path)
    else:
        print(f"Warning: {json_path} not found. Run config_parser.py first.")

    print("\nGenerating summary report...")
    db.export_summary_report('../../database/summary_report.txt')

    print("\nClosing database...")
    db.close()

    print("Database build complete!")


if __name__ == '__main__':
    main()
