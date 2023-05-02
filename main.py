import json
import smtplib
import requests
from pprint import pprint
from dataclasses import dataclass

JOB_URL = "https://app.recruiterbox.com/widget/%s/openings/"
COMPANY_ID = None
KEYWORDS = ["devops", "software", "dev ops"]


def get_jobs(url: str, keywords: str) -> list:
    req = requests.get(url=url)
    jobs = []
    for job in json.loads(req.content):
        for keyword in keywords:
            if keyword.lower() in job["title"].lower():
                jobs.append(job)
                continue
    return [job["title"] for job in jobs]


@dataclass
class Email:
    user: str
    password: str
    to_addrs: str
    from_addr: str


def email_jobs(jobs: list, email: Email):
    smtp_connection = smtplib.SMTP_SSL(
        host="smtp.gmail.com", port=smtplib.SMTP_SSL_PORT
    )
    smtp_connection.login(user=email.user, password=email.password)
    smtp_connection.send_message(
        to_addrs=email.to_addrs, from_addr=email.from_addr, msg=f"Found jobs:\n {jobs}"
    )


def main():
    # list jobs from company that match keywords
    jobs = get_jobs(JOB_URL % COMPANY_ID, KEYWORDS)
    pprint(jobs)


if __name__ == "__main__":
    main()
