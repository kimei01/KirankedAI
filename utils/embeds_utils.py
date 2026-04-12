import requests as req

def get_embed_color(tier):
    embed_color = ""
    netherite = "B200ED"
    diamond = "82CAFF"
    emerald = "50C878"
    gold = "D4AF37"
    iron = "D4D7D9"
    coal = "151716"
    unrated = "FFFFFF"
    if tier.startswith("Netherite"): 
        embed_color = netherite
    elif tier.startswith("Diamond"): 
        embed_color = diamond
    elif tier.startswith("Emerald"): 
        embed_color = emerald
    elif tier.startswith("Gold"): 
        embed_color = gold
    elif tier.startswith("Iron"): 
        embed_color = iron
    elif tier.startswith("Coal"):
        embed_color = coal
    else: 
        embed_color = unrated
    embed_color = int(embed_color, 16)
    return embed_color

def get_rank_icon(tier):
    icon = ""
    netherite = "<:netherite:1484086882634698893>"
    diamond = "<:diamond:1484086857439510658>"
    emerald = "<:emerald:1484086828922441768>"
    gold = "<:gold:1484086796571639848>"
    iron = "<:iron:1484086759808827493>"
    coal = "<:coal:1484086724559900692>"
    unrated = "<:grey_question:>"
    if tier.startswith("Netherite"): 
        icon = netherite
    elif tier.startswith("Diamond"): 
        icon = diamond
    elif tier.startswith("Emerald"): 
        icon = emerald
    elif tier.startswith("Gold"): 
        icon = gold
    elif tier.startswith("Iron"): 
        icon = iron
    elif tier.startswith("Coal"):
        icon = coal
    else: 
        icon = unrated
    return icon
def get_country_flag(country): 

    if not country or country == "N/A": 
        return ""
    else: 
        country = country.lower()
        flag = f":flag_{country}:"
        return flag
def get_skin(uuid): 
    try: 
        skin = f"https://vzge.me/bust/250/{uuid}" 
        req.get(skin, timeout = 5)
        return skin
    except: 
        skin = f"https://vzge.me/bust/250/X-Steve"
        return skin


