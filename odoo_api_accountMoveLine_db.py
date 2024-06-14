'''
Realizado por: Ernesto Caraballo
Fecha actual: 05/06/2024

.- Conectarme a la api (OK)
.- Extraer los registros del modelo: account.move.line
.- Determinas los campos útiles del modelo para cada caso (852, GPOS, etc)

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
    
    sql = f'INSERT INTO accountMoveLine VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.executemany(sql,mdata)
    con.commit()
    return f'he terminado...'


def load_from_API(salto: int = 0, bloque: int = 1):
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    total_records = models.execute_kw(db, uid, password, 'account.move.line', 'search_count', [[]])
    
    ordersLines = models.execute_kw(db, uid, password,'account.move.line', 'search_read',
                                    [[]],
                                    {'fields':['id','date','create_date','write_date','__last_update','move_id','move_name','ref','journal_id','account_id','account_internal_type',
                                               'account_internal_group','name','quantity','price_unit','debit','credit','balance','amount_currency','price_subtotal','price_total',
                                               'date_maturity','currency_id','partner_id','product_id','payment_id','tax_line_id','tax_base_amount','amount_residual',
                                               'amount_residual_currency','matching_number','x_studio_fabricante'],
                                     'offset':salto, 'limit':bloque})
    
    return ordersLines


def total_records_from_API():
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    return models.execute_kw(db, uid, password, 'account.move.line', 'search_count', [[]])

    
def main():
    
    
    total_records = total_records_from_API()

    remaining_records = total_records
    start = 1 #start no cambia es un ciclo
    block = 2500 #block cambia sólo con el último grupo de registros

    rcontador = 0
    while True:
        if remaining_records == 0:
            break
        elif block > remaining_records:
            block = remaining_records
        else:
            data = []
            for line in load_from_API(rcontador, block):
                renglon = []
                for v in line.values():
                    renglon.append(is_list(v))
                data.append(renglon)
            
            results = write_to_db(data)
            print(results)    

         
            #actualizar estado de variables    
            data.clear()
            remaining_records = remaining_records - block
            rcontador = rcontador + block
            print(f'start: {start+rcontador}...remaining_records: {remaining_records}\n')
            

    
if __name__ == '__main__':
    main()
