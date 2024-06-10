import xmlrpc.client
import openpyxl


'''
Realizado por: Ernesto Caraballo
Fecha actual: 05/06/2024

.- Conectarme a la api (OK)
.- Extraer los registros del modelo: account.move
.- Determinas los campos útiles del modelo para cada caso (852, GPOS, etc)
.- Llevar los registros a excel

'''

def main():
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    total_records = models.execute_kw(db, uid, password, 'account.move.line', 'search_count', [[]])
    
    print(f'total registros: {total_records}')
    #print(models.execute_kw(db, uid, password, 'account.move.line', 'check_access_rights', ['read'], {'raise_exception': False}))

    #ordersLines = models.execute_kw(db, uid, password, 'account.move.line', 'fields_get',[],{'attributes': ['string']})
    
    '''
    'id','__last_update','display_name','move_id','move_name','date','ref','parent_state','journal_id','company_id',
                                               'company_currency_id','account_id','account_internal_type','account_internal_group','account_root_id','sequence',
                                               'name','quantity','price_unit','discount','debit','credit','balance','cumulated_balance','amount_currency',
                                               'price_subtotal','price_total','reconciled','blocked','date_maturity','currency_id','partner_id','product_uom_id',
                                               'product_id','product_uom_category_id','reconcile_model_id','payment_id','statement_line_id','statement_id',
                                               'tax_ids','group_tax_id','tax_line_id','tax_group_id','tax_base_amount','tax_repartition_line_id','tax_tag_ids',
                                               'tax_audit','tax_tag_invert','amount_residual','amount_residual_currency','full_reconcile_id','matched_debit_ids',
                                               'matched_credit_ids','matching_number','analytic_line_ids','analytic_account_id','analytic_tag_ids',
                                               'recompute_tax_line','display_type','is_rounding_line','exclude_from_invoice_tab','create_uid','create_date',
                                               'write_uid','write_date','move_attachment_ids','vehicle_id','need_vehicle','purchase_line_id','purchase_order_id',
                                               'is_anglo_saxon_line','predict_from_name','expected_pay_date','internal_note','next_action_date','sale_line_ids',
                                               'asset_ids','consolidation_journal_line_ids','followup_line_id','followup_date','product_type','is_landed_costs_line',
                                               'non_deductible_tax_value','x_studio_many2one_field_FCO3N','x_studio_related_field_eOzzb','x_studio_many2one_field_BMZyG',
                                               'x_studio_related_field_4zjYm','x_studio_fabricante'
    '''
    '''
    ('parent_state','not in',['cancel','draft']),('name','not like', '%Diferencia%'), ('journal_id','not like','%Retenci%'),
                                      ('tax_line_id','not like','%IVA 16%'), ('ref','not like','Cancelaci%'), ('ref','not like','igtf%'),
                                      '|',('account_internal_type','!=','False',),('account_internal_group','!=','False')
    '''
    
    '''
    {'fields':['id','__last_update','display_name','move_id','move_name','date','ref','parent_state','journal_id',
                                               'company_currency_id','account_id','account_internal_type','account_internal_group','name','quantity','price_unit',
                                               'debit','credit','balance','amount_currency','price_subtotal','price_total','date_maturity',
                                               'currency_id','partner_id','product_uom_id','product_id','product_uom_category_id','payment_id','tax_ids','tax_line_id',
                                               'tax_base_amount','amount_residual','amount_residual_currency','matched_debit_ids',
                                               'matched_credit_ids','matching_number','create_date','write_date',
                                               'purchase_line_id','purchase_order_id','expected_pay_date','sale_line_ids','product_type','x_studio_many2one_field_FCO3N',
                                               'x_studio_related_field_eOzzb','x_studio_many2one_field_BMZyG','x_studio_related_field_4zjYm','x_studio_fabricante'],
                                                    'offset':0, 'limit':2000}
                                                    {'fields':['id','__last_update','display_name','move_id','move_name','date','ref','parent_state','journal_id',
                                               'company_currency_id','account_id','account_internal_type','account_internal_group','name','quantity','price_unit',
                                               'debit','credit','balance','amount_currency','price_subtotal','price_total','date_maturity',
                                               'currency_id','partner_id','product_uom_id','product_id','product_uom_category_id','payment_id','tax_ids','tax_line_id',
                                               'tax_base_amount','amount_residual','amount_residual_currency','matched_debit_ids',
                                               'matched_credit_ids','matching_number','create_date','write_date',
                                               'purchase_line_id','purchase_order_id','expected_pay_date','sale_line_ids','product_type','x_studio_many2one_field_FCO3N',
                                               'x_studio_related_field_eOzzb','x_studio_many2one_field_BMZyG','x_studio_related_field_4zjYm','x_studio_fabricante'],
                                                    'offset':0, 'limit':2000}
                                                    '''
    
    '''
    ordersLines = models.execute_kw(db, uid, password,'account.move.line', 'search_read',
                                    [[('parent_state','not in',['cancel','draft']),]],
                                    {'fields':['id','__last_update','display_name','move_id','move_name','date','ref','parent_state','journal_id',
                                               'company_currency_id','account_id','account_internal_type','account_internal_group','name','quantity','price_unit',
                                               'debit','credit','balance','amount_currency','price_subtotal','price_total','date_maturity',
                                               'currency_id','partner_id','product_uom_id','product_id','product_uom_category_id','payment_id','tax_ids','tax_line_id',
                                               'tax_base_amount','amount_residual','amount_residual_currency','matched_debit_ids',
                                               'matched_credit_ids','matching_number','create_date','write_date',
                                               'purchase_line_id','purchase_order_id','expected_pay_date','sale_line_ids','product_type','x_studio_many2one_field_FCO3N',
                                               'x_studio_related_field_eOzzb','x_studio_many2one_field_BMZyG','x_studio_related_field_4zjYm','x_studio_fabricante'],
                                                    'offset':0, 'limit':2000})
    ''' 
    
    ordersLines = models.execute_kw(db, uid, password,'account.move.line', 'search_read',
                                    [[('parent_state','not in',['cancel','draft']),]],
                                    {'fields':['id','__last_update','display_name','move_id','move_name','date','ref','parent_state','journal_id',
                                               'company_currency_id','account_id','account_internal_type','account_internal_group','name','quantity','price_unit',
                                               'debit','credit','balance','amount_currency','price_subtotal','price_total','date_maturity',
                                               'currency_id','partner_id','product_uom_id','product_id','product_uom_category_id','payment_id','tax_ids','tax_line_id',
                                               'tax_base_amount','amount_residual','amount_residual_currency','matched_debit_ids',
                                               'matched_credit_ids','matching_number','create_date','write_date',
                                               'purchase_line_id','purchase_order_id','expected_pay_date','sale_line_ids','product_type','x_studio_many2one_field_FCO3N',
                                               'x_studio_related_field_eOzzb','x_studio_many2one_field_BMZyG','x_studio_related_field_4zjYm','x_studio_fabricante'],
                                                    'offset':0, 'limit':2000})
    '''
    contador = 1
    for orderLine in ordersLines:
        print(f'\n**** item: {contador} ****')
        print(f"{orderLine}")
        contador +=1      
    '''
    
    
    campos = []
    for campo in ordersLines[0].keys():
        campos.append(campo)
        
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'account.moveLine'
    
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
    
    wb.save(r"C:\\Users\\ESCH\Desktop\\odoo-852\\excel\\accountMoveLine.xlsx")
            
    
    print(f"\n********************\nSe acab´lo que se daba")
    
    
if __name__ == '__main__':
    main()
    
    

