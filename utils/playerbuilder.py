import requests as req
from utils.calculatorUtils import elo_tier, format_time, format_playtime, rate
import mcsrapi
from models import playerinfo, seasonstats, totalstats, playerinfosummary
from datetime import datetime

def get_ranked_player_depth(user: str):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_user_info(user)
    user_info = data["data"]

    statistics_season = user_info["statistics"]["season"]
    statistics_total = user_info["statistics"]["total"]
    season = seasonstats(
        best_time=format_time(statistics_season["bestTime"]["ranked"]),
        playtime=format_playtime(statistics_season["playtime"]["ranked"]),
        best_winstreak=statistics_season["highestWinStreak"]["ranked"],
        matches=statistics_season["playedMatches"]["ranked"],
        wins=statistics_season["wins"]["ranked"],
        forfeits=statistics_season["forfeits"]["ranked"],
        completions=statistics_season["completions"]["ranked"],
        winrate=rate(statistics_season["wins"]["ranked"], statistics_season["playedMatches"]["ranked"]),
        forfeit_rate=rate(statistics_season["forfeits"]["ranked"], statistics_season["playedMatches"]["ranked"])
    )

    total_matches = statistics_total["playedMatches"]["ranked"]
    total_wins = statistics_total["wins"]["ranked"]
    total_forfeits = statistics_total["forfeits"]["ranked"]
    total = totalstats(
        best_time=format_time(statistics_total["bestTime"]["ranked"]),
        playtime=format_playtime(statistics_total["playtime"]["ranked"]),
        best_winstreak=statistics_total["highestWinStreak"]["ranked"],
        matches=total_matches,
        wins=total_wins,
        forfeits=total_forfeits,
        completions=statistics_total["completions"]["ranked"],
        winrate=rate(total_wins, total_matches),
        forfeit_rate=rate(total_forfeits, total_matches)
    )

    elo = user_info["eloRate"]
    country = user_info.get("country") or "N/A"
    playerinfo = playerinfo(
        nickname = user_info['nickname'],
        uuid = user_info['uuid'],
        country = country,
        tier = elo_tier(elo),
        elo = elo, 
        rank = user_info['eloRank'],
        season_highest_elo = user_info['seasonResult']['highest'], 
        season_lowest_elo = user_info['seasonResult']['lowest'],
        join_date = datetime.fromtimestamp(user_info["timestamp"]["firstOnline"]).strftime("%Y-%m-%d"),
        last_online = datetime.fromtimestamp(user_info["timestamp"]["lastOnline"]).strftime("%Y-%m-%d"),
    )
    
    return playerinfo, season, total

def get_ranked_player_summary(user: str): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_user_info(user)
    user_info = data["data"]
    playerinfosummary = playerinfosummary(
        playeruuid = user_info['uuid'],
        nickname = user_info['nickname'],
        elo = user_info['eloRate'], 
        rank = user_info['eloRank'],
        tier = elo_tier(user_info['eloRate']),
        country = user_info.get("country") or "N/A",
    )
    return playerinfosummary
