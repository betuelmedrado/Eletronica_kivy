
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

class ScreenLogin(Screen):

    lista = []
    map = {}
    def __init__(self,*args,**kwargs):
        super(ScreenLogin,self).__init__(**kwargs)


    def content_base(self):
        """
        To get the quant of returning client
        :return: A list witch the quant of found client
        """
        self.cpf = self.ids.login_cpf.text

        conn = sqlite3.connect('Eletronica.db')
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

        if len(cliente) < 1:
            self.ids.warning.text = 'Nome ou CPF invalido!'
            self.ids.float_layout.add_widget(ButtonRegister())
        else:
            self.ids.warning.text = ''
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

    def valor_button(self):
        print('entrou')


class ScreenRegister(Screen,Date):

    def __init__(self,**kwargs):
        super(ScreenRegister,self).__init__(**kwargs)

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


        conn = sqlite3.connect('Eletronica.db')
        cursor = conn.cursor()
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
            self.ids.label_warning.text = ''
            # self.ids.cadastro_cpf.color_mode = 'none'
            self.ids.cadastro_cpf.line_color_focus = 0, 0, 0, 1
        except sqlite3.IntegrityError:
            self.ids.label_warning.text = f'CPF ({str(cpf)}) já cadastrado'
            self.ids.cadastro_cpf.color_mode = 'custom'
            self.ids.cadastro_cpf.line_color_focus = 1,0,0,1

    def criaBd(self):
        conn = sqlite3.connect('Eletronica.db')
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

    def __init__(self,*args,**kwargs):
        super(Aparelho,self).__init__(**kwargs)
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

            conn = sqlite3.connect('Eletronica.db')
            conn.cursor()
            conn.execute('INSERT INTO produtos(Entrada,ValorConserto,ClienteID,Modelo,Marca,Serial,Defeito,Situação)'
                         'VALUES ("'+str(self.date)+'","'+str(valorConserto)+'" ,"'+str(id_nome)+'", "'+str(modelo)+'", "'+str(marca)+'","'+str(serial)+'" ,"'+str(defeito)+'", "'+str(situacao)+'")')
            conn.commit()

            self.ids.modelo.text = ''
            self.ids.id_marca.text = ''
            self.ids.serial.text = ''
            self.ids.defeito.text = ''
            self.ids.cituacao.text = ''
            self.ids.valor_conserto.text = ''

            self.snackbar('Aparelho salvo com sucesso!')

            MDApp.get_running_app().root.ids.manager.current = 'screenimage'
        except:
            print('ERRO class Aparelho')

    def snackbar(self, texto):
        snack = SnackBar(texto)
        snack.open()


class ScreenView(Screen):

    lista = []
    get = []
    def __init__(self,*args,**kwargs):
        super(ScreenView,self).__init__(**kwargs)

    def content_user(self):

        self.data = {}
        linha = []
        # Geting the name of file txt
        try:
            with open('getNome.json','r', encoding='utf-8') as get_data:
                 self.data = json.load(get_data)

            conn = sqlite3.connect('Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cliente WHERE CPF == "'+str(self.data["CPF"])+'" ')
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

        conn = sqlite3.connect('Eletronica.db')
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
                self.ids.scroll.add_widget(Box_View(content=str(item['Modelo']),
                                                    sub=str(item['Marca']),
                                                    imag=str(item['Modelo']).title()))

        except AttributeError:
            print('ERROR: linha 324 na class ScreenView a variavel get não recebel um data base!')

    def on_pre_enter(self):

        self.content_user()
        self.content_device()
        self.insert_content_produtos()

    def on_leave(self):
        self.get.clear()
        # with open('getNome.json', 'w') as nome:
        #     json.dump([],nome)
        pass

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

    def data_base(self):

        #geting the name of device
        nome_device = open('NameDevice.txt','r', encoding='utf-8')
        device_nome = nome_device.read()
        nome_device.close()

        # geting the id of client
        _id_cliente = self.name_id()

        conn = sqlite3.connect('Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos WHERE ClienteID == "'+str(_id_cliente['ID'])+'" AND Modelo == "'+str(device_nome)+'"  ')
        content = cursor.fetchall()

        # geting the id current of device
        self.id_current = str(content[0][0])

        self.ids.modelo.text = str(content[0][6])
        self.ids.id_marca.text = str(content[0][7])
        self.ids.serial.text = str(content[0][8])
        self.ids.defeito.text = str(content[0][9])
        self.ids.valor_conserto.text = str(content[0][3])

        if str(content[0][10]) == 'Orçamento':
            self.ids.cituacao.icon = 'hand-back-left'
            self.ids.cituacao.text = str(content[0][10])
            self.ids.orcamento.active = True
        elif str(content[0][10]) == 'Arrumar':
            self.ids.cituacao.icon = 'account-check'
            self.ids.cituacao.text = str(content[0][10])
            self.ids.arrumar.active = True
        elif str(content[0][10]) =='Devolver':
            self.ids.cituacao.icon = 'thumb-down'
            self.ids.cituacao.text = str(content[0][10])
            self.ids.devolcer.active = True
        elif str(content[0][10]) == 'Entregue':
            self.ids.cituacao.icon = 'handshake'
            self.ids.cituacao.text = str(content[0][10])
            self.ids.arrumado.active = True
        elif str(content[0][10]) == 'Arrumado':
            self.ids.cituacao.icon = 'check-underline-circle'
            self.ids.cituacao.text = str(content[0][10])
            self.ids.entregue.active = True

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
            coon = sqlite3.connect('Eletronica.db')
            cursor = coon.cursor()
            cursor.execute('UPDATE produtos SET Modelo = "'+str(self.ids.modelo.text)+'", Marca = "'+str(self.ids.id_marca.text)+'", Serial = "'+str(self.ids.serial.text)+'", Defeito = "'+str(self.ids.defeito.text)+'", ValorConserto = "'+str(self.ids.valor_conserto.text)+'", Situação = "'+str(self.ids.cituacao.text)+'" '
            'WHERE ID == "'+str(self.id_current)+'" ')

            coon.commit()
            self.ids.text_warning.text = 'Alterações feita com sucesso!'
            Clock.schedule_once(self.warning, 3)
        except :
            self.ids.text_warning.text = 'As alterações não foram salvas!'
            Clock.schedule_once(self.warning, 5)

    def warning(self,*args):
        self.ids.text_warning.text = ''

    def on_pre_enter(self, *args):
        self.data_base()


