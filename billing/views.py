import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .mixins import ExportMixin
from .models import *
from django.db.models import Q
from .forms import (
    SignUpForm, BrandForm, ProductGroupForm, SupplierForm,
    ProductForm, CustomerForm, InvoiceForm, InvoiceDetailFormSet,
    ProductSearchForm, BrandSearchForm, ProductGroupSearchForm,
    SupplierSearchForm, CustomerSearchForm, InvoiceSearchForm,
)
from decimal import Decimal
from shared.mixins import StaffRequiredMixin
from shared.decorators import audit_action

# === HOME (Página principal) ===
@login_required
def home(request):
    """Vista principal del sistema. Muestra resumen general."""
    context = {
        'total_brands': Brand.objects.count(),
        'total_products': Product.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_invoices': Invoice.objects.count(),
        'recent_invoices': Invoice.objects.all()[:5],  # Últimas 5
        'low_stock': Product.objects.filter(stock__lte=5, is_active=True),
    }
    return render(request, 'billing/home.html', context)


# ── Definición de columnas disponibles para Productos ────────────────────────
PRODUCT_ALL_COLUMNS = [
    {
        'key':     'image',
        'label':   'Imagen',
        'default': True,
        'export':  (lambda obj: 'Con imagen' if obj.image else 'Sin imagen', 'Imagen'),
    },
    {
        'key':     'name',
        'label':   'Nombre',
        'default': True,
        'export':  ('name', 'Nombre'),
    },
    {
        'key':     'brand',
        'label':   'Marca',
        'default': True,
        'export':  ('brand.name', 'Marca'),
    },
    {
        'key':     'group',
        'label':   'Categoría',
        'default': True,
        'export':  ('group.name', 'Categoría'),
    },
    {
        'key':     'unit_price',
        'label':   'Precio',
        'default': True,
        'export':  ('unit_price', 'Precio ($)'),
    },
    {
        'key':     'stock',
        'label':   'Stock',
        'default': True,
        'export':  ('stock', 'Stock'),
    },
    {
        'key':     'balance',
        'label':   'Balance',
        'default': True,
        'export':  (lambda obj: str(obj.balance), 'Balance ($)'),
    },
    {
        'key':     'suppliers',
        'label':   'Proveedores',
        'default': True,
        'export':  (lambda obj: ', '.join(s.name for s in obj.suppliers.all()), 'Proveedores'),
    },
    {
        'key':     'id',
        'label':   'Código (ID)',
        'default': False,
        'export':  ('id', 'Código'),
    },
    {
        'key':     'description',
        'label':   'Descripción',
        'default': False,
        'export':  ('description', 'Descripción'),
    },
    {
        'key':     'is_active',
        'label':   'Estado',
        'default': False,
        'export':  (lambda obj: 'Sí' if obj.is_active else 'No', 'Estado'),
    },
    {
        'key':     'created_at',
        'label':   'Fecha creación',
        'default': False,
        'export':  (lambda obj: obj.created_at.strftime('%d/%m/%Y'), 'Fecha creación'),
    },
]

# ── Definición de columnas disponibles para Marcas ────────────────────────
BRAND_ALL_COLUMNS = [
    {
        'key':     'name',
        'label':   'Nombre',
        'default': True,
        'export':  ('name', 'Nombre'),
    },
    {
        'key':     'description',
        'label':   'Descripción',
        'default': True,
        'export':  ('description', 'Descripción'),
    },
    {
        'key':     'is_active',
        'label':   'Estado',
        'default': True,
        'export':  (lambda obj: 'Sí' if obj.is_active else 'No', 'Estado'),
    },
    {
        'key':     'created_at',
        'label':   'Fecha creación',
        'default': False,
        'export':  (lambda obj: obj.created_at.strftime('%d/%m/%Y'), 'Fecha creación'),
    },
]

