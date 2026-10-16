# Example Balance Script
# This demonstrates common CraftTweaker patterns for rebalancing

# ============================================================================
# RECIPE REMOVALS - Remove overpowered or conflicting recipes
# ============================================================================

# Remove a specific recipe (by output item)
# recipes.remove(<Botania:manaResource:14>);  # Removes Dragonstone recipe

# Remove ALL recipes for an item
# recipes.remove(<minecraft:diamond_sword>);

# ============================================================================
# RECIPE ADDITIONS - Add new balanced recipes
# ============================================================================

# Shaped recipe (specific pattern required)
# recipes.addShaped(<Botania:manaResource:14>, [
#     [<ore:ingotManasteel>, <Botania:manaResource>, <ore:ingotManasteel>],
#     [<Botania:manaResource>, <minecraft:diamond>, <Botania:manaResource>],
#     [<ore:ingotManasteel>, <Botania:manaResource>, <ore:ingotManasteel>]
# ]);

# Shapeless recipe (any arrangement)
# recipes.addShapeless(<minecraft:gunpowder> * 2, [
#     <minecraft:coal>, <minecraft:sand>, <ore:dustSalt>
# ]);

# ============================================================================
# FURNACE RECIPES
# ============================================================================

# Add smelting recipe (input, output)
# furnace.addRecipe(<minecraft:iron_ingot>, <minecraft:iron_ore>);

# Remove smelting recipe
# furnace.remove(<minecraft:iron_ingot>);

# ============================================================================
# ORE DICTIONARY - Make items interchangeable
# ============================================================================

# Add item to ore dictionary
# <Botania:manaResource:0>.addTooltip("This is Manasteel!");

# ============================================================================
# HIDE ITEMS FROM NEI - Clean up creative menu
# ============================================================================

# Hide creative-only or disabled items
# mods.nei.NEI.hide(<Botania:manaGlass>);

# ============================================================================
# EXAMPLE: MAKE TINKERS' TOOLS HARDER
# ============================================================================

# Uncomment to implement:

# Remove easy tool station recipe
# recipes.remove(<TConstruct:ToolStationBlock>);

# Add harder recipe requiring iron
# recipes.addShaped(<TConstruct:ToolStationBlock>, [
#     [<minecraft:iron_ingot>, <minecraft:crafting_table>, <minecraft:iron_ingot>],
#     [<ore:plankWood>, null, <ore:plankWood>],
#     [<ore:plankWood>, null, <ore:plankWood>]
# ]);

# ============================================================================
# EXAMPLE: BALANCE MAGIC MODS
# ============================================================================

# Make Thaumonomicon require specific research item
# recipes.remove(<Thaumcraft:ItemThaumonomicon>);
# recipes.addShaped(<Thaumcraft:ItemThaumonomicon>, [
#     [null, <minecraft:feather>, null],
#     [<ore:dyeBlack>, <minecraft:book>, <ore:dyeBlack>],
#     [null, <Thaumcraft:ItemResource:0>, null]
# ]);

# ============================================================================
# EXAMPLE: FOOD BALANCE
# ============================================================================

# Make golden apples harder (require gold blocks instead of ingots)
# recipes.remove(<minecraft:golden_apple:0>);
# recipes.addShaped(<minecraft:golden_apple:0>, [
#     [<minecraft:gold_block>, <minecraft:gold_block>, <minecraft:gold_block>],
#     [<minecraft:gold_block>, <minecraft:apple>, <minecraft:gold_block>],
#     [<minecraft:gold_block>, <minecraft:gold_block>, <minecraft:gold_block>]
# ]);

# ============================================================================
# BEST PRACTICES
# ============================================================================

# 1. Comment your changes - explain WHY
# 2. Test in creative mode first
# 3. Use /mt reload to test changes without restart
# 4. Check minetweaker.log for errors
# 5. Commit to git after testing
# 6. Document in your balance plan

# ============================================================================
# NOTES
# ============================================================================

# - This file is commented out - uncomment lines to activate
# - Use NEI to find item IDs (<modid:item:meta>)
# - Ore dictionary: <ore:ingotIron> matches any iron ingot
# - Numbers after * indicate quantity: <item> * 4 = 4 items
# - null = empty slot in shaped recipes
# - Shapeless recipes can be in any order

print("Example balance script loaded - all examples commented out");
