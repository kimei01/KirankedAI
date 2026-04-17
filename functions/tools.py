from datetime import datetime
import anthropic 
import requests
import mcsrapi
from utils.calculatorUtils import elo_tier, format_time, format_playtime, rate, get_country_code
from collections import defaultdict
from utils.playerbuilder import get_ranked_player_depth, get_ranked_player_summary

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

def get_ranked_player_details(user: str):
    player = get_ranked_player_depth(user)
    return player

def get_user_recent_matches(user, count: int = 10, season: int = None, sort: str = "newest"): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_user_matches(count, season, sort)
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


def leaderboard_player(season: int = None , country: str = None): 
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

    user_info = data['data']['users'] 
    season_result = user_info['seasonResult']
    players = [] 
    for user in user_info:
        players.append({ 
            'nickname': user['nickname'], 
            'elo': season_result['eloRate'],
            'Rank': season_result['eloRank'],
            'phasepoints': season_result['phasePoint'],
            'tier': elo_tier(user['eloRate']),
            'country': user['country'] or "N/A", 
        })
    return players

def leaderboard_bestTime(season: int = 0):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_record_leaderboard(season)
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

def playerversus_stats(user1, user2, season: int = None):  
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_matchup(user1, user2, season)
    player_data = sorted(data['data']['players'], key=lambda x: x['eloRank'])
    matchup_results = data['data']['results']
    p1 = get_ranked_player_summary(player_data[0])
    p2 = get_ranked_player_summary(player_data[1])
    
    
    elo_change = data['data']['changes']
    totalgames = matchup_results['ranked']['total']
    p1_wins = matchup_results['ranked'][p1['playeruuid']]
    p2_wins = matchup_results['ranked'][p2['playeruuid']]
    p1_elochange = elo_change[p1['playeruuid']]
    p2_elochange = elo_change[p2['playeruuid']]  

    return p1, p2, totalgames, p1_wins, p2_wins, p1_elochange, p2_elochange     


def playerversus_matches(user1, user2, count: int = 10, season: int = None): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_matches(user1, user2, count, season)
    matches = data['data']
    p1 = get_ranked_player_summary(user1)
    p2 = get_ranked_player_summary(user2)
    
    match_list = []
    for match in matches[:count]:
        p1_nickname = p1['nickname']
        uuid1 = p1['playeruuid']    
        p2_nickname = p2['nickname']
        uuid2 = p2['playeruuid']
        result = match['result']
        winner = result['uuid']
        if winner == uuid1: 
            winner = p1_nickname
            loser = p2_nickname
        elif winner == uuid2:
            winner = p2_nickname
            loser = p1_nickname
        match_list.append({ 
            'date': datetime.fromtimestamp(match['date']).strftime('%Y-%m-%d'),
            'season': match['season'],
            'time': format_time(result['time']),
            'matchup': f"{p1_nickname} vs {p2_nickname}",
            'winner': winner,
            'loser': loser,
            'seed': match['seedType'],
            'bastiontype': match['bastionType'],


        })
    return match_list

def analyze_recent_match(match_id: str ): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.match_details(match_id)
    details = data['data']
    seed = details['seed']
    player_data = details['players']

    elo_change = details['changes']
    completion = details['completion']
    variations = seed['variations']
    result = details['result']
    forfeit = details['forfeited']
    
    #User1 Statistics 
    p1 = get_ranked_player_summary(player_data[0])
    p1_elochange = elo_change[p1['playeruuid']]
    
    #User 2 Statistics
    p2 = get_ranked_player_summary(player_data[1])
    p2_elochange = elo_change[p2['playeruuid']]
   

    
    if forfeit == True:
        if result['uuid'] == p1['playeruuid'] :
            completion = "Forfeited by " + p2['nickname']
        else: 
            completion = "Forfeited by " + p1['nickname']
    elif forfeit == False:
        winner = result['uuid']
        if winner == p1['playeruuid']: 
            winner = p1['nickname']
            loser = p2['nickname']
        elif winner == p2['playeruuid']:
            winner = p2['nickname']
            loser = p1['nickname']
        
    timelines = details['timelines']
    results = []
    milestones = [
    "story.enter_the_nether",
    "nether.find_bastion",
    "nether.find_fortress",
    "nether.obtain_blaze_rod",
    "story.follow_ender_eye",
    "story.enter_the_end",
    "projectelo.timeline.dragon_death",
    ]
    player1_uuid = p1['playeruuid']
    player2_uuid = p2['playeruuid']

    players = defaultdict(list)
    for t in timelines:
        players[t["uuid"]].append(t)
    player1_timelines = players[player1_uuid]
    player2_timelines = players[player2_uuid]
    p1_by_type = {t["type"]: t["time"] for t in player1_timelines}
    p2_by_type = {t["type"]: t["time"] for t in player2_timelines}
    
    

    for milestone in milestones:
        p1_time = p1_by_type.get(milestone, None)
        p2_time = p2_by_type.get(milestone, None)

        if p1_time is not None and p2_time is not None:
            diff = p1_time - p2_time
            results.append({
            "milestone": milestone,
            "p1": p1_time,
            "p2": p2_time,
            "diff": diff
        })
        else:
            results.append({
            "milestone": milestone,
            "p1": p1_time if p1_time is not None else "N/A",
            "p2": p2_time if p2_time is not None else "N/A",
            "diff": "N/A"
        })
    # find the enter_the_nether entry from results
    nether_entry = next((r for r in results if r["milestone"] == "story.enter_the_nether"), None)
    if nether_entry is not None:
        results.insert(0, {
            "milestone": "overworld",
            "p1": nether_entry["p1"],  # time from 0 to nether for p1
            "p2": nether_entry["p2"],  # time from 0 to nether for p2
            "diff": nether_entry["diff"] if nether_entry["diff"] != "N/A" else "N/A"
        })

    match_details = { 
        'date': datetime.fromtimestamp(details['date']).strftime('%Y-%m-%d'),
        'season': details['season'],
        'time': format_time(result['time']),
        'seed': seed['overworld'],
        'bastiontype': seed['nether'],
        'variations': variations, 
        'completion': completion,
        'winner': winner, 
        'loser': loser,
        'p1_elochange': p1_elochange,
        'p2_elochange': p2_elochange,
        'timelines': results,
    }
    return match_details
   



   
    
    
