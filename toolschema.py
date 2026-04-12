from anthropic.types import ToolParam


get_ranked_player_schema =  ToolParam({
    "name": "get_ranked_player",
    "description": "Get MCSR Ranked stats for a player",
    "input_schema": {
      "type": "object",
      "properties": {
        "user": {
          "type": "string",
          "description": "Minecraft username to look up"
        }
      },
      "required": ["user"]
    }
})  
show_season_schema = ToolParam({
    "name": "show_season",
    "description": "Get current MCSR Ranked season info including season number, start/end dates, days elapsed, and days remaining",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
})

leaderboard_player_schema = ToolParam({
    "name": "leaderboard_player",
    "description": "Get the top 150 players on the current season ELO leaderboard, including nickname, ELO rating, and tier",
    "input_schema": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of players to retrieve from the top of the leaderboard"
            }
        },
        
    }
})

leaderboard_best_time_schema = ToolParam({
    "name": "leaderboard_bestTime",
    "description": "Get the top 100 ranked speedruns in season N, including player nickname, best completion time, seed type, and bastion type",
    "input_schema": {
        "type": "object",
        "properties": {
            "season": {
                "type": "integer",
                "description": "Season number for which to retrieve speedrun records"
            }
        },
    }
})

player_versus_schema = ToolParam({
    "name": "playerVersus",
    "description": "Get head-to-head matchup data for two players including ELO, rank, tier, country, ranked wins against each other, and projected ELO changes",
    "input_schema": {
        "type": "object",
        "properties": {
            "user1": {
                "type": "string",
                "description": "Minecraft username of the first player"
            },
            "user2": {
                "type": "string",
                "description": "Minecraft username of the second player"
            }
        },
        "required": ["user1", "user2"]
    }
})

ALL_TOOLS = [
    show_season_schema,
    leaderboard_player_schema,
    leaderboard_best_time_schema,
    player_versus_schema,
]