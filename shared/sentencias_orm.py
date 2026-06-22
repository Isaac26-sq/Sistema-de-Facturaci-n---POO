# CREATE

#  In [1]: samsung = Brand.objects.create(name='Samsung', description='Electronics')
# INSERT INTO "billing_brand" ("name", "description", "is_active", "created_at", "updated_at")
# VALUES ('Samsung', 'Electronics', 1, '2026-06-22 01:51:44.725399', '2026-06-22 01:51:44.725428') RETURNING "billing_brand"."id"
# Execution time: 0.000297s [Database: default]

# In [2]: apple = Brand.objects.create(name='Apple')

# INSERT INTO "billing_brand" ("name", "description", "is_active", "created_at", "updated_at")
# VALUES ('Apple', NULL, 1, '2026-06-22 01:50:24.482443', '2026-06-22 01:50:24.482490') RETURNING "billing_brand"."id"

# Execution time: 0.001708s [Database: default]

# In [3]: electronics = ProductGroup.objects.create(name='Electronics')
# INSERT INTO "billing_productgroup" ("name", "is_active", "created_at", "updated_at")
# VALUES ('Electronics', 1, '2026-06-22 01:53:05.912144', '2026-06-22 01:53:05.912163') RETURNING "billing_productgroup"."id"

# Execution time: 0.002287s [Database: default]

# In [4]: dist = Supplier.objects.create(name='TechDist', email='info@tech.com')
# INSERT INTO "billing_supplier" ("name", "contact_name", "email", "phone", "address", "is_active", "created_at", "updated_at")
# VALUES ('TechDist', NULL, 'info@tech.com', NULL, NULL, 1, '2026-06-22 01:53:35.182849', '2026-06-22 01:53:35.182870') RETURNING "billing_supplier"."id"

# Execution time: 0.002105s [Database: default]

# In [5]: global_s = Supplier.objects.create(name='GlobalSupply')
# INSERT INTO "billing_supplier" ("name", "contact_name", "email", "phone", "address", "is_active", "created_at", "updated_at")
# VALUES ('GlobalSupply', NULL, NULL, NULL, NULL, 1, '2026-06-22 01:54:29.145354', '2026-06-22 01:54:29.145369') RETURNING "billing_supplier"."id"

# Execution time: 0.001747s [Database: default]

# In [6]: phone = Product.objects.create(name='Galaxy S24', brand=samsung, group=electronics, unit_price=999.99, stock=50)
# INSERT INTO "billing_product" ("name", "description", "brand_id", "group_id", "unit_price", "stock", "image", "is_active", "created_at", "updated_at")
# VALUES ('Galaxy S24', NULL, 10, 5, '999.990000000', 50, '', 1, '2026-06-22 02:13:54.728641', '2026-06-22 02:13:54.728673') RETURNING "billing_product"."id"

# Execution time: 0.002147s [Database: default]

# In [7]: phone.suppliers.add(dist, global_s)
# BEGIN

# Execution time: 0.000034s [Database: default]
# INSERT
#     OR
# IGNORE INTO "billing_product_suppliers" ("product_id", "supplier_id")
# VALUES (5, 6), (5, 7)

# Execution time: 0.001592s [Database: default]

# In [8]: client = Customer.objects.create(dni='0912345678', first_name='Juan', last_name='Perez')
# INSERT INTO "billing_customer" ("dni", "first_name", "last_name", "email", "phone", "address", "is_active", "created_at", "updated_at")
# VALUES ('0912345678', 'Juan', 'Perez', NULL, NULL, NULL, 1, '2026-06-22 02:14:52.865441', '2026-06-22 02:14:52.865463') RETURNING "billing_customer"."id"

# Execution time: 0.001027s [Database: default]

# In [9]: profile = CustomerProfile.objects.create(customer=client, taxpayer_type='ruc', payment_terms='credit_30', credit_limit=5000)
# INSERT INTO "billing_customerprofile" ("customer_id", "taxpayer_type", "payment_terms", "credit_limit", "notes")
# VALUES (5, 'ruc', 'credit_30', '5000', NULL) RETURNING "billing_customerprofile"."id"

# Execution time: 0.001815s [Database: default]


# In [10]: inv = Invoice.objects.create(customer=client, subtotal=999.99, tax=120, total=1119.99)
# INSERT INTO "billing_invoice" ("customer_id", "invoice_date", "subtotal", "tax", "total", "is_active")
# VALUES (5, '2026-06-22 02:21:31.660917', '999.990000000', '120', '1119.99000000', 1) RETURNING "billing_invoice"."id"

