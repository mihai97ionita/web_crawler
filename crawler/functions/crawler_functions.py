import json
import os

import redis

from crawler.concurrency.FutureCollector import FutureCollector
from crawler.factory.chrome_driver_factory import create_web_driver
from crawler.factory.redis_connection_factory import create_redis_connection
from crawler.functions.parse_functions import future_of_functions, future_of_function, find_university

# 10 minutes
cache_expiry_time = 10 * 60 * 1000


def crawler_and_parse(parse_function, parse_url):
    try:
        return crawler_and_parse_with_cache(parse_function, parse_url)
    except:
        return parse_function(parse_url)


def crawler_and_parse_with_cache(parse_function, parse_url):
    redis_connection = create_redis_connection()
    crawled_page = get_crawled_page_from_redis(redis_connection, parse_url)
    if crawled_page:
        return crawled_page
    else:
        crawled_page = parse_function(parse_url)
        set_crawled_page_in_redis(redis_connection, parse_url, crawled_page)
        return crawled_page


def get_crawled_page_from_redis(redis_connection, key):
    value = redis_connection.get(key)
    if value:
        return json.loads(value)
    else:
        None


def get_value_from_redis(redis_connection, key):
    return redis_connection.get(key)


def set_crawled_page_in_redis(redis_connection, key, crawled_page):
    json_crawled_page = json.dumps(crawled_page)
    set_value_in_redis(redis_connection, key, json_crawled_page)


def set_value_in_redis(redis_connection, key, value):
    redis_connection.mset({key: value})
    redis_connection.pexpire(key, cache_expiry_time)


def filter_by_info_selected(crawled_page, selected_info):
    crawled_dict_info = {}
    for k in crawled_page:
        if k in selected_info:
            crawled_dict_info[k] = crawled_page[k]
    return crawled_dict_info
