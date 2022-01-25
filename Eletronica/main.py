
from kivy import require
require('1.11.1')

#KivyMD  MD
from kivymd.app import MDApp
from kivymd.uix.button import MDTextButton, MDFlatButton, MDIconButton,MDFillRoundFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast # To show a message
from kivymd.uix.imagelist import SmartTileWithStar

#Kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.scatter import ScatterPlane, Scatter
from kivy.uix.image import Image

import sqlite3
import json
from datetime import date
import os

Window.size = 1200, 700



class Date:
    day = date.today().day
    month = date.today().month
    year = date.today().year

    def __init__(self):

        self.date_current = f'{str(self.day).zfill(2)}/{str(self.month).zfill(2)}/{self.year}'

class Manager(BoxLayout):
    pass

class ScreenImage(Screen):
    pass

class BtClientLogin(MDBoxLayout):
    map = {}
    lista = []
    def __init__(self, id, msg, *args, **kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        self.get_id = id
        self.get_msg = str(msg)

    def content_base(self):
        """
        To get the quant of returning client
        :return: A list witch the quant of found client
        """

        dict_clientes = dict()


        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ID, Nome FROM cliente WHERE ID == "' + self.get_id + '"')
        cliente = cursor.fetchall()

            # for iten in cursor.fetchall():
            #     self.map["ID"] = str(iten[0])
            #     self.map["Cadatro"] = str(iten[1])
            #     self.map["Nome"] = str(iten[2])
            #     self.map["CPF"] = str(iten[3])
            #     self.map["Bairro"] = str(iten[4])
            #     self.map["Logradouro"] = str(iten[5])
            #     self.map["Endereço"] = str(iten[6])
            #     self.map["Numero"] = str(iten[7])
            #     self.map["Telefone"] = str(iten[8])
            #     self.map["Celular"] = str(iten[9])
            #     self.map["Email"] = str(iten[10])
            #     self.lista.append(self.map.copy())

        dict_clientes["ID"] = cliente[0][0]
        dict_clientes["Nome"] = cliente[0][1]

        with open('getNome.json', 'w', encoding='utf-8') as nom:
            json.dump(dict_clientes, nom, indent=2)

        MDApp.get_running_app().root.ids.manager.current = 'screenview'

        conn.close()
        self.lista.clear()
        self.map.clear()


class ScreenLogin(Screen):

    lista = []
    map = {}
    def __init__(self,*args,**kwargs):
        super(ScreenLogin,self).__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

    def see_scroll_client(self):
        cpf = self.ids.login_cpf.text
        nome = self.ids.nome.text

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()

        if nome == '' and cpf == '':
            self.ids.scroll_client.clear_widgets()
        elif cpf != '':
            cursor.execute('SELECT ID, Nome FROM cliente '
                           'WHERE Cpf == "' + str(cpf) + '" ')

            self.ids.scroll_client.clear_widgets()
            for data in cursor.fetchall():
                self.ids.nome.text = str(data[1])
        else:
            cursor.execute('SELECT ID, Nome FROM cliente '
                           'WHERE Nome LIKE "' + str(nome) + '%" ')

            self.ids.scroll_client.clear_widgets()
            for data in cursor.fetchall():
                self.ids.scroll_client.add_widget(BtClientLogin(str(data[0]), str(data[1])))
        conn.close()

    def content_base(self):
        """
        To get the quant of returning client
        :return: A list witch the quant of found client
        """
        self.cpf = self.ids.login_cpf.text

        if self.cpf == '':
            pass
        else:
            conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cliente WHERE CPF == "' + self.cpf + '"')

            for iten in cursor.fetchall():
                self.map["ID"] = str(iten[0])
                self.map["Cadatro"] = str(iten[1])
                self.map["Nome"] = str(iten[2])
                self.map["CPF"] = str(iten[3])
                self.map["Bairro"] = str(iten[4])
                self.map["Logradouro"] = str(iten[5])
                self.map["Endereço"] = str(iten[6])
                self.map["Numero"] = str(iten[7])
                self.map["Telefone"] = str(iten[8])
                self.map["Celular"] = str(iten[9])
                self.map["Email"] = str(iten[10])
                self.lista.append(self.map.copy())
            conn.close()
        if len(self.lista) == 1:
            self.get_data_cliente(self.lista)
        elif len(self.lista) == 0:
            self.get_data_cliente(self.lista)
        else:
            self.pop_entry(self.lista)

        self.lista.clear()
        self.map.clear()

    def get_data_cliente(self, cliente,*args,**kwargs):
        """

        :param cliente: Receive the clients
        :return:
        """

        dict_clientes = {}

        if self.cpf == '':
            pass
        else:
            if len(cliente) < 1:
                # self.ids.warning.text = 'Nome ou CPF invalido!'
                toast('      Nome ou CPF invalido!      \nSem cadastro no banco de dados! ',duration=5)
                self.ids.float_layout.add_widget(ButtonRegister())
            else:
                self.ids.float_layout.remove_widget(ButtonRegister())
                dict_clientes["ID"] = cliente[0]["ID"]
                dict_clientes["Nome"] = cliente[0]["Nome"]
                dict_clientes["CPF"] = cliente[0]["CPF"]

                with open('getNome.json','w',encoding='utf-8') as nom:
                    json.dump(dict_clientes, nom, indent=2)

                MDApp.get_running_app().root.ids.manager.current = 'screenview'

    def pop_entry(self, cliente, *args,**kwargs):

        box = MDBoxLayout(orientation="vertical")
        # box = ScrollView()

        bt = Button(text=f"Nome: ")

        # for n,persom in enumerate(cliente):
        #     # print(persom)
        #     box.add_widget(MDTextButton(on_press=(self.valor_button()),text=f"Nome: {persom['Nome']} Cpf: {persom['CPF']}", font_size='20sp'))

        box.add_widget(bt)

        pop = Popup(title='Relacionados',size_hint=(None,None), size=('400','400'), content=box)

        pop.open()

    def limpar(self):
        self.ids.login_cpf.text = ''
        self.ids.nome.text = ''

    def valor_button(self):
        print('entrou')


class ScreenRegister(Screen,Date):

    def __init__(self,**kwargs):
        super(ScreenRegister,self).__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        self.date = self.date_current

    def on_pre_enter(self):
        self.criaBd()

    def cadastro(self):
        cadastro = str(self.date)
        nome = self.ids.cadastro_nome.text.title()
        cpf = self.ids.cadastro_cpf.text
        logradouro = self.ids.cadastro_logradouro.text.title()
        endereco = self.ids.cadastro_endereco.text.title()
        bairro = self.ids.cadastro_bairro.text.title()
        numero = self.ids.cadastro_numero.text
        telefone = self.ids.cadastro_telefone.text
        celular = self.ids.cadastro_celular.text
        email = self.ids.cadastro_email.text


        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        if nome == '':
            toast('Sem informação do nome ou Cpf!', duration=8)
        else:
            try:
                cursor.execute('INSERT INTO cliente(Cadastro,Nome,CPF,Logradouro,Endereço,Bairro,Numero,Telefone,Celular,Emeil)'
                               'VALUES ("'+cadastro+'","'+nome+'","'+cpf+'","'+logradouro+'","'+endereco+'","'+bairro+'","'+numero+'","'+telefone+'","'+celular+'","'+email+'");')
                conn.commit()

                self.ids.cadastro_nome.text = ''
                self.ids.cadastro_cpf.text = ''
                self.ids.cadastro_logradouro.text =''
                self.ids.cadastro_endereco.text = ''
                self.ids.cadastro_bairro.text = ''
                self.ids.cadastro_numero.text = ''
                self.ids.cadastro_telefone.text = ''
                self.ids.cadastro_celular.text =''
                self.ids.cadastro_email.text = ''
                # self.ids.cadastro_cpf.color_mode = 'none'
                self.ids.cadastro_cpf.line_color_focus = 0, 0, 0, 1
                toast('Cadastro feito com sucesso!')
            except sqlite3.IntegrityError:
                toast(f'CPF ({str(cpf)}) já cadastrado', duration=5)
                self.ids.cadastro_cpf.color_mode = 'custom'
                self.ids.cadastro_cpf.line_color_focus = 1,0,0,1
        conn.close()

    def criaBd(self):
        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        conn.cursor()
        conn.execute('CREATE TABLE IF NOT EXISTS cliente(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ' 
                     'Cadastro TEXT NOT NULL,'
                     'Nome TEXT NOT NULL,'
                     'CPF TEXT UNIQUE,'
                     'Logradouro Text,'
                     'Endereço TEXT NOT NULL,'
                     'Numero Text,'
                     'Bairro TEXT,'                     
                     'Telefone TEXT,'
                     'Celular TEXT,'
                     'Emeil TEXT);')


        conn.execute('CREATE TABLE IF NOT EXISTS produtos(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                     'Entrada TEXT ,'
                     'Saida TEXT, '
                     'ValorConserto REAL,'
                     'Garantia TEXT,'
                     'ClienteID INTEGER NOT NULL,'
                     'Modelo TEXT ,'
                     'Marca TEXT,'
                     'Serial TEXT,'
                     'Defeito TEXT,'
                     'Situação,'
                     'Pago TEXT'
                     ' );')

        conn.execute('CREATE TABLE IF NOT EXISTS estoque(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
                     'Aparelho TEXT, '                     
                     'Modelo Text,'
                     'Marca Text,'
                     'Avarias TEXT,'
                     'Prateleira INTEGER,'
                     'EspacoPrateleira TEXT,'
                     'Valor TEXT);')

        conn.execute('CREATE TABLE IF NOT EXISTS StockPartsDevices(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                    'ID_Device INTEGER NOT NULL,'
                    'Peca TEXT NOT NULL,'
                    'Modelo TEXT,'
                    'Serial TEXT,'
                    'ValorUnit REAL,'
                    'ValorSoma REAL,'
                    'Quantidade INTEGER);')


        conn.execute('CREATE TABLE IF NOT EXISTS prateleira(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
                     'PrateleirNum TEXT);')

        conn.execute('CREATE TABLE IF NOT EXISTS EspacoPrateleira (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
                     'IDPrateleira INTEGER NOT NULL,'
                     'Espaco TEXT)')

        conn.commit()


class IconListItem(OneLineIconListItem):
    icons = StringProperty()

# This class does parts of class "screeView"
# Essa class faz part da class "screeView"
class Aparelho(BoxLayout,Date): # content of a popup

    def __init__(self, *args,**kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        self.date = self.date_current

        register = ScreenView()
        try:
            self.ids.see_user_device.text = register.content_user()
        except ValueError:
            print('ERROR: linha 209 class Aparelho Não recebel nem um conteudo da class ScreenView!')

        self.msg_device = ''

    # conteudo do on_focus do TextField
        marca = ['Sansung','CCE','LG','Panasonic','Tochiba','Sony','HP','Philco']        #########
        self.lista = [
            {
                "viewclass": "IconListItem",
                "icons":"devices",
                "text": str(i),
                "height":dp(56),
                "callback": self.inserir,
                "on_release": (lambda x=i: self.inserir(x)),
            } for i in marca]

        self.menu_widget = MDDropdownMenu(
            caller=self.ids.id_marca,
            items=self.lista,
            position='bottom',
            width_mult=4
        )

    def file_image(self):
        file = open('NameDevice.txt','r')
        file_imag = file.read()
        file.close()

        if file_imag == '':
            pass
        else:
            self.ids.modelo.text = str(file_imag[:-4])

            # clearing the file after text field receive the text
            clear_file = open('NameDevice.txt','w')
            clear_file.write('')
            clear_file.close()

    def inserir(self,x=''):        ##########
        self.ids.id_marca.text = str(x)
        self.menu_widget.dismiss()

    def situacao(self,txt):
        if txt == 'Orçamento':
            self.ids.cituacao.icon = 'hand-back-left'
            self.ids.cituacao.text = txt
        elif txt == 'Arrumar':
            self.ids.cituacao.icon = 'account-check'
            self.ids.cituacao.text = txt
        elif txt =='Devolver':
            self.ids.cituacao.icon = 'thumb-down'
            self.ids.cituacao.text = txt
        elif txt == 'Entregue':
            self.ids.cituacao.icon = 'handshake'
            self.ids.cituacao.text = txt
        elif txt == 'Arrumado':
            self.ids.cituacao.icon = 'check-underline-circle'
            self.ids.cituacao.text = txt

    def save_produto(self):

        if self.ids.modelo.text == '' or self.ids.id_marca.text == '':
            toast('Não foi inserido um aparelho ou uma marca!')
        else:
            try:
                with open('getNome.json', 'r') as id_n:
                    nome = json.load(id_n)

                id_nome = nome['ID']
                modelo = self.ids.modelo.text
                marca = self.ids.id_marca.text
                serial = self.ids.serial.text
                defeito = self.ids.defeito.text
                situacao = self.ids.cituacao.text
                valorConserto = self.ids.valor_conserto.text

                conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
                conn.cursor()
                conn.execute('INSERT INTO produtos(Entrada,ValorConserto,ClienteID,Modelo,Marca,Serial,Defeito,Situação)'
                             'VALUES ("'+str(self.date)+'","'+str(valorConserto)+'" ,"'+str(id_nome)+'", "'+str(modelo)+'", "'+str(marca)+'","'+str(serial)+'" ,"'+str(defeito)+'", "'+str(situacao)+'")')
                conn.commit()
                conn.close()

                self.ids.modelo.text = ''
                self.ids.id_marca.text = ''
                self.ids.serial.text = ''
                self.ids.defeito.text = ''
                self.ids.cituacao.text = ''
                self.ids.valor_conserto.text = ''

                toast('Aparelho salvo com sucesso!')

                MDApp.get_running_app().root.ids.manager.current = 'screenimage'
            except:
                print('ERRO class Aparelho')

    def see_image(self,*args,**kwargs):

        scroll_image = ImageParts()

        pop = Popup(title='Selecionar image',size_hint=(None,None),size=('300dp','350dp'),
                    background_color=(0,0,0,1),content=scroll_image)
        pop.open()

    def snackbar(self, texto):
        snack = SnackBar(texto)
        snack.open()

# class that receives thes class Box_View
class ScreenView(Screen):

    lista = []
    get = []
    def __init__(self,*args,**kwargs):
        super(ScreenView,self).__init__(**kwargs)
        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

    def content_user(self):

        self.data = {}
        linha = []
        # Geting the name of file txt
        try:
            with open('getNome.json','r', encoding='utf-8') as get_data:
                 self.data = json.load(get_data)

            conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM cliente WHERE CPF == "'+str(self.data["CPF"])+'" ')
            except KeyError:
                cursor.execute('SELECT * FROM cliente WHERE ID == "' + str(self.data["ID"]) + '" ')

        except sqlite3.OperationalError as error_sqlite3:
            print('ERROR: linha 268 na class ScreenView Não existi o data base')
        except FileNotFoundError:
            print('ERROR: Não foi criado um arquivo json!')
        except TypeError:
            pass

        try:
            linha = cursor.fetchall()
        except UnboundLocalError:
            print('ERROR: linha 277 class ScreenView Não foi criado um data base!')

        try:
            self.ids.title_client.text = f'{str(self.data["Nome"]).title()}'
        except KeyError:
            pass
        except TypeError:
            pass

        try:
            if linha[0][1] == '':
                self.ids.see_register.text = ''
            else:
                self.ids.see_register.text = f'Cadastrado em {str(linha[0][1])}\n\n' \
                                             f'Nome: {str(linha[0][2].title())}\n\n'\
                                            f'CPF: {str(linha[0][3])} \n\n' \
                                            f'Bairro: {str(linha[0][7])}\n\n'\
                                            f'{str(linha[0][4])}: {linha[0][5]}      ' \
                                            f'N°: {str(linha[0][6])}\n\n' \
                                            f'Tel: {str(linha[0][8])}\n\n' \
                                            f'Cel: {str(linha[0][9])}\n\n' \
                                            f'Email: {str(linha[0][10])}'
            register = self.ids.see_register.text
            return register
        except IndexError:
            print('ERROR: linha 294 na class "ScreenView" Lista vasia não tem um data base')


    def content_device(self):
        dirct = {}
        get = ''

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        conn.cursor()
        try:
            get = conn.execute('SELECT * FROM produtos '
                               'WHERE ClienteID == "'+str(self.data["ID"])+'";')
        except sqlite3.OperationalError:
            print('ERROR: linha 306 na class ScreenView Não existe o data base!')
        except :
            pass

        for item in get.fetchall():

            dirct['ID'] = item[0]
            dirct['Entrada'] = item[1]
            dirct['Saida'] = item[2]
            dirct['ValorConserto'] = item[3]
            dirct['Garantia'] = item[4]
            dirct['ClienteID'] = item[5]
            dirct['Modelo'] = item[6]
            dirct['Marca'] = item[7]
            dirct['Serial'] = item[8]
            dirct['Defeito'] = item[9]
            dirct['Situação'] = item[10]
            dirct['Pago'] = item[11]
            self.get.append(dirct.copy())

    def insert_content_produtos(self):
        """
        Geting the devicesed of cliente
        Obtendo os aparelhos do cliente
        :return:
        """
        # print(self.get.fetchall())
        self.ids.scroll.clear_widgets()

        try:
            # Here return the button with device
            for item in self.get:

                if item['Saida'] == None :
                    item['Saida'] = ' '
                else:
                    item['Saida'] = f'[size=13]Data\nda entrega[/size] {item["Saida"]}'

                self.ids.scroll.add_widget(Box_View(id_text=item['ID'],
                                                    content=str(item['Modelo']),
                                                    sub=str(item['Marca']),
                                                    imag=str(item['Modelo']).title(),
                                                    delivery=str(item['Saida'])))

        except AttributeError:
            print('ERROR: linha 324 na class ScreenView a variavel get não recebel um data base!')

    def on_pre_enter(self):

        self.content_user()
        self.content_device()
        self.insert_content_produtos()

    def on_leave(self):
        self.get.clear()

    def popup_incerir_aparelho(self):
        screen = Aparelho()

        bt = MDIconButton(icon=('export'))
        screen.add_widget(bt)

        pop = Popup(title='incerir aparelho',auto_dismiss=False,content=screen)

        bt.bind(on_press=pop.dismiss)
        pop.open()


class ButtonRegister(MDFillRoundFlatIconButton):

    def enter(self):
        MDApp.get_running_app().root.ids.manager.current = 'screenregister'


class View_device(BoxLayout):
    def __init__(self,texto='',**kwargs):
        super().__init__(**kwargs)
        self.ids.content_device.text = str(texto)

    def go_edit(self):
        MDApp.get_running_app().root.ids.manager.current = 'editdevice'

class EditDevice(Screen):

    id_current = ''
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

    def dropdownmenu(self):
        marca = ['Sansung', 'CCE', 'LG', 'Panasonic', 'Tochiba', 'Sony', 'HP', 'Philco']  #########
        self.lista = [
            {
                "viewclass": "IconListItem",
                "icons": "devices",
                "text": str(i),
                "height": dp(56),
                "callback": self.inserir,
                "on_release": (lambda x=i: self.inserir(x)),
            } for i in marca]

        self.menu_widget = MDDropdownMenu(
            caller=self.ids.id_marca,
            items=self.lista,
            position='bottom',
            width_mult=4
        ).open()

    def inserir(self, x=''):  ##########
        self.ids.id_marca.text = str(x)
        # self.menu_widget.dismiss()

    def name_id(self):
        with open('getNome.json','r') as nome_id:
            _id_nome = json.load(nome_id)
        return _id_nome

    def garantia(self, cinal):
        valor = 0
        try:
            valor = int(self.ids.mes_garantia.text)
        except ValueError:
            pass

        if cinal == '-':
            valor -= 10
            if valor < 0:
                valor = 0
        elif cinal == '+':
            valor += 10
        self.ids.mes_garantia.text = str(valor)
        self.ids.dias.text = f'{str(valor)} Dias'

    def info_client(self):
        id = self.name_id()
        print(self.user_folder)
        conn = sqlite3.connect(self.user_folder + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cliente '
                       'WHERE ID == "'+ str(id['ID']) +'" ')
        info_client = cursor.fetchall()
        self.ids.label_entry_device.text = f'Data entrada aparelho:\n {info_client[0][1]}'
        self.ids.see_client_device.text = f'Cadastrado em {str(info_client[0][1])}\n\n' \
                                            f'Nome: {str(info_client[0][2].title())}\n\n'\
                                            f'CPF: {str(info_client[0][3])} \n\n' \
                                            f'Bairro: {str(info_client[0][7])}\n\n'\
                                            f'{str(info_client[0][4])}: {info_client[0][5]}      ' \
                                            f'N°: {str(info_client[0][6])}\n\n' \
                                            f'Tel: {str(info_client[0][8])}\n\n' \
                                            f'Cel: {str(info_client[0][9])}\n\n' \
                                            f'Email: {str(info_client[0][10])}'

    def data_base(self):
        self.info_client()

        with open('getNome.json','r', encoding='utf-8') as id:
            id_device = json.load(id)
            id.close()

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos WHERE ID == "'+str(id_device['Id_device'])+'" ')
        content = cursor.fetchall()

        # geting the id current of device
        self.id_current = str(content[0][0])

        self.ids.modelo.text = str(content[0][6])
        self.ids.id_marca.text = str(content[0][7])
        self.ids.serial.text = str(content[0][8])
        self.ids.defeito.text = str(content[0][9])
        self.ids.valor_conserto.text = str(content[0][3])
        self.ids.dias.text = f'{str(content[0][4])} Dias'

        # Here is to if the text garantia is enpty he not receive None
        if str(content[0][4]) == 'None':
            self.ids.mes_garantia.text = ''
        else:
            self.ids.mes_garantia.text = str(content[0][4])

        cituacao = str(content[0][10])
        if cituacao == 'Orçamento':
            self.ids.cituacao.icon = 'hand-back-left'
            self.ids.cituacao.text = cituacao
            self.ids.orcamento.active = True
        elif cituacao == 'Arrumar':
            self.ids.cituacao.icon = 'account-check'
            self.ids.cituacao.text = cituacao
            self.ids.arrumar.active = True
        elif cituacao =='Devolver':
            self.ids.cituacao.icon = 'thumb-down'
            self.ids.cituacao.text = cituacao
            self.ids.devolcer.active = True
        elif cituacao == 'Entregue':
            self.ids.cituacao.icon = 'handshake'
            self.ids.cituacao.text = cituacao
            self.ids.entregue.active = True
        elif cituacao == 'Arrumado':
            self.ids.cituacao.icon = 'check-underline-circle'
            self.ids.cituacao.text = cituacao
            self.ids.arrumado.active = True
        conn.close()

        if cituacao == 'Entregue':

            input = f'[b]Data entrada:[/b] {content[0][1]}'
            output = f'[b]Data saida:[/b] {content[0][2]}'
            warranty = f'Garantia de {content[0][4]} dias!'
            self.ids.box_garantia.add_widget(Rotulo_garantia(str(input), str(output), str(warranty)))


    def situacao(self,txt=None):
        if txt == 'Orçamento':
            self.ids.cituacao.icon = 'hand-back-left'
            self.ids.cituacao.text = txt
        elif txt == 'Arrumar':
            self.ids.cituacao.icon = 'account-check'
            self.ids.cituacao.text = txt
        elif txt == 'Devolver':
            self.ids.cituacao.icon = 'thumb-down'
            self.ids.cituacao.text = txt
        elif txt == 'Entregue':
            self.ids.cituacao.icon = 'handshake'
            self.ids.cituacao.text = txt
        elif txt == 'Arrumado':
            self.ids.cituacao.icon = 'check-underline-circle'
            self.ids.cituacao.text = txt

    def save_data(self):

        try:
            coon = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
            cursor = coon.cursor()
            cursor.execute('UPDATE produtos SET Garantia = "'+ str(self.ids.mes_garantia.text) +'", Modelo = "'+str(self.ids.modelo.text)+'", Marca = "'+str(self.ids.id_marca.text)+'", Serial = "'+str(self.ids.serial.text)+'", Defeito = "'+str(self.ids.defeito.text)+'", ValorConserto = "'+str(self.ids.valor_conserto.text)+'", Situação = "'+str(self.ids.cituacao.text)+'" '
            'WHERE ID == "'+str(self.id_current)+'" ')

            coon.commit()
            toast('Alterações feita com sucesso!')
        except :
            toast('As alterações não foram salvas!')

        if self.ids.entregue.active == True:
            if self.ids.mes_garantia.text == '':
                toast('Você esta fazendo a entrega do aparelho porem Não deu a garantia!\nE por isso a entrega não pode ser comcluida', duration=8)
            else:
                data = Date()
                cursor.execute('UPDATE produtos SET Saida = "'+ str(data.date_current) +'" '
                                'WHERE ID == "'+ str(self.id_current) +'" ')
                toast('Entrega salva com cusseço!')
                coon.commit()
        coon.close()

    def on_pre_enter(self, *args):
        self.data_base()

    def on_leave(self):
        self.ids.box_garantia.clear_widgets()


class Box_View(MDCard):

    map = {}
    def __init__(self,id_text='', content='',sub='',imag='', delivery='', **kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        # self.ids.bt_content.text = str(content)
        self.id_text = str(id_text)
        self.text = str(content)
        self.sub_text = str(sub)

        self.delivery = str(delivery)

        # see if has the image in folder and retunr a True or False
        # veja se tem a imagem na pasta e retorne um True ou False
        sis = os.path.exists('image/image_parts/'+ imag + '.png')

        if sis == True:
            self.image = str('image/image_parts/' + imag + '.png')
        else:
            self.image = str('image/image_parts/Outros.png')


    # Only to geting the id of client to find the device of client
    # Só para obter o id do cliente para encotrar o aparelho do cliente
    def get_id_client(self):
        with open('getNome.json','r') as client:
            id_cliet = json.load(client)
            client.close()
        return id_cliet['ID']

    def see_content_deviced(self,txt):

        # geting id of client
        id_client = self.get_id_client()

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        # cursor.execute('SELECT * FROM produtos WHERE ClienteID == "'+str(id_client)+'" AND ID == "' + str(txt.text) + '" ')
        cursor.execute('SELECT * FROM produtos WHERE ID == "'+ str(self.id_text) +'" ')
        get_cursor = cursor.fetchall()

        return get_cursor

    # Here is to open the content of popup
    def text_of_button(self,txt):

        obg_device = self.see_content_deviced(txt)

        screen_view = MDApp.get_running_app().root.ids.manager.get_screen('screenview')

        cobrança = obg_device[0][11]
        if str(cobrança) == 'None':
            cobrança = 'Não'

        # geting the content of one class
        view_deviced = View_device(texto=f'[size={"40dp"}][b][u]{obg_device[0][6]}[/u][/b][/size]\n\n '
                                         f'Marca: {obg_device[0][7]}\n\n'
                                         f'Valor: {obg_device[0][3]}\n\n'
                                         f'Garantia\n\n'
                                         f'Serial: {obg_device[0][8]}\n\n'
                                         f'Defeito: {obg_device[0][9]}\n\n'
                                         f'Situação: {obg_device[0][10]}\n\n'
                                         f'Pago: {cobrança}')
        view_deviced.ids.data.text = obg_device[0][1]

        # One Content of popup
        conteiner = BoxLayout(orientation='vertical')

        # One Button
        bt = MDFlatButton(text='Exit')

        pop = Popup(title='Deviced', size_hint=(.505,.75),
                    pos_hint=({'x': .0, 'center_y': .409}),
                    content=conteiner)

        bt.on_release = pop.dismiss

        conteiner.add_widget(view_deviced)
        conteiner.add_widget(bt)


        with open('getNome.json', 'r') as id:
            id_device = json.load(id)
            id_device['Id_device'] = obg_device[0][0]
            id.close()


        with open('getNome.json', 'w') as write_id:
            json.dump(id_device, write_id, indent=2)

        screen_view.ids.mdcard_view = pop.open()

    

# class to add an MDTextField
class Text(MDBoxLayout):
    pass

# class to add an CheckBox
class Check(MDBoxLayout):
    pass

class NewUsedParts(Screen):
    pass

class ButtonParts(MDCard):
    def __init__(self,namber='', id='', label='',amount='',**kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        self.namber = str(namber)
        self.get_id = id
        self.labels = label
        self.amount = amount

    def view_parts(self):
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').add_widget(InsertDeviceParts(self.get_id,True))

    def popup(self,id,*args,**kwargs):

        # MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').children[0]

        self.id_root = id

        box = BoxLayout(orientation='vertical')
        box_button = BoxLayout(spacing='20dp', padding='10dp')

        image = Image(source='image/atencao.png')

        popup = Popup(title='Deseja excluir essa peça?', size_hint=(None, None), size=('300dp', '200dp'), content=box)

        bt_sim = Button(text='Sim', on_press=self.delet_parts, on_release=popup.dismiss)
        bt_nao = Button(text='Não', on_release=popup.dismiss)

        box_button.add_widget(bt_sim)
        box_button.add_widget(bt_nao)

        box.add_widget(image)
        box.add_widget(box_button)

        popup.open()


    def delet_parts(self,*args):

        try:
            conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM StockPartsDevices '
                           'WHERE ID == "'+self.id_root+'"; ')
            conn.commit()
            conn.close()
            toast(f'Dados deletado com sucesso')
            self.parent.remove_widget(self)
        except:
            toast('Erro! ao deletar os dados')


class OpenPartsDevices(MDBoxLayout):

    def __init__(self,text_id='',texto='',sub='',prateleira='',info='', **kwargs):
        """

        :param text_id: this is an id to the content
        :param texto: An text to be isert on class ButtonStock
        :param sub: An text to be isert on class ButtonStock
        :param prateleira: An text to be isert on class ButtonStock
        :param kwargs: An text to be isert on class ButtonStock
        """
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        self.text_id = str(text_id)
        self.texto = str(texto)
        self.sub_text = str(sub)
        self.prateleira = str(prateleira)

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque '
                       'WHERE ID == "'+self.text_id +'" ')
        content = cursor.fetchall()
        conn.close()

        self.ids.info.text = '[b]Avarias:[/b]  ' + str(info) + '\n\n[b]Model[/b]:  '+ str(content[0][2]) + '\n\nPrateleira\n' + f'[color=#eb3434]{str(prateleira)}[/color]'


        self.creat_txt()
        self.insert_button()

    def insert_button(self,*args,):
        file_id = open('get_id.txt', 'r')
        id = file_id.read()
        file_id.close()

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM StockPartsDevices '
                       'WHERE ID_Device = "'+str(id)+'" ')

        for n, part in enumerate(cursor.fetchall()):
            self.ids.scroll_parts.add_widget(BoxLayout(size_hint_y=None,height=('7dp')))
            self.ids.scroll_parts.add_widget(ButtonParts(namber=str(n+1)+'  [size=40]|[/size]', id=str(part[0]),label=part[2], amount='Quant/'+str(part[7])))


    def creat_txt(self):
        file_jsom = open('get_id.txt', 'w')
        file = file_jsom.write(str(self.text_id))
        file_jsom.close()

    def insert_parts(self):
        self.parent.add_widget(InsertDeviceParts())

    def fechar(self,msg,*args):
        self.clear_widgets()
        # ScreenEstoque().ids.float.remove_widget(msg.parent.parent)
        # print('fechar')


class ButtonStock(BoxLayout):
    def __init__(self,number='', text_id='',texto='',sub='',prateleira='', **kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        self.number = str(number)
        self.text_id = str(text_id)
        self.rotulo = str(texto)
        self.sub_text = str(sub)
        self.prateleira = str(prateleira)

# Here open an box to show thes select devices
    def open_devices(self, id):

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque '
                       'WHERE ID = "'+id+'";')

        content = cursor.fetchall()
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').add_widget(OpenPartsDevices(
            content[0][0], content[0][1]+' - '+content[0][3], content[0][4], str(content[0][5]) + '/' + str(content[0][6]), str(content[0][4])))

    def edit(self, id):

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque '
                       'WHERE ID == "'+ str(id) +'" ')
        content = cursor.fetchall()

        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.label.text = '[color=#FF0000]Editar aparelho[/color]\n'
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.aparelho.text = str(content[0][1])
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.marca.text = str(content[0][3])
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.modelo.text = str(content[0][2])
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.avarias.text = str(content[0][4])
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.prateleira.text = str(content[0][5])
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.espaco.text = str(content[0][6])
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.button_save.text = 'Edit'

    def popup_delet_self(self,roots, *args,**kwargs):
        self.roots = roots

        box = BoxLayout(orientation='vertical',padding='10dp',spacing='10dp')

        box_bt = BoxLayout(spacing='10dp')
        image = Image(source='image/atencao.png')

        self.pop = Popup(title=f'Deseja excluir esse aparelho  " {self.rotulo} "?',size_hint=(None,None),size=('300dp','200dp'), content=box)

        bt_sim = Button(text='Sim',on_release=self.delet_self)
        bt_nao = Button(text='Não', on_release=self.pop.dismiss)
        box_bt.add_widget(bt_sim)
        box_bt.add_widget(bt_nao)

        box.add_widget(image)
        box.add_widget(box_bt)
        self.pop.open()

    def delet_self(self,*args):

        # MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').children[0].clear_widgets()

        try:
            conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM estoque '
                           'WHERE ID == "'+ str(self.text_id)+'" ')

            cursor.execute('DELETE FROM StockPartsDevices '
                           'WHERE ID_Device == "'+ str(self.text_id) +'" ')
            conn.commit()
            conn.close()
            MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').ids.show_parts.remove_widget(self.roots)
            toast('Dados excluidos com sucesso!')
            self.pop.dismiss()
        except:
            toast('Erro! ao excluir os dados!')


