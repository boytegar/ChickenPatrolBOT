from datetime import datetime
import json
import os
import random
import sys
from urllib.parse import parse_qs, unquote
import time

from chickenpatrol import ChickenPatrol

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_query():
    try:
        with open('chickenpatrol_query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("Failed find chickenpatrol_query.txt ")
        return [  ]
    except Exception as e:
        print("Failed find chickenpatrol_query.txt ", str(e))
        return [  ]

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def get(id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None
        return tokens[str(id)]

def save(id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r[{now}] | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("\nWaiting Done, Starting....\n")

def main():
    auto_buy = input("auto buy chicken y/n  : ").strip().lower()
    # auto_game = input("auto play game  y/n  : ").strip().lower()
    while True:
        start_time = time.time()
        delay = 5*3651
        clear_terminal()
        queries = load_query()
        sum = len(queries)
        chicken = ChickenPatrol()
        for index, query in enumerate(queries, start=1):
            users = parse_query(query).get('user')
            print_(f"[SxG]======== Account {index}/{sum} | {users.get('username','')} ========[SxG]")
            data_auth = chicken.auth(query)
            if data_auth is not None:
                token = data_auth.get('access_token')
            
                data_user = chicken.get_user(token)
                if data_user is not None:
                    user = data_user.get('user',{})
                    airdropPoint = user.get('airdropPoint',0)
                    usdt = user.get('usdt',0)
                    tap = user.get('tap',0)
                    print_(f"Balance : {usdt} USDT | {airdropPoint} TCN")
                    if auto_buy == 'y':
                        if airdropPoint >= 1000:
                            print_(f"Buying Chicken...")
                            chicken.buy_tcn(token)
                    chick = user.get('chick',[])
                    for item in chick:
                        print_(f"Chick Army : Rank {item.get('rank')}")
                    data_tap = chicken.tap(token=token, tap=tap)
                    if data_tap is not None:
                        usdt = data_tap.get('usdt')
                        airdrop = data_tap.get('airdrop')
                        print_(f"Tap : {usdt} USDT | {airdrop} TCN")
                    
                    task = data_user.get('task')
                    taskOne = task.get('taskOne')
                    if not taskOne:
                        chicken.clear_task(token, 'joinchannel')
                    taskTwo = task.get('taskTwo')
                    if not taskTwo:
                        chicken.clear_task(token, 'joinchat')
                    taskThree = task.get('taskThree')
                    if not taskThree:
                        chicken.clear_task(token, 'followx')
                    taskFour = task.get('taskFour')
                    taskFive = task.get('taskFive')
                    if not taskFive:
                        chicken.clear_task(token, 'followxbinance')
                    taskSix = task.get('taskSix')

        
        end_time = time.time()
        delays = delay - (end_time - start_time)
        print_delay(delays)

if __name__ == "__main__":
    main()

                



