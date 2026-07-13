#!/usr/bin/env python3
"""Compile advanced free-throw stats for an NBA player from play-by-play data.

Data sources (both free, no API key):
  - stats.nba.com  : player lookup + game log (which games he played)
  - cdn.nba.com    : per-game play-by-play JSON (every FT tagged "1 of 2" etc.)

Outputs, per season:
  - Trips to the line by type (2-shot, 3-shot, and-one/1-shot, technical)
  - FT% on the 1st vs 2nd attempt of 2-shot trips
  - FT% on the 2nd attempt after MAKING vs after MISSING the 1st
  - Both-made / split / both-missed breakdown of 2-shot trips
  - And-one FT% (non-technical 1-of-1 attempts)

Usage:
  python3 ft_stats.py                                  # Curry, 2025-26 regular season
  python3 ft_stats.py --player "Stephen Curry" --season 2025-26
  python3 ft_stats.py --season-type Playoffs
  python3 ft_stats.py --json out.json                  # also dump raw numbers

Stdlib only; needs Python 3.8+. Responses are cached in .cache/ so re-runs
don't re-download ~70 games.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

STATS_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Accept": "application/json",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}

CACHE_DIR = Path(__file__).resolve().parent / ".cache"


def fetch(url, cache_key=None, retries=3, delay=0.6):
    if cache_key:
        cached = CACHE_DIR / cache_key
        if cached.exists():
            return json.loads(cached.read_text())
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=STATS_HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if cache_key:
                CACHE_DIR.mkdir(exist_ok=True)
                (CACHE_DIR / cache_key).write_text(json.dumps(data))
            time.sleep(delay)  # be polite to the API
            return data
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            last_err = e
            time.sleep(2 ** (attempt + 1))
    raise SystemExit(
        f"Failed to fetch {url}\n  {last_err}\n"
        "If this is a 403/connection error, the network may be blocking "
        "stats.nba.com / cdn.nba.com — allowlist both domains and retry."
    )


def resultset_rows(payload, name=None):
    """stats.nba.com returns {resultSets:[{name,headers,rowSet}]}; zip into dicts."""
    for rs in payload.get("resultSets", payload.get("resultSet", [])):
        if name is None or rs["name"] == name:
            return [dict(zip(rs["headers"], row)) for row in rs["rowSet"]]
    return []


def find_player(name, season):
    url = (
        "https://stats.nba.com/stats/playerindex?College=&Country=&DraftPick="
        "&DraftRound=&DraftYear=&Height=&Historical=1&LeagueID=00"
        f"&Season={season}&SeasonType=Regular%20Season&TeamID=0&Weight="
    )
    rows = resultset_rows(fetch(url, cache_key=f"playerindex_{season}.json"))
    want = name.strip().lower()
    for r in rows:
        full = f"{r['PLAYER_FIRST_NAME']} {r['PLAYER_LAST_NAME']}".lower()
        if full == want:
            return r["PERSON_ID"], f"{r['PLAYER_FIRST_NAME']} {r['PLAYER_LAST_NAME']}"
    matches = [
        (r["PERSON_ID"], f"{r['PLAYER_FIRST_NAME']} {r['PLAYER_LAST_NAME']}")
        for r in rows
        if want in f"{r['PLAYER_FIRST_NAME']} {r['PLAYER_LAST_NAME']}".lower()
    ]
    if len(matches) == 1:
        return matches[0]
    if matches:
        opts = ", ".join(m[1] for m in matches[:10])
        raise SystemExit(f"Ambiguous player '{name}'. Matches: {opts}")
    raise SystemExit(f"No player named '{name}' found for {season}.")


def league_game_ids(season, season_type):
    """All game IDs for a season (deduped from the two team rows per game)."""
    url = (
        "https://stats.nba.com/stats/leaguegamelog?Counter=0&Direction=ASC"
        f"&LeagueID=00&PlayerOrTeam=T&Season={season}"
        f"&SeasonType={urllib.parse.quote(season_type)}&Sorter=DATE"
    )
    key = f"leaguegamelog_{season}_{season_type.replace(' ', '')}.json"
    rows = resultset_rows(fetch(url, cache_key=key), "LeagueGameLog")
    seen = {}
    for r in rows:
        seen.setdefault(r["GAME_ID"], (r["GAME_ID"], r["GAME_DATE"], r["MATCHUP"]))
    return sorted(seen.values())


def game_ids(player_id, season, season_type):
    url = (
        f"https://stats.nba.com/stats/playergamelog?PlayerID={player_id}"
        f"&Season={season}&SeasonType={urllib.parse.quote(season_type)}"
    )
    key = f"gamelog_{player_id}_{season}_{season_type.replace(' ', '')}.json"
    rows = resultset_rows(fetch(url, cache_key=key), "PlayerGameLog")
    return [(r["Game_ID"], r["GAME_DATE"], r["MATCHUP"]) for r in rows]


FT_RE = re.compile(r"free throw\s+(technical|flagrant)?\s*(\d)\s+of\s+(\d)", re.I)
TECH_RE = re.compile(r"free throw technical", re.I)


def classify(action):
    """Return (kind, index, total, made) for a freethrow action, else None.

    kind: 'regular' | 'flagrant' | 'technical'
    """
    desc = action.get("description", "") or ""
    sub = (action.get("subType", "") or "").lower()
    made = action.get("shotResult") == "Made" or (
        "shotResult" not in action and not desc.upper().startswith("MISS")
    )
    m = FT_RE.search(desc) or FT_RE.search("free throw " + sub)
    if m:
        kind = (m.group(1) or "regular").lower()
        return kind, int(m.group(2)), int(m.group(3)), made
    if TECH_RE.search(desc) or "technical" in sub:
        return "technical", 1, 1, made
    return None


def collect_fts(games, player_id):
    """Fetch play-by-play for each game, return this player's FT events grouped
    into trips (consecutive attempts of the same 'n of N' sequence)."""
    trips = []
    for i, (gid, date, matchup) in enumerate(games, 1):
        print(f"  [{i}/{len(games)}] {date} {matchup}", file=sys.stderr)
        url = f"https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{gid}.json"
        pbp = fetch(url, cache_key=f"pbp_{gid}.json")
        actions = pbp["game"]["actions"]
        current = None
        for a in actions:
            if a.get("actionType") != "freethrow" or a.get("personId") != player_id:
                continue
            info = classify(a)
            if info is None:
                continue
            kind, idx, total, made = info
            if idx == 1 or current is None or current["kind"] != kind:
                current = {"kind": kind, "total": total, "makes": [], "game": gid}
                trips.append(current)
            current["makes"].append(made)
    return trips


def collect_fts_league(games):
    """Fetch play-by-play for each game and return FT trips for ALL players,
    tagged with player/team from the event itself (trade-proof)."""
    trips = []
    for i, (gid, date, matchup) in enumerate(games, 1):
        print(f"  [{i}/{len(games)}] {date} {matchup}", file=sys.stderr)
        url = f"https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{gid}.json"
        pbp = fetch(url, cache_key=f"pbp_{gid}.json")
        current = {}  # personId -> open trip (FTs by different players can interleave)
        for a in pbp["game"]["actions"]:
            if a.get("actionType") != "freethrow":
                continue
            info = classify(a)
            if info is None:
                continue
            kind, idx, total, made = info
            pid = a.get("personId")
            cur = current.get(pid)
            if idx == 1 or cur is None or cur["kind"] != kind:
                cur = {
                    "kind": kind, "total": total, "makes": [], "game": gid,
                    "personId": pid,
                    "player": a.get("playerNameI") or a.get("playerName") or str(pid),
                    "team": a.get("teamTricode") or "UNK",
                }
                current[pid] = cur
                trips.append(cur)
            cur["makes"].append(made)
    return trips


def summarize(trips):
    s = {
        "trips_2shot": 0, "trips_3shot": 0, "trips_andone": 0, "trips_tech": 0,
        "ft1_2shot": [0, 0], "ft2_2shot": [0, 0],          # [made, att]
        "ft2_after_make": [0, 0], "ft2_after_miss": [0, 0],
        "both_made": 0, "split": 0, "both_missed": 0,
        "andone": [0, 0], "tech": [0, 0],
        "ft_3shot": [0, 0],
        "total": [0, 0],
    }
    for t in trips:
        makes = t["makes"]
        for m in makes:
            s["total"][1] += 1
            s["total"][0] += int(m)
        if t["kind"] == "technical":
            s["trips_tech"] += 1
            for m in makes:
                s["tech"][1] += 1
                s["tech"][0] += int(m)
        elif t["total"] == 1:
            s["trips_andone"] += 1
            s["andone"][1] += 1
            s["andone"][0] += int(makes[0])
        elif t["total"] == 2:
            s["trips_2shot"] += 1
            s["ft1_2shot"][1] += 1
            s["ft1_2shot"][0] += int(makes[0])
            if len(makes) > 1:
                s["ft2_2shot"][1] += 1
                s["ft2_2shot"][0] += int(makes[1])
                key = "ft2_after_make" if makes[0] else "ft2_after_miss"
                s[key][1] += 1
                s[key][0] += int(makes[1])
                if makes[0] and makes[1]:
                    s["both_made"] += 1
                elif makes[0] or makes[1]:
                    s["split"] += 1
                else:
                    s["both_missed"] += 1
        elif t["total"] == 3:
            s["trips_3shot"] += 1
            for m in makes:
                s["ft_3shot"][1] += 1
                s["ft_3shot"][0] += int(m)
    return s


def pct(pair):
    made, att = pair
    return f"{made}/{att} ({made / att:.1%})" if att else "0/0 (—)"


def report(name, season, season_type, s):
    lines = [
        f"\n{name} — {season} {season_type} — Free Throw Breakdown",
        "=" * 60,
        f"Overall FT:            {pct(s['total'])}",
        "",
        "Trips to the line:",
        f"  2-shot trips:        {s['trips_2shot']}",
        f"  3-shot trips:        {s['trips_3shot']}",
        f"  And-one (1-shot):    {s['trips_andone']}",
        f"  Technical:           {s['trips_tech']}",
        "",
        "2-shot trips:",
        f"  1st attempt:         {pct(s['ft1_2shot'])}",
        f"  2nd attempt:         {pct(s['ft2_2shot'])}",
        f"  2nd after MAKE:      {pct(s['ft2_after_make'])}",
        f"  2nd after MISS:      {pct(s['ft2_after_miss'])}",
        f"  Both made:           {s['both_made']}",
        f"  Split (1 of 2):      {s['split']}",
        f"  Both missed:         {s['both_missed']}",
        "",
        f"And-one FTs:           {pct(s['andone'])}",
        f"3-shot trip FTs:       {pct(s['ft_3shot'])}",
        f"Technical FTs:         {pct(s['tech'])}",
    ]
    return "\n".join(lines)


def pct_only(pair):
    made, att = pair
    return f"{made / att:.1%}" if att else "—"


TEAM_TABLE_HEADER = (
    "| Team | FT | FT% | 2-shot trips | 1st FT% | 2nd FT% "
    "| 2nd after make | 2nd after miss | And-one FT% | Tech FT% |\n"
    "|---|---|---|---|---|---|---|---|---|---|"
)


def table_row(label, s):
    return (
        f"| {label} | {s['total'][0]}/{s['total'][1]} | {pct_only(s['total'])} "
        f"| {s['trips_2shot']} | {pct_only(s['ft1_2shot'])} | {pct_only(s['ft2_2shot'])} "
        f"| {pct_only(s['ft2_after_make'])} | {pct_only(s['ft2_after_miss'])} "
        f"| {pct_only(s['andone'])} | {pct_only(s['tech'])} |"
    )


def league_report_md(season, season_type, trips, top_n=8):
    lines = [f"# NBA Free Throw Breakdown — {season} {season_type}", ""]
    league = summarize(trips)
    lines += ["## League totals", "", "```",
              report("NBA (all players)", season, season_type, league).strip(),
              "```", ""]

    by_team = {}
    for t in trips:
        by_team.setdefault(t["team"], []).append(t)
    team_stats = {tm: summarize(ts) for tm, ts in by_team.items()}
    ranked_teams = sorted(
        team_stats,
        key=lambda tm: (team_stats[tm]["total"][0] / team_stats[tm]["total"][1])
        if team_stats[tm]["total"][1] else 0,
        reverse=True,
    )

    lines += ["## Team comparison (sorted by FT%)", "", TEAM_TABLE_HEADER]
    lines += [table_row(tm, team_stats[tm]) for tm in ranked_teams]

    for tm in sorted(by_team):
        lines += ["", f"## {tm}", "", "```",
                  report(tm, season, season_type, team_stats[tm]).strip(), "```",
                  "", f"Top {top_n} players by FT attempts:", "", TEAM_TABLE_HEADER]
        by_player = {}
        for t in by_team[tm]:
            by_player.setdefault(t["player"], []).append(t)
        player_stats = {p: summarize(ts) for p, ts in by_player.items()}
        ranked = sorted(player_stats, key=lambda p: -player_stats[p]["total"][1])
        lines += [table_row(p, player_stats[p]) for p in ranked[:top_n]]

    return "\n".join(lines) + "\n", team_stats


def run_league(args):
    games = league_game_ids(args.season, args.season_type)
    if not games:
        raise SystemExit(f"No {args.season_type} games found for {args.season}.")
    print(f"Fetching play-by-play for {len(games)} games…", file=sys.stderr)
    trips = collect_fts_league(games)
    md, team_stats = league_report_md(args.season, args.season_type, trips)
    out_dir = Path(__file__).resolve().parent / "reports"
    out_dir.mkdir(exist_ok=True)
    slug = f"league_{args.season}_{args.season_type.replace(' ', '').lower()}"
    out = out_dir / f"{slug}.md"
    out.write_text(md)
    print(f"\nFull report written to {out}\n")
    print("Team comparison (sorted by FT%):\n")
    print(TEAM_TABLE_HEADER)
    ranked = sorted(
        team_stats,
        key=lambda tm: (team_stats[tm]["total"][0] / team_stats[tm]["total"][1])
        if team_stats[tm]["total"][1] else 0,
        reverse=True,
    )
    for tm in ranked:
        print(table_row(tm, team_stats[tm]))
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"season": args.season, "season_type": args.season_type,
             "games": len(games), "teams": team_stats}, indent=2))
        print(f"\nRaw numbers written to {args.json}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--league", action="store_true",
                    help="analyze every game in the season, grouped by team")
    ap.add_argument("--player", default="Stephen Curry")
    ap.add_argument("--season", default="2025-26", help="e.g. 2025-26")
    ap.add_argument("--season-type", default="Regular Season",
                    choices=["Regular Season", "Playoffs"])
    ap.add_argument("--json", metavar="FILE", help="also write raw numbers as JSON")
    args = ap.parse_args()

    if args.league:
        run_league(args)
        return

    pid, full_name = find_player(args.player, args.season)
    print(f"Player: {full_name} (id {pid})", file=sys.stderr)
    games = game_ids(pid, args.season, args.season_type)
    if not games:
        raise SystemExit(f"No {args.season_type} games found for {full_name} in {args.season}.")
    print(f"Fetching play-by-play for {len(games)} games…", file=sys.stderr)
    trips = collect_fts(games, pid)
    s = summarize(trips)
    print(report(full_name, args.season, args.season_type, s))
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"player": full_name, "season": args.season,
             "season_type": args.season_type, "games": len(games), "stats": s},
            indent=2))
        print(f"\nRaw numbers written to {args.json}")


if __name__ == "__main__":
    main()
