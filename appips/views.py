
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView,UpdateView,ListView,UpdateView,DetailView,FormView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect



#Usuarios

class UsuarioCreate(CreateView):
    model = Usuario
    fields = '__all__'  
    template_name = 'usuario_form.html'  
    success_url = reverse_lazy('listar_usuarios')  

    def form_valid(self, form):
        messages.success(self.request, "El usuario ha sido creado y guardado exitosamente.")
        return super().form_valid(form)

def home(request):
    return render(request, 'home.html')

def listar_usuarios(request):
    query = request.GET.get('q','') 
    usuarios = Usuario.objects.filter(
        Q(numero_identificacion__icontains=query) |
        Q(primer_nombre__icontains=query) |
        Q(primer_apellido__icontains=query)
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Detectar si es una solicitud AJAX
        data = []
        for usuario in usuarios:
            data.append({
                'tipo_identificacion': usuario.get_tipo_identificacion_display(),
                'numero_identificacion': usuario.numero_identificacion,
                'primer_nombre': usuario.primer_nombre,
                'segundo_nombre': usuario.segundo_nombre,
                'primer_apellido': usuario.primer_apellido,
                'segundo_apellido': usuario.segundo_apellido,
                
            })
        return JsonResponse({'usuarios': data})
    
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

class UsuarioUpdate(UpdateView):
    model = Usuario
    fields = '__all__' 
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('listar_usuarios')

    def form_valid(self, form):
        messages.success(self.request, "El usuario ha sido actualizado exitosamente.")
        return super().form_valid(form)
    
class UsuarioDelete(DeleteView):
    model = Usuario
    template_name = 'usuario_confirm_delete.html'
    success_url = reverse_lazy('listar_usuarios')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El usuario ha sido eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

#Medicos

class MedicoCreate(CreateView):
    model = Medico
    fields = '__all__'  
    template_name = 'medico_form.html'  
    success_url = reverse_lazy('listar_medicos')  

    def form_valid(self, form):
        messages.success(self.request, "El medico ha sido creado y guardado exitosamente.")
        return super().form_valid(form)
    
def listar_medicos(request):
    query = request.GET.get('q','')  # Obtenemos el filtro de búsqueda desde el formulario
    medicos = Medico.objects.filter(
        Q(numero_identificacion__icontains=query) |
        Q(primer_nombre__icontains=query) |
        Q(primer_apellido__icontains=query)
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Detectar si es una solicitud AJAX
        data = []
        for medico in medicos:
            data.append({
                'tipo_identificacion': medico.get_tipo_identificacion_display(),
                'numero_identificacion': medico.numero_identificacion,
                'primer_nombre': medico.primer_nombre,
                'segundo_nombre': medico.segundo_nombre,
                'primer_apellido': medico.primer_apellido,
                'segundo_apellido': medico.segundo_apellido,
                'especialidad_medica':medico.especialidad_medica,
                # Agrega otros campos si es necesario
            })
        return JsonResponse({'medicos': data})
    
    return render(request, 'listar_medicos.html', {'medicos': medicos})
   
class MedicoUpdate(UpdateView):
    model = Medico
    fields = '__all__'  
    template_name = 'medico_form.html'
    success_url = reverse_lazy('listar_medicos')

    def form_valid(self, form):
        messages.success(self.request, "El medico ha sido actualizado exitosamente.")
        return super().form_valid(form)
    
class MedicoDelete(DeleteView):
    model = Medico
    template_name = 'medico_confirm_delete.html'
    success_url = reverse_lazy('listar_medicos')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El medico ha sido eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
    
# Citas


class CitasLista(ListView):
    model = Citas
    template_name = 'citas_list.html'  

class CitaUpdate(UpdateView):
    model = Citas
    fields = '__all__'  
    template_name = 'cita_form.html'
    success_url = reverse_lazy('lista_citas')

    def form_valid(self, form):
        messages.success(self.request, "La cita ha sido actualizado exitosamente.")
        return super().form_valid(form)

class CitaDelete(DeleteView):
    model = Citas
    template_name = 'confirmar_eliminar.html'  
    success_url = reverse_lazy('lista_citas')  #

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "la cita ha sido eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
    
class HistoriaClinicaListView(ListView):
    model = HistoriaClinica
    template_name = "historias_clinicas_list.html"
    context_object_name = "historias_clinicas"

    def get_queryset(self):
        # Opcional: Filtrar por algún criterio, como usuario autenticado
        return HistoriaClinica.objects.all()
     
class HistoriaClinicaDetailView(DetailView):
    model = HistoriaClinica
    template_name = "historia_clinica_detail.html"
    context_object_name = "historia_clinica"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        historia_clinica = self.object
        usuario = historia_clinica.usuario  # FK a Usuario desde HistoriaClinica
        context["edad"] = usuario.edad  # Usando la propiedad calculada
        return context


    
class CompletarCitaView(FormView):
    template_name = "completar_cita.html"
    success_url = reverse_lazy("lista_citas")  # Redirige a la lista de citas tras completar
    form_class = CompletarCitaForm  # Define un formulario para diagnóstico, tratamiento, etc.

    def form_valid(self, form):
        cita_id = self.kwargs["pk"]
        cita = get_object_or_404(Citas, pk=cita_id)
        if cita.asistio and cita.estado == "Pendiente":
            cita.completar_cita(
                diagnostico=form.cleaned_data["diagnostico"],
                tratamiento=form.cleaned_data["tratamiento"],
                observaciones=form.cleaned_data["observaciones"],
            )
        return super().form_valid(form)

class RegistroCitaListView(ListView):
    model = RegistroCita
    template_name = "registros_citas_list.html"
    context_object_name = "registros_citas"

    def get_queryset(self):
        historia_clinica_id = self.kwargs.get("historia_clinica_id")
        return RegistroCita.objects.filter(historia_clinica_id=historia_clinica_id)

class AgendaCreateView(CreateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'agenda_form.html'
    success_url = reverse_lazy('listar_medicos')  # Define la URL de redirección

    def form_valid(self, form):
        messages.success(self.request, "La agenda ha sido registrada exitosamente.")
        return super().form_valid(form)
    
# class CitaCreate(CreateView):
#     model = Citas
#     form_class = CitaForm
#     template_name = 'cita_form.html'
#     success_url = reverse_lazy('lista_citas')

#     def get_form_kwargs(self):
#         # Llama al método padre para obtener los argumentos base
#         kwargs = super().get_form_kwargs()

#         # Obtiene los parámetros 'medico' y 'fecha' de la URL
#         medico_id = self.request.GET.get('medico')
#         fecha = self.request.GET.get('fecha')

#         # Agrega estos parámetros a kwargs
#         if medico_id:
#             kwargs['medico_id'] = medico_id  # Se envía al formulario como argumento
#         if fecha:
#             kwargs['fecha'] = fecha  # También se envía al formulario como argumento

#         return kwargs
    


class CitaCreate(CreateView):
    model = Citas
    form_class = CitaForm
    template_name = 'cita_form.html'
    success_url = reverse_lazy('lista_citas')

    def get_form_kwargs(self):
        # Llama al método padre para obtener los argumentos base
        kwargs = super().get_form_kwargs()

        # Obtiene los parámetros 'medico' y 'fecha' de la URL
        medico_id = self.request.GET.get('medico')
        fecha = self.request.GET.get('fecha')

        # Agrega estos parámetros a kwargs
        if medico_id:
            kwargs['medico_id'] = medico_id  # Se envía al formulario como argumento
        if fecha:
            kwargs['fecha'] = fecha  # También se envía al formulario como argumento

        return kwargs


def obtener_horas_disponibles(request):
        medico_id = request.GET.get('medico')
        fecha = request.GET.get('fecha')

        try:
            agenda = Agenda.objects.get(medico_id=medico_id, fecha=fecha)
            horarios = agenda.horarios.all()
            data = {
                'horas': [
                    {
                        'hora': str(horario.hora),
                        'disponible': horario.disponible
                    } for horario in horarios
                ]
            }
            return JsonResponse(data)
        except Agenda.DoesNotExist:
            return JsonResponse({'horas': []})
