from ghapi.all import GhApi
from datetime import datetime, timedelta

api = GhApi(owner='advanced-security-demo')

alert_count = 0
total_time_to_remediate_seconds = 0

for alert in api.code_scanning.list_alerts_for_repo(repo="hm-demo", state="fixed"):
    time_to_remediate = datetime.strptime(
        alert.fixed_at,  "%Y-%m-%dT%XZ") - datetime.strptime(alert.created_at,  "%Y-%m-%dT%XZ")
    total_time_to_remediate_seconds += time_to_remediate.total_seconds()
    alert_count += 1

print("MTTR: " + str(timedelta(seconds=total_time_to_remediate_seconds/alert_count)))
print("total_alerts: " + str(alert_count))
