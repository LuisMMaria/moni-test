from rest_framework import serializers

# Import models
from loans.models import Gender, Loan


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ('state', 'created_date', 'deleted_date')
        extra_kwargs = {'status': {'required': False}}

    # DNI Validation
    def validate_dni(self, value):
        if value > 999999 and value < 100000000 and isinstance(value, int):
            return value
        raise serializers.ValidationError('El DNI es incorrecto')

    # Override to_representation method
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'last_name': instance.last_name,
            'dni': instance.dni,
            'email': instance.email,
            'gender': instance.gender.gender_name,
            'amount': instance.amount,
            'status': instance.status
        }
