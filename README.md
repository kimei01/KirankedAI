> [!NOTE]
> FastAPI backend complete. Plain HTML/CSS/JS frontend in active development.

## KirankedAI
A full-stack web app for the [MCSR Ranked](https://mcsrranked.com) Minecraft speedrunning community. Users can view a live leaderboard and ask natural language questions about player stats — powered by Claude AI.

## What is MCSR Ranked?
MCSR Ranked is a mod built for Minecraft as a competitive matchmaking system for speedrunners to race against other players in ranked matches and climb a global ladder.
Learn more at the [official MCSR Ranked website](https://mcsrranked.com).
For developers, the API documentation is available [here](https://mcsrranked.com/api).

## Features
- Ask natural language questions about any player's stats
- Claude autonomously decides which API endpoints to call and synthesizes results into a plain English answer
- Live leaderboard data pulled directly from the MCSR Ranked API
- Edge case handling (invalid usernames, API timeouts, out-of-scope questions)

---

## Commands (CLI)

| Command / Query | Description |
|-----------------|-------------|
| `"Who is rank 1 in season 9?"` | Get the top player for a given season |
| `"What is [player]'s elo?"` | Look up a player's current elo and rank |
| `"Compare [player1] vs [player2]"` | Head-to-head record between two players |
| `"Show me the top 10 leaderboard"` | Display current season leaderboard |
| `"What are the fastest ranked runs?"` | Show all-time best runs |

---

## Tech Stack

- **Backend:** Python + FastAPI
- **AI:** Anthropic Claude API (Haiku)
- **Frontend:** Plain HTML + CSS + JS → React + Vite + Tailwind (rebuild)
- **Data:** MCSR Ranked REST API (live data)

## Architecture

```
User question
    ↓
FastAPI POST /ask
    ↓
Claude receives question + tool definitions
    ↓
Claude decides which tool to call + params
    ↓
Backend executes MCSR API call
    ↓
Result fed back to Claude as tool_result
    ↓
Claude writes plain English answer
    ↓
Response returned to user
```

---

## Installation

### Prerequisites
- Python 3.8+
- An Anthropic API key from the [Anthropic Console](https://console.anthropic.com)

### Steps

1. Clone the repository
```bash
git clone https://github.com/yourusername/kiranked-web.git
cd kiranked-web
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your API key
```env
ANTHROPIC_API_KEY=your_key_here
```

4. Run the CLI
```bash
python main.py
```

---

## Roadmap

- [x] SDK installed and API key configured
- [x] Basic multi-turn conversation working
- [x] All tools written with JSON schemas
- [x] Claude reply logic and edge case handling complete
- [ ] FastAPI wrapper (`POST /ask`)
- [ ] Plain HTML + CSS + JS frontend (leaderboard + AI chat)
- [ ] Deploy (Railway for backend, Vercel for frontend)
- [ ] React + Vite + Tailwind frontend rebuild
- [ ] Polish and share with the MCSR community

---

## About this Project

Kiranked Web evolved from [Kiranked](https://github.com/kimei01/kiranked), an existing Discord bot for MCSR Ranked stats. The goal is to bring the same functionality to the web with a richer UI and a natural language AI interface — so anyone in the community can ask questions about players and stats without needing to know any commands.

Built to learn FastAPI, the Anthropic Claude API, agentic AI patterns, and eventually React.
