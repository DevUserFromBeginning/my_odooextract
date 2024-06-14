'''
Realizado por: Ernesto Caraballo
Fecha actual: 05/06/2024

.- Conectarme a la api (OK)
.- Extraer los registros del modelo: account.move
.- Determinas los campos útiles del modelo para cada caso (852, GPOS, etc)
.- Llevar los registros a excel

'''
import xmlrpc.client
import sqlite3


def is_list(field):
    '''
    Función que toma el argumento y devuelve el contenido de la segunda posición, en caso
    que el argumento sea una lista de 2 o más elementos
    
    :param field: es la lista que se recibe
    :return: el segundo elemento de la lista o el primer elemento en caso que la lista sea de longitud 1
    '''
    if isinstance(field, list):
        '''if len(field) > 1:
            return field[1]
        elif len(field) == 1:
            return field[0]
        else:
            return 0'''
        return str(field)
    else:
        return field


def write_to_db(mdata) -> str:
    db = r"C:\\Users\\ESCH\Desktop\\odoo-852\\db\\odoo_local.db"
    con = sqlite3.connect(db)
    
    cur  = con.cursor()
    
    sql = f'INSERT INTO accountMove VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.executemany(sql,mdata)
    con.commit()
    return f'he terminado...'


def load_from_API():
    '''
    Función para consultar y traer todos los artículos del modelo account.move
    
    :param: no recibe parámetros
    :return: devuelve una lista cuyos elementos son diccionarios con todos los registros devueltos por la API
    '''
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    

       
    ordersLines = models.execute_kw(db, uid, password,'account.move', 'search_read',
                                    [[]],
                                    {'fields':['id','sequence_number','name','highest_name','date','ref','journal_id','line_ids','partner_id','move_type',
                                               'country_code','payment_reference','amount_untaxed','amount_tax','amount_total', 'amount_residual',
                                               'payment_state','invoice_date','invoice_date_due','invoice_origin',
                                               'invoice_payment_term_id','invoice_line_ids','invoice_partner_display_name','__last_update',
                                               'display_name','create_date','partner_shipping_id','manual_currency_rate','fiscal_provider',
                                               'x_tasa','sale_order_id','sale_order_number','rate','amount_untaxed_rate',
                                               'amount_tax_rate','amount_total_rate','x_studio_total_','x_studio_deuda','x_tipodoc','x_ncontrol',
                                               'x_studio_related_field_35Zlc', 'x_studio_orden_de_compra']})
    return ordersLines


def main():
    
    
    data = []
    for line in load_from_API():
        renglon = []
        for v in line.values():
            renglon.append(is_list(v))
        data.append(renglon)
    
    results = write_to_db(data)
    print(results)
    
    
if __name__ == '__main__':
    main()
    
    

