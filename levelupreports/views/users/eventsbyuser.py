from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all

class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            db_cursor.execute("""
                SELECT 
                    *
                FROM
                    EVENTS_BY_USER
                """)
            dataset = dict_fetch_all(db_cursor)
            events_by_user = []
            for row in dataset:
                event = {
                    'description': row['description'],
                    'date': row['date'],
                    'time': row['time'],
                    'organizer': row['organizer_id'],
                    'game': row['game_id']
                }
                user_dict = None
                for user_event in events_by_user:
                    if user_event['organizer_id'] == row['organizer_id']:
                        user_dict = user_event
                if user_dict:
                    user_dict['events'].append(event)
                else:
                    events_by_user.append({
                        "organizer_id": row['organizer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })
        template = 'users/list_with_events.html'
        context = {
            "userevent_list": events_by_user
        }
        return render(request, template, context)