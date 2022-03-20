from datetime import datetime

from requests import request
from config import NOTION_TOKEN, TWEET_DB
from util import log_error

PAGE_URI = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": NOTION_TOKEN,
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def add_data_to_notion(data):
    response = request(method='POST', url=PAGE_URI, headers=headers, json=data)
    print("Notion Call : ", response.status_code, " : ", str(datetime.now()))
    if response.status_code != 200:
        print("Notion ERROR : ", str(response.json()['message']), " : ", str(datetime.now()))
        log_error(response.json()['message'])
        return False
    return True


def create_data(tweets):
    n = len(tweets)
    for i in range(n - 1, -1, -1):
        print(tweets[i].full_text)
        data = {
            "parent": {
                "database_id": TWEET_DB
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": tweets[i].full_text[:12].strip() + ' : ' +
                                           str(datetime.today()).split(' ')[
                                               0]
                            }
                        }
                    ]
                }, "Id": {
                    "rich_text": [
                        {
                            "text": {
                                "content": str(tweets[i].id)
                            }
                        }
                    ]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": tweets[i].full_text
                                }
                            }
                        ]
                    }
                }
            ]
        }
        response = add_data_to_notion(data)
        if not response:
            return tweets[i].id
    return None
