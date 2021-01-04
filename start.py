from yahoo_oauth import OAuth2
import click
from fantasybball.util import *


def main(oauth_path, week, league_id, excel_dest_path):
    sc = OAuth2(None, None, from_file=oauth_path)
    stats = pd.DataFrame(
        curate_team_stats(flatten_team_matchup_information_from_api(get_team_data(sc, league_id, week))))
    to_excel(stats, excel_dest_path)


if __name__ == '__main__':
    import sys
    week = sys.argv[1]
    main(
        oauth_path="~/oauth2.json",
        week=week,
        league_id="402.l.166838",
        excel_dest_path=f"./nyc_bball_league/w{week}.xlsx"
    )

    main(
        oauth_path="~/oauth2.json",
        week=week,
        league_id="402.l.64329",
        excel_dest_path=f"./2021_taiwan_number1/w{week}.xlsx"
    )