# ── Definición de columnas disponibles para Grupos de Productos ────────────────────────
PRODUCTGROUP_ALL_COLUMNS = [
    {
        'key':     'name',
        'label':   'Nombre',
        'default': True,
        'export':  ('name', 'Nombre'),
    },
    {
        'key':     'is_active',
        'label':   'Estado',
        'default': True,
        'export':  (lambda obj: 'Sí' if obj.is_active else 'No', 'Estado'),
    },
    {
        'key':     'created_at',
        'label':   'Fecha creación',
        'default': False,
        'export':  (lambda obj: obj.created_at.strftime('%d/%m/%Y'), 'Fecha creación'),
    },
]

# ── Definición de columnas disponibles para Proveedores ────────────────────────
SUPPLIER_ALL_COLUMNS = [
    {
        'key':     'name',
        'label':   'Nombre',
        'default': True,
        'export':  ('name', 'Nombre'),
    },
    {
        'key':     'contact_name',
        'label':   'Contacto',
        'default': True,
        'export':  ('contact_name', 'Contacto'),
    },
    {
        'key':     'email',
        'label':   'Email',
        'default': True,
        'export':  ('email', 'Email'),
    },
    {
        'key':     'phone',
        'label':   'Teléfono',
        'default': True,
        'export':  ('phone', 'Teléfono'),
    },
    {
        'key':     'address',
        'label':   'Dirección',
        'default': False,
        'export':  ('address', 'Dirección'),
    },
    {
        'key':     'is_active',
        'label':   'Estado',
        'default': False,
        'export':  (lambda obj: 'Sí' if obj.is_active else 'No', 'Estado'),
    },
]

# ── Definición de columnas disponibles para Clientes ────────────────────────
CUSTOMER_ALL_COLUMNS = [
    {
        'key':     'dni',
        'label':   'DNI/RUC',
        'default': True,
        'export':  ('dni', 'DNI/RUC'),
    },
    {
        'key':     'last_name',
        'label':   'Apellido',
        'default': True,
        'export':  ('last_name', 'Apellido'),
    },
    {
        'key':     'first_name',
        'label':   'Nombre',
        'default': True,
        'export':  ('first_name', 'Nombre'),
    },
    {
        'key':     'email',
        'label':   'Email',
        'default': True,
        'export':  ('email', 'Email'),
    },
    {
        'key':     'phone',
        'label':   'Teléfono',
        'default': True,
        'export':  ('phone', 'Teléfono'),
    },
    {
        'key':     'address',
        'label':   'Dirección',
        'default': False,
        'export':  ('address', 'Dirección'),
    },
    {
        'key':     'is_active',
        'label':   'Estado',
        'default': False,
        'export':  (lambda obj: 'Sí' if obj.is_active else 'No', 'Estado'),
    },
]

# ── Definición de columnas disponibles para Facturas ────────────────────────
INVOICE_ALL_COLUMNS = [
    {
        'key':     'id',
        'label':   'N° Factura',
        'default': True,
        'export':  ('id', 'N° Factura'),
    },
    {
        'key':     'customer',
        'label':   'Cliente',
        'default': True,
        'export':  (lambda obj: obj.customer.full_name, 'Cliente'),
    },
    {
        'key':     'invoice_date',
        'label':   'Fecha',
        'default': True,
        'export':  (lambda obj: obj.invoice_date.strftime('%d/%m/%Y %H:%M'), 'Fecha'),
    },
    {
        'key':     'subtotal',
        'label':   'Subtotal',
        'default': True,
        'export':  ('subtotal', 'Subtotal ($)'),
    },
    {
        'key':     'tax',
        'label':   'IVA',
        'default': True,
        'export':  ('tax', 'IVA ($)'),
    },
    {
        'key':     'total',
        'label':   'Total',
        'default': True,
        'export':  ('total', 'Total ($)'),
    },
]

