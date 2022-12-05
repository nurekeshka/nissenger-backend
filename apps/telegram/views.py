from rest_framework.response import Response
from rest_framework.request import Request
from apps.telegram.models import bot
from rest_framework import views
from apps.timetable import utils


class NotifyAdmins(views.APIView):
    @utils.json
    def post(self, request: Request, json: dict, *args, **kwargs):
        message = json['message']
        bot.send_to_admins(message)
        return Response()
