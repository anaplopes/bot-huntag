# -*- coding: utf-8 -*-
import re
import os
import time
from math import ceil
from datetime import datetime
from unicodedata import name
from selenium import webdriver
from unidecode import unidecode
from utils.dirfile import DirFileUtil
from selenium.webdriver.common.by import By
from database.db_connection import DbConnection
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Gallery:

    def __init__(self):
        self.db = DbConnection()
        self.dirfile = DirFileUtil()


    def config(self):
        # inicia e configura driver
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        # service = Service('C:/chromedriver_win32/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(20) # seconds
        # driver.maximize_window()
        return driver


    def login(self, driver):
        try:
            driver.get('https://app.huntag.com.br/Login')
            driver.find_element(By.ID, 'Email').send_keys('diana.godoi@grupotj.com.br')
            driver.find_element(By.ID, 'Password').send_keys('Tj123456!')
            driver.find_element(By.XPATH, '//input[@type="submit"][@value="Login"]').submit()

        except Exception as e:
            error = str(e)
            print(f'Login Error: {error}')
            raise Exception(f'Login Error: {error}')


    def search(self, driver, row):
        try:
            # selecionar categoria
            categoria = Select(driver.find_element(By.ID, 'categoriesSelect'))
            categoria.select_by_visible_text('Merchandising')

            # selecionar subcategoria
            time.sleep(5)
            subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
            subcategoria_1 = Select(subcategorias[0])
            subcategoria_1.select_by_visible_text(row['subcategoria1'])

            time.sleep(5)
            subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
            subcategoria_2 = Select(subcategorias[1])
            subcategoria_2.select_by_visible_text(row['subcategoria2'])

            if row['subcategoria3']:
                time.sleep(5)
                subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
                subcategoria_3 = Select(subcategorias[2])
                subcategoria_3.select_by_visible_text(row['subcategoria3'])

            if row['subcategoria4']:
                time.sleep(5)
                subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
                subcategoria_4 = Select(subcategorias[3])
                subcategoria_4.select_by_visible_text(row['subcategoria4'])

            if row['subcategoria5']:
                time.sleep(5)
                subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
                subcategoria_5 = Select(subcategorias[4])
                subcategoria_5.select_by_visible_text(row['subcategoria5'])

            # pesquisar
            time.sleep(3)
            driver.find_element(By.ID, 'SearchButton').click()

        except Exception as e:
            error = str(e)
            print(f'Search Error: {error}')
            raise Exception(f'Search Error: {error}')


    def download_control(self, item_name:str, filename:str, category:str, status:str):
        try:
            self.db.insert(
                table='download_control',
                columns='item_name, filename, category, status, created_on',
                values=f'"{item_name}", "{filename}", "{category}", "{status}", "{datetime.now().strftime("%d/%m/%Y %H:%M")}"')

        except Exception as e:
            error = str(e)
            print(f'Download Control Error: {error}')
            raise Exception(f'Download Control Error: {error}')


    def moved_file(self, filename:str, item_name:str, title:str):
        try:
            moved = False
            dir_download = 'C:/Users/diana/Downloads'
            dir_hd = f'E:/HUNTAG/{title}/{item_name}'
        
            self.dirfile.create_dirs(dirname=dir_hd)
            
            for root, dirs, files in os.walk(dir_download):
                for name in files:
                    if name.startswith(filename.split('.')[0]):
                        self.dirfile.copy_file(source=f'{dir_download}/{name}', destiny=f'{dir_hd}')

                        print(f'{datetime.now()} - Inserindo no controle de download ...')
                        self.download_control(item_name=item_name, filename=filename, category=title, status="Arquivo baixado")
                        moved = True

                        time.sleep(5)
                        self.dirfile.delete_file(filename=f'{dir_download}/{name}')

                        time.sleep(5)
                        break

            if not moved:
                print(f'{datetime.now()} - Inserindo no controle de download ...')
                self.download_control(item_name=item_name, filename=filename, category=title, status="Arquivo não movido")


        except Exception as e:
            error = str(e)
            print(f'Moved File Error: {error}')
            raise Exception(f'Moved File Error: {error}')


    def run(self):
        try:
            print(f'{datetime.now()} - Configurando o driver ...')
            driver = self.config()

            print(f'{datetime.now()} - Fazendo login ...')
            self.login(driver=driver)

            print(f'{datetime.now()} - Buscando programação ...')
            rows = self.db.select_filter(table='schedule', where='isActive = "true"')
            if not rows:
                print(f'{datetime.now()} - Nenhuma execução programada')

            for row in rows:
                sub1 = row["subcategoria1"]
                sub2 = f'/{row["subcategoria2"]}' if row["subcategoria2"] else ''
                sub3 = f'/{row["subcategoria3"]}' if row["subcategoria3"] else ''
                sub4 = f'/{row["subcategoria4"]}' if row["subcategoria4"] else ''
                sub5 = f'/{row["subcategoria5"]}' if row["subcategoria5"] else ''
                title = f'{sub1}{sub2}{sub3}{sub4}{sub5}'
                
                print(f'{datetime.now()} - Pesquisando {title} ...')
                self.search(driver=driver, row=row)
                
                time.sleep(5)
                records = driver.execute_script("return document.getElementsByClassName('item active')")
                txt_records_search = driver.execute_script("return document.querySelectorAll('.text-center h2')[0].textContent")
                total_records_search = int(re.findall(r'\d+', txt_records_search)[0])
                qtd_records_page = len(records)
                qtd_page = ceil(total_records_search / 30)
                idx = 0
                while qtd_records_page > 0:

                    time.sleep(5)
                    print(f'{datetime.now()} - Selecionar registro {idx + 1} de {len(records)} ...')
                    records[idx].click()

                    time.sleep(5)
                    item_name = driver.execute_script("return document.querySelector('.item h3').textContent")

                    try:
                        download = driver.execute_script("return document.querySelectorAll('.item-download a')")
                        titulo = driver.execute_script("return document.getElementsByClassName('panel-footer title ellipsis')")

                        for index, item in enumerate(download):
                            name = titulo[index].text
                            file_name = unidecode(name).replace('\n', '_').replace(' ', '+')

                            be_downloaded = self.db.select_filter(table='download_control', where=f'filename = "{file_name}"')
                            if be_downloaded:
                                continue

                            print(f'{datetime.now()} - Baixando arquivo ...')
                            item.click()
                        
                            time.sleep(20) # 20 segundos
                            print(f'{datetime.now()} - Movendo arquivo {name} ...')
                            self.moved_file(filename=file_name, item_name=item_name, title=title)
                        
                        time.sleep(5)
                        print(f'{datetime.now()} - Voltando a pagina ...')
                        driver.find_element(By.XPATH, '//div[@id="hbreadcrumb"]/ol/li/a[@href="/"]').click()

                        if qtd_page > 1 and qtd_records_page == 1:
                            time.sleep(5)
                            print(f'{datetime.now()} - Indo para proxima pagina ...')
                            next_page = driver.execute_script("return document.getElementsByClassName('fa fa-chevron-right')")
                            next_page[0].click()
                            
                            records = driver.execute_script("return document.getElementsByClassName('item active')")
                            qtd_records_page = len(records)
                            qtd_page -= 1
                            idx = 0

                        else:
                            time.sleep(5)
                            qtd_records_page -= 1
                            idx += 1
                            records = driver.execute_script("return document.getElementsByClassName('item active')")

                    except Exception as e:
                        error = str(e)
                        print(f'Run Error: {error}')
                        self.download_control(item_name=item_name, filename='', category=title, status=f'Run Error: {error}')
                        pass
                    
                time.sleep(5)
                print(f'{datetime.now()} - Voltando a Home Page ...')
                self.db.update(table='schedule', col_val='isActive = "false"', where=f'id = {row["id"]}')
                driver.find_element(By.XPATH, '//div/ul/li/a[@href="/Home/Gallery"]').click()
            
            print('Finalizado')

        except Exception as e:
            error = str(e)
            print(error)
            return error

        finally:
            try:
                self.db.finish()
                driver.close()
                driver.quit()
            except Exception:
                pass

robot = Gallery()
robot.run()
