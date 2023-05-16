from django.http import JsonResponse
from .models import Attendee
from .models import ConferenceVO
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json

class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


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
        "conference": ConferenceVODetailEncoder(),
    }


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_vo_id=None):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_vo_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference_href = f'/api/conferences/{conference_vo_id}/'
            conference = ConferenceVO.objects.get(import_href=conference_href)
            content["conference"] = conference
        except ConferenceVO.DoesNotExist:
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

@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = ConferenceVO.objects.get(["name"])
                content["name"] = conference
        except ConferenceVO.DoesNotExist:
            return JsonResponse(
                {"message": "No associated conference"},
                status=400,
            )
        Attendee.objects.filter(id=id).update(**content)
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )



    # if request.method == "DELETE":
    #     count, _ = Attendee.objects.filter(id=id).delete()
    #     return JsonResponse({"deleted": count > 0})
    
    # elif request.method == "PUT":
    #     attendee = json.loads(request.body)
    #     attendee["conference"] = (
    #         Conference.objects.get(
    #             name=(attendee["conference"]["name"])
    #         )
    #     )
    #     Attendee.objects.filter(id=id).update(**attendee)
    
    # attendee = Attendee.objects.get(id=id)
    # return JsonResponse(
    #         attendee,
    #         encoder=AttendeeDetailEncoder,
    #         safe=False,
    # )

