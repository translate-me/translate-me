from rest_framework import serializers

class ValuesSerializer(serializers.Serializer):
    amount_words = serializers.IntegerField()
    total_price = serializers.FloatField()
