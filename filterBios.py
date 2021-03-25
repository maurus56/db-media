import timing
import time
import random
import hashlib
import string
import re
import gc
import threading

import logging
from logging.config import dictConfig
from settings.logger import logging_config

from instagram_private_api import (
    Client as appClient, ClientError as appClientError, __version__ as client_version)  # app
from instagram_web_api import (
    Client as webClient, ClientError as webClientError)    # web

from db_actions import db_Add_Row, db_Edit_Row, db_Get_Data, print_stats
from settings.db import *
import proxy.proxy_handler as proxy_handler


dictConfig(logging_config)
logMyScrapper = logging.getLogger('MyScrapper')
# logMain = logging.getLogger(__name__)

# logMyScrapper.debug('debug')
# logMyScrapper.info('info')
# logMyScrapper.warning('warning')
# logMyScrapper.error('error')
# logMyScrapper.critical('critical')

class MyClient(webClient):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()


class MyScrapper():
    def __init__(self):
        self.done = False

    # def __thread_pop(self):
    #     list = []

    #     threadlock = threading.Lock()
    #     with threadlock:
    #         a = list.pop(0)

    def _parse_user_bio(self, bio: str):
        words = [
            "([dD][jJ])",       # dj
            "([Mm]anage)",      # managers
            "([mM]usic)",       # musician
            "([dD]ance)",       # dancers
            "([bB]ailar)",      # bailarines
            "([cC]h?oreogra)",  # coreografos
            "([aA]cade)",       # academia
            "([pP]rod)"         # droductores
        ]
        a = [x.group().lower() for x in re.finditer(r"|".join(words), bio)]
        return ' '.join(list(set(a)))

    def _get_poi(self, api, web: bool):
        where = "is_checked = 0 AND error = 0"
        user = db_Get_Data(
            f"SELECT user_id, user_name FROM user WHERE {where}", True)
        if not user:
            logMyScrapper.critical("db_error: no user found with condition")
            raise Exception
        try:
            if web:
                user_info = api.user_info2(user[1])     # web
                business = 'is_business_account'
            else:
                user_info = api.user_info(user[0])      # app
                user_info = user_info['user']           # app
                business = 'is_business'

        except (appClientError, webClientError) as e:
            logMyScrapper.error(f"{user}::client_error: {e}")
            data = {}
            data['table'] = 'user'
            data['id'] = user[0]
            data['is_checked'] = 0
            data['error'] = 1
            db_Edit_Row(data)
            return 1

        except Exception as e:
            logMyScrapper.critical(f"{user}::connection_error: {e}")
            # data = {}
            # data['table'] = 'user'
            # data['id'] = user[0]
            # data['is_checked'] = 0
            # data['error'] = 1
            # db_Edit_Row(data)
            return 10

        match = self._parse_user_bio(user_info['biography'])
        if match or user_info[business]:
            logMyScrapper.info(f"{user}::match: {match}")
            data = {}
            data['table'] = 'poi'
            data['poi_id'] = user[0]
            data['poi_name'] = user_info['username']
            data['is_private'] = user_info['is_private']
            data['is_business'] = user_info[business]
            data['is_checked'] = 0
            data['note'] = match if match else ''
            data['poi_mail'] = ''
            data['poi_phone'] = ''
            data['bool'] = 0
            if user_info[business] and not web:
                # data['poi_mail'] = 'none'
                # data['poi_phone'] = 'none'
                data['bool'] = 1
                if user_info['public_email']:
                    if len(user_info['public_email']) > 45:
                        data['poi_mail'] = 'too_long'
                    else:
                        data['poi_mail'] = user_info['public_email']
                if user_info['public_phone_number']:
                    data['poi_phone'] = f"(+{user_info['public_phone_country_code']}) {user_info['public_phone_number']}"
            # print(data)
            
            db_Add_Row(data)
        else:
            logMyScrapper.info(f"{user}")

        data = {}
        data['table'] = 'user'
        data['id'] = user[0]
        data['is_checked'] = 1
        db_Edit_Row(data)
        return 0

    def _get_contact_info(self, api: appClient):
        where = "error = 0 and bool = 0 and poi_phone = '' and poi_mail = '' and is_business = 1"
        user = db_Get_Data(
            f"SELECT poi_id, poi_name FROM poi WHERE {where}", True)
        if not user:
            logMyScrapper.critical("db_error: no user found with condition")
            raise Exception

        try:
            user_info = api.user_info(user[0])
            user_info = user_info['user']
        # print(int(user_info['is_business']))
        except (appClientError, webClientError) as e:
            logMyScrapper.error(f"{user}::client_error: {e}")
            data = {}
            data['table'] = 'poi'
            data['id'] = user[0]
            data['error'] = 1
            db_Edit_Row(data)
            return 1

        except Exception as e:
            logMyScrapper.critical(f"{user}::connection_error: {e}")
            # data = {}
            # data['table'] = 'poi'
            # data['id'] = user[0]
            # data['error'] = 1
            # db_Edit_Row(data)
            return 10

        data = {}
        data['table'] = 'poi'
        data['id'] = user[0]
        data['bool'] = 1
        # data['poi_mail'] = 'none'
        # data['poi_phone'] = 'none'
        data['is_business'] = int(user_info['is_business'])
        print(user_info['is_business'])
        if user_info['is_business']:
            if user_info['public_email']:
                if len(user_info['public_email']) > 45:
                    data['poi_mail'] = 'too_long'
                else:
                    data['poi_mail'] = user_info['public_email']
                    print(user_info['public_email'])
            if user_info['public_phone_number']:
                phone = f"(+{user_info['public_phone_country_code']}) {user_info['public_phone_number']}"
                data['poi_phone'] = phone
                print(phone)
        # print(data)
        logMyScrapper.info(f"""{user}::contact: {data['poi_mail'] if data['poi_mail'] else ''} | {data['poi_phone'] if data['poi_phone'] else ''}""")
        db_Edit_Row(data)
        return 0

    def _update_poi_tags(self, api: MyClient):
        where = "bool = 0 and poi_phone != '' and poi_mail != ''"
        user = db_Get_Data(
            f"SELECT poi_id, poi_name FROM poi WHERE {where}", True)
        if not user:
            logMyScrapper.critical("db_error: no user found with condition")
            raise Exception

        try:
            user_info = api.user_info2(user[1])     # web
            business = 'is_business_account'

        except (appClientError, webClientError) as e:
            logMyScrapper.error(f"{user}::client_error: {e}")
            data = {}
            data['table'] = 'poi'
            data['id'] = user[0]
            data['error'] = 1
            db_Edit_Row(data)
            return 1

        except Exception as e:
            logMyScrapper.critical(f"{user}::connection_error: {e}")
            # data = {}
            # data['table'] = 'poi'
            # data['id'] = user[0]
            # data['error'] = 1
            # db_Edit_Row(data)
            return 10

        match = self._parse_user_bio(user_info['biography'])
        print(match)
        if match:
            data = {}
            data['table'] = 'poi'
            data['pid'] = user[0]
            data['note'] = match if match else ''
            db_Add_Row(data)
        return 0

    def _get_proxy_handler(self):
        return proxy_handler._return_proxyHandler()

    def _get_user_agent(self):
        return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'

    def _get_client(self, app: bool = False, new_id=False):
        if app:
            return appClient(ig_user, ig_pass)
        else:
            if new_id:
                return MyClient(auto_patch=True, drop_incompat_key=True,
                                proxy_handler=self._get_proxy_handler(),
                                user_agent=self._get_user_agent())
            return MyClient(auto_patch=True, drop_incompat_key=True)

    def run_web_poi(self, count: int = 1, stats: bool = False):
        logMyScrapper.info(f"API Version: {client_version}")
        api = self._get_client()
        error = 0
        for i in range(1, count + 1):
            print(f"\nCount: {i}")
            e = self._get_poi(api, web=True)
            # e = self._get_contact_info(app_api)

            error += e
            if error >= 10:
                break

            if i % 1000 == 0:
                del api
                gc.collect()
                elapsed = timing.secondsToStr(time.time() - timing.start)
                timing.log('1000 mark, Wait 60m', elapsed=elapsed)
                time.sleep(random.randint(3400, 3600))
                api = self._get_client()
            elif i % 150 == 0:
                del api
                gc.collect()
                elapsed = timing.secondsToStr(time.time() - timing.start)
                timing.log('150 mark, Wait 10m', elapsed=elapsed)
                time.sleep(random.randint(600, 650))
                api = self._get_client()
            elif i % 50 == 0:
                del api
                gc.collect()
                elapsed = timing.secondsToStr(time.time() - timing.start)
                timing.log('50 mark, Wait 2ms', elapsed=elapsed)
                time.sleep(random.randint(120, 150))
                api = self._get_client()
            else:
                sleep = random.randint(5, 10)
                print(f"Sleep: {sleep}s")
                time.sleep(sleep)

        if stats:
            self.return_stats()

    def return_stats(self):
        print_stats()


if __name__ == '__main__':
    import subprocess
    logMyScrapper.info('----- STARTED NEW INSTANCE -----')
    lastError = subprocess.check_output(['tail', '-1', 'logs/error.log'])
    if b'connection_error' in lastError:
        exit()

    time.sleep(random.randint(4,40))
    test = MyScrapper()
    test.run_web_poi(count=1, stats=False)
    # test.run_web_poi(count=random.randint(35, 45), stats=True)
    # test.return_stats()
