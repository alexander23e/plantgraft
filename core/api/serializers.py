from rest_framework import serializers

from core.erp.models import Sale


class SaleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

    def to_representation(self, instance):
        return {'id': instance.pk, 'fecha_registro': instance.date_joined_format(), 'tipo': instance.get_type_display(), 'cliente': instance.client.user.names, 'total': instance.total}
