#!/usr/bin/env python3
"""
Main extraction runner - coordinates parsing and database building
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config_parser import ConfigParser
from database_builder import ModpackDatabase


def main():
    print("=" * 60)
    print("MODPACK REBALANCING DATA EXTRACTION")
    print("=" * 60)

    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    config_dir = project_root / 'config'
    database_dir = project_root / 'database'

    # Ensure database directory exists
    database_dir.mkdir(exist_ok=True)

    print(f"\nProject root: {project_root}")
    print(f"Config directory: {config_dir}")
    print(f"Database directory: {database_dir}")

    # Step 1: Parse all configuration files
    print("\n" + "=" * 60)
    print("STEP 1: Parsing Configuration Files")
    print("=" * 60)

    parser = ConfigParser(str(config_dir))
    all_configs = parser.scan_all_configs()

    print(f"\n[OK] Parsed {len(all_configs)} configuration files")

    # Export parsed data
    json_output = database_dir / 'parsed_configs.json'
    csv_output = database_dir / 'parsed_configs.csv'

    print(f"\nExporting to JSON: {json_output.name}")
    parser.export_to_json(str(json_output), all_configs)

    print(f"Exporting to CSV: {csv_output.name}")
    parser.export_to_csv(str(csv_output), all_configs)

    # Step 2: Build database
    print("\n" + "=" * 60)
    print("STEP 2: Building Database")
    print("=" * 60)

    db_path = database_dir / 'modpack.db'
    db = ModpackDatabase(str(db_path))

    print(f"\nDatabase location: {db_path.name}")
    db.connect()

    print("Creating database schema...")
    db.create_schema()

    print("Importing parsed configurations...")
    db.import_parsed_configs(str(json_output))

    print("Generating summary report...")
    summary_path = database_dir / 'summary_report.txt'
    db.export_summary_report(str(summary_path))

    db.close()

    # Step 3: Display summary
    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)

    print("\nGenerated files:")
    print(f"  [+] {json_output.name} - All parsed configs in JSON format")
    print(f"  [+] {csv_output.name} - Flattened config data for Excel")
    print(f"  [+] {db_path.name} - SQLite database")
    print(f"  [+] {summary_path.name} - Summary report")

    print("\nNext steps:")
    print("  1. Open parsed_configs.csv in Excel for quick browsing")
    print("  2. Use DB Browser for SQLite to query modpack.db")
    print("  3. Review summary_report.txt for database statistics")
    print("  4. Start analyzing and identifying balance issues")

    print("\n" + "=" * 60)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
