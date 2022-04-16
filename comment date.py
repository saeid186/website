import requests
from requests.auth import HTTPBasicAuth
import json


keys = "'WO-19830','WO-19826','WO-19799','WO-19769','WO-19761','WO-19723','WO-19698','WO-19689','WO-19688','WO-19687','WO-19633','WO-19622','WO-19604','WO-19597','WO-19596','WO-19582','WO-19581','WO-19579','WO-19522','WO-19516','WO-19504','WO-19503','WO-19412','WO-19400','WO-19381','WO-19380','WO-19379','WO-19368','WO-19343','WO-19311','WO-19306','WO-19249','WO-19213','WO-19208','WO-19207','WO-19177','WO-19176','WO-19171','WO-19168','WO-19131','WO-19119','WO-19108','WO-19101','WO-19079','WO-19057','WO-19054','WO-19044','WO-19042','WO-19041','WO-19035','WO-19033','WO-18995','WO-18976','WO-18960','WO-18944','WO-18942','WO-18935','WO-18932','WO-18930','WO-18929','WO-18922','WO-18907','WO-18899','WO-18897','WO-18891','WO-18873','WO-18865','WO-18845','WO-18843','WO-18838','WO-18835','WO-18834','WO-18828','WO-18827','WO-18822','WO-18817','WO-18802','WO-18786','WO-18779','WO-18778','WO-18760','WO-18744','WO-18718','WO-18716','WO-18711','WO-18710','WO-18705','WO-18628','WO-18604','WO-18601','WO-18600','WO-18577','WO-18573','WO-18569','WO-18566','WO-18551','WO-18550','WO-18535','WO-18532','WO-18528','WO-18523','WO-18513','WO-18508','WO-18507','WO-18493','WO-18485','WO-18478','WO-18477','WO-18465'"
url = f"https://yax.mobinnet.net/rest/api/2/search?jql=key%20in%20({keys})&fields=comment&maxResults=200"

auth = HTTPBasicAuth("yax", "mnmn4700Wd7")

headers = {
   "Accept": "application/json"
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)

# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# for i in range(len(len(response.json()['groups']['items']))):
print(len(response.json()['issues']))
print(response.json())

for i in range(len(response.json()['issues'])):
   print(response.json()['issues'][0]['key'])
   print(response.json()['issues'][0]['fields']['comment']['comments'][0])

