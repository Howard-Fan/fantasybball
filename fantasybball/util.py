import yahoo_fantasy_api as yfa
import pandas as pd


player_statistic_conversion_map = {
    "9004003": [{"name": "FGM", "type": lambda x: int(x)}, {"name": "FGA", "type": lambda x: int(x)}],
    "5": {"name": "FG%", "type": lambda x: float(x)},
    "9007006": [{"name": "FTM", "type": lambda x: int(x)}, {"name": "FTA", "type": lambda x: int(x)}],
    "8": {"name": "FT%", "type": lambda x: float(x)},
    "10": {"name": "3PTM", "type": lambda x: int(x)},
    "12": {"name": "PTS", "type": lambda x: int(x)},
    "15": {"name": "REB", "type": lambda x: int(x)},
    "16": {"name": "AST", "type": lambda x: int(x)},
    "17": {"name": "ST", "type": lambda x: int(x)},
    "18": {"name": "BLK", "type": lambda x: int(x)},
    "19": {"name": "TO", "type": lambda x: int(x)}
}


def get_team_data(sc, league_id: str, week: int):
    """
    Returns:
    {
        "fantasy_content":{
            "league": [
                {league information},
                {matchup information}
            ]
        }
    }
    """
    gm = yfa.Game(sc, 'nba')
    return gm.to_league(league_id).matchups(week=week)


def flatten_team_matchup_information_from_api(api_data: dict):
    """
    team_data: the direct output from get_team_data()
    
    Returns: 
    [
        {
            "team_id": "1",
            "team_name": "Howard's Team",
            "team_stats": [
                {
                   "stat":{
                      "stat_id":"9004003",
                      "value":"185/358"
                   }
                },
                ...
            ]
        }
        ...
    ]
    """

    matchups = api_data.get("fantasy_content").get("league")[1].get("scoreboard").get("0").get("matchups")
    matchup_count = matchups.get("count")

    teams = list()

    for i in range(matchup_count):
        matchup = matchups.get(str(i))
        teams_per_matchup = matchup.get("matchup").get("0").get("teams")
        team_count_per_matchup = teams_per_matchup.get("count")

        for j in range(team_count_per_matchup):
            team = teams_per_matchup.get(str(j)).get("team")
            team_info = team[0]
            team_stats = team[1].get("team_stats").get("stats")

            result = dict()
            for info in team_info:
                if isinstance(info, dict):
                    if info.get("id"):
                        result.update({
                            "team_id": info.get("id")
                        })
                    elif info.get("name"):
                        result.update({
                            "team_name": info.get("name")
                        })
            result.update({
                "team_stats": team_stats
            })
            teams.append(result)
    return teams


def curate_team_stats(team_data: dict):
    """
    team_data: Curated API data from flatten_team_matchup_information_from_api()

    Returns:
    [
        {
            "team_id": "1",
            "team_name": "Howard's Team",
            "FGM": 100,
            "FGA": 300,
            ...
        }
        ...
    ]
    """

    final_results = list()

    for team in team_data:
        result = dict()
        result.update({"team_name": team.get("team_name")})
        stats = team.get("team_stats")
        for stat in stats:
            stat_conversion_helper = player_statistic_conversion_map.get(stat.get("stat").get("stat_id"))

            if isinstance(stat_conversion_helper, list):
                # This branch is to split up FGM/A and FTM/A
                made_stat_name = stat_conversion_helper[0].get("name")
                attempted_stat_name = stat_conversion_helper[1].get("name")
                made_stat_value = stat_conversion_helper[0].get("type")(stat.get("stat").get("value").split("/")[0])
                attempted_stat_value = stat_conversion_helper[1].get("type")(stat.get("stat").get("value").split("/")[1])

                result.update(
                    {
                        made_stat_name: made_stat_value,
                        attempted_stat_name: attempted_stat_value,
                    }
                )
            else:
                # This is for everything else
                stat_name = stat_conversion_helper.get("name")
                stat_value = stat_conversion_helper.get("type")(stat.get("stat").get("value"))

                result.update(
                    {
                        stat_name: stat_value
                    }
                )
        final_results.append(result)
    return final_results


def to_excel(df, dest_path="~/Desktop/fbball.xlsx"):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(dest_path, engine="xlsxwriter")

    # Write the dataframe data to XlsxWriter. Turn off the default header and
    # index and skip one row to allow us to insert a user defined header.
    df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a list of column headers, to use in add_table().
    column_settings = [{"header": column} for column in df.columns]

    # Add the Excel table structure. Pandas will add the data.
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
