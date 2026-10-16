# Modpack Rebalancing System

## 🎯 System Overview

A comprehensive workflow and database system for rebalancing the entire devbuild modpack. All configuration data has been extracted, parsed, and organized for easy analysis and modification.

## 📊 Extraction Complete

✅ **75,578 configuration settings** extracted
✅ **693 config files** parsed
✅ **57 mods** cataloged
✅ **3 output formats**: SQLite database, JSON, CSV
✅ **7.3 MB** database ready for queries

## 🚀 Quick Start

### 1. View Your Data (Pick One Method)

**Option A: Excel (Easiest)**
```
Open: database/parsed_configs.csv
Use filters to search/sort all 75,000+ settings
```

**Option B: SQLite (Most Powerful)**
```
1. Download DB Browser for SQLite (free)
   https://sqlitebrowser.org/
2. Open: database/modpack.db
3. Run queries to find specific settings
```

**Option C: JSON (For Programmers)**
```
Read: database/parsed_configs.json
Parse with Python/JavaScript/etc
```

### 2. Read the Guide

📖 **Start here**: `docs/REBALANCING_GUIDE.md`

Complete guide covering:
- How to use the extracted data
- Rebalancing workflow
- Key config files to review
- CraftTweaker scripting
- Common balance scenarios
- SQL query examples

### 3. Start Balancing

```
1. Identify issues (overpowered items, difficulty curve, etc.)
2. Search database for relevant settings
3. Make changes (config files OR CraftTweaker scripts)
4. Test in-game
5. Commit to git
6. Repeat!
```

## 📁 Project Structure

```
devbuild/
│
├── database/                    # ⭐ START HERE
│   ├── modpack.db              # SQLite database (query everything)
│   ├── parsed_configs.csv      # Open in Excel
│   ├── parsed_configs.json     # Raw data
│   └── summary_report.txt      # Stats overview
│
├── docs/
│   ├── REBALANCING_GUIDE.md    # 📖 FULL DOCUMENTATION
│   └── analysis/               # Your notes go here
│
├── scripts/
│   ├── parsing/                # Python extraction tools
│   │   ├── config_parser.py   # Parses config files
│   │   ├── database_builder.py # Builds database
│   │   └── run_extraction.py  # Main runner
│   │
│   └── crafttweaker/           # CraftTweaker balance scripts
│       ├── README.md           # How to use .zs scripts
│       └── example_balance.zs  # Template
│
├── config/                     # Original mod configs (edit these)
└── REBALANCING_README.md       # This file
```

## 🔍 Example Queries

### Excel CSV Search

Open `database/parsed_configs.csv` and filter:

- **Find all damage values**: Filter "Key" column for "damage"
- **See Botania settings**: Filter "File" for "Botania"
- **Find spawn rates**: Filter "Key" for "spawn"

### SQL Database Queries

```sql
-- All difficulty settings
SELECT * FROM config_settings
WHERE setting_key LIKE '%difficult%' OR setting_key LIKE '%damage%';

-- Iguana Tinker Tweaks settings
SELECT * FROM config_settings
WHERE mod_id = 'IguanaTinkerTweaks';

-- Dungeon configurations
SELECT * FROM config_settings
WHERE file_path LIKE '%Dungeon%';
```

## 🎮 Key Mods to Balance

### Critical Priority
- **Iguana Tinker Tweaks** - Tool progression
- **Hunger Overhaul** - Food difficulty
- **Spice of Life** - Food variety
- **Dynamic Difficulty** - Mob scaling

### High Priority
- **Chocolate Quest** - Dungeon frequency/loot
- **Tinkers' Construct** - Tool mechanics
- **Botania** - Magic items
- **Thaumcraft** - Magic research
- **Custom Spawner** - Mob spawns (huge config)

### Balance Considerations
- **Twilight Forest** vs **Aether** - Dimension difficulty
- **Mo' Creatures** - Additional mobs
- **Biomes O' Plenty** - World generation
- **Pam's Harvestcraft** - Food availability

## 🛠️ Tools & Resources