# Execution time: 0.002084s [Database: default]

# In [11]: det = InvoiceDetail.objects.create(invoice=inv, product=phone, quantity=1, unit_price=phone.unit_price)
# INSERT INTO "billing_invoicedetail" ("invoice_id", "product_id", "quantity", "unit_price", "subtotal")
# VALUES (10, 5, 1, '999.990000000', '999.990000000') RETURNING "billing_invoicedetail"."id"

# Execution time: 0.001035s [Database: default]

# In [11]: Brand.objects.create(name='Nike')
# INSERT INTO "billing_brand" ("name", "description", "is_active", "created_at", "updated_at")
# VALUES ('Nike', NULL, 1, '2026-06-22 02:46:53.581238', '2026-06-22 02:46:53.581263') RETURNING "billing_brand"."id"

# Execution time: 0.001484s [Database: default]
# Out[11]: <Brand: Nike>

# READ 

# In [26]: Brand.objects.all()
# Out[26]: SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  ORDER BY "billing_brand"."name" ASC
#  LIMIT 21

# Execution time: 0.000297s [Database: default]
# <QuerySet [<Brand: Apple>, <Brand: Samsung>]>

# In [27]: Brand.objects.get(name='Samsung')
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."name" = 'Samsung'
#  LIMIT 21

# Execution time: 0.000176s [Database: default]
# Out[27]: <Brand: Samsung>

# In [28]: Product.objects.filter(unit_price__gt=500)
# Out[28]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  WHERE "billing_product"."unit_price" > '500'
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000287s [Database: default]
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."id" = 10
#  LIMIT 21

# Execution time: 0.000201s [Database: default]
# <QuerySet [<Product: Galaxy S24 (Samsung)>]>

# In [29]: Product.objects.filter(unit_price__range=(100,500))
# Out[29]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  WHERE "billing_product"."unit_price" BETWEEN '100' AND '500'
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000295s [Database: default]
# <QuerySet []>

# In [30]: Product.objects.filter(name__icontains='gal')
# Out[30]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  WHERE "billing_product"."name" LIKE '%gal%' ESCAPE '\'
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000446s [Database: default]
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."id" = 10
#  LIMIT 21

# Execution time: 0.000241s [Database: default]
# <QuerySet [<Product: Galaxy S24 (Samsung)>]>

# In [31]: Product.objects.exclude(stock=0)
# Out[31]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  WHERE NOT ("billing_product"."stock" = 0)
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000227s [Database: default]
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."id" = 10
#  LIMIT 21

# Execution time: 0.000249s [Database: default]
# <QuerySet [<Product: Galaxy S24 (Samsung)>]>


# In [32]: Product.objects.order_by('-unit_price')
# Out[32]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  ORDER BY "billing_product"."unit_price" DESC
#  LIMIT 21

# Execution time: 0.000326s [Database: default]
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."id" = 10
#  LIMIT 21

# Execution time: 0.000323s [Database: default]
# <QuerySet [<Product: Galaxy S24 (Samsung)>]>

# In [33]: Product.objects.count()
# SELECT COUNT(*) AS "__count"
#   FROM "billing_product"

# Execution time: 0.000193s [Database: default]
# Out[33]: 1

# In [34]: Product.objects.filter(stock=0).exists()
# SELECT 1 AS "a"
#   FROM "billing_product"
#  WHERE "billing_product"."stock" = 0
#  LIMIT 1

# Execution time: 0.000226s [Database: default]
# Out[34]: False


# UPDATE

# In [35]: b = Brand.objects.get(name='Samsung'); b.description = 'Updated'; b.save()
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."name" = 'Samsung'
#  LIMIT 21

# Execution time: 0.000189s [Database: default]
# UPDATE "billing_brand"
#    SET "name" = 'Samsung',
#        "description" = 'Updated',
#        "is_active" = 1,
#        "created_at" = '2026-06-22 02:12:33.263224',
#        "updated_at" = '2026-06-22 02:27:07.625892'
#  WHERE "billing_brand"."id" = 10

# Execution time: 0.003914s [Database: default]

# In [36]: p = Product.objects.get(name='Galaxy S24')
# SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  WHERE "billing_product"."name" = 'Galaxy S24'
#  LIMIT 21

