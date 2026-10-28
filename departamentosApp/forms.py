from django import forms

from .models import Departamento


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = (
            'nombre',
            'encargado',
            'horario',
            'telefono',
            'descripcion',
            'prioridad',
        )
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'