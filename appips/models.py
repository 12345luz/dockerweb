from django.db import models 
import unicodedata
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from datetime import date
class Usuario(models.Model):


    TIPO_IDENTIFICACION_CHOICES = [
        ('RC', 'Registro Civil'),
        ('TI', 'Tarjeta De Identidad'),
        ('CE', 'Cédula De Extranjería'),
        ('CC', 'Cédula De Ciudadanía'),
        ('PA', 'Pasaporte'),
        ('MS', 'Menor Sin Identificación'),
        ('AS', 'Adulto Sin Identificación'),
        ('CD', 'Carnet Diplomático'),
        ('NV', 'Certificado Nacido Vivo')
    ]

    GENERO_CHOICES=[
        ('F','FEMENINO'),
        ('M','MASCULINO'),
    ]

    CODIGO_PERTENENCIA_CHOICES = [
        (1, 'Indígena'),
        (2, 'ROM (gitano)'),
        (3, 'Raizal (archipiélago de San Andrés y Providencia)'),
        (4, 'Palanquero de San Basilio'),
        (5, 'Negro(a), Mulato(a), Afrocolombiano(a) o Afro descendiente'),
        (6, 'Ninguna de las anteriores'),
    ]

    CODIGO_OCUPACION_CHOICES=[
        (9611, 'Recolectores de basura y material reciclable'),
        (9612, 'Clasificadores de desechos'),
        (9613, 'Barrenderos y afines'),
        (9621, 'Mensajeros, mandaderos, maleteros y repartidores'),
        (9622, 'Personas que realizan trabajos varios'),
        (9624, 'Acarreadores de agua y recolectores de leña'),
        (9625, 'Recolectores de dinero y surtidores de máquinas de venta automática'),
        (9626, 'Lectores de medidores'),
        (9629, 'Otras ocupaciones elementales no clasificadas en otros grupos primarios'),
        (9998, 'Jubilado, desempleado, ama de casa, estudiante, dedicación al hogar, menor de edad'),
        (9999, 'No informa'),
        ]
    
    CODIGO_NIVEL_EDUCATIVO_CHOICES = [
    
            (1, 'Preescolar'),
            (10, 'Especialización'),
            (11, 'Maestría'),
            (12, 'Doctorado'),
            (13, 'Ninguno'),
            (2, 'Básica Primaria'),
            (3, 'Básica Secundaria'),
            (4, 'Media Académica o Clásica'),
            (5, 'Media Técnica (Bachillerato Técnico)'),
            (6, 'Normalista'),
            (7, 'Técnica Profesional'),
            (8, 'Tecnológica'),
            (9, 'Profesional'),
    ]

    
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_IDENTIFICACION_CHOICES)
    numero_identificacion = models.CharField(max_length=18, primary_key=True)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
   
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    codigo_pertenencia_etnica = models.SmallIntegerField(choices=CODIGO_PERTENENCIA_CHOICES)
    codigo_ocupacion = models.SmallIntegerField(choices=CODIGO_OCUPACION_CHOICES)  
    codigo_nivel_educativo = models.SmallIntegerField(choices=CODIGO_NIVEL_EDUCATIVO_CHOICES)  
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"
    
    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"
    
    def clean_text(self, text):
       
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        return text.upper()
    
    def save(self, *args, **kwargs):
        # Validar antes de guardar
        self.clean()

        # Transformar los datos al formato deseado
        if self.primer_apellido:
            self.primer_apellido = self.clean_text(self.primer_apellido)
        if self.segundo_apellido:
            self.segundo_apellido = self.clean_text(self.segundo_apellido)
        if self.primer_nombre:
            self.primer_nombre = self.clean_text(self.primer_nombre)
        if self.segundo_nombre:
            self.segundo_nombre = self.clean_text(self.segundo_nombre)

        super().save(*args, **kwargs)
    def edad(self):
        if self.fecha_nacimiento:
            hoy = date.today()
            return hoy.year - self.fecha_nacimiento.year - (
                (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None
    
class Medico(models.Model):

    TIPO_IDENTIFICACION_CHOICES = [
        ('CE', 'Cédula De Extranjería'),
        ('CC', 'Cédula De Ciudadanía'),
        ('PA', 'Pasaporte'),
        ('CD', 'Carnet Diplomático'),
    ]

    numero_identificacion = models.CharField(max_length=18, primary_key=True)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_IDENTIFICACION_CHOICES)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30) 
    especialidad_medica=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"
    
    def clean_text(self, text):
       
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        return text.upper()
    def save(self, *args, **kwargs):
        # Validar antes de guardar
        self.clean()

        # Transformar los datos al formato deseado
        if self.primer_apellido:
            self.primer_apellido = self.clean_text(self.primer_apellido)
        if self.segundo_apellido:
            self.segundo_apellido = self.clean_text(self.segundo_apellido)
        if self.primer_nombre:
            self.primer_nombre = self.clean_text(self.primer_nombre)
        if self.segundo_nombre:
            self.segundo_nombre = self.clean_text(self.segundo_nombre)

        super().save(*args, **kwargs)

from datetime import timedelta, datetime


class HorarioCita(models.Model):
    agenda = models.ForeignKey('Agenda', on_delete=models.CASCADE, related_name='horarios')
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)  # Define si la hora está disponible

    def __str__(self):
        return f"{self.hora} - {'Disponible' if self.disponible else 'Ocupado'}"

class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    intervalo = models.IntegerField(default=30)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Borrar horarios existentes para evitar duplicados
        self.horarios.all().delete()
        
        # Generar nuevos horarios
        hora_actual = datetime.combine(self.fecha, self.hora_inicio)
        hora_fin = datetime.combine(self.fecha, self.hora_fin)
        while hora_actual < hora_fin:
            HorarioCita.objects.create(
                agenda=self,
                hora=hora_actual.time(),
                disponible=True
            )
            hora_actual += timedelta(minutes=self.intervalo)


class Citas(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="citas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="citas")
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    motivo_consulta = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')],
        default='Pendiente'
    )
    asistio = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def completar_cita(self, diagnostico, tratamiento, observaciones=""):
        if self.asistio and self.estado == 'Pendiente':
            self.estado = 'Completada'
            self.save()
            
            # Obtener la historia clínica del usuario
            historia_clinica, created = HistoriaClinica.objects.get_or_create(usuario=self.usuario)

            # Crear el registro de la cita en la historia clínica
            RegistroCita.objects.create(
                historia_clinica=historia_clinica,
                cita=self,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                observaciones=observaciones
            )


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

            # Marcar la hora como ocupada
        HorarioCita.objects.filter(
            agenda__medico=self.medico,
            agenda__fecha=self.fecha_cita,
            hora=self.hora_cita
        ).update(disponible=False)
class HistoriaClinica(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="historia_clinica"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historia Clínica de {self.usuario}"

class RegistroCita(models.Model):
    historia_clinica = models.ForeignKey(
        HistoriaClinica, on_delete=models.CASCADE, related_name="registros_citas"
    )
    cita = models.OneToOneField(
        Citas, on_delete=models.CASCADE, related_name="registro_cita"
    )
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro de Cita el {self.cita.fecha_cita} para {self.historia_clinica.usuario}"


    


