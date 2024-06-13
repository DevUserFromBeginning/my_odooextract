'''
    Realizado por: Ernesto Caraballo
    Fecha actual: 05/06/2024

    .- Conectarme a la api (OK)
    .- Extraer los registros del modelo: product.template
    .- Crear maestro de productos desde odoo
    .- llevar la data a db (sqlite por el momento)
    .- Quizá tambien pueda utilizar product.product
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
    
    sql = f'INSERT INTO productTemplate VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.executemany(sql,mdata)
    con.commit()
    return f'he terminado...'


def load_from_API():
    '''
    Función para consultar y traer todos los artículos del modelo product.template
    
    :param: no recibe parámetros
    :return: devuelve una lista cuyos elementos son diccionarios con todos los registros devueltos por la API
    '''
    url = 'https://importvzla-import-import.odoo.com'
    db = 'importvzla-import-import-import-5808788'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # no voy a implementar el filtro de RA, para traer todos los artículos
    # 'x_studio_many2one_field_a487A': Línea
    # 'x_studio_sublinea_1': Sub-Línea
    # 'x_studio_many2one_field_2qA7w': Fabricante (categoria)                                            
    ordersLines = models.execute_kw(db, uid, password,'product.template', 'search_read',
                                 [[['categ_id','in',['Principal','Servicios y Software']],['type','!=','consu']]],
                                 {'fields':['id','default_code','name','categ_id','x_studio_many2one_field_2qA7w','x_studio_many2one_field_a487A',
                                            'x_studio_sublinea_1','x_studio_upc','__last_update','type','currency_id','cost_currency_id','uom_name',
                                            'qty_available','virtual_available','incoming_qty','outgoing_qty','sale_line_warn','sales_count','price',
                                            'standard_price','purchased_product_qty','list_price']})
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
