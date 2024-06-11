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
class MoveLines:
    # lista con todo los objetos creados
    all = []
    
    def __init__(self, id: int, date: str, create_date: str, write_date: str, last_update: str, move_id: str, move_name: str, ref: str, 
                 journal_id: str ,account_id: str ,account_internal_type: str, account_internal_group: str,
                 name: str, quantity: float, price_unit: float, debit: float, credit: float, balance: float,
                 amount_currency: float, price_subtotal: float, price_total: float, date_maturity: str, 
                 currency_id: str, partner_id: str, product_id: str, payment_id: str, tax_ids: str, 
                 tax_line_id: str, tax_base_amount:float, amount_residual: float, amount_residual_currency:float,
                 matched_debit_ids: str, matched_credit_ids: str, matching_number: str, purchase_line_id: str,
                 purchase_order_id: str, sale_line_ids: str, product_type: str, 
                 x_studio_related_field_4zjYm: str, x_studio_fabricante: str) -> None:
        
        # run validations to the received arguments
        self.id  = id,
        self.date = date,
        self.create_date = create_date,
        self.write_date = write_date,
        self.last_update = last_update,
        self.move_id = move_id, #desconstruir
        self.move_name = move_name,
        self.ref = ref,
        self.journal_id = journal_id, #desconstruir; crear el maestro de diarios
        self.account_id = account_id, #desconstruir; crear el maestro de cuentas contables
        self.account_internal_type = account_internal_type,
        self.account_internal_group = account_internal_group,
        self.name = name,
        self.quantity = quantity,
        self.price_unit = price_unit, 
        self.debit = debit,
        self.credit = credit,
        self.balance = balance,
        self.amount_currency = amount_currency,
        self.price_subtotal = price_subtotal,
        self.price_total = price_total,
        self.date_maturity = date_maturity,
        self.currency_id = currency_id, #desconstruir; dejar sólo la moneda "USD/VES/EUR..."
        self.partner_id = partner_id, #descontruir; crear el maestro de clientes y proveedores
        self.product_id = product_id, #desconstruir; crear el maestro de artículos...relacionarlo
        self.payment_id = payment_id,
        self.tax_ids = tax_ids,
        self.tax_line_id = tax_line_id, 
        self.tax_base_amount = tax_base_amount,
        self.amount_residual = amount_residual,
        self.amount_residual_currency = amount_residual_currency,
        self.matched_debit_ids = matched_debit_ids,
        self.matched_credit_ids = matched_credit_ids,
        self.matching_number = matching_number,
        self.purchase_line_id = purchase_line_id, #desconstruir; articulo: id - name
        self.purchase_order_id = purchase_order_id, #desconstruir; order: id - name/ref
        self.sale_line_ids = sale_line_ids, #desconstruir; articulo: id - name
        self.product_type = product_type,
        #estos dos campos; si la relación del artículo está correcta no los necesito
        self.x_studio_related_field_4zjYm = x_studio_related_field_4zjYm, #desconstruir; sublinea: id - descripción
        self.x_studio_fabricante = x_studio_fabricante #desconstruir; fabricante: id - descripción
        
        MoveLines.all.append(self)
        
    def __repr__(self) -> str:
        return f"MoveItem(íd:{self.id}, 'move_id':{self.move_id})"
        
 
def main():
    url = 'https://importvzla-import-import-prueba-12847814.dev.odoo.com'
    db = 'importvzla-import-import-prueba-12847814'
    username = 'francisco.tellez@import-import.com'
    password = '1129734'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    mOffset = 0
    mLimit = 5
    
    ordersLines = models.execute_kw(db, uid, password,'account.move.line', 'search_read',
                                    [[('parent_state','not in',['cancel','draft']),]],
                                    {'fields':['id','date','create_date','write_date','__last_update','move_id','move_name','ref','journal_id','account_id','account_internal_type',
                                               'account_internal_group','name','quantity','price_unit','debit','credit','balance','amount_currency','price_subtotal','price_total',
                                               'date_maturity','currency_id','partner_id','product_id','payment_id','tax_ids','tax_line_id','tax_base_amount','amount_residual',
                                               'amount_residual_currency','matched_debit_ids','matched_credit_ids','matching_number','purchase_line_id','purchase_order_id',
                                               'sale_line_ids','product_type','x_studio_related_field_4zjYm','x_studio_fabricante'],
                                     'offset':mOffset, 'limit':mLimit})
    
    '''         
    contador = 1
    for linea in ordersLines:
        print(f'\nitem: {contador}\n')
        for key, value in linea.items():
            print(f'campo: {key}, valor: {value}')       
        contador += 1
    '''
    
    for line in ordersLines:
        MoveLines(
            id  = line['id'],
            date = line['date'],
            create_date = line['create_date'],
            write_date = line['write_date'],
            last_update = line['__last_update'],
            move_id = line['move_id'][0], #retreive only the id of the move_id
            move_name = line['move_name'],
            ref = line['ref'],
            journal_id = line['journal_id'],
            account_id = line['account_id'],
            account_internal_type = line['account_internal_type'],
            account_internal_group = line['account_internal_group'],
            name = line['name'],
            quantity = line['quantity'],
            price_unit = line['price_unit'],
            debit = line['debit'],
            credit =line['credit'],
            balance = line['balance'],
            amount_currency = line['amount_currency'],
            price_subtotal=line['price_subtotal'],
            price_total=line['price_total'],
            date_maturity=line['date_maturity'],
            currency_id=line['currency_id'],
            partner_id=line['partner_id'],
            product_id=line['product_id'],
            payment_id=line['payment_id'],
            tax_ids=line['tax_ids'],
            tax_line_id=line['tax_line_id'],
            tax_base_amount=line['tax_base_amount'],
            amount_residual=line['amount_residual'],
            amount_residual_currency=line['amount_residual_currency'],
            matched_debit_ids=line['matched_debit_ids'],
            matched_credit_ids=line['matched_credit_ids'],
            matching_number=line['matching_number'],
            purchase_line_id=line['purchase_line_id'],
            purchase_order_id=line['purchase_order_id'],
            sale_line_ids=line['sale_line_ids'],
            product_type=line['product_type'],
            x_studio_related_field_4zjYm=line['x_studio_related_field_4zjYm'],
            x_studio_fabricante=line['x_studio_fabricante']
        )
          
    print(list(MoveLines.all))
    print(f"\n********************\nSe acab´lo que se daba")
    
        
if __name__ == '__main__':
    main()
    
    

