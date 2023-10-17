from ghapi.all import GhApi
from datetime import datetime, timedelta
from pprint import pprint

api = GhApi(owner='advanced-security-demo')

for alert in api.code_scanning.list_alerts_for_repo(repo="bertelsmann-demo", state="open"):
    pprint(alert)   