from vk_api import VkApi

access_token= "vk1.a.6GBvUbFf44fl2uzHdKfIp2LCYsAFdWhnqTTiIIbXChJd-IGZk0n51dLrUWHSJPt7UGAvPZ9xJFalwQYLv8JPS6fVqxnBVFD5SMv8WnlHJnuakwTxYmXoflyLbgD7-9eHBIQysM6QBVM9oERw2sDzuLpF1WLHc7BbNz31sAg95Bz2QyHv8EAiik6wTgbDF_ET"


session = VkApi(token=access_token)
vk = session.get_api()

def get_group_members():
    return vk.groups.getMembers(group_id='dtf', fields='photo_max_orig, bdate', count=100)