class ScreenEstoque(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

    def closed(self,roots):
        self.remove_widget(roots)

    def on_pre_enter(self,*args):
        self.show_device()

    def show_device(self, *args):
        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        data = cursor.execute('SELECT * FROM estoque')

        self.ids.show_parts.clear_widgets()
        for n, iten in enumerate(data.fetchall()):

            self.ids.show_parts.add_widget(BoxLayout(size_hint_y=None,height=('11dp')))

            self.ids.show_parts.add_widget(ButtonStock(number=str(n+1),text_id=iten[0], texto=iten[1] + ' - ' + iten[3], sub=iten[4], prateleira=str(iten[5]) + '/' + str(iten[6])))

    def search_device(self,*args):
        aparelho = str(self.ids.pesq_aparelho.text).title()
        marca = str(self.ids.pesq_marca.text).title()
        modelo = str(self.ids.pesq_modelo.text).title()

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque '
                       'WHERE Aparelho LIKE "'+aparelho+'%" AND Marca LIKE "'+marca+'%" AND Modelo LIKE "'+modelo+'%" ')
        self.ids.show_parts.clear_widgets()

        for n, iten in enumerate(cursor.fetchall()):
            self.ids.show_parts.add_widget(BoxLayout(size_hint_y=None, height=('11dp')))
            self.ids.show_parts.add_widget(ButtonStock(number=str(n+1),text_id=iten[0],texto=iten[1] + ' - ' + iten[3], sub=iten[4], prateleira=str(iten[5]) + '/' + str(iten[6])))

        if aparelho == '' and marca == '' and modelo == '':
            self.show_device()

    def valid_stock(self):

        valid = True

        self.aparelho = str(self.ids.aparelho.text)
        self.marca = str(self.ids.marca.text)
        self.modelo = str(self.ids.modelo.text)
        self.avarias = str(self.ids.avarias.text)
        self.prateleira = str(self.ids.prateleira.text)
        self.espaco = str(self.ids.espaco.text)

        if self.aparelho == '':
            toast('Campo aparelho vasio secione ou digite um aparelho!', duration=5)
            valid = False

        return valid

    def save_deviced(self, msg, *args):
        self.valid_stock()

        # opening the file txt to get the id
        file_id = open('get_id.txt')
        id = file_id.read()
        file_id.close

        conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
        cursor = conn.cursor()

        if msg == 'Edit':
            cursor.execute('UPDATE estoque  '
                           'SET Aparelho = "'+ self.aparelho +'", Modelo = "'+ self.modelo +'", Marca = "'+self.marca+'", Avarias = "'+self.avarias+'", Prateleira = "'+self.prateleira +'", EspacoPrateleira = "'+ self.espaco+'" '
                           'WHERE ID == "'+ id +'" ')
            conn.commit()
            self.return_field()
            toast('Dados alterados com sucesso!')

        elif msg == 'Save':

            # situacao = 'Usado'
            # valor = '50.0'
            if self.valid_stock():

                try:
                    cursor.execute('INSERT INTO estoque(Aparelho, Modelo, Marca, Avarias, Prateleira, EspacoPrateleira)'
                                   'VALUES("'+ self.aparelho +'","'+ self.modelo +'","'+ self.marca +'","'+ self.avarias +'","'+ self.prateleira +'","'+ self.espaco +'")')
                    conn.commit()

                    self.ids.aparelho.text = ''
                    self.ids.marca.text = ''
                    self.ids.modelo.text = ''
                    self.ids.avarias.text = ''
                    self.ids.prateleira.text = ''
                    self.ids.espaco.text = ''

                    self.show_device()
                    toast('Os dados foram salvos com sucesso!')
                except:
                    toast('ERRO! Os dados não foram salvos!!!')
            else:
                pass
        conn.close()
    def return_field(self):
        self.ids.label.text = 'Inserir aparelho\n'
        self.ids.aparelho.text = ''
        self.ids.marca.text = ''
        self.ids.modelo.text = ''
        self.ids.avarias.text = ''
        self.ids.prateleira.text = ''
        self.ids.espaco.text = ''
        self.ids.button_save.text = 'Save'

    def add_parts(self, *args):
        self.add_widget(InsertDeviceParts())


