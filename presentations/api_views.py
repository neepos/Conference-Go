from django.http import JsonResponse
from .models import Presentation
from events.models import Conference
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "title"
    ]

    def get_extra_data(self, o):
        return {"status": o.status.name}


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.filter(conference=conference_id)
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Conference does not exist"},
                status=400,
            )
        presentation = Presentation.objects.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False
        )
    

@require_http_methods(["GET", "DELETE", "PUT"])
def api_show_presentation(request, id):

    if request.method == "DELETE":
        count,  = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": (count > 0)})

    elif request.method == "PUT":
        presentation = json.loads(request.body)
        presentation["conference"] = (
            Conference.objects.get(
                name=(presentation["conference"]["name"])
            )
        )
        Presentation.objects.filter(id=id).update(**presentation)

    presentation = Presentation.objects.get(id=id)
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False
    )
