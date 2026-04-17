from anthropic.types import ToolParam


app_tools = ToolParam[
  {
    "name": "show_season",
    "description": "Returns current season information including season number, start/end dates, days since start, and days until end.",
    "input_schema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_ranked_player_details",
    "description": "Returns detailed ranked player information for a given username.",
    "input_schema": {
      "type": "object",
      "properties": {
        "user": {
          "type": "string",
          "description": "The player's username or identifier."
        }
      },
      "required": ["user"]
    }
  },
  {
    "name": "get_user_recent_matches",
    "description": """
        Returns a list of recent matches for a given user, including match results, ELO changes, seed info, and player details.
        Before calling this tool, ask the user if they want the results sorted,
        and if so, by what field and direction. Wait for their response before calling.
        Sorted by: newest, oldest, fastest, slowest
        """,
    "input_schema": {
      "type": "object",
      "properties": {
        "user": {
          "type": "string",
          "description": "The player's username or identifier."
        },
        "count": {
          "type": "integer",
          "description": "Number of recent matches to return. Defaults to 10.",
          "default": 10,
          "minimum": 1,
          "maximum": 100,
          "description": "Number of results to return (max 50)"
        },
        "season": {
          "type": "integer",
          "description": "Season number to filter matches by. If omitted, returns matches from all seasons."
        },
        "sort": {
          "type": "string",
          "description": "Sort order for matches. Defaults to 'newest'.",
          "default": "newest",
          "enum": ["newest", "oldest"]
        }
      },
      "required": ["user"]
    }
  },
  {
    "name": "leaderboard_player",
    "description": "Returns leaderboard data for players, optionally filtered by season or country (only one filter can be applied at a time).",
    "input_schema": {
      "type": "object",
      "properties": {
        "season": {
          "type": "integer",
          "description": "Season number to filter the leaderboard by. Cannot be used together with country."
        },
        "country": {
          "type": "string",
          "description": "Country name to filter the leaderboard by. Cannot be used together with season."
        }
      },
      "required": []
    }
  },
  {
    "name": "leaderboard_bestTime",
    "description": "Returns the best time leaderboard (record runs), including player nicknames, times, seed types, bastion info, and dates.",
    "input_schema": {
      "type": "object",
      "properties": {
        "season": {
          "type": "integer",
          "description": "Season number to retrieve the record leaderboard for. Defaults to 0 (current or all-time).",
          "default": 0
        }
      },
      "required": []
    }
  },
  {
    "name": "playerversus_stats",
    "description": "Returns head-to-head stats between two players, including ELO data, total games, win counts, and ELO changes.",
    "input_schema": {
      "type": "object",
      "properties": {
        "user1": {
          "type": "string",
          "description": "Username or identifier for the first player."
        },
        "user2": {
          "type": "string",
          "description": "Username or identifier for the second player."
        },
        "season": {
          "type": "integer",
          "description": "Season number to filter the matchup by. If omitted, uses all seasons."
        }
      },
      "required": ["user1", "user2"]
    }
  },
  {
    "name": "playerversus_matches",
    "description": "Returns a list of recent head-to-head matches between two players, including results, seed types, and bastion info.",
    "input_schema": {
      "type": "object",
      "properties": {
        "user1": {
          "type": "string",
          "description": "Username or identifier for the first player."
        },
        "user2": {
          "type": "string",
          "description": "Username or identifier for the second player."
        },
        "count": {
          "type": "integer",
          "description": "Number of matches to return. Defaults to 10.",
          "default": 10,
          "minimum": 1,
          "maximum": 50,
          "description": "Number of results to return (max 50)."
            
        },
        "season": {
          "type": "integer",
          "description": "Season number to filter matches by. If omitted, uses all seasons."
        }
      },
      "required": ["user1", "user2"]
    }
  },
  {
    "name": "analyze_recent_match",
    "description": "Returns detailed analysis of a specific match by ID, including milestone split times for both players, seed info, ELO changes, forfeit status, and winner/loser.",
    "input_schema": {
      "type": "object",
      "properties": {
        "match_id": {
          "type": "string",
          "description": "The unique match ID to retrieve details for."
        }
      },
      "required": ["match_id"]
    }
  }
]