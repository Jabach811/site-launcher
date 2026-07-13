# nba-ft-stats — working notes for Claude sessions

Read this before running or modifying the tool. **After every run or
significant change, append a dated entry to the Learnings Log below** —
that's how sessions build on each other.

## What this is

`ft_stats.py` compiles per-attempt free-throw splits (1st vs 2nd attempt of
2-shot trips, 2nd-attempt FT% after a make vs a miss, and-one FT%, trip-type
counts) from NBA play-by-play. Two modes:

- Player mode (default): `python3 ft_stats.py --player "Stephen Curry" --season 2025-26`
- League mode: `python3 ft_stats.py --league --season 2025-26` — fetches all
  ~1,230 games once, groups by team (and top players per team), writes a full
  markdown report to `reports/`.

## Data sources & format notes

- `stats.nba.com` (player index, game logs, league game log): needs
  browser-ish headers incl. `Referer: https://www.nba.com/` — see
  `STATS_HEADERS`. Responses are `resultSets` header/rowSet pairs.
- `cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{gameId}.json`:
  per-game events. FT events: `actionType == "freethrow"`, subType/description
  like `Free Throw 1 of 2` / `Technical` / `Flagrant 1 of 2`, result in
  `shotResult` ("Made"/"Missed"; description `MISS` prefix is the fallback).
  Events carry `personId`, `playerNameI`, `teamTricode` — team attribution
  comes from the event itself, so trades are handled per-game automatically.
- Everything is cached in `.cache/` (gitignored); a full league season is
  ~1,230 files. Delete the cache to force refetch.

## Known caveats

- Non-technical "1 of 1" FTs are counted as and-ones; a few per season are
  actually away-from-play/delay-of-game FTs, so and-one counts can be off by
  a shot or two.
- The liveData parsing (`classify()`) has been validated against synthetic
  data shaped like the real feed, but **not yet against a real response** —
  network access has been blocked in every session so far. On the first real
  run, sanity-check one game's output against the NBA.com box score and
  record the result here.

## Environment gotchas (hard-won)

- Claude Code remote environments enforce a network allowlist. This tool
  needs `stats.nba.com` AND `cdn.nba.com` (subdomains are not implied by
  `nba.com`). Symptom when blocked: `curl: (56) CONNECT tunnel failed,
  response 403` — check `curl -sS "$HTTPS_PROXY/__agentproxy/status"`.
- Network-policy changes do NOT propagate into a running container; only
  sessions started after the change get the new policy. Don't poll and wait —
  tell the user a fresh session is needed.
- `import`ing the module during testing creates `__pycache__/` — it's
  gitignored now, but check `git status` before committing.

## Learnings Log

Append entries newest-last: `- YYYY-MM-DD: what was learned/changed/run.`

- 2026-07-13: Built player mode; unit-tested classify/summarize offline
  (all pass). Could not run for real — network blocked (see gotchas).
- 2026-07-13: Accidentally committed `__pycache__`; removed and gitignored.
- 2026-07-13: Added `--league` mode: dedupes game IDs from leaguegamelog
  (two team rows per game), keeps per-player open-trip state because FTs by
  different players can interleave (e.g. double technicals) — verified with a
  synthetic 2-game season end-to-end via pre-seeded `.cache/`. Still zero
  real runs; first real league run should verify one game vs NBA.com.
