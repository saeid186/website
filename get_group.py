import requests
import sys


# def get_groups(username):
#     url = f"https://yax.mobinnet.net/rest/api/2/user?username={username}&expand=groups"
#
#     payload = {}
#     headers = {
#         'Authorization': 'Basic bS5uYXNpcmk6UmFkaXVzQDE4Ng==',
#         'Cookie': 'JSESSIONID=jira06~67319EE1CC848A478ED9C6AF019E4567; atlassian.xsrf.token=B0EB-WX8T-AIR7-0FSH_da76e410d5de1e946c757c70cbd293b7721dadba_lin'
#     }
#
#     resp = requests.request("GET", url, headers=headers, data=payload)
#     return resp
#
#
# def groups_to_list(user_resp):
#     user_groups = []
#     for i in range(len(user_resp.json()['groups']['items'])):
#         if "Reporting" not in user_resp.json()['groups']['items'][i]['name']:
#             user_groups.append(user_resp.json()['groups']['items'][i]['name'])
#     return user_groups
#
#
# first_user_groups = groups_to_list(get_groups("m.nasiri"))
# second_user_groups = groups_to_list(get_groups("ba.dehghani"))
#
#
# print(list(set(first_user_groups) - set(second_user_groups)))
# print(list(set(second_user_groups) - set(first_user_groups)))


