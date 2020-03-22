# Elo Football Ratings — Documentation

The objective of this documentation is three-fold. The application works on first building a database of leagues, teams, fixtures, schedules, and results. This was accomplished by partially reverse enigineering  the [SofaScore](https://sofascore.com) API.

## Reverse Engineering the SofaScore API

Although the SofaScore API is not public, it is very intuitive, standard, and attainable through simple GET requests to thier JSON data. There is no API key required, and viewing the XHR requests upon loading any relevant page get you everything you need.

The SofaScore base URL is [https://www.sofascore.com/](https://www.sofascore.com/). This is the host for all data requests. Although alternate API calls would be more direct, the default web route for SofaScore's League Homepages is a robust dashboard of information and already requests all the JSON data we need to collect for the purpose of this project.

## The SofaScore League Homepage

For example, the English Premier League's live homepage is at:
[%root%/tournament/football/england/premier-league/17](https://www.sofascore.com/tournament/football/england/premier-league/17)

The league page web route is, naturally: `<competition>/<sport>/<country>/<name>/<id>`. Fortunately, most of those parameters are very easy to guess based on the league you want, and if your guesswork should fail you can always just navigate the website. The `id` parameter is the only non-human readable parameter, and, thankfully, also the endpoint, so this is all I made note of for later. Turns out, keeping the data up to date is very painless.

There are a number of JSON requests made by the league pages, for betting odds, Teams-Of-The-Week, and so on. Those can all be ingored. The only JSON response we need is the __current season__ response. It's very similar to the league page's static web route,  just with a `season_id` as the endpoint. For the 19-20 English Premier League Season, the all-important JSON request is:

```/u-tournament/17/season/23776/json```

where:

1. `season_id = 23776`
2. A JSON response is explicitly specified, and
3. The `timestamp` query string used by the server is ommitted for our purpose.

I assume I usually would want the latest data, but even if not, I can always modify the exent of results parsed. Also to note: `season_id` is league-specific, so it should be made note of. But essentially with onlythe stored tuple of (league_id, season_id), we can keep any league covered by SofaScore up to date.

## The league.season JSON Response

There are a couple things to note generally about what I will call our `league.season` request its JSON response. One is that the first parameter, I'll call it `competition_type`, has the value `u-tournament` for _all domestic and continental club competitions_. This includes knockout cup competitions, pure league competitions, group/knockout competitions and everything in between. Unless I were to expand the scope to national teams as well (which is [thouroughly covered elsewhere](https://eloratings.net/) so I won't),  `/u-tournament/` can be treated as a constant base route, narrowing our specific request routes to the form `/<league_id>/season/<season_id>/json`.

The other thing to notice is that these JSON responses are typically 150-200kb in size, and growing slightly as the season progresses. All of it is great data, ranging from advanced team statistic aggregates to league average cards per game, but the vast majority is superfluous to the scope of a metric such as Elo. That is, in one sense, the entire purpose of peripahal-statistics-agnostic metric such as Elo. This is the beauty of it.

What we do, however, care about, is the the chronologically-contexed fixtures and matchups, and, of course, the results of those matches relative to the metric's predictions.

### I forgot we had to iterate through the rounds, ughh

Now that Python has`fetch_json`ed the raw  JSON response we will discuss as a Python-type syntax and data types. The current, ongoing round number (in which at least 1 match has been completed) is found at
`json_response['standingsTables'][0]['round']` . This is passed to the round iterator to avoid parsing  rounds that have no completed matches.

For each completed round (and any incomplete round where at least one match has `'status': {'code': 100, 'type': finished}`), our JSON request takes the `league/season` route as a base URI and appends the scope `match/round/<round_num>` , i.e. requesting individual matched grouped by round ( in SQL logic: `SELECT 'match' WHERE 'round' = round_num`).

### The match/round JSON response

This response contains very useful `events` dictionary key, whose value is a `list` of `len(matches_per_round)` where that length is constant within a league but dependent on how many teams are in it at one time.  Each list element is a dictionary representing a match in that round. The home and away `team_id`s can be fetched from the dictionary, and it also conveniently has attribute `status`, which is checked for response `{'code': 100, 'type': finished}` in order to parse the result. If the match has been completed, the dictionary has attribute `winnerCode`, which maps to a value in `(0, 0.5, 1)` where 0 is an away win, 0.5 is a draw, and 1 is a home win. Because these values make  the same measurement as our Elo-weighted `Expected-Result` , they can be mapped directly for comparison.
