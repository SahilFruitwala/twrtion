from apscheduler.schedulers.blocking import BlockingScheduler
from twitter import tweets_to_notion
import datetime


def start_fetching():
    print("Scheduler Started : ", str(datetime.datetime.now()))
    tweets_to_notion()


tweets_to_notion()
scheduler = BlockingScheduler()
scheduler.add_job(start_fetching, 'interval', hours=3)
scheduler.start()
