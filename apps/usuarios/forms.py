from urllib import request
from django import forms
from apps.usuarios.models import Cliente, Usuario, Profesional
from apps.solicitudes.models import Solicitud

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username','email', 'password','rol']
    rol = forms.ChoiceField(choices=Usuario.ROLES, widget=forms.Select(attrs={'id': 'id_rol'}))


    #para encriptar la contraseña 
    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Aseguramos que se encripte la contraseña

        if commit:
            user.save()
        return user    
 
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['direccion', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefono'].required = False
        self.fields['direccion'].required = False

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if direccion is None and self.fields.rol == 'Cliente':
            raise forms.ValidationError('Este campo es obligatorio para los Clientes.')
        return direccion

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono is None and self.fields.rol == 'Cliente':
            raise forms.ValidationError('Este campo es obligatorio para los Clientes.')
        return telefono



class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['especialidad', 'disponibilidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especialidad'].required = False

    def clean_especialidad(self):
        # Validar solo si el campo es visible
        especialidad = self.cleaned_data.get('especialidad')
        if especialidad is None and self.instance.rol == 'Profesional':
            raise forms.ValidationError('Este campo es obligatorio para los profesionales.')
        return especialidad






class SolicitudForm(forms.ModelForm):
    nombre_servicio = forms.CharField(max_length=100, label="Nombre del Servicio")
    descripcion_servicio = forms.CharField(widget=forms.Textarea, label="Descripción del Servicio")
    
    class Meta:
        model = Solicitud
        fields = ['cliente', 'fecha_servicio', 'estado']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cliente'].initial = user.cliente  # Establecemos el cliente relacionado al usuario
            self.fields['cliente'].widget = forms.HiddenInput()  # Ocultamos el campo cliente
            self.fields['estado'].widget = forms.HiddenInput() # Ocultamos el campo estado


