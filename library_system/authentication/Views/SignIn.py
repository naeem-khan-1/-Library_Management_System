from django.shortcuts import render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User
from authentication.Serializers.SignInSerializer import SignInSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from library_app.Serializers.RacksViewSerializer import RacksListSerializer, ShowRacksSerializer
from library_app.models import Racks


class SignInPage(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('login.html')
    template_name = template.origin.name
    serializer_class = SignInSerializer

    def get(self, request):

        return Response({'profiles': 'abc'})


class SignIn(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            user.token = get_token(user.username)
            user.save()

            user_obj = {
                "id": user.id,
                "token": user.token,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "is_admin": user.is_admin,
            }

            if user.is_admin:
                racks = Racks.objects.all()
                serializer = RacksListSerializer(racks, many=True)
                return render(request, 'Add_Rack_New.html', {"user_data": user_obj, "data": serializer.data})
            else:
                rack = Racks.objects.all()
                serializer = ShowRacksSerializer(rack, many=True)
                return render(request, 'show_racks.html', {"user_data": user_obj, "data": serializer.data})

        return render(request, 'login.html')


def get_token(username):
    token, created = Token.objects.get_or_create(user=User.objects.get(username=username))
    token.delete()
    token, created = Token.objects.get_or_create(user=User.objects.get(username=username))

    api_token = "Token " + token.key

    return api_token
