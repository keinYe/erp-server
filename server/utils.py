from .module import redis_client
import logging
import time

logger = logging.getLogger(__name__)

def mark_online(user):
    user_id = str(user.id).encode('utf-8')
    now = int(time.time())
    expires = now + (5 * 60) + 10
    all_users_key = "online-users/%d" % (now // 60)
    user_key = "user-activity/%s" % user_id
    p = redis_client.pipeline()
    p.sadd(all_users_key, user_id)
    p.set(user_key, now)
    p.expireat(all_users_key, expires)
    p.expireat(user_key, expires)
    p.execute()

def get_online():
    current = int(time.time()) // 60
    minutes = range(5)
    users = redis_client.sunion(
        ["online-users/%d" % (current - x) for x in minutes]
    )

    return len([int(u.decode('utf-8')) for u in users])

def mark_dyn_data(id, data):
    user_id = str(id).encode('utf-8')
    data = str(data).encode('utf-8')
    expires = int(time.time()) + 60
    data_key = "dyn_data/%s" % user_id
    logger.info("id = {}, data = {}, expires ={}, data_key = {}".format(user_id, data, expires, data_key))
    p = redis_client.pipeline()
    p.set(data_key, data)
    p.expireat(data_key, expires)
    p.execute()

def get_dyn_data(id):
    user_id = str(id).encode('utf-8')
    data_key = "dyn_data/%s" % user_id
    data = redis_client.get(data_key)
    logger.info("id = {}, data_key = {}, data = {}".format(user_id, data_key, data))

    if data:
        return int(data)
    return None