# Execution time: 0.000187s [Database: default]

# In [37]: p.suppliers.add(global_s)
# BEGIN

# Execution time: 0.000028s [Database: default]
# INSERT
#     OR
# IGNORE INTO "billing_product_suppliers" ("product_id", "supplier_id")
# VALUES (5, 7)

# Execution time: 0.000885s [Database: default]

# In [38]: p.suppliers.remove(global_s)
# BEGIN

# Execution time: 0.000036s [Database: default]
# DELETE
#   FROM "billing_product_suppliers"
#  WHERE ("billing_product_suppliers"."product_id" = 5 AND "billing_product_suppliers"."supplier_id" IN (7))

# Execution time: 0.001146s [Database: default]

# In [39]: p.suppliers.clear()
# BEGIN

# Execution time: 0.000044s [Database: default]
# DELETE
#   FROM "billing_product_suppliers"
#  WHERE "billing_product_suppliers"."product_id" = 5

# Execution time: 0.001305s [Database: default]

# In [40]: p.suppliers.set([dist])
# BEGIN

# Execution time: 0.000034s [Database: default]
# SELECT "billing_supplier"."id" AS "id"
#   FROM "billing_supplier"
#  INNER JOIN "billing_product_suppliers"
#     ON ("billing_supplier"."id" = "billing_product_suppliers"."supplier_id")
#  WHERE "billing_product_suppliers"."product_id" = 5
#  ORDER BY "billing_supplier"."name" ASC

# Execution time: 0.000208s [Database: default]
# INSERT
#     OR
# IGNORE INTO "billing_product_suppliers" ("product_id", "supplier_id")
# VALUES (5, 6)

# Execution time: 0.001167s [Database: default]


# In [41]: c = Customer.objects.get(dni='0912345678')
# SELECT "billing_customer"."id",
#        "billing_customer"."dni",
#        "billing_customer"."first_name",
#        "billing_customer"."last_name",
#        "billing_customer"."email",
#        "billing_customer"."phone",
#        "billing_customer"."address",
#        "billing_customer"."is_active",
#        "billing_customer"."created_at",
#        "billing_customer"."updated_at"
#   FROM "billing_customer"
#  WHERE "billing_customer"."dni" = '0912345678'
#  LIMIT 21

# Execution time: 0.000200s [Database: default]

# In [42]: c.profile.credit_limit = 10000; c.profile.save()
# SELECT "billing_customerprofile"."id",
#        "billing_customerprofile"."customer_id",
#        "billing_customerprofile"."taxpayer_type",
#        "billing_customerprofile"."payment_terms",
#        "billing_customerprofile"."credit_limit",
#        "billing_customerprofile"."notes"
#   FROM "billing_customerprofile"
#  WHERE "billing_customerprofile"."customer_id" = 5
#  LIMIT 21

# Execution time: 0.000190s [Database: default]
# UPDATE "billing_customerprofile"
#    SET "customer_id" = 5,
#        "taxpayer_type" = 'ruc',
#        "payment_terms" = 'credit_30',
#        "credit_limit" = '10000',
#        "notes" = NULL
#  WHERE "billing_customerprofile"."id" = 3

# Execution time: 0.003536s [Database: default]

# In [44]: Product.objects.update(unit_price=F('unit_price') * 1.10)
# UPDATE "billing_product"
#    SET "unit_price" = ("billing_product"."unit_price" * 1.1)

# Execution time: 0.005159s [Database: default]
# Out[44]: 1


# DELETE

# In [47]: Brand.objects.get(name='Nike').delete()
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."name" = 'Nike'
#  LIMIT 21

# Execution time: 0.000180s [Database: default]
# SELECT "billing_product"."id"
#   FROM "billing_product"
#  WHERE "billing_product"."brand_id" IN (12)
#  ORDER BY "billing_product"."name" ASC

# Execution time: 0.000141s [Database: default]
# BEGIN

# Execution time: 0.000030s [Database: default]
# DELETE
#   FROM "billing_brand"
#  WHERE "billing_brand"."id" IN (12)

# Execution time: 0.001024s [Database: default]
# Out[47]: (1, {'billing.Brand': 1})

# In [48]: Brand.objects.filter(name='Nike').delete()
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."name" = 'Nike'

# Execution time: 0.000182s [Database: default]
# BEGIN

