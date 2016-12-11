from google.cloud import bigquery
import json
import re

ALLOWED_CHARS = ' .!:/'

TIMEOUT_MS = 10000
PAGESIZE = 100
SQL_QUERY = 'SELECT payload FROM (          \
TABLE_DATE_RANGE([githubarchive:day.],       \
    DATE_ADD(CURRENT_TIMESTAMP(), -1, "DAY"),\
    CURRENT_TIMESTAMP()                      \
)) WHERE type = "PushEvent" LIMIT 100'  # careful what you wish for!


def query_githubarchive():
    client = bigquery.Client(project="commit-simulator")
    query = client.run_sync_query(SQL_QUERY)
    query.timeout_ms = TIMEOUT_MS
    query.max_results = PAGESIZE
    query.run()
    
    assert query.complete

    rows = query.rows
    token = query.page_token
    
    payloads = []
    
    while True:
        for row in rows:
            payloads.append(row[0])
        if token is None:
            break
        rows, total_count, token = query.fetch_data(page_token=token)
    
    return payloads
    
    
def is_valid_char(c):
    return c.isalnum() or c in ALLOWED_CHARS

def sanitize_message(message):
    message = message.strip()
    message = message.replace('\n', ' ')
    message = ''.join(filter(is_valid_char, message))
    return message


def decode_payloads(payloads):
    """ Returns a set of commit messages from JSON PushEvent objects """
    
    push_events = [json.loads(p) for p in payloads]
    commit_msgs = set()
    for event in push_events:
        for c in event['commits']:
            message = sanitize_message(c['message'])
            commit_msgs.add(message)

    return commit_msgs
    
    
def query_commits():
    raw_payloads = query_githubarchive()
    print("{0} commits fetched".format(len(raw_payloads)))
    return decode_payloads(raw_payloads)


if __name__ == "__main__":
    query_commits()
