def format_playtime(ms):
    if ms is None: 
        return " No games played"
    seconds = ms // 1000
    minutes = seconds // 60
    hours = int(minutes // 60)
    return hours


def format_time(ms):
    if ms is None:
        return "No time set.."
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    miliseconds = ms % 1000
    if minutes > 0:
        return f"{minutes}:{seconds:02d}.{miliseconds:03d}"
    return f"{seconds}.{miliseconds:03d}s"

def elo_tier(elo): 
    if elo is None: 
        return "Unrated"
    if elo >= 2000:
        return "Netherite"
    elif elo >= 1800:
        return "Diamond III"
    elif elo >= 1650:
        return "Diamond II"
    elif elo >= 1500:
        return "Diamond I"
    elif elo >= 1400:
        return "Emerald III"
    elif elo >= 1300:
        return "Emerald II"
    elif elo >= 1200:
        return "Emerald I"
    elif elo >= 1100:
        return "Gold III"
    elif elo >= 1000:
        return "Gold II"
    elif elo >= 900:
        return "Gold I"
    elif elo >= 800:
        return "Iron III"
    elif elo >= 700:
        return "Iron II"
    elif elo >= 600:
        return "Iron I"
    elif elo >= 500:
        return "Coal III"
    elif elo >= 400:
        return "Coal II"
    elif elo >= 0:
        return "Coal I"
    else:
        return "Unrated"