class Box_View(MDCard):

    map = {}
    def __init__(self,content='',sub='',imag='',**kwargs):
        super().__init__(**kwargs)
        # self.ids.bt_content.text = str(content)
        self.text = str(content)
        self.sub_text = str(sub)
        self.image = str('image/'+ imag + '.png')

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

        conn = sqlite3.connect('Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos WHERE ClienteID == "'+str(id_client)+'" AND Modelo == "' + str(txt.text) + '" ')
        get_cursor = cursor.fetchall()

        # print('teste', get_cursor)
        return get_cursor


    # Here is to open the content of popup
    def text_of_button(self,txt):

        # print(self.image)
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

        # always writing the name of device in file txt
        # sempre escrevendo o nome do aparelho no arquivo txt
        name_device = open('NameDevice.txt','w',encoding='utf-8')
        name_device.write(str(obg_device[0][6]))
        name_device.close()

        # screen_view.ids.mdcard_view.add_widget(pop.open())
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
        self.namber = str(namber)
        self.get_id = id
        self.labels = label
        self.amount = amount

    def view_parts(self):
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').add_widget(InsertDeviceParts(self.get_id,True))


    def popup(self,id,*args,**kwargs):

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
            conn = sqlite3.connect('Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM StockPartsDevices '
                           'WHERE ID == "'+self.id_root+'"; ')
            conn.commit()
            conn.close()
            toast(f'Dados deletado com sucesso')
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
        self.ids.info.text = str(info) + '\n\nPrateleira\n' + f'[color=#eb3434]{str(prateleira)}[/color]'

        self.text_id = str(text_id)
        self.texto = str(texto)
        self.sub_text = str(sub)
        self.prateleira = str(prateleira)

        self.creat_txt()
        self.insert_button()

    def insert_button(self,*args,):
        file_id = open('get_id.txt', 'r')
        id = file_id.read()
        file_id.close()

        conn = sqlite3.connect('Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM StockPartsDevices '
                       'WHERE ID_Device = "'+str(id)+'" ')

        for n, part in enumerate(cursor.fetchall()):
            self.ids.scroll_parts.add_widget(BoxLayout(size_hint_y=None,height=('7dp')))
            self.ids.scroll_parts.add_widget(ButtonParts(namber=str(n+1), id=str(part[0]),label=part[2], amount='Quant/'+str(part[7])))


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

        self.number = str(number)
        self.text_id = str(text_id)
        self.rotulo = str(texto)
        self.sub_text = str(sub)
        self.prateleira = str(prateleira)

# Here open an box to show thes select devices
    def open_devices(self, id):

        conn = sqlite3.connect('Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque '
                       'WHERE ID = "'+id+'";')

        content = cursor.fetchall()
        MDApp.get_running_app().root.ids.manager.get_screen('screenestoque').add_widget(OpenPartsDevices(
            content[0][0], content[0][1]+' - '+content[0][3], content[0][4], str(content[0][5]) + '/' + str(content[0][6]), str(content[0][4])))


