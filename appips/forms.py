# forms.py
from django import forms
from .models import Citas, Usuario, Medico,HistoriaClinica

class CitaForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Seleccione un paciente",
        to_field_name="numero_identificacion",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Número de Identificación del Paciente"
    )
    
    medico = forms.ModelChoiceField(
        queryset=Medico.objects.all(),
        empty_label="Seleccione un médico",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Médico"
    )
    
    class Meta:
        model = Citas
        fields = ['usuario', 'medico', 'fecha_cita', 'hora_cita', 'motivo_consulta', 'estado', 'asistio']


class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = '__all__'

from django import forms

class CompletarCitaForm(forms.Form):
    diagnostico = forms.CharField(widget=forms.Textarea, required=True)
    tratamiento = forms.CharField(widget=forms.Textarea, required=True)
    observaciones = forms.CharField(widget=forms.Textarea, required=False)