# Execution time: 0.000026s [Database: default]
# Out[48]: (0, {})

# In [50]: phone.suppliers.remove(dist)
# BEGIN

# Execution time: 0.000033s [Database: default]
# DELETE
#   FROM "billing_product_suppliers"
#  WHERE ("billing_product_suppliers"."product_id" = 5 AND "billing_product_suppliers"."supplier_id" IN (6))

# Execution time: 0.001202s [Database: default]


# Relaciones

# In [52]: phone.brand.name
# Out[52]: 'Samsung'

# In [53]: samsung.products.all()
# Out[53]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  WHERE "billing_product"."brand_id" = 10
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000580s [Database: default]
# <QuerySet [<Product: Galaxy S24 (Samsung)>]>

# In [54]: phone.suppliers.all()
# Out[54]: SELECT "billing_supplier"."id",
#        "billing_supplier"."name",
#        "billing_supplier"."contact_name",
#        "billing_supplier"."email",
#        "billing_supplier"."phone",
#        "billing_supplier"."address",
#        "billing_supplier"."is_active",
#        "billing_supplier"."created_at",
#        "billing_supplier"."updated_at"
#   FROM "billing_supplier"
#  INNER JOIN "billing_product_suppliers"
#     ON ("billing_supplier"."id" = "billing_product_suppliers"."supplier_id")
#  WHERE "billing_product_suppliers"."product_id" = 5
#  ORDER BY "billing_supplier"."name" ASC
#  LIMIT 21

# Execution time: 0.000274s [Database: default]
# <QuerySet []> 

# In [55]: phone.suppliers.all()
# Out[55]: SELECT "billing_supplier"."id",
#        "billing_supplier"."name",
#        "billing_supplier"."contact_name",
#        "billing_supplier"."email",
#        "billing_supplier"."phone",
#        "billing_supplier"."address",
#        "billing_supplier"."is_active",
#        "billing_supplier"."created_at",
#        "billing_supplier"."updated_at"
#   FROM "billing_supplier"
#  INNER JOIN "billing_product_suppliers"
#     ON ("billing_supplier"."id" = "billing_product_suppliers"."supplier_id")
#  WHERE "billing_product_suppliers"."product_id" = 5
#  ORDER BY "billing_supplier"."name" ASC
#  LIMIT 21

# Execution time: 0.000147s [Database: default]
# <QuerySet []>

# In [56]: dist.products.all()
# Out[56]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  INNER JOIN "billing_product_suppliers"
#     ON ("billing_product"."id" = "billing_product_suppliers"."product_id")
#  WHERE "billing_product_suppliers"."supplier_id" = 6
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000376s [Database: default]
# <QuerySet []>

# In [57]: Product.objects.filter(suppliers__name='TechDist')
# Out[57]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  INNER JOIN "billing_product_suppliers"
#     ON ("billing_product"."id" = "billing_product_suppliers"."product_id")
#  INNER JOIN "billing_supplier"
#     ON ("billing_product_suppliers"."supplier_id" = "billing_supplier"."id")
#  WHERE "billing_supplier"."name" = 'TechDist'
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000269s [Database: default]
# <QuerySet []>

# In [58]: client.profile.credit_limit
# Out[58]: 5000

# In [59]: Customer.objects.filter(profile__taxpayer_type='ruc')
# Out[59]: SELECT "billing_customer"."id",
#        "billing_customer"."dni",
#        "billing_customer"."first_name",
#        "billing_customer"."last_name",
#        "billing_customer"."email",
#        "billing_customer"."phone",
#        "billing_customer"."address",
#        "billing_customer"."is_active",
#        "billing_customer"."created_at",
#        "billing_customer"."updated_at"
#   FROM "billing_customer"
#  INNER JOIN "billing_customerprofile"
#     ON ("billing_customer"."id" = "billing_customerprofile"."customer_id")
#  WHERE "billing_customerprofile"."taxpayer_type" = 'ruc'
#  ORDER BY "billing_customer"."last_name" ASC,
#           "billing_customer"."first_name" ASC
#  LIMIT 21

# Execution time: 0.000236s [Database: default]
# <QuerySet [<Customer: Perez, Juan>]>


# In [60]: from django.db.models import Q

