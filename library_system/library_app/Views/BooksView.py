from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from rest_framework.renderers import TemplateHTMLRenderer

from authentication.BusinessLogic.TokenVarify import is_authenticated_user
from library_app.Serializers.RacksViewSerializer import RacksSerializer
from library_app.models import Racks, Books
from library_app.Serializers.BooksViewSerializer import BooksListSerializer, BooksSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from library_system.pagination import StandardResultSetPagination


class BooksListView(ListAPIView):
    serializer_class = BooksListSerializer
    pagination_class = StandardResultSetPagination
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('Add_Book_New.html')
    template_name = template.origin.name

    def get_queryset(self):
        queryset = Books.objects.all()

        return queryset


class BooksView(APIView):
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        email = request.data.pop('email')[0]
        token = request.data.pop('token')[0]
        request.POST._mutable = mutable
        is_authenticated = is_authenticated_user(email, token)
        racks = request.data["racks"]

        books_count = Books.objects.filter(racks=racks).count()

        if books_count < 10:

            serializer = BooksSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(redirect_to='/library/racks_view/' + racks)

        rack = Racks.objects.get(id=racks)

        serializer = RacksSerializer(rack)
        return render(request, 'Add_Book_New.html',
                        {"data": serializer.data, "rack_name": rack.rack_name, "books_count": books_count})

    def put(self, request):
        try:
            obj_id = request.data["id"]
        except Exception as e:
            print(e)
            return Response({"detail": "Id not found in data!"}, status=422)

        book = Books.objects.filter(id=obj_id).first()
        serializer = BooksSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=422)


class BooksDetailedView(APIView):
    def get(self, request, pk):
        book = Books.objects.get(id=pk)

        serializer = BooksSerializer(book)

        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        Books.objects.get(id=pk).delete()

        return Response({"detail": "Deleted Book Successfully!"}, status=200)


class ShowBooksList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('show_books_new.html')
    template_name = template.origin.name
    serializer_class = BooksSerializer

    def get(self, request):

        search_text = self.request.GET.get('search_text', None)
        search_option = self.request.GET.get('books_search', None)
        rack_id = self.request.GET.get('rack', None)

        if search_text:
            if search_option == "author":
                books = Books.objects.filter(author__icontains=search_text)
            if search_option == "publication_year":
                books = Books.objects.filter(published_year__icontains=search_text)
            if search_option == "book_title":
                books = Books.objects.filter(book_title__icontains=search_text)
        else:
            books = Books.objects.all()

        if rack_id:
            books = Books.objects.filter(racks_id=rack_id)

        serializer = BooksSerializer(books, many=True)

        return Response({"data": serializer.data}, status=200)


class ShowBooksUserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('show_books.html')
    template_name = template.origin.name
    serializer_class = BooksSerializer

    def get(self, request):
        search_text = self.request.GET.get('search_text', None)
        search_option = self.request.GET.get('books_search', None)
        rack_id = self.request.GET.get('rack', None)

        if search_text:
            if search_option == "author":
                books = Books.objects.filter(author__icontains=search_text)
            if search_option == "publication_year":
                books = Books.objects.filter(published_year__icontains=search_text)
            if search_option == "book_title":
                books = Books.objects.filter(book_title__icontains=search_text)
        else:
            books = Books.objects.all()

        if rack_id:
            books = Books.objects.filter(racks_id=rack_id)

        serializer = BooksSerializer(books, many=True)

        return Response({"data": serializer.data}, status=200)


class ShowRackBooksList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('show_books_new.html')
    template_name = template.origin.name
    serializer_class = BooksSerializer

    def get(self, request):
        rack_id = self.request.GET.get('rack', None)
        if rack_id:
            books = Books.objects.filter(racks_id=rack_id)
        else:
            books = []

        serializer = BooksSerializer(books, many=True)

        return Response({"data": serializer.data}, status=200)


class ShowRackBooksUserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template = loader.get_template('show_books.html')
    template_name = template.origin.name
    serializer_class = BooksSerializer

    def get(self, request):
        rack_id = self.request.GET.get('rack', None)
        if rack_id:
            books = Books.objects.filter(racks_id=rack_id)
        else:
            books = []

        serializer = BooksSerializer(books, many=True)

        return Response({"data": serializer.data}, status=200)
