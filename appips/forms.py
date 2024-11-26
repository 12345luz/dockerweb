# forms.py
from django import forms
from .models import Citas, Usuario, Medico,HistoriaClinica,Agenda

from django.http import JsonResponse

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = '__all__'

class CompletarCitaForm(forms.Form):
    diagnostico = forms.CharField(widget=forms.Textarea, required=True)
    tratamiento = forms.CharField(widget=forms.Textarea, required=True)
    observaciones = forms.CharField(widget=forms.Textarea, required=False)

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['medico', 'fecha', 'hora_inicio', 'hora_fin', 'intervalo']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'intervalo': forms.NumberInput(attrs={'class': 'form-control'}),
        }



# class CitaForm(forms.ModelForm):
#     usuario = forms.ModelChoiceField(
#         queryset=Usuario.objects.all(),
#         empty_label="Seleccione un paciente",
#         to_field_name="numero_identificacion",
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Número de Identificación del Paciente"
#     )
    
#     medico = forms.ModelChoiceField(
#         queryset=Medico.objects.all(),
#         empty_label="Seleccione un médico",
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Médico"
#     )

#     fecha_cita = forms.DateField(
#         widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#         label="Fecha de la Cita"
#     )

#     motivo_consulta = forms.CharField(
#         max_length=200,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         label="Motivo de la Consulta"
#     )

#     hora_cita = forms.ChoiceField(
#         choices=[],  # Se llenará dinámicamente desde JavaScript
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Hora de la Cita"
#     )

#     estado = forms.ChoiceField(
#         choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')],
#         initial='Pendiente',
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Estado"
#     )
    
#     asistio = forms.BooleanField(
#         required=False,
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         label="¿Asistió?"
#     )

#     class Meta:
#         model = Citas
#         fields = ['usuario', 'medico', 'fecha_cita', 'hora_cita', 'motivo_consulta', 'estado', 'asistio']

class CitaForm(forms.ModelForm):
    # Definimos los campos como antes
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
    fecha_cita = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Fecha de la Cita"
    )
    hora_cita = forms.ChoiceField(
        choices=[],  # Se llenará dinámicamente
        widget=forms.Select(attrs={'class': 'form-control'}),

        label="Hora de la Cita"
    )
    estado = forms.ChoiceField(
        choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')],
        initial='Pendiente',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Estado"
    )
    asistio = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="¿Asistió?"
    )

    class Meta:
        model = Citas
        fields = ['usuario', 'medico', 'fecha_cita', 'hora_cita', 'motivo_consulta', 'estado', 'asistio']

    def __init__(self, *args, **kwargs):
        # Extrae los argumentos adicionales del constructor
        medico_id = kwargs.pop('medico_id', None)
        fecha = kwargs.pop('fecha', None)

        super().__init__(*args, **kwargs)

        # Si se pasa un médico y una fecha, carga las horas disponibles
        if medico_id and fecha:
            try:
                agenda = Agenda.objects.get(medico_id=medico_id, fecha=fecha)
                horarios = agenda.horarios.filter(disponible=True)
                self.fields['hora_cita'].choices = [(str(horario.hora), str(horario.hora)) for horario in horarios]

                # Imprimir en consola las opciones cargadas
                print("Opciones de hora_cita cargadas:", self.fields['hora_cita'].choices)

            except Agenda.DoesNotExist:
                self.fields['hora_cita'].choices = []

