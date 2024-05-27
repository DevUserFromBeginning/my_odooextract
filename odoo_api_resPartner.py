import xmlrpc.client
import openpyxl


'''
Realizado por: Ernesto Caraballo
Fecha actual: 10/05/2024

.- Conectarme a la api (OK)
.- Extraer los registros del modelo: crm.leads
.- Determinas los campos útiles del modelo para cada caso (852, GPOS, etc)
.- Llevar los registros a excel

'''

def main():
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'admin'
    password = 'Import2023!'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    #['company_id', '=', 'Import Import'] # filtro de compañía...aparentemente no funciona
    # pendiente de este tema 
    ordersLines = models.execute_kw(db, uid, password,'res.partner', 'search_read',
                                 [[]],
                                 {'fields':['id','company_id','name','display_name','user_id','comment','category_id','credit_limit','active','employee','type','street','street2','zip','city',
                                            'state_id','country_id','country_code','email','email_formatted','phone','mobile','is_company','industry_id','company_type',
                                            'user_ids','contact_address','commercial_partner_id','commercial_company_name','company_name','self','__last_update',
                                            'create_uid','create_date','channel_ids','contact_address_complete','property_product_pricelist','team_id',
                                            'phone_sanitized','phone_mobile_search','credit','debit','debit_limit','total_invoiced','currency_id','purchase_line_ids',
                                            'sale_order_count','sale_order_ids','unpaid_invoices','total_due','total_overdue','taxpayer','type_invoice_usd','type_invoice_ves',
                                            'x_studio_canal_comercial','x_tipopersona','x_studio_proveedor','x_studio_bpid','x_studio_tipo_de_proveedor','x_studio_zonas_de_ventas',
                                            'x_studio_tipo_de_cliente','x_studio_cliente']})
    '''
    for orderLine in ordersLines:
        print(orderLine)
        print('\n')
    '''
    campos = []
    for campo in ordersLines[0].keys():
        campos.append(campo)
        
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'res.partner'
    
    tmpRow = 1
    tmpColumn = 1
    for _ in range(0, len(campos)):
        ws.cell(row=1, column=_+1).value = campos[_]
        
    tmpRow = tmpRow + 1 #to make content start filling at row 2
    tmpColumn = 1
    
    for order in ordersLines:
        for campo in campos:
            ws.cell(row=tmpRow, column=tmpColumn).value= str(order[campo])
            tmpColumn = tmpColumn + 1
        tmpColumn=1
        tmpRow = tmpRow + 1
    
    wb.save(r"C:\\Users\\ESCH\Desktop\\odoo\\excel\\resPartner.xlsx")        
    
    print(f"\n********************\nSe acab´lo que se daba")
    
    
if __name__ == '__main__':
    main()