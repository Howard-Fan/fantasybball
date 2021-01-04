from yahoo_oauth import OAuth2
import click
from fantasybball.util import *


@click.command()
@click.option("--oauth_path", required=True, type=str)
@click.option("--week", required=True, type=str)
@click.option("--league_id", required=True, type=str)
@click.option("--excel_dest_path", required=False, type=str)
def main(oauth_path, week, league_id, excel_dest_path):
    sc = OAuth2(None, None, from_file=oauth_path)
    stats = pd.DataFrame(
        curate_team_stats(flatten_team_matchup_information_from_api(get_team_data(sc, league_id, week))))
    to_excel(stats, excel_dest_path)


ny_league_id = "402.l.166838"
tw_league_id = "402.l.64329"
week_to_process = "1"
