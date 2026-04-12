import requests as req
import urllib

api = "https://api.mcsrranked.com/"

class MCSRRankedAPI: 
    def __init__(self):
        self.api = api
    def get_user_info(self, user): 
        user1 = urllib.parse.quote(user, safe='_')
        url = f"{self.api}users/{user1}"
        response = req.get(url, timeout=5)
        return response.json()
    def get_official_leaderboard(self, user): 
        url = f"https://mcsrranked.com/stats/{user}"
        return url
    def get_current_season(self): 
        response = req.get(f"{self.api}leaderboard", timeout=5)
        return response.json()['data']['season']['number']
    def get_leaderboard(self, season = None): 
        if season is not None: 
            response = req.get(f"{self.api}leaderboard?season={season}", timeout=5)
        else: 
            response = req.get(f"{self.api}leaderboard", timeout=5)
        return response.json()
    def get_leaderboard_by_country(self, country = None): 
        response = req.get(f"{self.api}leaderboard?country={country}", timeout=5)
        return response.json()
    
    def get_record_leaderboard(self): 
        response = req.get(f"{self.api}record-leaderboard", timeout=5)
        return response.json()
    def get_matchup(self, user1, user2):
        response = req.get(f"{self.api}users/{user1}/versus/{user2}", timeout = 5)
        return response.json()
    def get_match(self, user1, user2, count, season):
        response = req.get(f"{self.api}users/{user1}/versus/{user2}/matches", timeout = 5)
        return response.json()
