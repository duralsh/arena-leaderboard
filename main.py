from config import get_db_config
from db_driver import DataBaseDrivers
from datetime import datetime, timedelta, timezone
import csv
import random
import json

db_config = get_db_config()
db_drivers = DataBaseDrivers(db_config=db_config)

LEADERBOARD_START_TIME = datetime(2024, 3, 18, 15, 9, 10, tzinfo=timezone.utc)  ## BAD NAMING, change later

TICKET_PRICE = 0.1 * 1e18




def get_leaderboard(user_id, page_number, limit_per_page):
    start_index = (page_number - 1) * limit_per_page
    end_index = start_index + limit_per_page
    leaderboard = {
        "users": [],
        "currentUser": {}
    }

    buy_weights = db_drivers.query_buy_weight(LEADERBOARD_START_TIME)

    matching_user_tuple = [(index, weight_tuple) for index, weight_tuple in enumerate(buy_weights) if weight_tuple[1] == user_id]

    leaderboard["currentUser"] =  {
        "userId": matching_user_tuple[0][1][1],
        "twitterHandle": matching_user_tuple[0][1][2],
        "twitterName": matching_user_tuple[0][1][4],
        "twitterPhoto": matching_user_tuple[0][1][3],
        "address": matching_user_tuple[0][1][5],
        "tickets": (int(matching_user_tuple[0][1][0]) / TICKET_PRICE),
        "rank": matching_user_tuple[0][0] + 1
    }
    for indice, record in enumerate(buy_weights[start_index:end_index], start=start_index):
        trader_id, cnt, twitter_handle, twitter_name, twitter_photo, address = record[1], int(record[0]), record[2], record[4], record[3], record[5]
        user_info = {
            "userId": trader_id,
            "twitterHandle": twitter_handle,
            "twitterName": twitter_name,
            "twitterPhoto": twitter_photo,
            "address": address,
            "tickets": int(cnt / TICKET_PRICE),
            "rank": indice + 1
        }
        leaderboard["users"].append(user_info)

    return leaderboard


def write_leaderboard_to_csv(leaderboard, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "TwitterHandle", "Tickets", "Address"])
        for user in leaderboard['users']:
            writer.writerow([user['rank'], user['twitterHandle'], user['tickets'], user['address']])


def create_randomized_list(users):
    twitter_handles = []
    total_tickets = sum([user["tickets"] for user in users])
    # Loop through each user and add their handle based on the number of tickets
    for user in users:
        twitter_handles.extend([user["twitterHandle"]] * user["tickets"])
    
    # Shuffle the list randomly
    random.shuffle(twitter_handles)
    return twitter_handles

leaderboard = get_leaderboard("82a9b8d8-60cf-47b9-81e1-36779aa13c20", 1, 500000)
randomized_list = create_randomized_list(leaderboard["users"])
raffle_list = [{"text": user} for user in randomized_list]

# raffle_list = raffle_list[:60000]

with open('raffle-wheel/entries.json', 'w') as file:
        json.dump(raffle_list, file, indent=2)