from __future__ import print_function

import datetime
import csv
import os.path
import subprocess
import httplib2
import googleapiclient.discovery as discovery


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z' 
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=20, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        calendar_id = "agishanl01@gmail.com"

        event = {
            "summary": "",
            "location": "",
            "description": "",
            "colorId": "",
            "start": {
                "dateTime": "2023-10-03T08:34:25.332069+01:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": "2023-10-03T08:34:25.332069+01:00",
                "timeZone": "Europe/London",
            },
            "reccurence": [
                "RRULE:FREQ=DAILY;COUNT=3"
            ],
            "attendees": [
                {"email": "coolsbug25@gmail.com"}
            ]
        }

        keys_to_update = ["summary", "location", "description", "colorId", "attendees"];

        csv_input = input("What is the name of your csv file?\n")

        dict = {}

        if csv_input is None:
            for key in keys_to_update:
                user_input = input(f"Enter new value for '{key}': ")
                if key.strip().lower() == "attendees" :
                    attendees = [{"email": user_input}]
                    event[key] = attendees
        else:
            with open(f'{csv_input}', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                first_row = next(csv_reader)
                second_row = next(csv_reader)
                for key, value in zip(first_row, second_row):
                    dict[key] = value
        
    
        event = service.events().insert(calendarId="primary", body=event).execute();
        print(f"Event created {event.get('htmlLink')}")

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()

