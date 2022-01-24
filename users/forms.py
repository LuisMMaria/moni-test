from django import forms

# Import User model
from .models import User


# Define UserForm
class UserForm(forms.ModelForm):

    # Password confirmation extra field
    password_confirmation = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Las contraseñas deben coincidir',
            'id': 'password_confirmation'
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'name', 'last_name',
                  'email', 'password', 'is_staff', 'is_superuser']
        # Labels for template
        labels = {
            'username': 'Nombre de Usuario',
            'name': 'Nombre/s',
            'last_name': 'Apellido/s',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
            'is_staff': 'Es staff',
            'is_superuser': 'Es superusuario',
            'password_confirmation': 'Confirmación de contraseña'
        }

        # Style for template
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'No debe contener espacios',
                    'id': 'username'
                }
            ),
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
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'id': 'email'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'id': 'password'
                }
            ),
            'is_staff': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'id': 'is_staff'
                }
            ),
            'is_superuser': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'id': 'is_superuser'
                }
            )
        }

    # Override clean method to check if both
    # password fields have the same value
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('password_confirmation')

        if password != confirm_password:
            self.add_error('password_confirmation',
                           'Las contraseñas no coinciden')

        return cleaned_data

    # Override save method to store the password hashed
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
