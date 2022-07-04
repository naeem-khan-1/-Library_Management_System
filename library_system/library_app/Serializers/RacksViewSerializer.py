
from rest_framework import serializers

from library_app.Serializers.BooksViewSerializer import BooksSerializer
from library_app.models import Racks, Books


class ShowRacksSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField('get_books_count')

    class Meta:
        model = Racks
        fields = '__all__'

    def get_books_count(self, obj):
        count = Books.objects.filter(racks=obj).count()
        return count


class RacksListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Racks
        fields = '__all__'


class RacksSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField('get_books')

    class Meta:
        model = Racks
        fields = '__all__'

    def get_books(self, obj):
        serializer_context = {'request': self.context.get('request')}
        books = Books.objects.filter(racks=obj).all()
        serializer = BooksSerializer(books, many=True, context=serializer_context)

        return serializer.data

    def create(self, validate_data):
        racks = Racks.objects.create(**validate_data)

        return racks

    def update(self, instance, validate_data):
        Racks.objects.filter(id=instance.id).update(**validate_data)

        return instance

