from datetime import datetime
import anthropic 
import requests
import mcsrapi
from utils.calculatorUtils import elo_tier, format_time, format_playtime 

def rate(numerator, denominator):
    if not denominator:
        return 0.0
    return round(numerator / denominator * 100, 2)

def get_country_code(user_input: str) -> str | None:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": f'Convert "{user_input}" to a lowercase ISO 3166-1 alpha-2 country code. Reply with ONLY the 2-letter code, nothing else. If unrecognized, reply with "unknown".'
        }]
    )
    
    code = response.content[0].text.strip()
    return None if code == "unknown" else code


def get_ranked_player_details(user: str):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_user_info(user)
    user_info = data["data"]

    statistics_season = user_info["statistics"]["season"]
    statistics_total = user_info["statistics"]["total"]

    season_matches = statistics_season["playedMatches"]["ranked"]
    season_wins = statistics_season["wins"]["ranked"]
    season_forfeits = statistics_season["forfeits"]["ranked"]

    total_matches = statistics_total["playedMatches"]["ranked"]
    total_wins = statistics_total["wins"]["ranked"]
    total_forfeits = statistics_total["forfeits"]["ranked"]

    elo = user_info["eloRate"]
    country = user_info.get("country") or "N/A"

    return {
        "nickname": user_info["nickname"],
        "uuid": user_info["uuid"],
        "country": country,
        "tier": elo_tier(elo),
        "elo": elo,
        "elo_rank": user_info["eloRank"],
        "season_highest_elo": user_info["seasonResult"]["highest"],
        "season_lowest_elo": user_info["seasonResult"]["lowest"],
        "join_date": datetime.fromtimestamp(user_info["timestamp"]["firstOnline"]).strftime("%Y-%m-%d"),
        "last_online": datetime.fromtimestamp(user_info["timestamp"]["lastOnline"]).strftime("%Y-%m-%d"),
        "season": {
            "best_time": format_time(statistics_season["bestTime"]["ranked"]),
            "playtime": format_playtime(statistics_season["playtime"]["ranked"]),
            "best_winstreak": statistics_season["highestWinStreak"]["ranked"],
            "matches": season_matches,
            "wins": season_wins,
            "forfeits": season_forfeits,
            "completions": statistics_season["completions"]["ranked"],
            "winrate": rate(season_wins, season_matches),
            "forfeit_rate": rate(season_forfeits, season_matches),
        },
        "total": {
            "best_time": format_time(statistics_total["bestTime"]["ranked"]),
            "playtime": format_playtime(statistics_total["playtime"]["ranked"]),
            "best_winstreak": statistics_total["highestWinStreak"]["ranked"],
            "matches": total_matches,
            "wins": total_wins,
            "forfeits": total_forfeits,
            "completions": statistics_total["completions"]["ranked"],
            "winrate": rate(total_wins, total_matches),
            "forfeit_rate": rate(total_forfeits, total_matches),
        },
        "leaderboard_url": api.get_official_leaderboard(user),
        "current_season": api.get_current_season(),
    }
#change api please
def user_recent_matches(user, count: int = None): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_user_matches(user)
    matches = data['data']
    
    match_list = []
    for match in matches[:count]: 
        uuid1 = match['players'][0]['uuid']
        uuid2 = match['players'][1]['uuid']
        result = match['result']
        winner = result['uuid']
        changes = {c['uuid']: c['change'] for c in match['changes']}
        if winner == uuid1: 
            winner = match['players'][0]['nickname']
            loser = match['players'][1]['nickname']
        elif winner == uuid2:
            winner = match['players'][1]['nickname']
            loser = match['players'][0]['nickname']
        match_list.append({ 
            'date': datetime.fromtimestamp(match['date']).strftime('%Y-%m-%d'),
            'season': match['season'],
            'time': format_time(result['time']),
            'winner': winner,
            'loser': loser,
            'player1': match['players'][0]['nickname'],
            'player2': match['players'][1]['nickname'],
            'player1_elo': match['players'][0]['eloRate'],
            'player2_elo': match['players'][1]['eloRate'],
            'elo_changes': {
                match['players'][0]['nickname']: changes.get(uuid1, None),
                match['players'][1]['nickname']: changes.get(uuid2, None),
            },
            'seed_id': match['seed']['id'],
            'seedType': match['seedType'],
            'bastiontype': match['bastionType'],
        })
    return match_list