class InsertDeviceParts(Scatter):
    quant = 0
    pos_erro = 0
    pos_cont = 0
    valid_content= []
    def __init__(self,get_id='',edit=False, **kwargs):
        super().__init__(**kwargs)

        self.user_folder = MDApp.get_running_app().user_data_dir + '/'

        self.get_id = get_id
        self.edit = edit

        # Here is to open the insertDeviceParts with thes field amount
        # Aqui é para abrir o insertDeviceParts com o valor do campo
        if self.edit:
            self.editing()

    def editing(self):
        try:
            conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM StockPartsDevices '
                           'WHERE ID == "'+ str(self.get_id) +'" ')
            content = cursor.fetchall()

            soma_valor = float(content[0][5])
            soma_cont = int(content[0][7])
            soma = float(soma_valor * soma_cont)

            self.ids.controller_pecas.text = str(content[0][2])
            self.ids.controller_pecas.readonly = True
            self.ids.controller_modelo.text = str(content[0][3])
            self.ids.controller_modelo.readonly = True
            self.ids.controller_serial.text = str(content[0][4])
            self.ids.controller_serial.readonly = True
            self.ids.controller_valor.text = str(content[0][5])
            self.ids.controller_soma.text = f'{soma:,.2f}'
            self.ids.controller_cont.text = str(content[0][7])

            self.valid_content.append(content[0])
        except:
            pass
        conn.close()

    def fechar(self, msg,*args):
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').remove_widget(self)

    def cont(self,bool,*args):
        """
        Function to alter the field of amounths
        Função para alterar o campo da quantidade
        :param bool: Receive True or False to valid the sinal + or _
        :return:
        """

        try:
            controller_cont = self.ids.controller_cont.text
            self.ids.controller_cont.text = ''
            if controller_cont == '':
                controller_cont = '0'

            self.quant = int(controller_cont)

            if bool: # if the button +  is pressing ========<
                self.quant += 1
                self.ids.controller_cont.text += str(self.quant)

                try:
                    valor = float(self.ids.controller_valor.text) * int(self.ids.controller_cont.text)
                except:
                    valor = 0

                self.ids.controller_soma.text = f'{valor:.2f}'
            elif self.quant <= 0:
                self.ids.controller_cont.text = str(0)
            else: # if the button - is press =============<
                self.quant -= 1
                self.ids.controller_cont.text = str(self.quant)

                try:
                    valor = float(self.ids.controller_valor.text) * int(self.ids.controller_cont.text)
                except:
                    valor = 0
                self.ids.controller_soma.text = f'{valor:.2f}'
        except:
            pass

    def valid(self,*args):
        try:
            self.parts = self.ids.controller_pecas.text
            self.model = self.ids.controller_modelo.text
            self.serial = self.ids.controller_serial.text

            self.valor_unit = self.ids.controller_valor.text
            self.valor_soma = self.ids.controller_soma.text
            self.cont = self.ids.controller_cont.text
        except:
            pass

    def on_pecas(self,*args):
        if int(self.ids.controller_cont.text) >= 1:
            pass
        else:
            self.ids.controller_cont.text = '1'

        if self.ids.controller_pecas.text == '':
            self.ids.controller_cont.text = '0'

    def on_valor_unit(self,*args):

        valor_unit = self.ids.controller_valor.text
        cont = self.ids.controller_cont.text

        #  Text_valor here is to  valid the field of entry of number
        # aqui é para validar o campo de entrada do número
        if valor_unit.isnumeric():
            self.pos_erro = len(valor_unit)
        elif '.' in valor_unit:
        # this "try" is to see if the field does sum
        # esta "try" é para ver se o campo soma
            try:
                s = float(valor_unit) + 1
                self.pos_erro = len(valor_unit)
            except ValueError:
                self.ids.controller_valor.text = str(valor_unit[0:self.pos_erro])
                print('Error in field valor unic')
        elif valor_unit == '':
            self.pos_erro = 0
        else:
            if self.pos_erro > 0:
                self.ids.controller_valor.text = str(valor_unit[0:self.pos_erro])
            else:
                self.ids.controller_valor.text = ''

        try:
            soma = float(valor_unit) * int(cont)
        except ValueError:
            soma = 0.0

        self.ids.controller_soma.text = str(soma)

    def on_texto(self,*args,**kwargs):

        try:
            # here is only to valid the field text
            # aqui é apenas para validar o texto do campo
            text_valor = self.ids.controller_valor.text
            text_cont = self.ids.controller_cont.text

            #  Text_valor here is to  valid the field of entry of number
            # aqui é para validar o campo de entrada do número
            if text_valor.isnumeric():
                self.pos_erro = len(text_valor)
            elif '.' in text_valor:
            # this "try" is to see if the field does sum
            # esta "try" é para ver se o campo soma
                try:
                    s = float(text_valor) + 1
                    self.pos_erro = len(text_valor)
                except ValueError:
                    self.ids.controller_valor.text = str(text_valor[0:self.pos_erro])
                    print('Error in field valor unic')
            elif text_valor == '':
                self.pos_erro = 0
            else:
                if self.pos_erro > 0:
                    self.ids.controller_valor.text = str(text_valor[0:self.pos_erro])
                else:
                    self.ids.controller_valor.text = ''

            # Text_cont ==========
            if text_cont.isnumeric():
                self.pos_cont = len(text_cont)
            elif text_cont == '':
                self.pos_cont = 0
            else:
                if self.pos_cont > 0:
                    self.ids.controller_cont.text = str(text_cont[0:self.pos_cont])
                else:
                    self.ids.controller_cont.text = '0'
        except:
            pass

    def save_data_deviced(self):

        parts = self.ids.controller_pecas.text
        model = self.ids.controller_modelo.text
        serial = self.ids.controller_serial.text

        valor_unit = self.ids.controller_valor.text
        cont = self.ids.controller_cont.text


        try:
            # Here change the seting of box insertPartsDevices
            if self.edit:
                try:
                    if float(valor_unit) != float(self.valid_content[0][5]) and int(cont) != int(self.valid_content[0][7]):
                        self.popup_save(f'Campos alterados:\nValor:  {self.valid_content[0][5]}  =>  {valor_unit}\n'
                                        f'Quantidade:  {self.valid_content[0][7]}  =>  {cont}')
                    elif float(valor_unit) != float(self.valid_content[0][5]):
                        self.popup_save(f'Campo alterado:\nValor  {self.valid_content[0][5]}  =>  {valor_unit}')
                    elif int(cont) != int(self.valid_content[0][7]):
                        self.popup_save(f'Campo alterado:\nQuantidade alterada:  {self.valid_content[0][7]}  =>  {cont}')
                    else:
                        toast('Nenhun dados alterados para ser salvo!')

                except ValueError:
                    valor_unit = 0
                    if float(valor_unit) != float(self.valid_content[0][5]):
                        self.popup_save(f'Campo alterado {self.valid_content[0][5]} => {valor_unit}')
                    elif int(cont) != int(self.valid_content[0][7]):
                        self.popup_save(f'Campo alterado:\nQuantidade alterada:{self.valid_content[0][7]} => {cont}')
            else:

                if parts == '':
                    toast('Insira pelo menos o nome da peça!')
                else:
                    self.ids.controller_cont.text = '1'
                    file_id = open('get_id.txt','r')
                    id = file_id.read()
                    file_id.close()

                    conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO StockPartsDevices(ID_Device, Peca, Modelo, Serial, ValorUnit, Quantidade)'
                                   'VALUES("'+ str(id) +'", "'+ str(parts).title() +'", "'+ str(model) +'", "'+ str(serial) +'", "'+ str(valor_unit) +'", "'+ str(cont) +'" )')
                    conn.commit()
                    conn.close()
                    self.fechar(self)
                    toast('Dados salvos com sucesso!')
        except:
            toast('Erro! Ao salvar dados')

    def update(self,*args,**kwargs):

        valor_unit = self.ids.controller_valor.text
        cont = self.ids.controller_cont.text
        try:
            conn = sqlite3.connect(str(self.user_folder) + 'Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE StockPartsDevices '
                           'SET ValorUnit = "'+str(valor_unit)+'", Quantidade = "'+ str(cont) +'" '
                           'WHERE ID == "'+ str(self.get_id) +'" ')
            conn.commit()
            conn.close()
            toast('Dados alterado com sucesso!')
        except:
            toast('Erro! ao alterar os dados!!!')

    def popup_save(self,msg='',*args,**kwargs):

        box = BoxLayout(orientation='vertical')
        box_button = BoxLayout(spacing='20dp',padding='5dp')

        image = Image(source='image/atencao.png')
        label = MDLabel(text=str(msg),halign='center')

        popup = Popup(title='Alterar dados?',size_hint=(None,None),size=('300dp','200dp'), content=box)

        bt_sim = Button(text='Sim', on_press = self.update, on_release = popup.dismiss)
        bt_nao = Button(text='Não', on_release=popup.dismiss)

        box_button.add_widget(bt_sim)
        box_button.add_widget(bt_nao)

        box.add_widget(image)
        box.add_widget(label)
        box.add_widget(box_button)

        popup.open()


