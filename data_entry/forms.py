from django import forms
from .models import Pengguna
STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)


class AddressForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(choices=STATES)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=False)

class PenggunaForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATES)

    class Meta:
        model = Pengguna
        exclude = ['tanggal_join',]

from django import forms
from .models import Unit  # Pastikan model Unit diimpor

KATEGORI_PARAM_CHOICES = [
    ('OPTB', 'OPTB'),
    ('BLEND', 'BLEND'),
]

class UploadParamFromFileForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), label="Unit")
    kategori_param = forms.ChoiceField(choices=KATEGORI_PARAM_CHOICES, label="Kategori Parameter")
    file = forms.FileField(label="Pilih File")

from django import forms
from .models import Pengguna, Content

class PenggunaForm(forms.ModelForm):
    class Meta:
        model = Pengguna
        fields = ['email', 'address_1', 'address_2', 'state']

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['author', 'artikel', 'set_view']

from django import forms

class ProjectSearchForm(forms.Form):
    keyword = forms.CharField(label='Cari Project', required=False)

from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    aktivitas1 = forms.CharField(max_length=100)
    aktivitas2 = forms.CharField(max_length=100)
    aktivitas3 = forms.CharField(max_length=100)

    class Meta:
        model = Project
        fields = ['nama', 'deskripsi', 'mulai', 'selesai', 'penanggungjawab', 'jumlah', 'pendanaan', 'file']





