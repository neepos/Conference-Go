from django.http import JsonResponse
from .models import Attendee
from events.models import Conference
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = ["name"]


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceListEncoder(),
    }


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.object.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )
        
        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False
        )

def api_show_attendee(request, id):
    """
    Returns the details for the Attendee model specified
    by the id parameter.
    """
    attendee = Attendee.objects.get(id=id)
    return JsonResponse(
        {
            "email": attendee.email,
            "name": attendee.name,
            "company_name": attendee.company_name,
            "created": attendee.created,
            "conference": {
                "name": attendee.conference.name,
                "href": attendee.conference.get_api_url(),
            },
        }
    )
