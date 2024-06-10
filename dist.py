# esto es una prueba
# no podía escribir en la bd
import sqlite3
import xmlrpc.client
import openpyxl

def is_list(field):
    if type(field) is list:
        if len(field) > 1:
            return field[1]
        else:
            return field[0]
    else:
        return field


def main():
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # pasar todos los artículos a la bd
    ordersLines = models.execute_kw(db, uid, password,'product.template', 'search_read',
                                 [[['categ_id','in',['Principal','Servicios y Software']],['type','!=','consu'],['x_studio_many2one_field_2qA7w','=','RA']]],
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
