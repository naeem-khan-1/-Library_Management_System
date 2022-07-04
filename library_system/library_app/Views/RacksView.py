from django.http import HttpResponseRedirect
from django.shortcuts import render

from library_app.models import Racks, Books
from library_app.Serializers.RacksViewSerializer import RacksListSerializer, RacksSerializer, ShowRacksSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.template import loader
from rest_framework.renderers import TemplateHTMLRenderer
from authentication.BusinessLogic.TokenVarify import is_authenticated_user


class ShowRacksList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('show_racks_new.html')
    template_name = template.origin.name
    serializer_class = ShowRacksSerializer

    def get(self, request):

        search_text = self.request.GET.get('search_text', None)

        if search_text:
            rack = Racks.objects.filter(rack_name__icontains=search_text)
        else:
            rack = Racks.objects.all()

        serializer = ShowRacksSerializer(rack, many=True)

        return Response({"data": serializer.data}, status=200)


class ShowRacksUserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('show_racks.html')
    template_name = template.origin.name
    serializer_class = ShowRacksSerializer

    def get(self, request):

        search_text = self.request.GET.get('search_text', None)

        if search_text:
            rack = Racks.objects.filter(rack_name__icontains=search_text)
        else:
            rack = Racks.objects.all()

        serializer = ShowRacksSerializer(rack, many=True)

        return Response({"data": serializer.data}, status=200)

class RacksListView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('Add_Rack_New.html')
    template_name = template.origin.name
    serializer_class = RacksSerializer

    def get(self, request):
        rack = Racks.objects.all()

        serializer = RacksSerializer(rack, many=True)

        return Response({"data": serializer.data}, status=200)


class RacksView(APIView):
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        email = request.data.pop('email')[0]
        token = request.data.pop('token')[0]
        request.POST._mutable = mutable

        serializer = RacksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # return Response(serializer.data, status=200)
            return HttpResponseRedirect(redirect_to='/library/racks_list')
        return Response(serializer.errors, status=422)

    def put(self, request):
        try:
            obj_id = request.data["id"]
        except Exception as e:
            print(e)
            return Response({"detail": "Id not found in data!"}, status=422)

        rack = Racks.objects.filter(id=obj_id).first()
        serializer = RacksSerializer(rack, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=422)


class RacksDetailedView(APIView):

    def get(self, request, pk):
        rack = Racks.objects.get(id=pk)

        serializer = RacksSerializer(rack)

        # return Response(serializer.data, status=200)
        return render(request, 'Add_Book_New.html', {"data": serializer.data, "rack_name": rack.rack_name})

    def delete(self, request, pk):
        Racks.objects.get(id=pk).delete()

        return Response({"detail": "Deleted Rack Successfully!"}, status=200)
