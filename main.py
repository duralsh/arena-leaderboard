from config import get_db_config
from db_driver import DataBaseDrivers
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

db_config = get_db_config()
db_drivers = DataBaseDrivers(db_config=db_config)

query_time = datetime(2024, 3, 10, 15, 9, 10, tzinfo=timezone.utc)  ## BAD NAMING, change later

ticket_price = 0.1 * 1e18

buy_weigts = db_drivers.query_buy_weight(query_time)



def get_leaderboard(user_id, page_number, limit_per_page):
    start_index = (page_number - 1) * limit_per_page
    end_index = start_index + limit_per_page
    leaderboard = {
        "users": [],
        "currentUser": {}
    }

    for indice, record in enumerate(buy_weigts[start_index:end_index], start=start_index):
        trader_id, cnt, twitter_handle = record[1], int(record[0]), record[2]
        user_info = {
            "userId": trader_id,
            "twitterHandle": twitter_handle,
            "tickets": int(cnt / ticket_price),
            "rank": indice + 1
        }
        leaderboard["users"].append(user_info)

        if user_id == trader_id:
            leaderboard["currentUser"] = user_info

    return leaderboard


@app.route('/api/leaderboard/<user_id>', methods=['GET'])
def leaderboard_api(user_id):
    page_number = int(request.args.get('page', 1))
    limit_per_page = int(request.args.get('limit', 10))

    if page_number <= 0:
        return jsonify({"error": "Page number must be a positive integer."}), 400

    leaderboard = get_leaderboard(user_id, page_number, limit_per_page)

    return jsonify(leaderboard)


leaderboard = get_leaderboard("5dd3663e-4a9e-4e92-b4dd-09a45b7b2f2c", 2, 10)

print(leaderboard)


if __name__ == '__main__':
    app.run(debug=True)