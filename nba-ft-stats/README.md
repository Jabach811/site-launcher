# NBA Advanced Free Throw Stats

Compiles per-attempt free throw splits for any NBA player by parsing every
game's play-by-play log — stuff box scores don't show:

- Trips to the line by type: 2-shot, 3-shot, and-one (1-shot), technical
- FT% on the 1st vs 2nd attempt of 2-shot trips
- FT% on the 2nd attempt **after making** vs **after missing** the 1st
- Both-made / split / both-missed counts on 2-shot trips
- And-one FT%

## Usage

Requires only Python 3.8+ (no packages to install):

```bash
python3 ft_stats.py                                        # Steph Curry, 2025-26 regular season
python3 ft_stats.py --player "Stephen Curry" --season 2025-26
python3 ft_stats.py --season-type Playoffs
python3 ft_stats.py --json curry.json                      # also dump raw numbers
```

First run downloads ~1 play-by-play file per game (a minute or two);
responses are cached in `.cache/` so re-runs are instant.

## Network requirements

The script talks to two public NBA endpoints (no login/API key):

- `stats.nba.com` — player lookup and game log
- `cdn.nba.com` — per-game play-by-play JSON

If you run this inside a Claude Code remote environment, the environment's
network policy must allow both domains.

## How the stats are derived

Every free throw in the NBA's play-by-play feed is tagged like
`Free Throw 1 of 2`, `2 of 2`, `1 of 1`, or `Technical`, with a
made/missed result. Consecutive attempts are grouped into "trips";
non-technical `1 of 1` attempts are counted as and-ones. (A tiny number of
1-of-1s can come from away-from-play or delay-of-game fouls, so and-one
counts may be off by a shot or two over a season.)
