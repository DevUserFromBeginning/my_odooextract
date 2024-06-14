CREATE TABLE "productTemplate"(
	"id" INTEGER,
	"default_code"	TEXT(50),
	"name"	TEXT(250),
	"categ_id"	TEXT(30),
	"fabricante"	TEXT(20),
	"linea"	TEXT(20),
	"sublinea"	TEXT(20),
	"upc"	TEXT(20),
	"__last_update"	TEXT(19),
	"type"	TEXT(7),
	"currency_id"	TEXT,
	"cost_currency_id"	TEXT,
	"uom_name"	TEXT(8),
	"qty_available" REAL,
	"virtual_available" REAL,
	"incoming_qty" REAL,
	"outgoing_qty" REAL,
	"sale_line_warn" TEXT(100),
	"sales_count" REAL,
	"price" REAL,
	"standard_price" REAL,
	"purchased_product_qty" REAL,
	"list_price" TEXT(20),
	PRIMARY KEY("id")
);

CREATE TABLE "productProduct"(
	"id" INTEGER,
	"default_code"	TEXT(50),
	"name"	TEXT(250),
	"categ_id"	TEXT(30),
	"fabricante"	TEXT(20),
	"linea"	TEXT(20),
	"sublinea"	TEXT(20),
	"upc"	TEXT(20),
	"__last_update"	TEXT(19),
	"type"	TEXT(7),
	"currency_id"	TEXT,
	"uom_name"	TEXT(8),
	"qty_available" REAL,
	"virtual_available" REAL,
	"free_qty" REAL,
	"incoming_qty" REAL,
	"outgoing_qty" REAL,
	"quantity_svl" REAL,
	"sale_expected" REAL,
	"sale_line_warn" TEXT(100),
	"sales_count" REAL,
	"sale_num_invoiced" INTEGER,
	"price" REAL,
	"price_extra" REAL,
	"lst_price" REAL,
	"standard_price" REAL,
	"sale_avg_price" REAL,
	"purchased_product_qty" REAL,
	"purchase_num_invoiced" INTEGER,
	"purchase_avg_price" REAL,
	"total_cost" REAL,
	"normal_cost" REAL,
	"cost_currency_id" INTEGER,
	"value_svl" REAL,	
	PRIMARY KEY("id")
);

CREATE TABLE resPartner(
	"id" INTEGER,
	"name" TEXT(250),
	"active" TEXT(10),
	"type" TEXT(50),
	"street" TEXT(250),
	"street2" TEXT(250),
	"zip" TEXT(6),
	"city" TEXT(20),
	"state_id" TEXT(10),
	"country_id" TEXT(10),
	"country_code" TEXT(10),
	"company_type" TEXT(25),
	"contact_address" TEXT(250),
	"commercial_company_name" TEXT(150),
	"__last_update" TEXT(19),
	"contact_address_complete" TEXT(250),
	"credit" REAL,
	"debit" REAL,
	"total_invoiced" REAL,
	"currency_id" TEXT(10),
	"sale_order_count" INTEGER,
	"total_due" REAL,
	"total_overdue" REAL,
	"x_studio_canal_comercial" TEXT(25),
	"x_tipopersona" TEXT(30),
	"x_studio_bpid" TEXT(20),
	"x_studio_tipo_de_proveedor" TEXT(20),
	"x_studio_zonas_de_ventas" TEXT(20),
	"x_studio_tipo_de_cliente" TEXT(20),
	"x_studio_cliente" TEXT(10),
	PRIMARY KEY("id")
);

CREATE TABLE accountMove(
	"id" INTEGER,
	"sequence_number" INTEGER,
	"name" TEXT(20),
	"highest_name" TEXT(30),
	"date" TEXT(10),
	"ref" TEXT(150),
	"journal_id" TEXT(50),
	"line_ids" TEXT(30),
	"partner_id" TEXT(100),
	"move_type" TEXT(20),
	"country_code" TEXT(4),
	"payment_reference" TEXT(30),
	"amount_untaxed" REAL,
	"amount_tax" REAL,
	"amount_total" REAL,  
	"amount_residual" REAL, 
	"payment_state" TEXT(20),
	"invoice_date" TEXT(10),
	"invoice_date_due" TEXT(10),
	"invoice_origin" TEXT(10),
	"invoice_payment_term_id" TEXT(40) ,
	"invoice_line_ids" TEXT(50),
	"invoice_partner_display_name" TEXT(150), 
	"__last_update" TEXT(19),
	"display_name" TEXT(150),
	"create_date" TEXT(19),
	"partner_shipping_id" TEXT(100),
	"manual_currency_rate" REAL,
	"fiscal_provider" TEXT(150),
	"x_tasa" REAL,
	"sale_order_id" TEXT(30),
	"sale_order_number" TEXT(30),
	"rate" REAL,
	"amount_untaxed_rate" REAL,
	"amount_tax_rate" REAL,
	"amount_total_rate" REAL,
	"x_studio_total_" REAL,
	"x_studio_deuda" REAL,
	"x_tipodoc" TEXT(15),
	"x_ncontrol" TEXT(15),
	"x_studio_related_field_35Zlc" TEXT(100),
	"x_studio_orden_de_compra" TEXT(100),
	PRIMARY KEY("id")
);

CREATE TABLE accountMoveLine(
	"id" INTEGER,
	"date" TEXT(10),
	"create_date" TEXT(19),
	"write_date" TEXT(19),
	"__last_update" TEXT(19),
	"move_id" TEXT(100),
	"move_name" TEXT(50) ,
	"ref" TEXT(150),
	"journal_id" TEXT(50),
	"account_id" TEXT(50),
	"account_internal_type" TEXT(20), 
	"account_internal_group" TEXT(20),
	"name" TEXT(150),
	"quantity" REAL,
	"price_unit" REAL,
	"debit" REAL,
	"credit" REAL,
	"balance" REAL,
	"amount_currency" REAL,
	"price_subtotal" REAL,
	"price_total" REAL,
	"date_maturity" TEXT(10),
	"currency_id" TEXT(4),
	"partner_id" TEXT(100),
	"product_id" TEXT(250),
	"payment_id" TEXT(30),
	"tax_line_id" TEXT(100),
	"tax_base_amount" REAL,
	"amount_residual" REAL,
	"amount_residual_currency" REAL,
	"matching_number" TEXT(20),
	"fabricante" TEXT(20),
	PRIMARY KEY("id")
);

CREATE VIEW IF NOT EXISTS facturaVentas AS
SELECT
	id, invoice_date AS Fecha, ref AS Factura, invoice_partner_display_name AS Cliente, amount_untaxed AS Base, amount_tax AS Impuesto, amount_total AS Total,
	CASE 
		WHEN amount_residual < 0 THEN 0 
		ELSE amount_residual 
	END as Pendiente, 
	CASE 	
		WHEN payment_state = "in_payment" THEN "SinConciliar"  
		WHEN payment_state = "not_paid" THEN "Pendiente"  
		WHEN payment_state = "partial" THEN "Parcial" 
		WHEN payment_state = "paid" THEN "Pagada"
		ELSE payment_state
	END AS Estado, 
	invoice_origin
	
FROM 
	accountMove
WHERE
	move_type = 'out_invoice'
	AND payment_state <> 'reversed'

SELECT * from facturaVentas	
	
DROP TABLE productTemplate;
DROP TABLE productProduct;
DROP TABLE resPartner;
DROP TABLE accountMove;
DROP TABLE accountMoveLine;
DROP VIEW facturaVentas;


