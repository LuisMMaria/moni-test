from django.db import models


# Gender Model
class Gender(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    gender_name = models.CharField('Género', max_length=50)

    def __str__(self):
        return self.gender_name


# Loan Model
class Loan(models.Model):
    # Fields
    # Required Fields
    id = models.AutoField(primary_key=True)
    dni = models.IntegerField('DNI')
    name = models.CharField('Nombre', max_length=80)
    last_name = models.CharField('Apellido', max_length=80)
    email = models.EmailField('E-mail', max_length=254)
    gender = models.ForeignKey(
        Gender,
        on_delete=models.CASCADE,
        verbose_name='Género'
        )
    amount = models.FloatField('Monto')
    status = models.BooleanField('Estado')  # Approved or not

    # ExtraFields
    # Field for logical deletion/elimination
    state = models.BooleanField('Estado eliminación', default=True)
    created_date = models.DateField(
        'Fecha de Creación',
        auto_now=False,
        auto_now_add=True
        )
    deleted_date = models.DateField(
        'Fecha de Eliminación',
        auto_now=True,
        auto_now_add=False
        )

    class Meta:
        ordering = ['id']
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return str(self.id) + ' de ' + self.name + ', ' + self.last_name
