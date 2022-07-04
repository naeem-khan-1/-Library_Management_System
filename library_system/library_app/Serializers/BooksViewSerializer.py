
from rest_framework import serializers
from library_app.models import Books


class BooksListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = '__all__'


class BooksSerializer(serializers.ModelSerializer):
    rack_name = serializers.CharField(source="racks.rack_name", read_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model = Books
        fields = '__all__'

    def create(self, validate_data):
        validated_data = self.initial_data
        racks = validate_data.pop("racks", None)
        book = Books.objects.create(racks=racks, **validate_data)

        return book

    def update(self, instance, validate_data):
        validated_data = self.initial_data
        racks_id = validated_data.pop("racks_id", None)
        Books.objects.filter(id=instance.id).update(racks_id=racks_id, **validate_data)

        return instance

