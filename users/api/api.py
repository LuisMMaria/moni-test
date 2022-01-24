# API
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

# Serializer
from users.api.serializers import UserSerializer
# Permissions
from permissions.permissions import IsSuperUser, IsStaffUser, IsOwner


# ViewSet for Users
class UserViewSet(viewsets.ModelViewSet):
    # Define serializer class
    serializer_class = UserSerializer
    # Class that is going to be used for user authentication
    authentication_classes = [TokenAuthentication]
    # Allowed Methods
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']

    # get_queryset method override
    def get_queryset(self, pk=None):
        # If true means that is a retrieve request
        if pk is not None:
            return self.get_serializer().Meta.model.objects.\
                filter(id=pk).first()
        else:
            # return list with all active users
            return self.get_serializer().Meta.model.objects.\
                filter(is_active=True)

    # Override get_permissions method to get the right permissions
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            if self.request.user.is_authenticated:
                return [permission() for permission in [
                    IsSuperUser | IsStaffUser | IsOwner, ]]
            else:
                return [permission() for permission in [
                    IsSuperUser | IsStaffUser, ]]
        elif self.action in ['destroy', 'create']:
            return [permission() for permission in [
                IsSuperUser | IsStaffUser, ]]
        elif self.action in ['update', 'partial_update']:
            # A user can modify his own data, but if it is a
            # superuser can modify data of all users
            return [permission() for permission in [
                IsSuperUser | IsOwner, ]]
        else:
            return [permission() for permission in [AllowAny]]

    # Override create method
    def create(self, request):
        serialized_user = self.serializer_class(data=request.data)
        # Ask if user data is valid
        if serialized_user.is_valid():
            # Avoid users to give greater permissions to themselves
            if not request.user.is_superuser:
                serialized_user.validated_data['is_superuser'] = False
            if not request.user.is_staff:
                serialized_user.validated_data['is_staff'] = False

            user = serialized_user.save()
            token = Token.objects.get(user=user)
            return Response(
                [
                    {'mensaje': 'Usuario creado con éxito'},
                    serialized_user.data,
                    {'token': str(token)}
                ],
                status=status.HTTP_201_CREATED
                )
        else:
            # If user data is not validated
            return Response(
                serialized_user.errors,
                status=status.HTTP_400_BAD_REQUEST
                )

    # Override update method that handles put and patch http methods
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serialized_user = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
            )
        serialized_user.is_valid(raise_exception=True)

        # Avoid users to give greater permissions to themselves
        if not request.user.is_superuser:
            serialized_user.validated_data['is_superuser'] = False
            if not request.user.is_staff:
                serialized_user.validated_data['is_staff'] = False

        self.perform_update(serialized_user)
        return Response(
            [
                {'mensaje': 'Usuario actualizado con éxito'},
                serialized_user.data
            ])

    # Override destroy method to do logic delete
    def destroy(self, request, pk=None):
        usr = self.get_queryset(pk)
        if usr:
            usr.is_active = False
            usr.save()
            # Save the user with state field set False
            return Response(
                {'mensaje': 'Usuario eliminado correctamente'},
                status=status.HTTP_204_NO_CONTENT
                )
        # Couldn't find a user with that pk
        return Response(
            {'error': 'Usuario no encontrado'},
            status=status.HTTP_400_BAD_REQUEST
            )
