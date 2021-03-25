import time
import random
from instagram_private_api import (Client, __version__ as client_version)
from db_actions import db_Add_Row, db_Get_Data, db_Edit_Row
from settings.db import ig_pass, ig_user


def save_followers(results, count: int, new: int):
    count_ = 0
    new_ = 0
    data = {}
    data['table'] = 'user'
    data['is_checked'] = False
    for i in results.get('users', []):
        data['user_name'] = i['username']
        data['user_id'] = i['pk']
        count_ += 1
        new_ += db_Add_Row(data)

    # with open(f"db/followers/{username}.csv", '+a') as file:
    #     for i in results.get('users', []):
    #         file.write(f"{i['pk']},{i['username']}\n")
    #         count_ += 1
    print(f"Batch: {count_}  New: {new_}  Total: {new+new_}/{count+count_}")
    return count+count_, new+new_

def check(id: int):
    data = {}
    data['table'] = 'poi'
    data['id'] = id
    # data['is_checked'] = 1
    data['got_followers'] = 1
    db_Edit_Row(data)


def get_followers(api: Client, user_id: int = None, following=False, max_count: int = None):
    print('\nClient version: {0!s}'.format(client_version))
    print("Getting Followers")
    if not user_id:
        user_id = db_Get_Data(
            "SELECT poi_id FROM poi WHERE got_followers = 0 AND is_private = 0 AND note = 'dj'", fetchone=True)
        user_id = user_id[0] if user_id else user_id

    # user_info = api.user_info(user_id)
    # user_id = user_info['user']['pk']

    # if not user_info['user']['is_private']:
    if user_id:
        try:
            # print('Not Private')
            count = 0
            new = 0
            rank = api.generate_uuid()

            if following:
                results = api.user_following(user_id, rank)
            else:
                results = api.user_followers(user_id, rank)

            count, new = save_followers(results, count, new)
            next_max_id = results.get('next_max_id')
            pause = random.randint(2, 4)
            print(f"Sleep for {pause}s")
            while next_max_id:
                if max_count:
                    if count >= max_count:       # get only first n or so
                        break
                if following:
                    results = api.user_following(
                        user_id, rank_token=rank, max_id=next_max_id)
                else:
                    results = api.user_followers(
                        user_id, rank_token=rank, max_id=next_max_id)

                count, new = save_followers(results, count, new)
                next_max_id = results.get('next_max_id')

                pause = random.randint(3, 6)
                print(f"Sleep for {pause}s")
                time.sleep(pause)

            if not following:
                get_followers(api, user_id=user_id, following=True)
            
            check(user_id)            

        except Exception as e:
            print(e)
            with open('logs/last.txt', '+a') as file:
                file.write(str(time.localtime))
                file.write(f"user_id = {user_id}")
                file.write(f"count = {count}")
                file.write(f"rank = {rank}")
                file.write(f"next_max_id = {next_max_id if next_max_id else None}\n\n")


if __name__ == '__main__':
    api = Client(ig_user, ig_pass)
    # get_followers(api, 37348821, max_count=1) # zo_rezo
    # get_followers(api, 192288545, False, 1)  # djmmadrid
    get_followers(api)

