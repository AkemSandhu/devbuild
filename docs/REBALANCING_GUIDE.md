# Modpack Rebalancing Guide

## Overview
This document describes the comprehensive workflow for rebalancing your Minecraft modpack. The system has extracted **75,578 configuration entries** from **57 mods** and organized them for analysis and modification.

## Project Structure

```
devbuild/
├── database/                    # All extracted data
│   ├── modpack.db              # SQLite database (7.3 MB)
│   ├── parsed_configs.json     # Raw JSON data (2.6 MB)
│   ├── parsed_configs.csv      # Excel-compatible (5.7 MB)
│   └── summary_report.txt      # Quick stats
│
├── scripts/
│   ├── parsing/                # Data extraction tools
│   │   ├── config_parser.py   # Parses .cfg/.json/.prop files
│   │   ├── database_builder.py # Builds SQLite database
│   │   └── run_extraction.py  # Main runner script
│   │
│   └── crafttweaker/           # CraftTweaker scripts (.zs)
│       └── (your balance changes go here)
│
├── docs/
│   └── analysis/               # Your analysis notes
│
└── config/                     # Original mod configs
    └── (all mod configuration files)
```

## Data Extraction Complete

### What Was Extracted
- **693 configuration files** parsed
- **75,578 individual settings** cataloged
- **57 mods** identified and categorized
- **2 biomes** auto-detected
- All data available in 3 formats: SQLite, JSON, CSV

### Key Mods in Your Pack
- **Difficulty/Combat**: Iguana Tinker Tweaks, Dynamic Difficulty, Hunger Overhaul
- **Magic Systems**: Thaumcraft, Botania, Forbidden Magic
- **Tools/Combat**: Tinkers' Construct, ExtraTiC
- **Dungeons**: Chocolate Quest, Roguelike Dungeons
- **Dimensions**: Twilight Forest, Aether, BOP dimensions
- **Food**: Hunger Overhaul, Spice of Life, Pam's Harvestcraft
- **Mobs**: Mo' Creatures, Custom Spawner (extensive configs)
- **World Gen**: Biomes O' Plenty, OreSpawn, Structures

## Using the Extracted Data

### Method 1: Excel/LibreOffice (Quick Start)

1. Open `database/parsed_configs.csv` in Excel
2. Use filters to browse by:
   - **File** column: Source config file
   - **Category** column: Config section
   - **Key** column: Setting name
   - **Value** column: Current value

**Example searches:**
- Filter "Key" for "damage" → Find all damage values
- Filter "Category" for "mob" → Find mob settings
- Filter "File" contains "Botania" → See all Botania settings

### Method 2: SQLite Database (Advanced)

Download **DB Browser for SQLite** (free): https://sqlitebrowser.org/

**Useful Queries:**

```sql
-- Find all difficulty-related settings
SELECT * FROM config_settings
WHERE setting_key LIKE '%difficult%'
   OR setting_key LIKE '%damage%'
   OR setting_key LIKE '%health%';

-- See all Chocolate Quest dungeon configs
SELECT * FROM config_settings
WHERE file_path LIKE '%Chocolate%Dungeon%';

-- Find all spawn-related settings
SELECT mod_id, setting_key, setting_value
FROM config_settings
WHERE setting_key LIKE '%spawn%';

-- Get all config settings for a specific mod
SELECT category, setting_key, setting_value
FROM config_settings
WHERE mod_id = 'IguanaTinkerTweaks'
ORDER BY category, setting_key;
```

### Method 3: JSON (For Scripts)

```python
import json

with open('database/parsed_configs.json', 'r') as f:
    data = json.load(f)

# Access any config file
botania_config = data['Botania.cfg']['data']
print(botania_config['general']['darkQuartz.enabled'])
```

## Rebalancing Workflow

### Step 1: Identify Issues

**Create a spreadsheet/document tracking:**
- What's overpowered/underpowered?
- Which mods are out of balance with each other?
- Progression bottlenecks or shortcuts?

