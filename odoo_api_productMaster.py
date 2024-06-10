'''
    Realizado por: Ernesto Caraballo
    Fecha actual: 05/06/2024

    .- Conectarme a la api (OK)
    .- Extraer los registros del modelo: product.template
    .- Crear maestro de productos desde odoo
    .- llevar la data a db (sqlite por el momento)
    .- Quizá tambien pueda utilizar product.product
'''

import sqlite3
import xmlrpc.client


#en caso que el valor devuelto sea una lista, debo tomar el primer elemento, siempre
# cuando la lista contien más de 1 elemento, el significativo está en [1]
def is_list(field):
    if type(field) is list:
        if len(field) > 1:
            return field[1]
        else:
            return field[0]
    else:
        return field

'''
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'
'''

def main():
    url = 'https://importvzla-import-import.odoo.com'
    db = 'importvzla-import-import-import-5808788'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # pasar todos los artículos a la bd
    # no voy a implementar el filtro de RA, para traer todos los artículos
    #,['x_studio_many2one_field_2qA7w','=','RA']
    ordersLines = models.execute_kw(db, uid, password,'product.template', 'search_read',
                                 [[['categ_id','in',['Principal','Servicios y Software']],['type','!=','consu']]],
                                 {'fields':['id','default_code','name','categ_id','x_studio_many2one_field_a487A','x_studio_sublinea_1',
                                            'x_studio_upc','type','currency_id','cost_currency_id','uom_name','product_variant_ids',
                                            'product_variant_id','__last_update','x_studio_many2one_field_2qA7w']})
    
    data = []
    for line in ordersLines:
        renglon = []
        for v in line.values():
            renglon.append(is_list(v))
        data.append(renglon)
    
    
    db = r"C:\\Users\\ESCH\Desktop\\odoo-852\\db\\852.db"
    con = sqlite3.connect(db)
    
    cur  = con.cursor()
    
    sql = f'INSERT INTO productMaster VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.executemany(sql,data)
    con.commit()
    
    
            
if __name__ == '__main__':
    main()
