import xmlrpc.client
import openpyxl



def main():
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    
    lastUpdatedId = models.execute_kw(db, uid, password,'stock.move.line', 'search_read',
                                 [[['picking_code','not in',['internal',False]],['qty_done','!=',0],['state','!=','cancel'],
                                   '|',('picking_type_id','like','Principal: Expediciones'),('picking_type_id','like', 'Operador Logistico: Recepciones')]],
                                 {'fields':['id','__last_update']})
                            
    #****
    # quizá hay una forma más eficiente de buscar, filtrar fechas
    #****
    
    # buscar los documentos que se actualizaron en una fecha
    # y crear una lista de los id correspondientes
    # list comprehention con los id de los documentos de una fecha
    movedLines = [orderId['id'] for orderId in lastUpdatedId if orderId['__last_update'][0:10] == '2024-03-04']
    #print(movedLines)
    
    ordersLines = models.execute_kw(db, uid, password,'stock.move.line', 'search_read',
                                 [[('id','in',movedLines),['picking_code','not in',['internal',False]],['qty_done','!=',0],['state','!=','cancel'],
                                   '|',('picking_type_id','like','Principal: Expediciones'),('picking_type_id','like', 'Operador Logistico: Recepciones')]],
                                 {'fields':['id','move_id','origin','__last_update','display_name','product_id','location_id','location_dest_id',
                                            'picking_type_id','picking_partner_id','qty_done','product_uom_id','sale_price',
                                            'picking_id','state']})
    
    contador = 1
    for orderLine in ordersLines:
        print(f'item: {contador}')
        print(orderLine)
        print('\n')
        contador +=1    
    
if __name__ == '__main__':
    main()
    
