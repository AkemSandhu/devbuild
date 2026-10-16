# CraftTweaker Scripts Directory

## What Are CraftTweaker Scripts?

CraftTweaker (formerly MineTweaker) lets you modify recipes, items, and game mechanics using scripts written in `.zs` files.

## How to Use

1. Create `.zs` files in this directory
2. Start/restart Minecraft to load scripts
3. Use `/mt reload` in-game to reload without restart
4. Check `minetweaker.log` for errors

## Script Naming Convention

Use descriptive names:
- `balance_weapons.zs` - Weapon recipe changes
- `harder_magic.zs` - Make magic items harder to obtain
- `food_tweaks.zs` - Food recipe modifications
- `remove_exploits.zs` - Remove overpowered recipes

## Example Scripts

See `example_balance.zs` for starter template

## Documentation

- CraftTweaker Wiki: https://docs.blamejared.com/
- Recipe syntax: https://docs.blamejared.com/en/1.12/Vanilla/Recipes/Recipes_Crafting_Table/
- ModTweaker (mod support): https://github.com/jaredlll08/ModTweaker

## Finding Item IDs

In-game with NEI:
1. Enable cheat mode
2. Hover over item
3. Press `Shift + Click` to copy ID
4. Use in scripts as `<modid:itemname:meta>`

Example: `<Botania:manaResource:0>` = Manasteel Ingot