def show_season(): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_leaderboard()
    season = data['data']['season']
    season_num = season['number']
    season_start = datetime.fromtimestamp(season['startsAt'])
    season_end = datetime.fromtimestamp(season['endsAt'])
    time_now = datetime.now()
    days_since_start = (time_now - season_start).days
    days_until_end = (season_end - time_now).days
    season_info = {
        "number": season_num,
        "start": season_start,
        "end": season_end,
        "days_since_start": days_since_start,
        "days_until_end": days_until_end
    }
    return season_info

def leaderboard_player(season: int = None, country: str = None): 
    api = mcsrapi.MCSRRankedAPI()
    
    if season is not None and country is not None:
        return "Please provide only one filter at a time"
    
    if season is not None:
        data = api.get_leaderboard(season=season)
    elif country is not None:
        code = get_country_code(country)
        if code is None:
            return "Country not recognized"
        data = api.get_leaderboard_by_country(country=code)
    else:
        data = api.get_leaderboard()

    return data
    user_info = data['data']['users'] 
    season_result = user_info['seasonResult']
    players = [] 
    for user in user_info:
        players.append({ 
            'nickname': user['nickname'], 
            'elo': season_result['eloRate'],
            'eloRank': season_result['eloRank'],
            'phasepoints': season_result['phasePoint'],
            'tier': elo_tier(user['eloRate']),
            'country': user['country'] or "N/A", 
        })
    return players

def leaderboard_bestTime(season: int = None):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_record_leaderboard()
    runs = data['data']
    run_list = []
    for run in runs:
        run_list.append({ 
            'nickname': run['user']['nickname'], 
            'best_time': format_time(run['time']),
            'Seed type': run['seed']['overworld'],
            'Variations':run['seed']['variations'],
            'bastion': run['seed']['nether'],
            'date': datetime.fromtimestamp(run['date']).strftime('%Y-%m-%d'),
        })
    return run_list

def playerVersus_stats(user1, user2):  
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_matchup(user1, user2)
    player_data = sorted(data['data']['players'], key=lambda x: x['eloRank'])
    matchup_results = data['data']['results']

    #User1 Statistics 
    p1_ID = player_data[0]['uuid']
    p1_nickname = player_data[0]['nickname']
    p1_elo = player_data[0]['eloRate']
    p1_eloRank = player_data[0]['eloRank']
    p1_tier = elo_tier(p1_elo)
    
    p1_country = player_data[0]['country'] or "N/A"
    p1_rankedWins = matchup_results['ranked'][p1_ID]
    
    #User 2 Statistics
    p2_ID = player_data[1]['uuid']
    p2_nickname = player_data[1]['nickname']
    p2_elo = player_data[1]['eloRate']
    p2_tier = elo_tier(p2_elo)
    p2_eloRank = player_data[1]['eloRank']
    p2_country = player_data[1]['country'] or "N/A"
    p2_rankedWins = matchup_results['ranked'][p2_ID]

    elo_change = data['data']['changes']
    p1_elochange = elo_change[p1_ID]
    p2_elochange = elo_change[p2_ID]  

    return { 
        'player1': {
            'nickname': p1_nickname,
            'elo': p1_elo,
            'tier': p1_tier,
            'eloRank': p1_eloRank,
            'country': p1_country,
            'rankedWins': p1_rankedWins,
            'eloChange': p1_elochange
        },
        'player2': {
            'nickname': p2_nickname,
            'elo': p2_elo,
            'tier': p2_tier,
            'eloRank': p2_eloRank,
            'country': p2_country,
            'rankedWins': p2_rankedWins,
            'eloChange': p2_elochange
        }
    }         

#change api please
def playerVersus_matches(user1, user2, count: int = None): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_matchup(user1, user2)
    matches = data['data']
    
    match_list = []
    for match in matches[:count]: 
        uuid1 = match['players'][0]['uuid']
        uuid2 = match['players'][1]['uuid']
        result = match['result']
        winner = result['uuid']
        if winner == uuid1: 
            winner = match['players'][0]['nickname']
            loser = match['players'][1]['nickname']
        elif winner == uuid2:
            winner = match['players'][1]['nickname']
            loser = match['players'][0]['nickname']
        match_list.append({ 
            'date': datetime.fromtimestamp(match['date']).strftime('%Y-%m-%d'),
            'season': match['season'],
            'time': format_time(result['time']),
            'winner': winner,
            'loser': loser,
            'seed': match['seedType'],
            'bastiontype': match['bastionType'],


        })
    return match_list

