import main
import os
import unittest


#Nao vai funcionar porque não existe uma lista de clientes
class TesteClientes(unittest.TestCase):
    def teste_adicionar_cliente(self):
        cliente = main.Cliente("Jose", 2)
        main.clientes.append(cliente)
        self.assertIn(cliente, main.clientes)


class TesteArquivoClientes(unittest.TestCase):
    def teste_arquivo_existe(self):
        arquivo_existe = os.path.exists('clientes.txt')
        self.assertTrue(arquivo_existe, "O arquivo clientes.txt não foi encontrado")
