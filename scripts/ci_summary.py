"""Print verified job and step results from the public GitHub Actions API."""
import json
import sys
from datetime import datetime
from urllib.request import Request, urlopen

repo = "Tenma24/cars-dealership-capstone"
run_id = sys.argv[1]


def fetch(path):
    request = Request("https://api.github.com/repos/" + repo + path,
                      headers={"User-Agent": "capstone-evidence"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


run = fetch("/actions/runs/" + run_id)
print("GitHub Actions: " + run["name"])
print("Run ID: " + str(run["id"]))
print("URL: " + run["html_url"])
print("Commit: " + run["head_sha"])
print("Status: " + run["status"])
print("Conclusion: " + str(run["conclusion"]))
for job in fetch("/actions/runs/" + run_id + "/jobs")["jobs"]:
    print("\nJob: " + job["name"])
    print("Job ID: " + str(job["id"]))
    print("Conclusion: " + str(job["conclusion"]))
    if job["completed_at"]:
        duration = (datetime.fromisoformat(job["completed_at"]) -
                    datetime.fromisoformat(job["started_at"])).total_seconds()
        print("Duration: " + str(int(duration)) + " seconds")
    for step in job["steps"]:
        print("  " + step["name"] + ": " + str(step["conclusion"]))