# === REGISTRO ===
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'  
    success_url = reverse_lazy('billing:brand_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

# === BRAND (CBV) ===
class BrandListView(ExportMixin, LoginRequiredMixin, ListView):
    model = Brand
    template_name = 'billing/brand_list.html'
    context_object_name = 'items'
    paginate_by = 3
    export_filename = 'marcas'
    ALL_COLUMNS = BRAND_ALL_COLUMNS

    def get_active_col_keys(self):
        cols_param = self.request.GET.get('cols', '').strip()
        if cols_param:
            all_keys = {c['key'] for c in self.ALL_COLUMNS}
            valid = [k.strip() for k in cols_param.split(',') if k.strip() in all_keys]
            if valid:
                return valid
        return [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]

    def get_dynamic_export_fields(self):
        active = set(self.get_active_col_keys())
        return [
            col['export']
            for col in self.ALL_COLUMNS
            if col['key'] in active and col.get('export') is not None
        ]

    @property
    def export_fields(self):
        return self.get_dynamic_export_fields()

    def get_queryset(self):
        qs = Brand.objects.all()
        form = BrandSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('name'):
                qs = qs.filter(name__icontains=form.cleaned_data['name'])
            val = form.cleaned_data.get('is_active')
            if val in ('0', '1'):
                qs = qs.filter(is_active=(val == '1'))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = BrandSearchForm(self.request.GET)
        ctx['all_columns'] = self.ALL_COLUMNS
        ctx['all_col_keys_json'] = json.dumps([c['key'] for c in self.ALL_COLUMNS])
        ctx['default_col_keys_json'] = json.dumps(
            [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]
        )
        return ctx

@login_required
@audit_action('CREATE_BRAND')  
def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca Creada exitosamente!')
            return redirect('billing:brand_list')
    else: form = BrandForm()
    return render(request, 'billing/brand_form.html', {'form':form, 'title':'Crear Marca'})

@login_required
@audit_action('UPDATE_BRAND')  
def brand_update(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca actulizada exitosamente!')
            return redirect('billing:brand_list')
    else: form = BrandForm(instance=brand)
    return render(request, 'billing/brand_form.html', {'form':form, 'title':'Editar Marca'})

@login_required
@audit_action('DELETE_BRAND')
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand eliminada exitosamente!')
        return redirect('billing:brand_list')
    return render(request, 'billing/brand_confirm_delete.html', {'object': brand})

class BrandDetailView(LoginRequiredMixin, DetailView):
    model = Brand
    template_name = 'billing/brand_detail.html'
    context_object_name = 'brand'

# === PRODUCTGROUP (CBV) ===
class ProductGroupListView(ExportMixin, LoginRequiredMixin, ListView):
    model = ProductGroup
    template_name = 'billing/product_group_list.html'
    context_object_name = 'items'
    paginate_by = 3
    export_filename = 'grupos'
    ALL_COLUMNS = PRODUCTGROUP_ALL_COLUMNS

    def get_active_col_keys(self):
        cols_param = self.request.GET.get('cols', '').strip()
        if cols_param:
            all_keys = {c['key'] for c in self.ALL_COLUMNS}
            valid = [k.strip() for k in cols_param.split(',') if k.strip() in all_keys]
            if valid:
                return valid
        return [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]

    def get_dynamic_export_fields(self):
        active = set(self.get_active_col_keys())
        return [
            col['export']
            for col in self.ALL_COLUMNS
            if col['key'] in active and col.get('export') is not None
        ]

    @property
    def export_fields(self):
        return self.get_dynamic_export_fields()

    def get_queryset(self):
        qs = ProductGroup.objects.all()
        form = ProductGroupSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('name'):
                qs = qs.filter(name__icontains=form.cleaned_data['name'])
            val = form.cleaned_data.get('is_active')
            if val in ('0', '1'):
                qs = qs.filter(is_active=(val == '1'))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = ProductGroupSearchForm(self.request.GET)
        ctx['all_columns'] = self.ALL_COLUMNS
        ctx['all_col_keys_json'] = json.dumps([c['key'] for c in self.ALL_COLUMNS])
        ctx['default_col_keys_json'] = json.dumps(
            [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]
        )
        return ctx

class ProductGroupCreateView(LoginRequiredMixin, CreateView):
    model = ProductGroup; 
    form_class = ProductGroupForm; 
    template_name = 'billing/product_group_form.html'; 
    success_url = reverse_lazy('billing:productgroup_list')

class ProductGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductGroup; 
    form_class = ProductGroupForm; 
    template_name = 'billing/product_group_form.html'; 
    success_url = reverse_lazy('billing:productgroup_list')

class ProductGroupDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = ProductGroup;
    template_name = 'billing/product_group_confirm_delete.html';
    success_url = reverse_lazy('billing:productgroup_list')
    staff_redirect_url = '/groups/'

class ProductGroupDetailView(LoginRequiredMixin, DetailView):
    model = ProductGroup
    template_name = 'billing/product_group_detail.html'
    context_object_name = 'productgroup'

# === SUPPLIER (CBV) ===
class SupplierListView(ExportMixin, LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'billing/supplier_list.html'
    context_object_name = 'items'
    paginate_by = 3
    export_filename = 'proveedores'
    ALL_COLUMNS = SUPPLIER_ALL_COLUMNS

    def get_active_col_keys(self):
        cols_param = self.request.GET.get('cols', '').strip()
        if cols_param:
            all_keys = {c['key'] for c in self.ALL_COLUMNS}
            valid = [k.strip() for k in cols_param.split(',') if k.strip() in all_keys]
            if valid:
                return valid
        return [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]

    def get_dynamic_export_fields(self):
        active = set(self.get_active_col_keys())
        return [
            col['export']
            for col in self.ALL_COLUMNS
            if col['key'] in active and col.get('export') is not None
        ]

    @property
    def export_fields(self):
        return self.get_dynamic_export_fields()

    def get_queryset(self):
        qs = Supplier.objects.all()
        form = SupplierSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('name'):
                qs = qs.filter(name__icontains=form.cleaned_data['name'])
            if form.cleaned_data.get('contact_name'):
                qs = qs.filter(contact_name__icontains=form.cleaned_data['contact_name'])
            if form.cleaned_data.get('email'):
                qs = qs.filter(email__icontains=form.cleaned_data['email'])
            if form.cleaned_data.get('phone'):
                qs = qs.filter(phone__icontains=form.cleaned_data['phone'])
            val = form.cleaned_data.get('is_active')
            if val in ('0', '1'):
                qs = qs.filter(is_active=(val == '1'))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SupplierSearchForm(self.request.GET)
        ctx['all_columns'] = self.ALL_COLUMNS
        ctx['all_col_keys_json'] = json.dumps([c['key'] for c in self.ALL_COLUMNS])
        ctx['default_col_keys_json'] = json.dumps(
            [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]
        )
        return ctx

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier; form_class = SupplierForm; 
    template_name = 'billing/supplier_form.html'; 
    success_url = reverse_lazy('billing:supplier_list')
class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier; 
    form_class = SupplierForm; 
    template_name = 'billing/supplier_form.html'; 
    success_url = reverse_lazy('billing:supplier_list')
class SupplierDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Supplier;
    template_name = 'billing/supplier_confirm_delete.html';
    success_url = reverse_lazy('billing:supplier_list')
    staff_redirect_url = '/suppliers/'

class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'billing/supplier_detail.html'
    context_object_name = 'supplier'

# === PRODUCT (CBV) ===
class ProductListView(ExportMixin, LoginRequiredMixin, ListView):
    model = Product
    template_name = 'billing/product_list.html'
    context_object_name = 'items'
    paginate_by = 3
    export_filename = 'productos'
    ALL_COLUMNS = PRODUCT_ALL_COLUMNS

    def get_active_col_keys(self):
        cols_param = self.request.GET.get('cols', '').strip()
        if cols_param:
            all_keys = {c['key'] for c in self.ALL_COLUMNS}
            valid = [k.strip() for k in cols_param.split(',') if k.strip() in all_keys]
            if valid:
                return valid
        return [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]

    def get_dynamic_export_fields(self):
        active = set(self.get_active_col_keys())
        return [
            col['export']
            for col in self.ALL_COLUMNS
            if col['key'] in active and col.get('export') is not None
        ]

    def get_queryset(self):
        qs = (
            Product.objects
            .select_related('brand', 'group')
            .prefetch_related('suppliers')
            .order_by('name')
        )
        form = ProductSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('name'):
                qs = qs.filter(name__icontains=form.cleaned_data['name'])
            if form.cleaned_data.get('brand'):
                qs = qs.filter(brand=form.cleaned_data['brand'])
            if form.cleaned_data.get('group'):
                qs = qs.filter(group=form.cleaned_data['group'])
            if form.cleaned_data.get('supplier'):
                qs = qs.filter(suppliers=form.cleaned_data['supplier'])
            if form.cleaned_data.get('price_min') is not None:
                qs = qs.filter(unit_price__gte=form.cleaned_data['price_min'])
            if form.cleaned_data.get('price_max') is not None:
                qs = qs.filter(unit_price__lte=form.cleaned_data['price_max'])
            if form.cleaned_data.get('stock_min') is not None:
                qs = qs.filter(stock__gte=form.cleaned_data['stock_min'])
            if form.cleaned_data.get('stock_max') is not None:
                qs = qs.filter(stock__lte=form.cleaned_data['stock_max'])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = ProductSearchForm(self.request.GET)
        ctx['all_columns'] = self.ALL_COLUMNS
        ctx['all_col_keys_json'] = json.dumps([c['key'] for c in self.ALL_COLUMNS])
        ctx['default_col_keys_json'] = json.dumps(
            [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]
        )
        return ctx
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'billing/product_form.html'
    success_url = reverse_lazy('billing:product_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_edit'] = False
        ctx['page_title'] = 'Nuevo Producto'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.name}" creado exitosamente.')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'billing/product_form.html'
    success_url = reverse_lazy('billing:product_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_edit'] = True
        ctx['page_title'] = f'Editar: {self.object.name}'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.name}" actualizado exitosamente.')
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product; 
    template_name = 'billing/product_confirm_delete.html'; 
    success_url = reverse_lazy('billing:product_list')
    staff_redirect_url = '/products/'
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product; 
    template_name = 'billing/product_detail.html'; 
    context_object_name = 'product'



# === CUSTOMER (CBV) ===
class CustomerListView(ExportMixin, LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'billing/customer_list.html'
    context_object_name = 'items'
    paginate_by = 3
    export_filename = 'clientes'
    ALL_COLUMNS = CUSTOMER_ALL_COLUMNS

    def get_active_col_keys(self):
        cols_param = self.request.GET.get('cols', '').strip()
        if cols_param:
            all_keys = {c['key'] for c in self.ALL_COLUMNS}
            valid = [k.strip() for k in cols_param.split(',') if k.strip() in all_keys]
            if valid:
                return valid
        return [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]

    def get_dynamic_export_fields(self):
        active = set(self.get_active_col_keys())
        return [
            col['export']
            for col in self.ALL_COLUMNS
            if col['key'] in active and col.get('export') is not None
        ]

    @property
    def export_fields(self):
        return self.get_dynamic_export_fields()

    def get_queryset(self):
        qs = Customer.objects.all()
        form = CustomerSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('dni'):
                qs = qs.filter(dni__icontains=form.cleaned_data['dni'])
            if form.cleaned_data.get('last_name'):
                qs = qs.filter(last_name__icontains=form.cleaned_data['last_name'])
            if form.cleaned_data.get('first_name'):
                qs = qs.filter(first_name__icontains=form.cleaned_data['first_name'])
            if form.cleaned_data.get('email'):
                qs = qs.filter(email__icontains=form.cleaned_data['email'])
            if form.cleaned_data.get('phone'):
                qs = qs.filter(phone__icontains=form.cleaned_data['phone'])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = CustomerSearchForm(self.request.GET)
        ctx['all_columns'] = self.ALL_COLUMNS
        ctx['all_col_keys_json'] = json.dumps([c['key'] for c in self.ALL_COLUMNS])
        ctx['default_col_keys_json'] = json.dumps(
            [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]
        )
        return ctx

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer; 
    form_class = CustomerForm; 
    template_name = 'billing/customer_form.html'; 
    success_url = reverse_lazy('billing:customer_list')
class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer; 
    form_class = CustomerForm; 
    template_name = 'billing/customer_form.html'; 
    success_url = reverse_lazy('billing:customer_list')
class CustomerDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Customer; 
    template_name = 'billing/customer_confirm_delete.html'; 
    success_url = reverse_lazy('billing:customer_list')
    staff_redirect_url = '/customers/'

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'billing/customer_detail.html'
    context_object_name = 'customer'


# === INVOICE (CBV) ===
class InvoiceListView(ExportMixin, LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    context_object_name = 'items'
    paginate_by = 3
    export_filename = 'facturas'
    ALL_COLUMNS = INVOICE_ALL_COLUMNS

    def get_active_col_keys(self):
        cols_param = self.request.GET.get('cols', '').strip()
        if cols_param:
            all_keys = {c['key'] for c in self.ALL_COLUMNS}
            valid = [k.strip() for k in cols_param.split(',') if k.strip() in all_keys]
            if valid:
                return valid
        return [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]

    def get_dynamic_export_fields(self):
        active = set(self.get_active_col_keys())
        return [
            col['export']
            for col in self.ALL_COLUMNS
            if col['key'] in active and col.get('export') is not None
        ]

    @property
    def export_fields(self):
        return self.get_dynamic_export_fields()

    def get_queryset(self):
        qs = Invoice.objects.select_related('customer').order_by('-invoice_date')
        form = InvoiceSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('customer'):
                q = form.cleaned_data['customer']
                qs = qs.filter(
                    Q(customer__first_name__icontains=q) |
                    Q(customer__last_name__icontains=q) |
                    Q(customer__dni__icontains=q)
                )
            if form.cleaned_data.get('date_from'):
                qs = qs.filter(invoice_date__date__gte=form.cleaned_data['date_from'])
            if form.cleaned_data.get('date_to'):
                qs = qs.filter(invoice_date__date__lte=form.cleaned_data['date_to'])
            if form.cleaned_data.get('total_min') is not None:
                qs = qs.filter(total__gte=form.cleaned_data['total_min'])
            if form.cleaned_data.get('total_max') is not None:
                qs = qs.filter(total__lte=form.cleaned_data['total_max'])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = InvoiceSearchForm(self.request.GET)
        ctx['all_columns'] = self.ALL_COLUMNS
        ctx['all_col_keys_json'] = json.dumps([c['key'] for c in self.ALL_COLUMNS])
        ctx['default_col_keys_json'] = json.dumps(
            [c['key'] for c in self.ALL_COLUMNS if c.get('default', True)]
        )
        return ctx

@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            formset.save()

            subtotal = sum(d.subtotal for d in invoice.details.all())
            invoice.subtotal = subtotal
            invoice.tax = subtotal * Decimal('0.15')
            invoice.total = invoice.subtotal + invoice.tax
            invoice.save()

            messages.success(request, f'Factura #{invoice.id} creada! Total: ${invoice.total}')
            return redirect('billing:invoice_list')
    else:
        form = InvoiceForm()
        formset = InvoiceDetailFormSet()
    return render(request, 'billing/invoice_form.html', {
        'form': form, 'formset': formset, 'title': 'Nueva Factura'
    })
class InvoiceDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Invoice; 
    template_name = 'billing/invoice_confirm_delete.html'; 
    success_url = reverse_lazy('billing:invoice_list')
    staff_redirect_url = '/invoices/'

@login_required
def invoice_detail(request, pk):
    """Muestra el detalle completo de una factura."""
    invoice = get_object_or_404(
        Invoice.objects.select_related('customer')
                       .prefetch_related('details__product'),
        pk=pk
    )
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})