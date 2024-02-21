import json

from django.http import HttpResponse, StreamingHttpResponse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from rest_framework import status, serializers, viewsets

from lobby.forms import RoomForm
from lobby.models import Rooms
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'  # Alternatively, specify the fields you want to include explicitly


class CreateRoomAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/lobby_form.html'

    def get(self, request, *args, **kwargs):
        html_to_string = render_to_string(self.template_name, {'form': RoomForm(), 'field_name': 'room_name'})
        return HttpResponse(html_to_string)

    def post(self, request, *args, **kwargs):
        form = RoomForm(request.data)
        if form.is_valid():
            room = form.save()
            room.add_user_to_room(self.request.user)
            Rooms.update_rooms()
            index_url = reverse_lazy('room', args=[room.room_name])
            return HttpResponse(headers={
                'HX-Redirect': index_url,
            })
        else:
            html_to_string = render_to_string(self.template_name, {'form': form})
            return HttpResponse(html_to_string)

    @staticmethod
    def room_added():
        return HttpResponse(
            status=status.HTTP_201_CREATED,
            headers={
                'success': True,
            }
        )


class RoomListAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/lobby_room_partial_update.html'

    def get(self, request):
        queryset = Rooms.objects.all()
        html_content = render_to_string('api/lobby_room_partial_update.html', {'rooms': queryset})
        return HttpResponse(html_content)

