from django import forms

from .models import Servicio, SolicitudServicio


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = (
            'nombre',
            'categoria',
            'descripcion',
            'plazo_dias',
            'gratuito',
            'estado',
        )
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class SolicitudServicioForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = ('servicio', 'motivo', 'direccion', 'telefono_contacto')
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.exclude(
            estado='no disponible',
        )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EstadoSolicitudForm(forms.Form):
    estado = forms.ChoiceField(
        choices=SolicitudServicio.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )