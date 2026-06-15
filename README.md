# 🧾 Sistema de Ventas y Facturación (Sales_A2)

Aplicación web desarrollada en **Django** para la gestión de un sistema de ventas y facturación. Permite administrar marcas, grupos de productos, proveedores, productos, clientes y facturas, incluyendo el cálculo automático de impuestos (IVA) y subtotales.

> Proyecto académico — Ingeniería de Software, Universidad Estatal de Milagro (UNEMI).

---

## 📑 Tabla de contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Modelo de datos](#-modelo-de-datos)
- [Requisitos previos](#-requisitos-previos)
- [Instalación y configuración](#-instalación-y-configuración)
- [Ejecución](#-ejecución)
- [Uso de la aplicación](#-uso-de-la-aplicación)
- [Decisiones de diseño](#-decisiones-de-diseño)
- [Notas y pendientes](#-notas-y-pendientes)

---

## ✨ Características

- **CRUD completo** para 6 módulos: Marcas, Grupos de productos, Proveedores, Productos, Clientes y Facturas.
- **Sistema de facturación** con líneas de detalle dinámicas (agregar/quitar productos en la misma pantalla).
- **Cálculo automático** de subtotal, IVA (15%) y total al guardar una factura.
- **Autenticación de usuarios**: registro (signup), inicio y cierre de sesión.
- **Acceso protegido**: todas las pantallas requieren sesión iniciada.
- **Interfaz responsiva** con Bootstrap 5.
- **Panel de administración** de Django habilitado para todos los modelos.

---

## 🛠 Tecnologías

| Componente        | Tecnología                     |
|-------------------|--------------------------------|
| Lenguaje          | Python 3.13                    |
| Framework         | Django 6.0.6                   |
| Base de datos     | SQLite 3                       |
| Frontend          | Bootstrap 5.3 (vía CDN)        |
| Estilos en forms  | django-widget-tweaks 1.5.1     |
| Idioma / Zona     | Español (es-ec) / UTC          |

---

## 📂 Estructura del proyecto

```
Sales_A2/
├── config/                     # Configuración del proyecto Django
│   ├── settings.py             # Ajustes (BD, apps, idioma, login)
│   ├── urls.py                 # Rutas raíz (admin, accounts, billing)
│   ├── asgi.py / wsgi.py       # Puntos de entrada del servidor
│   └── __init__.py
│
├── billing/                    # App principal (lógica de negocio)
│   ├── migrations/             # Migraciones de la base de datos
│   ├── templates/billing/      # Plantillas HTML del módulo
│   │   ├── base.html           # Plantilla base (navbar, footer, mensajes)
│   │   ├── *_list.html         # Listados de cada entidad
│   │   ├── *_form.html         # Formularios de crear/editar
│   │   └── *_confirm_delete.html  # Confirmaciones de borrado
│   ├── models.py               # Modelos (8 entidades)
│   ├── views.py                # Vistas (FBV + CBV)
│   ├── forms.py                # Formularios y formset de factura
│   ├── urls.py                 # Rutas de la app billing
│   └── admin.py                # Registro de modelos en el admin
│
├── templates/
│   └── registration/           # Plantillas de autenticación
│       ├── login.html
│       └── signup.html
│
├── static/                     # Archivos estáticos (CSS/JS/imágenes)
├── dbsalesA2.sqlite3           # Base de datos SQLite
├── manage.py                   # Utilidad de gestión de Django
├── requirements.txt            # Dependencias del proyecto
└── README.md
```

---

## 🗃 Modelo de datos

El sistema se compone de **8 entidades** relacionadas entre sí.

### Diagrama entidad–relación

```mermaid
erDiagram
    BRAND ||--o{ PRODUCT : "tiene"
    PRODUCT_GROUP ||--o{ PRODUCT : "agrupa"
    PRODUCT }o--o{ SUPPLIER : "es provisto por"
    CUSTOMER ||--|| CUSTOMER_PROFILE : "tiene perfil"
    CUSTOMER ||--o{ INVOICE : "genera"
    INVOICE ||--o{ INVOICE_DETAIL : "contiene"
    PRODUCT ||--o{ INVOICE_DETAIL : "aparece en"
```

### Descripción de las entidades

**Brand** (Marca) — Marcas de los productos.

| Campo        | Tipo          | Notas                  |
|--------------|---------------|------------------------|
| name         | CharField     | Único, obligatorio     |
| description  | TextField     | Opcional               |
| is_active    | BooleanField  | Por defecto `True`     |
| created_at   | DateTimeField | Automático al crear    |
| updated_at   | DateTimeField | Automático al editar   |

**ProductGroup** (Grupo de productos) — Categorías de productos.

| Campo      | Tipo         | Notas              |
|------------|--------------|--------------------|
| name       | CharField    | Único, obligatorio |
| is_active  | BooleanField | Por defecto `True` |

**Supplier** (Proveedor) — Empresas que abastecen productos.

| Campo         | Tipo        | Notas                          |
|---------------|-------------|--------------------------------|
| name          | CharField   | Nombre de la compañía          |
| contact_name  | CharField   | Persona de contacto (opcional) |
| email         | EmailField  | Opcional                       |
| phone         | CharField   | Opcional                       |
| address       | TextField   | Opcional                       |
| is_active     | BooleanField| Por defecto `True`             |

**Product** (Producto) — Artículos a la venta.

| Campo       | Tipo                | Notas                                  |
|-------------|---------------------|----------------------------------------|
| name        | CharField           | Obligatorio                            |
| description | TextField           | Opcional                               |
| brand       | ForeignKey → Brand  | `PROTECT` (no borra si está en uso)    |
| group       | ForeignKey → Group  | `PROTECT`                              |
| suppliers   | ManyToMany → Supplier | Varios proveedores por producto      |
| unit_price  | DecimalField        | Precio unitario                        |
| stock       | IntegerField        | Existencias, por defecto `0`           |

**Customer** (Cliente) — Personas o empresas que compran.

| Campo       | Tipo        | Notas                       |
|-------------|-------------|-----------------------------|
| dni         | CharField   | DNI/RUC, único              |
| first_name  | CharField   | Nombre                      |
| last_name   | CharField   | Apellido                    |
| email       | EmailField  | Opcional                    |
| phone       | CharField   | Opcional                    |
| address     | TextField   | Opcional                    |

> Incluye la propiedad `full_name` que devuelve `nombre + apellido`.

**CustomerProfile** (Perfil del cliente) — Datos extendidos, relación 1:1 con Customer.

| Campo         | Tipo         | Notas                                          |
|---------------|--------------|------------------------------------------------|
| taxpayer_type | CharField    | Tipo de contribuyente (Final/RUC/RISE)         |
| payment_terms | CharField    | Forma de pago (contado / crédito 15/30/60 días)|
| credit_limit  | DecimalField | Límite de crédito                              |
| notes         | TextField    | Observaciones                                  |

**Invoice** (Factura) — Cabecera de la factura.

| Campo        | Tipo                  | Notas                              |
|--------------|-----------------------|------------------------------------|
| customer     | ForeignKey → Customer | `PROTECT`                          |
| invoice_date | DateTimeField         | Fecha automática al crear          |
| subtotal     | DecimalField          | Calculado por la vista             |
| tax          | DecimalField          | IVA (15%), calculado por la vista  |
| total        | DecimalField          | `subtotal + tax`, calculado        |

**InvoiceDetail** (Detalle de factura) — Líneas de la factura.

| Campo      | Tipo                  | Notas                                       |
|------------|-----------------------|---------------------------------------------|
| invoice    | ForeignKey → Invoice  | `CASCADE` (se borra con la factura)         |
| product    | ForeignKey → Product  | `PROTECT`                                   |
| quantity   | IntegerField          | Cantidad, por defecto `1`                   |
| unit_price | DecimalField          | Precio unitario                             |
| subtotal   | DecimalField          | Calculado automáticamente: `cantidad × precio` |

---

## 📋 Requisitos previos

- **Python 3.13** (o compatible) instalado y disponible en el PATH.
- **pip** (incluido con Python).
- Verifica la instalación con:

```bash
python --version
pip --version
```

---

## ⚙️ Instalación y configuración

> Los comandos están pensados para **Windows (CMD)**. En Linux/Mac se activa el entorno con `source ent_sales_A2/bin/activate`.

**1. Ubícate en la carpeta del proyecto**

```cmd
cd Sales_A2
```

**2. Crea un entorno virtual**

```cmd
python -m venv ent_sales_A2
```

> El entorno virtual **no se comparte entre computadoras**. Si copiaste el proyecto de otra PC, borra la carpeta `ent_sales_A2` y vuelve a crearla con este comando.

**3. Activa el entorno virtual**

```cmd
ent_sales_A2\Scripts\activate
```

**4. Instala las dependencias**

```cmd
pip install -r requirements.txt
```

**5. Aplica las migraciones** (crea/actualiza las tablas de la base de datos)

```cmd
python manage.py migrate
```

**6. Crea un superusuario** (para acceder al admin y poder iniciar sesión)

```cmd
python manage.py createsuperuser
```

---

## ▶️ Ejecución

Con el entorno virtual activado:

```cmd
python manage.py runserver
```

Luego abre en el navegador:

| Recurso              | URL                                      |
|----------------------|------------------------------------------|
| Aplicación           | http://127.0.0.1:8000/                   |
| Panel de administración | http://127.0.0.1:8000/admin/          |
| Inicio de sesión     | http://127.0.0.1:8000/accounts/login/    |
| Registro             | http://127.0.0.1:8000/signup/            |

---

## 🧭 Uso de la aplicación

1. **Regístrate o inicia sesión.** Sin sesión activa, todas las pantallas redirigen al login.
2. **Carga los catálogos base** en este orden recomendado:
   - Marcas → Grupos → Proveedores → Productos → Clientes
   - (Un producto necesita una marca y un grupo existentes; una factura necesita clientes y productos).
3. **Crea una factura:**
   - Selecciona el cliente.
   - Agrega una o varias líneas de detalle (producto, cantidad, precio) con el botón **+ Agregar producto**.
   - Al guardar, el sistema calcula automáticamente:
     - `subtotal` = suma de los subtotales de cada línea
     - `tax` = 15% del subtotal (IVA)
     - `total` = subtotal + IVA

### Rutas principales

| Módulo      | Listado          | Crear                    |
|-------------|------------------|--------------------------|
| Marcas      | `/brands/`       | `/brands/create/`        |
| Grupos      | `/groups/`       | `/groups/create/`        |
| Proveedores | `/suppliers/`    | `/suppliers/create/`     |
| Productos   | `/products/`     | `/products/create/`      |
| Clientes    | `/customers/`    | `/customers/create/`     |
| Facturas    | `/invoices/`     | `/invoices/create/`      |

---

## 🧩 Decisiones de diseño

Esta sección explica el *por qué* de las principales decisiones técnicas.

### Vistas basadas en funciones (FBV) vs. en clases (CBV)

El proyecto combina ambos enfoques de forma intencional:

- **FBV** (`brand_*`, `invoice_create`): se usan donde conviene controlar manualmente el flujo `GET`/`POST`. El caso de **factura** lo requiere porque coordina **dos formularios a la vez** (la cabecera y el *formset* de detalles) y además calcula los totales antes de guardar — algo que en una vista genérica resulta forzado.
- **CBV** (`ProductGroup`, `Supplier`, `Product`, `Customer`): usan las vistas genéricas de Django (`ListView`, `CreateView`, `UpdateView`, `DeleteView`), que reducen el código repetitivo de un CRUD estándar.

### Bootstrap en los templates (no en `forms.py`)

Para las vistas en clases, las clases de Bootstrap se aplican en la **plantilla** mediante `django-widget-tweaks` (`{% render_field field class="form-control" %}`), no en los widgets del formulario. Esto mantiene `forms.py` libre de detalles de presentación (separación de responsabilidades): el formulario define *qué datos* se piden, y la plantilla define *cómo se ven*.

> Excepción: el formulario de factura (`InvoiceForm` / `InvoiceDetailFormSet`) sí define las clases en los widgets, porque su plantilla renderiza los campos directamente con `{{ field }}` para construir la tabla de detalles.

### Integridad referencial (`on_delete`)

- **`PROTECT`** en `Product.brand`, `Product.group`, `Invoice.customer` e `InvoiceDetail.product`: impide borrar un registro que está siendo usado (no se puede eliminar una marca si tiene productos asociados, por ejemplo). Protege la consistencia de los datos.
- **`CASCADE`** en `InvoiceDetail.invoice`: al eliminar una factura, sus líneas de detalle se eliminan automáticamente (no tiene sentido conservar detalles huérfanos).

### Cálculos automáticos

- `InvoiceDetail.subtotal` se calcula solo al guardar (`save()` sobrescrito): `cantidad × precio_unitario`.
- Los totales de la factura se calculan en la vista `invoice_create`, aplicando el **IVA del 15%** vigente en Ecuador.

### Seguridad

- Todas las vistas de negocio exigen sesión iniciada (decorador `@login_required` en FBV y `LoginRequiredMixin` en CBV).
- El cierre de sesión se hace por **POST** (no por GET) para evitar cierres accidentales, e incluye `{% csrf_token %}` como protección contra ataques CSRF.

---

## 📝 Notas y pendientes

- **`requirements.txt`** incluye paquetes que no pertenecen a este proyecto (Flask, Jinja2, Werkzeug, etc.), probablemente arrastrados de otro entorno. Para un proyecto Django limpio, las dependencias necesarias son únicamente: `Django`, `asgiref`, `sqlparse`, `tzdata` y `django-widget-tweaks`.
- **Etiquetas (`verbose_name`) cruzadas en `models.py`:** en el modelo `Invoice`, el campo `total` tiene `verbose_name='Activo'` y el campo `customer` tiene `verbose_name='Factura'`. No afectan el funcionamiento, pero conviene corregirlas para que las etiquetas coincidan con el dato real.
- **Mensajes de error:** para que las alertas de tipo error se muestren en rojo, agrega en `settings.py`:
  ```python
  from django.contrib.messages import constants as messages
  MESSAGE_TAGS = {messages.ERROR: 'danger'}
  ```

---

## 👨‍💻 Autor

Proyecto desarrollado por **Anthony** — Ingeniería de Software, UNEMI.
