from django.http import JsonResponse

from .models import Attendee


def api_list_attendees(request, conference_id):
    """
    Lists the attendees names and the link to the attendee
    for the specified conference id.

    """
    attendees = [
        {
            "name": a.name,
            "href": a.get_api_url(),
        }
        for a in Attendee.objects.filter(conference=conference_id)
    ]
    return JsonResponse({"attendees": attendees})


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
