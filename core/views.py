from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
import os
import google_apis_oauth
from googleapiclient.discovery import build
# Create your views here.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'
SCOPES = ['https://www.googleapis.com/auth/calendar']
JSON_FILEPATH = os.path.join(os.getcwd(),'client_id.json')

def GoogleCalendarInitView(request):
    oauth_url = google_apis_oauth.get_authorization_url(JSON_FILEPATH,SCOPES,REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)

def GoogleCalendarRedirectView(request):
        context ={}
        credentials=google_apis_oauth.get_crendentials_from_callback(request,JSON_FILEPATH,SCOPES,REDIRECT_URI)
        stringified_token = google_apis_oauth.stringify_credentials(credentials)
        creds,refreshed = google_apis_oauth.load_credentials(stringified_token)
        service =build('calendar','v3',credentials=creds)
        page_token = None
        while True:
            events_result = service.events().list(
            calendarId ='primary',pageToken =page_token).execute()
            print(events_result['items'])
            page_token = events_result.get('nextPageToken')
            if not page_token:
                break
        return HttpResponse(str(events_result))