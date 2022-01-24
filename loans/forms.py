from django import forms
from django.core.exceptions import ValidationError

# Import Loan model
from .models import Loan
# Import service that connect to Moni's API
from .api.services import LoanApproval


# Define LoanForm
class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            'name',
            'last_name',
            'dni',
            'email',
            'gender',
            'amount',
            'status']
        # Labels for template
        labels = {
            'name': 'Nombre/s',
            'last_name': 'Apellido/s',
            'dni': 'DNI',
            'email': 'Correo electrónico',
            'gender': 'Género',
            'amount': 'Monto'
        }

        # Style for template
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'last_name'
                }
            ),
            'dni': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'dni',
                    'maxlenght': '8'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'id': 'email'
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'gender'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'amount'
                }
            )
        }

    # Validation for DNI field
    def clean_dni(self):
        dni = self.data['dni']
        try:
            dni = int(dni)
            if dni > 999999 and dni < 100000000:
                return dni
            else:
                raise ValidationError('DNI no válido')
        except Exception:
            raise ValidationError('DNI no válido')

    # Data from MONI's API
    def clean_status(self):
        # Call the service to get response from Moni's API
        stat = LoanApproval().get_loan_approval(self.clean_dni())
        if type(stat) is bool:
            return stat
        else:
            raise ValidationError('Error al obtener la respuesta desde la API')
