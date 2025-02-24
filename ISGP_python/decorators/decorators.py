
from user_context import current_user_id
from redis_orm.redis_client import get_algorithim_status


class StopException(Exception):
    pass

def check_stop(func):
    def wrapper(*args, **kwargs):
        user_id = current_user_id.get()
        print('user id in wrapper is: ' + str(user_id))
        abort = get_algorithim_status(user_id)
        #print('abort is:' + str(abort))
        if abort is False:
                return None
        return func(*args, **kwargs)
    return wrapper


def check_stop_factory(user_id):
    #print('user id in wrapper is: ' + str(user_id))
    def check_stop(func):
        def wrapper(*args, **kwargs):
            
            abort = get_algorithim_status(user_id)
            if abort is False:
                return None
            return func(*args, **kwargs)
        return wrapper
    return check_stop



