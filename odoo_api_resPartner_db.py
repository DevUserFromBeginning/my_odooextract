'''
Realizado por: Ernesto Caraballo
Fecha actual: 10/05/2024

.- Conectarme a la api (OK)
.- Extraer los registros del modelo: crm.leads
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
    
    sql = f'INSERT INTO resPartner VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.executemany(sql,mdata)
    con.commit()
    return f'he terminado...'


def load_from_API():
    '''
    Función para consultar y traer todos los artículos del modelo product.product
    :param: no recibe parámetros
    :return orderLines: lista cuyos elementos son diccionarios con los registros devueltos por la API
    '''
    url = 'https://importvzla-import-import.odoo.com'
    db = 'importvzla-import-import-import-5808788'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    #['company_id', '=', 'Import Import'] # filtro de compañía...aparentemente no funciona
    # pendiente de este tema 
    ordersLines = models.execute_kw(db, uid, password,'res.partner', 'search_read',
                                 [[]],
                                 {'fields':['id','name','active','type','street','street2','zip','city','state_id','country_id',
                                            'country_code','company_type','contact_address','commercial_company_name','__last_update',
                                            'contact_address_complete','credit','debit','total_invoiced','currency_id','sale_order_count',
                                            'total_due','total_overdue','x_studio_canal_comercial','x_tipopersona','x_studio_bpid',
                                            'x_studio_tipo_de_proveedor','x_studio_zonas_de_ventas','x_studio_tipo_de_cliente','x_studio_cliente']})
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