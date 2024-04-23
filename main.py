from cliente import Cliente
from produto import Produto
from datetime import datetime
import sqlite3

conn = sqlite3.connect('BancoSQL.db')
cursor = conn.cursor()

try:
    cursor.execute('''CREATE TABLE clientes(
                    ID INTEGER PRIMARY KEY,
                    nome TEXT 
                    )
                        ''')
except:
    print(cursor.lastrowid)

try:
    cursor.execute('''CREATE TABLE compras(
                    ID INTEGER PRIMARY KEY ,
                    data TEXT,
                    IDclienteCompra INTEGER,
                    valorCompra REAL,
                    isPago TEXT,
                    FOREIGN KEY(IDclienteCompra) REFERENCES clientes(ID)
                    )
                        ''')
except:
    print(cursor.lastrowid)

try:
    with open('clientes.txt', 'r') as arquivoCliente:
        for linha in arquivoCliente:
            itens = linha.split(';')
            if itens:
                IDcliente = int(itens[0].strip())
                IDclienteS = itens[0].strip()
                clienteNome = itens[4].strip()
                cliente = Cliente(clienteNome, IDcliente)
                try:
                    SQLcliente = '''INSERT INTO clientes(ID, nome) VALUES (?, ?)'''
                    cursor.execute(SQLcliente, (IDclienteS, clienteNome))
                    conn.commit()
                except:
                    pass
except FileNotFoundError:
    print("Arquivo não Encontrado!")

try:
    id_compra = 1
    with open('pagamentos.txt', 'r') as arquivoPagamento:
        for linha in arquivoPagamento:
            itens = linha.split(';')
            if itens:
                data = (itens[1].strip())
                IDClienteCompra = int(itens[0].strip())
                valorCompra = float(itens[3].strip())
                isPago = itens[4].strip()
                if len(data) < 8:
                    data = "0" + data
                cursor.execute('SELECT * FROM compras WHERE ID = ?', (id_compra,))
                verificaBanco = cursor.fetchone()
                if verificaBanco:
                    pass
                else:
                    try:
                        SQLcompras = '''INSERT INTO compras(ID, data, IDclienteCompra,valorCompra,isPago) VALUES (?, ?, ?, ?, ?)'''
                        cursor.execute(SQLcompras, (id_compra, data, IDClienteCompra, valorCompra, isPago))
                        conn.commit()
                        id_compra += 1
                    except:
                        print(cursor.lastrowid)
                produto = Produto(IDClienteCompra, valorCompra, isPago, data)
except FileNotFoundError:
    print("Arquivo não Encontrado!")


cursor.execute('''
    SELECT c.nome, p.valorCompra, p.data
    FROM compras AS p
    INNER JOIN clientes AS c ON p.IDclienteCompra = c.ID
''')

rows = cursor.fetchall()

totalCompras = {}

for row in rows:
    cliente_nome, valor_compra, data_compra = row
    if cliente_nome not in totalCompras:
        totalCompras[cliente_nome] = []
    totalCompras[cliente_nome].append((valor_compra, data_compra))

for cliente_nome, detalhes in totalCompras.items():
    print(f"\nCliente: {cliente_nome}")
    for valor_compra, data_compra in detalhes:
        data_formatada = datetime.strptime(data_compra, '%d%m%Y').strftime('%d/%m/%Y')
        print(f"Compra de {valor_compra} em {data_formatada}")


cursor.execute('''
SELECT clientes.nome, clientes.ID, SUM(compras.valorCompra) as total_pago
FROM compras
INNER JOIN clientes ON compras.IDclienteCompra = clientes.ID
WHERE isPago = "t"
GROUP BY clientes.ID
''')
SQLpagoT = cursor.fetchall()


cursor.execute('''
SELECT clientes.nome, clientes.ID, SUM(compras.valorCompra) as total_devido
FROM compras
INNER JOIN clientes ON compras.IDclienteCompra = clientes.ID
WHERE isPago = "f"
GROUP BY clientes.ID
''')
SQLpagoF = cursor.fetchall()

clientes = {}

for row in SQLpagoT:
    cliente_nome, cliente_id, total_pago = row
    if cliente_nome not in clientes:
        clientes[cliente_nome] = {'id': cliente_id, 'total_pago': total_pago, 'total_devido': 0}


for row in SQLpagoF:
    cliente_nome, cliente_id, total_devido = row
    if cliente_nome not in clientes:
        clientes[cliente_nome] = {'id': cliente_id, 'total_pago': 0, 'total_devido': total_devido}
    else:
        clientes[cliente_nome]['total_devido'] = total_devido


for cliente in sorted(clientes.keys(), key=lambda x: clientes[x]['id']):
    dados = clientes[cliente]
    print(f"\nCliente: {cliente}\nValor Pago: R${dados['total_pago']}\nValor Devido: R${dados['total_devido']}")
cursor.close()