# In [61]: Product.objects.filter(Q(brand__name='Samsung') | Q(unit_price__gt=1000))
# Out[61]: SELECT "billing_product"."id",
#        "billing_product"."name",
#        "billing_product"."description",
#        "billing_product"."brand_id",
#        "billing_product"."group_id",
#        "billing_product"."unit_price",
#        "billing_product"."stock",
#        "billing_product"."image",
#        "billing_product"."is_active",
#        "billing_product"."created_at",
#        "billing_product"."updated_at"
#   FROM "billing_product"
#  INNER JOIN "billing_brand"
#     ON ("billing_product"."brand_id" = "billing_brand"."id")
#  WHERE ("billing_brand"."name" = 'Samsung' OR "billing_product"."unit_price" > '1000')
#  ORDER BY "billing_product"."name" ASC
#  LIMIT 21

# Execution time: 0.000276s [Database: default]
# SELECT "billing_brand"."id",
#        "billing_brand"."name",
#        "billing_brand"."description",
#        "billing_brand"."is_active",
#        "billing_brand"."created_at",
#        "billing_brand"."updated_at"
#   FROM "billing_brand"
#  WHERE "billing_brand"."id" = 10
#  LIMIT 21

# Execution time: 0.000208s [Database: default]
# <QuerySet [<Product: Galaxy S24 (Samsung)>]>

# -----------------------  Agregaciones   -----------------------

# In [62]: from django.db.models import Sum, Avg, Max, Min, Count

# In [63]: Product.objects.aggregate(avg=Avg('unit_price'))
# SELECT (CAST(AVG("billing_product"."unit_price") AS NUMERIC)) AS "avg"
#   FROM "billing_product"

# Execution time: 0.000301s [Database: default]
# Out[63]: {'avg': Decimal('1099.98900000000')}


# In [64]: Product.objects.aggregate(max=Max('unit_price'), min=Min('unit_price'))
# SELECT (CAST(MAX("billing_product"."unit_price") AS NUMERIC)) AS "max",
#        (CAST(MIN("billing_product"."unit_price") AS NUMERIC)) AS "min"
#   FROM "billing_product"

# Execution time: 0.000301s [Database: default]
# Out[64]: {'max': Decimal('1099.98900000000'), 'min': Decimal('1099.98900000000')}

# In [65]: Invoice.objects.filter(customer__dni='0912345678').aggregate(total=Sum('total'))
# SELECT (CAST(SUM("billing_invoice"."total") AS NUMERIC)) AS "total"
#   FROM "billing_invoice"
#  INNER JOIN "billing_customer"
#     ON ("billing_invoice"."customer_id" = "billing_customer"."id")
#  WHERE "billing_customer"."dni" = '0912345678'

# Execution time: 0.000255s [Database: default]
# Out[65]: {'total': Decimal('1119.99000000000')}

# In [66]: Brand.objects.annotate(n=Count('products')).values('name', 'n')
# Out[66]: SELECT "billing_brand"."name" AS "name",
#        COUNT("billing_product"."id") AS "n"
#   FROM "billing_brand"
#   LEFT OUTER JOIN "billing_product"
#     ON ("billing_brand"."id" = "billing_product"."brand_id")
#  GROUP BY "billing_brand"."id",
#           1,
#           "billing_brand"."description",
#           "billing_brand"."is_active",
#           "billing_brand"."created_at",
#           "billing_brand"."updated_at"
#  LIMIT 21

# Execution time: 0.000283s [Database: default]
# <QuerySet [{'name': 'Samsung', 'n': 1}, {'name': 'Apple', 'n': 0}]>


# In [67]: Product.objects.annotate(ns=Count('suppliers')).values('name', 'ns')
# Out[67    ]: SELECT "billing_product"."name" AS "name",
#        COUNT("billing_product_suppliers"."supplier_id") AS "ns"
#   FROM "billing_product"
#   LEFT OUTER JOIN "billing_product_suppliers"
#     ON ("billing_product"."id" = "billing_product_suppliers"."product_id")
#  GROUP BY "billing_product"."id",
#           1,
#           "billing_product"."description",
#           "billing_product"."brand_id",
#           "billing_product"."group_id",
#           "billing_product"."unit_price",
#           "billing_product"."stock",
#           "billing_product"."image",
#           "billing_product"."is_active",
#           "billing_product"."created_at",
#           "billing_product"."updated_at"
#  LIMIT 21

# Execution time: 0.000345s [Database: default]
# <QuerySet [{'name': 'Galaxy S24', 'ns': 0}]>