**Key Areas to Analyze:**
1. **Tool Progression** (Tinkers' vs vanilla vs magic tools)
2. **Food Economy** (Spice of Life + Hunger Overhaul interaction)
3. **Mob Difficulty** (Dynamic Difficulty + Custom Spawner)
4. **Dungeon Rewards** (Chocolate Quest loot tables)
5. **Magic Power Levels** (Thaumcraft vs Botania)
6. **Dimension Difficulty** (Twilight, Aether, Nether balance)

### Step 2: Plan Changes

**Two Methods to Implement Changes:**

#### A. Config File Edits (Simple)
- Edit files in `config/` directory directly
- Good for: On/off toggles, simple number tweaks
- Track changes in git: `git diff config/`

#### B. CraftTweaker Scripts (Complex)
- Create `.zs` files in `scripts/crafttweaker/`
- Good for: Recipe changes, item modifications, complex logic
- More powerful but requires learning MineTweaker/CraftTweaker syntax

### Step 3: Document Changes

Create a change log tracking:
- What was changed
- Why it was changed
- Expected impact
- Test results

**Example format:**
```
CHANGE LOG
==========

[2026-10-16] Tinker's Tool Balance Pass #1
- IguanaTinkerTweaks/main.cfg: xpPerLevelMultiplier: 2.0 → 3.0
  Reason: Tools leveling too fast in early game
  Impact: 50% slower tool leveling
  Status: Needs playtesting

[2026-10-16] Chocolate Quest Dungeon Frequency
- chocolateQuest.cfg: dungeonSeparation: 10 → 15
  Reason: Dungeons too common, trivializing exploration
  Impact: ~33% fewer dungeons
  Status: Implemented
```

### Step 4: Test Changes

**Testing Protocol:**
1. Create test world with creative/cheats
2. Test specific scenarios per change
3. Document results
4. Iterate

**Use Commands for Testing:**
- `/time set day` - Reset time
- `/gamemode creative` - Toggle modes
- `/tp <coords>` - Teleport
- NEI cheat mode - Spawn items

### Step 5: Commit to Git

```bash
git add config/ scripts/
git commit -m "Balance pass: Reduced dungeon frequency and tool XP"
git push
```

## Key Configuration Files to Review

###  High-Impact Configs

| File | What It Controls | Priority |
|------|------------------|----------|
| `IguanaTinkerTweaks/main.cfg` | Tool progression, mining levels, XP | **CRITICAL** |
| `HungerOverhaul/HungerOverhaul.cfg` | Food/farming difficulty | **CRITICAL** |
| `SpiceOfLife.cfg` | Food variety requirements | **CRITICAL** |
| `CoroUtil_DynamicDifficulty.cfg` | Mob difficulty scaling | **HIGH** |
| `chocolateQuest.cfg` | Dungeon frequency/difficulty | **HIGH** |
| `Botania.cfg` | Magic item availability | **HIGH** |
| `Thaumcraft.cfg` | Magic system balance | **HIGH** |
| `TinkersConstruct.cfg` | Core tool mechanics | **HIGH** |

### Dungeon/Structure Configs

All in `config/Chocolate/DungeonConfig/*.prop`:
- `stronghold.prop` - Underground dungeons
- `castles*.prop` - Castle structures
- `ship.prop` - Ocean ships
- `npcVillage.prop` - NPC villages

### Loot Tables

`config/TooMuchLoot/loot/generated/*.json` - Vanilla structure loot

### Spawn Configs

`config/CustomSpawner/` - Extensive mob spawning control per dimension/biome

## CraftTweaker Integration

### Creating Balance Scripts

Create files in `scripts/crafttweaker/`:

```javascript
// scripts/crafttweaker/balance_pass_1.zs

// Remove overpowered recipe
recipes.remove(<Botania:manaResource:14>);

// Add harder recipe
recipes.addShaped(<Botania:manaResource:14>, [
    [<ore:ingotManasteel>, <Botania:manaResource>, <ore:ingotManasteel>],
    [<Botania:manaResource>, <minecraft:diamond>, <Botania:manaResource>],
    [<ore:ingotManasteel>, <Botania:manaResource>, <ore:ingotManasteel>]
]);

// Modify tool stats (if supported)
// See ModTweaker documentation for mod-specific tweaks
```

### Reload Scripts In-Game

Use `/mt reload` command (requires MineTweaker/CraftTweaker installed)

## Analysis Tools

### Re-run Extraction (After Config Changes)

```bash
cd scripts/parsing
python run_extraction.py
```

This regenerates database with your changes, allowing before/after comparison.

### Compare Databases

```bash
# Save old database
cp database/modpack.db database/modpack_backup.db

# Make changes to configs
# Re-run extraction

# Use SQL to compare (in DB Browser)
```

## Common Balance Scenarios

### Scenario 1: "Tinker's Tools Are Overpowered"

**Files to Edit:**
- `IguanaTinkerTweaks/main.cfg`
- `IguanaTinkerTweaks/restrictions.cfg`
- `TinkersConstruct.cfg`

**Key Settings:**
```
xpPerLevelMultiplier - Increase to slow leveling
miningSpeedTweaks.multiplier - Reduce mining speed
harvestLevelTweaks - Change material tiers
```

### Scenario 2: "Food Is Too Easy/Hard"

**Files:**
- `HungerOverhaul/HungerOverhaul.cfg`
- `SpiceOfLife.cfg`
- `harvestcraft.cfg`

**Key Settings:**
```
cropRegrowthMultiplier - Slow/speed farming
food.history.length - Variety requirement
difficultyScaling - Hunger difficulty
```

### Scenario 3: "Dungeons Drop Too Much Loot"

**Methods:**
1. **Config**: Edit `config/TooMuchLoot/loot/generated/*.json`
2. **CraftTweaker**: Use loot table modification (if supported)
3. **ChocolateQuest**: Edit `config/Chocolate/ChestConfig/*.prop`

### Scenario 4: "Magic Mods Imbalanced"

**Botania vs Thaumcraft Progression:**
- Review `Botania.cfg` - Enable/disable features
- Review `Thaumcraft.cfg` - Research requirements
- Use CraftTweaker to adjust recipes between mods

## Advanced: Custom Analysis Scripts

Create Python scripts to analyze patterns:

```python
# scripts/analysis/find_outliers.py
import sqlite3

conn = sqlite3.connect('../../database/modpack.db')
cursor = conn.cursor()

# Find all damage values
cursor.execute('''
    SELECT mod_id, setting_key, setting_value
    FROM config_settings
    WHERE setting_key LIKE '%damage%'
      AND value_type = 'int'
''')

damages = cursor.fetchall()
for mod, key, value in damages:
    print(f"{mod:30} {key:40} {value}")
```

## Resources

### Documentation Links
- **CraftTweaker**: https://docs.blamejared.com/
- **ModTweaker**: https://github.com/jaredlll08/ModTweaker
- **Botania**: https://botaniamod.net/
- **Thaumcraft**: (Wiki links)
- **Tinkers' Construct**: https://tinkers-construct.fandom.com/

### Tools
- **DB Browser for SQLite**: https://sqlitebrowser.org/
- **VS Code**: Best editor for `.zs` scripts
- **Excel/LibreOffice**: For CSV analysis

## Troubleshooting

### "My changes aren't working"
1. Check syntax in config files (proper format)
2. Restart Minecraft (config changes need restart)
3. Check logs for errors: `logs/fml-client-latest.log`

### "CraftTweaker script errors"
- Check `/mt syntax` in-game
- Review `minetweaker.log`
- Verify item IDs with NEI (hover + copy)

### "Database is outdated"
```bash
cd scripts/parsing
python run_extraction.py
```

### "Want to reset everything"
```bash
git checkout config/  # Reset all configs
```

## Next Steps

1. **Open `database/parsed_configs.csv` in Excel** - Start browsing
2. **Install DB Browser for SQLite** - Query the database
3. **Create `docs/balance_plan.md`** - Document your vision
4. **Start small** - Change 1-2 settings, test, iterate
5. **Track everything** - Use git commits for each change
6. **Playtest regularly** - Balance is iterative

## Questions & Support

- Review this guide
- Check mod documentation
- Search CraftTweaker docs
- Test in creative mode first

---

**Database Stats:**
- 75,578 config settings extracted
- 57 mods cataloged
- 693 files parsed
- Ready for analysis!