### Required
- **Python 3.x** - Already used for extraction
- **Excel/LibreOffice** - View CSV data
- **Text Editor** - Edit config files

### Recommended
- **DB Browser for SQLite** - https://sqlitebrowser.org/
- **VS Code** - Best editor for .zs scripts
- **Git** - Already set up, track your changes

### Documentation
- **Full Guide**: `docs/REBALANCING_GUIDE.md`
- **CraftTweaker Docs**: https://docs.blamejared.com/
- **Mod Wikis**: Search "[modname] wiki"

## 📝 Workflow

```
1. ANALYZE
   ├─ Open database/parsed_configs.csv
   ├─ Search for specific settings
   └─ Identify balance issues

2. PLAN
   ├─ Document what needs changing
   ├─ Research mod interactions
   └─ Create change list

3. IMPLEMENT
   ├─ Method A: Edit config/*.cfg files directly
   └─ Method B: Create scripts/crafttweaker/*.zs scripts

4. TEST
   ├─ Launch game
   ├─ Test specific scenarios
   └─ Check for errors

5. DOCUMENT
   ├─ Update your balance notes
   ├─ Git commit with clear message
   └─ Track results

6. ITERATE
   └─ Repeat until balanced!
```

## 🔄 Re-running Extraction

If you make config changes and want to update the database:

```bash
cd scripts/parsing
python run_extraction.py
```

This regenerates all files in `database/` with your latest changes.

## 💡 Quick Tips

1. **Start Small** - Change 1-2 settings, test, iterate
2. **Use Git** - Commit after each successful change
3. **Test in Creative** - Spawn items, check recipes
4. **Read Configs** - Many have helpful comments
5. **Check Logs** - `logs/fml-client-latest.log` for errors
6. **Backup First** - Git makes this easy: `git commit -am "Backup before balance pass"`

## 📋 Example Balance Tasks

### Easy (Config Edits)
- Change dungeon spawn frequency
- Adjust crop growth rates
- Modify mob health values
- Enable/disable mod features

### Medium (Config + Testing)
- Rebalance food system
- Adjust tool progression curve
- Modify loot tables
- Change biome spawn weights

### Advanced (CraftTweaker)
- Add new recipes
- Remove overpowered recipes
- Cross-mod recipe integration
- Custom crafting chains

## 🆘 Troubleshooting

### "Database is outdated"
```bash
cd scripts/parsing && python run_extraction.py
```

### "Config changes aren't working"
1. Check file syntax (proper format)
2. Restart Minecraft completely
3. Check `logs/` for errors

### "CraftTweaker errors"
1. Check `/mt syntax` command in-game
2. Read `minetweaker.log`
3. Verify item IDs with NEI

### "Want to reset changes"
```bash
git log              # See commit history
git checkout <hash>  # Restore old version
# OR
git checkout config/ModName.cfg  # Reset one file
```

## 🎯 Next Steps

1. ✅ **Read** `docs/REBALANCING_GUIDE.md`
2. ✅ **Open** `database/parsed_configs.csv` in Excel
3. ✅ **Install** DB Browser for SQLite (optional but recommended)
4. ✅ **Create** `docs/analysis/balance_plan.md` with your vision
5. ✅ **Start** making small changes
6. ✅ **Test** everything thoroughly
7. ✅ **Commit** changes to git

## 📚 Documentation Index

- **This File** - Overview and quick start
- **docs/REBALANCING_GUIDE.md** - Complete rebalancing guide (START HERE)
- **scripts/crafttweaker/README.md** - CraftTweaker scripting guide
- **database/summary_report.txt** - Quick stats

## 🎉 You're Ready!

Everything is set up and ready to go. You have:
- ✅ All mod data extracted and organized
- ✅ Multiple tools to query and analyze
- ✅ Complete documentation
- ✅ Example scripts and workflows
- ✅ Git version control

**Start exploring the database and happy balancing!**

---

*Generated: 2026-10-16*
*Total Settings: 75,578*
*Mods Analyzed: 57*
*Ready for rebalancing!*