class Rotulo_garantia(MDCard):
    def __init__(self, input='', output='', warranty='', **kwargs):
        super().__init__(**kwargs)
        self.input = str(input)
        self.output = str(output)
        self.warranty   = str(warranty)


class ScreenPartsNew(Screen):
    pass


class SmartTile(SmartTileWithStar):
    def __init__(self,img='', img_text='',**kwargs):
        """
        Class to insert the image in class ImageParts
        :param img: receive the path of image
        :param img_text: receive only the name of image
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.image= str(img)
        self.img_text = str(img_text)

    def insert_name_image(self,*args,**kwargs):            # 795
        file = open('NameDevice.txt','w')
        file.write(str(self.img_text))
        self.parent.parent.parent.parent.parent.parent.dismiss()
        toast('Aperte qualquer tecla no campo modelo para preencher o campo modelo da image selecionado', duration=5)


class ImageParts(MDBoxLayout):
    def __init__(self, **kwargs):
        """
        Class to show the type of image
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.folder_image()
    def folder_image(self,*args, **kwargs):
        path = 'image/image_parts/'
        source = os.listdir(path)

        for img in source:
            self.ids.box_image.add_widget(SmartTile(img=str(path) + str(img), img_text=str(img)))


class EletronicaApp(MDApp):
    def build(self):
        Builder.load_string(open('kv_eletronica.kv', encoding='utf-8').read())
        # Builder.load_string(open('screens.kv', encoding='utf-8').read())
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Green'
        return Manager()


if __name__ == '__main__':
    EletronicaApp().run()