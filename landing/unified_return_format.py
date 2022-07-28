import json

def format_return_value(status_code, callout_func_name, msg):
    uni = json.dumps({'status_code':status_code, 'callout_func_name': callout_func_name, 'msg': msg})
    return uni