# API
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

# Serializers
from .serializers import LoanSerializer, GenderSerializer
# Service
from .services import LoanApproval
# Permissions
from permissions.permissions import IsStaffUser, IsSuperUser


class GenderViewSet(viewsets.ModelViewSet):
    serializer_class = GenderSerializer
    queryset = serializer_class.Meta.model.objects.all()


class LoanViewSet(viewsets.ModelViewSet):
    # Define serializer class
    serializer_class = LoanSerializer
    # Allowed methods
    http_method_names = ['get', 'post', 'delete']
    # Class that is going to be used for user authentication
    authentication_classes = [TokenAuthentication]

    # get_queryset method override
    def get_queryset(self, pk=None):
        # If true means that is a retrieve request
        if pk is not None:
            return self.get_serializer().Meta.model.objects.\
                filter(state=True).filter(id=pk).first()
        else:
            # return list with all active users
            return self.get_serializer().Meta.model.objects.\
                filter(state=True)

    # Override get_permissions method to get the right permissions
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permission() for permission in [
                IsSuperUser | IsStaffUser,
                ]]
        elif self.action == 'destroy':
            return [permission() for permission in [IsSuperUser]]
        else:
            return [permission() for permission in [AllowAny]]

    # Override create method to set the status field
    def create(self, request):
        serialized_loan = self.serializer_class(data=request.data)
        if serialized_loan.is_valid():
            # Call the service to get response from Moni's API
            stat = LoanApproval().get_loan_approval(serialized_loan.
                                                    validated_data['dni'])
            # Check if the return was a bool,
            # if not the response from Moni's API has an error
            if type(stat) is bool:
                if stat:
                    # API approved loan
                    serialized_loan.validated_data['status'] = True
                else:
                    # Not approved
                    serialized_loan.validated_data['status'] = False
                # Save in DB with the status value
                serialized_loan.save()
                return Response(
                    [
                        {'mensaje': 'Préstamo creado con éxito'},
                        serialized_loan.data
                    ],
                    status=status.HTTP_201_CREATED
                    )
            # Error response from Moni's API
            return Response(
                {'mensaje': 'Error en la respuesta desde la API externa'},
                status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serialized_loan.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    # Override destroy method to do logic delete
    def destroy(self, request, pk=None):
        loan = self.get_queryset(pk)
        if loan:
            loan.state = False
            loan.save()
            # Save the loan with state field set False
            return Response(
                {'mensaje': 'Préstamo eliminado correctamente'},
                status=status.HTTP_204_NO_CONTENT
                )
        # Couldn't find a loan with that pk
        return Response(
            {'error': 'Préstamo no encontrado'},
            status=status.HTTP_400_BAD_REQUEST
            )
