import praw
import pandas as pd
from datetime import datetime

reddit = praw.Reddit(
    client_id="hP_YOcCuQdPjeBon4705Wg",
    client_secret="np11AHHbdEnR_2Vj8_avn0jymiH3Fw",
    user_agent="Mein MA-Scraper by Funkelchen1996",
    username="Funkelchen1996",
    password="FiT_2022!"
)

search_queries = [
    'Overwatch 2 Perks', 'OW2 Perk', 'OW2 canceled',
    'Blizzard Perk', 'OW2 controversy', 'Perks', 'Perks Overwatch 2', 'Perks OW2', 'Perk', 'Perks balance', 'Perks balanced'
]

subreddit_list = [
    'Overwatch', 'Competitiveoverwatch',
    'Blizzard', 'gamingnews', 'GamerNews'
]

start_date = datetime(2025, 1, 1) 
end_date = datetime.now()

posts_data = []

print("Starte das Scrapen der Reddit-Beiträge...")

for subreddit_name in subreddit_list:
    subreddit = reddit.subreddit(subreddit_name)

    for query in search_queries:
        for submission in subreddit.search(query, sort='new', time_filter='all', limit=1000):
            submission_date = datetime.fromtimestamp(submission.created_utc)
            
            if start_date <= submission_date <= end_date:
                posts_data.append({
                    'title': submission.title,
                    'subreddit': subreddit_name,
                    'score': submission.score,
                    'id': submission.id,
                    'url': submission.url,
                    'num_comments': submission.num_comments,
                    'created': submission_date,
                    'body': submission.selftext
                })

# Doppelte Beiträge entfernen, falls vorhanden
posts_df = pd.DataFrame(posts_data).drop_duplicates(subset='id')

print(f'Anzahl der gesammelten Beiträge: {len(posts_df)}')

posts_df.to_csv('overwatch2_reddit_data_update_perks.csv', index=False)
print("Scraping abgeschlossen. Daten in 'overwatch2_reddit_data_update_perks.csv' gespeichert.")


