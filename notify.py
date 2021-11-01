#!/usr/bin/env python3
import datetime
import json
import os

import gspread
import requests

USCIS_NOTIFIER_LOG = "1PObXscjQSVnzskL20iQM8JNIlZl5OQi9sa-vopNTLnY"


def get_current_receipt_date():
    resp = requests.get(
        "https://egov.uscis.gov/processing-times/api/processingtime/I-130/CSC",
        headers={
            "referrer": "https://egov.uscis.gov/processing-times/",
        },
    )
    payload = resp.json()
    subtypes = payload["data"]["processing_time"]["subtypes"]
    form_134a_f21 = [s for s in subtypes if s["form_type"] == "134A-F21"][0]
    service_request_date = form_134a_f21["service_request_date"]
    return service_request_date


def notify(msg):
    resp = requests.post(
        "https://api.pushover.net/1/messages.json",
        json={
            "token": os.environ["PUSHOVER_API_KEY"],
            "user": os.environ["PUSHOVER_USER_KEY"],
            "message": msg,
            "title": "USCIS updated receipt date",
        },
    )
    resp.raise_for_status()


def get_uscis_receipt_worksheet():
    sa = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
    gc = gspread.service_account_from_dict(sa)
    sh = gc.open_by_key(USCIS_NOTIFIER_LOG)
    return sh.get_worksheet(0)


def get_previous_receipt_date(wks):
    return wks.get(f"B{wks.row_count}")[0][0]


def log_receipt_date(wks, receipt_date):
    wks.append_row([datetime.datetime.now().isoformat(), receipt_date])


def main():
    wks = get_uscis_receipt_worksheet()
    current = get_current_receipt_date()
    previous = get_previous_receipt_date(wks)
    if current != previous:
        notify(current)
    log_receipt_date(wks, current)


if __name__ == "__main__":
    main()
