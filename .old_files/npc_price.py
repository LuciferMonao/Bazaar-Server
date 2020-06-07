
def get_item_price(itemID):
    dict = get()[1]
    try:
        return(dict[itemID])
    except KeyError:
        return(0)


def get():
    dict = {
        "WHEAT":1,
        "SEEDS":0.5,
        "POTATO_ITEM":1,
        "CARROT_ITEM":1,
        "MELON":0.5,
        "PUMPKIN":4,
        "RED_MUSHROOM":4,
        "BROWN_MUSHROOM":4,
        "CACTUS":1,
        "INK_SACK:3":3,
        "SUGAR_CANE":2,
        "FEATHER":3,
        "RAW_BEEF":4,
        "LEATHER":3,
        "PORK":5,
        "RAW_CHICKEN":4,
        "ENCHANTED_EGG":435,
        "MUTTON":5,
        "RABBIT_HIDE":5,
        "RABBIT_FOOT":5,
        "RABBIT":4,
        "COBBLESTONE":1,
        "COAL":2,
        "IRON_INGOT":3,
        "GOLD_INGOT":4,
        "EMERALD":6,
        "DIAMOND":8,
        "INK_SACK:4":1,
        "REDSTONE":1,
        "QUARTZ":4,
        "ENDER_STONE":2,
        "GLOWSTONE_DUST":2,
        "OBSIDIAN":12,
        "GRAVEL":3,
        "FLINT":4,
        "SAND":2,
        "CLAY_BALL":3,
        "ICE":0.5,
        "ROTTEN_FLESH":2,
        "BONE":2,
        "SPIDER_EYE":3,
        "STRING":3,
        "ENDER_PEARL":10,
        "BLAZE_ROD":9,
        "GHAST_TEAR":16,
        "SLIME_BALL":5,
        "MAGMA_CREAM":8,
        "RAW_FISH":6,
        "RAW_FISH:1":10,
        "RAW_FISH:2":20,
        "PRISMARINE_SHARD":5,
        "PRISMARINE_CRYSTALS":5,
        "SPONGE":50,
        "LOG":2,
        "LOG:2":2,
        "LOG_2":2,
        "LOG_2:1":2,
        "LOG:3":2,
        "LOG:1":2,
        "NETHER_STALK":3,
        "SNOW_BALL":1,
    }
    keys = []

    for key in dict:
        keys.append(key)

    return([keys, dict])