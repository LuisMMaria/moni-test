from rest_framework import serializers

# Import model
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'last_name', 'email',
                  'is_active', 'is_staff', 'is_superuser',
                  'last_login', 'password')

    # Override create method
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # Override update method
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        if 'password' in validated_data:
            updated_user.set_password(validated_data['password'])
            updated_user.save()
        return updated_user
