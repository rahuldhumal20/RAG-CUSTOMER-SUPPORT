from datetime import datetime

def escalate_to_human(query):

    with open(
       "human_review_queue.txt",
       "a",
       encoding="utf-8"
    ) as file:

        file.write(
          f"""
Time: {datetime.now()}
Query: {query}
Status: Pending Human Review
------------------------
"""
        )

    return f"""
Escalation Triggered.

Ticket added to Human Review Queue.

Support team will review:
{query}
"""