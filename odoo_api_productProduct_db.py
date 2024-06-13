import xmlrpc.client
import sqlite3

'''
Realizado por: Ernesto Caraballo
Fecha actual: 10/05/2024

.- Conectarme a la api (OK)
.- Extraer los registros del modelo: product.product
.- Determinas los campos útiles del modelo para cada caso (852, GPOS, etc)
.- Llevar los registros a excel

'''

def is_list(field):
    '''
    Función que toma el argumento y devuelve el contenido de la segunda posición, en caso
    que el argumento sea una lista de 2 o más elementos
    
    :param field: es la lista que se recibe
    :return: el segundo elemento de la lista o el primer elemento en caso que la lista sea de longitud 1
    '''
    if isinstance(field, list):
        if len(field) > 1:
            return field[1]
        else:
            return field[0]
    else:
        return field


def write_to_db(mdata) -> str:
    db = r"C:\\Users\\ESCH\Desktop\\odoo-852\\db\\odoo_local.db"
    con = sqlite3.connect(db)
    
    cur  = con.cursor()
    
    sql = f'INSERT INTO productProduct VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.executemany(sql,mdata)
    con.commit()
    return f'he terminado...'


def load_from_API():
    '''
    Función para consultar y traer todos los artículos del modelo product.product
    :param: no recibe parámetros
    :return orderLines: lista cuyos elementos son diccionarios con los registros devueltos por la API
    '''
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    ordersLines = models.execute_kw(db, uid, password,'product.product', 'search_read',
                                 [[['categ_id','in',['Principal','Servicios y Software']],['type','!=','consu']]],
                                 {'fields':['id','default_code','name','categ_id','x_studio_many2one_field_2qA7w','x_studio_many2one_field_a487A',
                                            'x_studio_sublinea_1','x_studio_upc','__last_update','type','currency_id','uom_name',
                                            'qty_available','virtual_available','free_qty','incoming_qty',
                                            'outgoing_qty','quantity_svl','sale_expected','sale_line_warn','sales_count','sale_num_invoiced','price',
                                            'price_extra','lst_price','standard_price','sale_avg_price',
                                            'purchased_product_qty','purchase_num_invoiced','purchase_avg_price','total_cost','normal_cost',
                                            'cost_currency_id','value_svl']})
    
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