class ScreenEstoque(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def closed(self,roots):
        self.remove_widget(roots)

    def on_pre_enter(self,*args):
        self.show_device()

    def show_device(self, *args):
        conn = sqlite3.connect('Eletronica.db')
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

        conn = sqlite3.connect('Eletronica.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque '
                       'WHERE Aparelho LIKE "'+aparelho+'%" AND Marca LIKE "'+marca+'%" AND Modelo LIKE "'+modelo+'%" ')
        self.ids.show_parts.clear_widgets()

        for n, iten in enumerate(cursor.fetchall()):
            self.ids.show_parts.add_widget(BoxLayout(size_hint_y=None, height=('11dp')))
            self.ids.show_parts.add_widget(ButtonStock(number=str(n+1),text_id=iten[0],texto=iten[1] + ' - ' + iten[3], sub=iten[4], prateleira=str(iten[5]) + '/' + str(iten[6])))

        if aparelho == '' and marca == '' and modelo == '':
            self.show_device()

    def save_deviced(self,*args):
        aparelho = str(self.ids.aparelho.text)
        marca = str(self.ids.marca.text)
        modelo = str(self.ids.modelo.text)
        avarias = str(self.ids.avarias.text)
        prateleira = str(self.ids.prateleira.text)
        espaco = str(self.ids.espaco.text)

        # situacao = 'Usado'
        # valor = '50.0'
        try:
            conn = sqlite3.connect('Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO estoque(Aparelho, Modelo, Marca, Avarias, Prateleira, EspacoPrateleira)'
                           'VALUES("'+ aparelho +'","'+ modelo +'","'+ marca +'","'+ avarias +'","'+ prateleira +'","'+ espaco +'")')
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

    def add_parts(self, *args):
        self.add_widget(InsertDeviceParts())

class InsertDeviceParts(Scatter):
    quant = 0
    pos_erro = 0
    pos_cont = 0
    valid_content= []

    def __init__(self,get_id='',edit=False, **kwargs):
        super().__init__(**kwargs)
        self.get_id = get_id
        self.edit = edit

        # Here is to open the insertDeviceParts with thes field amount
        # Aqui é para abrir o insertDeviceParts com o valor do campo
        if edit:
            self.editing()

    def editing(self):
        try:
            conn = sqlite3.connect('Eletronica.db')
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
            self.ids.controller_soma.text = f'{soma:.2f}'
            self.ids.controller_cont.text = str(content[0][7])

            self.valid_content.append(content[0])
        except:
            pass

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

    def on_texto(self,*args,**kwargs):

        try:
            # self.valid()

            # if self.ids.controller_cont.text == '' or self.ids.controller_cont.text == 0:
            #     self.ids.controller_cont.text = '1'
            #     self.cont = 1
            # else:
            #     self.cont = int(self.ids.controller_cont.text)


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


            # try:
            #     soma = float(self.valor_unit) * int(self.cont)
            # except ValueError:
            #     soma = 0.0
            #
            # self.ids.controller_soma.text = str(soma)
        except:
            pass

    def save_data_deviced(self):
        self.valid()

        try:
            # Here change the seting of box insertPartsDevices
            if self.edit:
                try:
                    if float(self.valor_unit) != float(self.valid_content[0][5]) and int(self.cont) != int(self.valid_content[0][7]):
                        self.popup_save(f'Campos alterados:\nValor:  {self.valid_content[0][5]}  =>  {self.valor_unit}\n'
                                    f'Quantidade:  {self.valid_content[0][7]}  =>  {self.cont}')
                    elif float(self.valor_unit) != float(self.valid_content[0][5]):
                        self.popup_save(f'Campo alterado:\nValor  {self.valid_content[0][5]}  =>  {self.valor_unit}')
                    elif int(self.cont) != int(self.valid_content[0][7]):
                        self.popup_save(f'Campo alterado:\nQuantidade alterada:  {self.valid_content[0][7]}  =>  {self.cont}')
                    else:
                        pass

                except ValueError:
                    self.valor_unit = 0
                    if float(self.valor_unit) != float(self.valid_content[0][5]):
                        self.popup_save(f'Campo alterado {self.valid_content[0][5]} => {self.valor_unit}')
                    elif int(self.cont) != int(self.valid_content[0][7]):
                        self.popup_save(f'Campo alterado:\nQuantidade alterada:{self.valid_content[0][7]} => {self.cont}')
            else:
                file_id = open('get_id.txt','r')
                id = file_id.read()
                file_id.close()

                conn = sqlite3.connect('Eletronica.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO StockPartsDevices(ID_Device, Peca, Modelo, Serial, ValorUnit, Quantidade)'
                               'VALUES("'+ str(id) +'", "'+ str(self.parts) +'", "'+ str(self.model) +'", "'+ str(self.serial) +'", "'+ str(self.valor_unit) +'", "'+ str(self.cont) +'" )')
                conn.commit()
                conn.close()
            self.fechar(self)
            toast('Dados salvos com sucesso!')
        except:
            toast('Erro! Ao salvar dados')

    def update(self,*args,**kwargs):
        self.valid()
        try:
            conn = sqlite3.connect('Eletronica.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE StockPartsDevices '
                           'SET ValorUnit = "'+str(self.valor_unit)+'", Quantidade = "'+ str(self.cont) +'" '
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