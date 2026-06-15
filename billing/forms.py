from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Brand, ProductGroup, Supplier, Product, Customer, Invoice, InvoiceDetail
)

_sm_text   = {'class': 'form-control form-control-sm'}
_sm_select = {'class': 'form-select form-select-sm'}
_sm_number = {'class': 'form-control form-control-sm', 'min': '0'}

class ProductSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label='Nombre',
        widget=forms.TextInput(attrs={**_sm_text, 'placeholder': 'Buscar nombre…'})
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.order_by('name'),
        required=False, label='Marca', empty_label='Todas las marcas',
        widget=forms.Select(attrs=_sm_select)
    )
    group = forms.ModelChoiceField(
        queryset=ProductGroup.objects.order_by('name'),
        required=False, label='Grupo', empty_label='Todos los grupos',
        widget=forms.Select(attrs=_sm_select)
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.order_by('name'),
        required=False, label='Proveedor', empty_label='Todos los proveedores',
        widget=forms.Select(attrs=_sm_select)
    )
    price_min = forms.DecimalField(
        required=False, label='Precio mín',
        widget=forms.NumberInput(attrs={**_sm_number, 'placeholder': 'Mín', 'step': '0.01'})
    )
    price_max = forms.DecimalField(
        required=False, label='Precio máx',
        widget=forms.NumberInput(attrs={**_sm_number, 'placeholder': 'Máx', 'step': '0.01'})
    )
    stock_min = forms.IntegerField(
        required=False, label='Stock mín',
        widget=forms.NumberInput(attrs={**_sm_number, 'placeholder': 'Mín'})
    )
    stock_max = forms.IntegerField(
        required=False, label='Stock máx',
        widget=forms.NumberInput(attrs={**_sm_number, 'placeholder': 'Máx'})
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, label='Apellido', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields: self.fields[f].widget.attrs['class'] = 'form-control'

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'is_active': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }



class ProductGroupForm(forms.ModelForm):
    class Meta:
        model = ProductGroup
        fields = ['name', 'is_active']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'email', 'phone', 'address', 'is_active']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'brand', 'group', 'suppliers', 'unit_price', 'stock', 'is_active']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['dni', 'first_name', 'last_name', 'email', 'phone', 'address', 'is_active']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
        }


InvoiceDetailFormSet = forms.inlineformset_factory(
    Invoice,
    InvoiceDetail,
    fields=['product', 'quantity', 'unit_price'],
    extra=1,
    can_delete=True,
    widgets={
        'product': forms.Select(attrs={'class': 'form-select'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
    },
)