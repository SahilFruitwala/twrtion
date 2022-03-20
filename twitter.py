from tweepy import OAuth1UserHandler, API
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, USERNAME
from util import log_error
from notion import create_data

if not CONSUMER_KEY:
    print('error')
    exit(0)

auth = OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth)


def read_id():
    try:
        with open('./last_id.txt', 'r', encoding='UTF-8') as file:
            return file.read().strip()
    except Exception as error:
        log_error(error)
        return None


def fetch_tweets():
    id = read_id()
    query = "from:" + USERNAME + " AND exclude:retweets AND exclude:replies"
    if id:
        query += " AND since_id:" + id
    try:
        results = api.search_tweets(query, tweet_mode="extended", result_type='recent')
        # for result in results:
        #     print(result.full_text, result.id)
        if len(results) > 0:
            with open('./last_id.txt', 'w', encoding='UTF-8') as file:
                file.writelines(str(results[0].id))
            return results
        return None
    except Exception as error:
        log_error(error)
        return None


def tweets_to_notion():
    tweets = fetch_tweets()
    if tweets:
        result = create_data(tweets)
        if result:
            try:
                with open('./last_id.txt', 'w', encoding='UTF-8') as file:
                    file.writelines(str(result))
            except Exception as error:
                log_error(error)
