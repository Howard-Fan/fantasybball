# Fantasy Basketball Weekly Score Matchup

## Usage
* Install Python 3
* `pip install -r requirements.txt`
* `python main.py --oauth_path ./oauth2.json --week 1 --league_id 402.l.166838 --excel_dest_path ~/Desktop/fantasybball.xlsx`


## Yahoo Oauth2
https://developer.yahoo.com/oauth2/guide/

Then save the client id and secret key to a json file like
```json
{
    "consumer_key": "<consumer_key>",
    "consumer_secret": "consumer_secret",
}
```