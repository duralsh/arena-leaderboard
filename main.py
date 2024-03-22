from config import get_db_config
from db_driver import DataBaseDrivers
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

db_config = get_db_config()
db_drivers = DataBaseDrivers(db_config=db_config)

query_time = datetime(2024, 3, 10, 15, 9, 10, tzinfo=timezone.utc)  ## BAD NAMING, change later

ticket_price = 0.1 * 1e18




def get_leaderboard(user_id, page_number, limit_per_page):
    start_index = (page_number - 1) * limit_per_page
    end_index = start_index + limit_per_page
    leaderboard = {
        "users": [],
        "currentUser": {}
    }

    buy_weights = db_drivers.query_buy_weight(query_time)

    matching_user_tuple = [(index, weight_tuple) for index, weight_tuple in enumerate(buy_weights) if weight_tuple[1] == user_id]

    leaderboard["currentUser"] =  {
        "userId": matching_user_tuple[0][1][1],
        "twitterHandle": matching_user_tuple[0][1][2],
        "twitterName": matching_user_tuple[0][1][4],
        "twitterPhoto": matching_user_tuple[0][1][3],
        "tickets": (int(matching_user_tuple[0][1][0]) / ticket_price),
        "rank": matching_user_tuple[0][0]
    }
    for indice, record in enumerate(buy_weights[start_index:end_index], start=start_index):
        trader_id, cnt, twitter_handle, twitter_name, twitter_photo = record[1], int(record[0]), record[2], record[4], record[3]
        user_info = {
            "userId": trader_id,
            "twitterHandle": twitter_handle,
            "twitterName": twitter_name,
            "twitterPhoto": twitter_photo,
            "tickets": int(cnt / ticket_price),
            "rank": indice + 1
        }
        leaderboard["users"].append(user_info)

    return leaderboard


@app.route('/api/leaderboard/<user_id>', methods=['GET'])
def leaderboard_api(user_id):
    page_number = int(request.args.get('page', 1))
    limit_per_page = int(request.args.get('limit', 10))

    if page_number <= 0:
        return jsonify({"error": "Page number must be a positive integer."}), 400

    leaderboard = get_leaderboard(user_id, page_number, limit_per_page)

    return jsonify(leaderboard)


leaderboard = get_leaderboard("82a9b8d8-60cf-47b9-81e1-36779aa13c20", 1, 10)

print(leaderboard)


if __name__ == '__main__':
    app.run(debug=True)