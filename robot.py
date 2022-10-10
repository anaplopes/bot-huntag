# -*- coding: utf-8 -*-
import re
import os
import time
import unicodedata
from math import ceil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.operating import OperatingSystem
from database.connection import ConnectionDB
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Robot:

    def __init__(self):
        self.db = ConnectionDB()
        self.opsys = OperatingSystem()


    def config(self):
        # inicia e configura driver
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-logging')
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')
        service = Service(ChromeDriverManager().install())
        # service = Service('C:/chromedriver_win32/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1195, 666)
        driver.implicitly_wait(20) # seconds
        return driver


    def login(self, driver):
        try:
            driver.get(os.getenv('HUNTAG_URL'))
            driver.find_element(By.ID, 'Email').send_keys(os.getenv('EMAIL'))
            driver.find_element(By.ID, 'Password').send_keys(os.getenv('PASSWORD'))
            driver.find_element(By.XPATH, '//input[@type="submit"][@value="Login"]').submit()

        except Exception as e:
            raise Exception(f'Login Error: {str(e)}')


    def search(self, driver, row):
        try:
            # selecionar categoria
            categoria = Select(driver.find_element(By.ID, 'categoriesSelect'))
            categoria.select_by_visible_text('Merchandising')

            # selecionar subcategoria
            time.sleep(3)
            subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
            subcategoria_1 = Select(subcategorias[0])
            subcategoria_1.select_by_visible_text(row['subcategoria1'])

            time.sleep(3)
            subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
            subcategoria_2 = Select(subcategorias[1])
            subcategoria_2.select_by_visible_text(row['subcategoria2'])

            if row['subcategoria3']:
                time.sleep(3)
                subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
                subcategoria_3 = Select(subcategorias[2])
                subcategoria_3.select_by_visible_text(row['subcategoria3'])

            if row['subcategoria4']:
                time.sleep(3)
                subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
                subcategoria_4 = Select(subcategorias[3])
                subcategoria_4.select_by_visible_text(row['subcategoria4'])

            if row['subcategoria5']:
                time.sleep(3)
                subcategorias = driver.find_elements(By.XPATH, '//div[@id="subCategoriesDiv"]/select[@class="form-control"]')
                subcategoria_5 = Select(subcategorias[4])
                subcategoria_5.select_by_visible_text(row['subcategoria5'])

            # pesquisar
            time.sleep(3)
            driver.find_element(By.ID, 'SearchButton').click()

        except Exception as e:
            raise Exception(f'Search Error: {str(e)}')


    def download_control(self, category:str, item_name:str, fileId:str, file_name:str, status:str):
        try:
            self.db.insert(
                table='download_control',
                columns='category, itemName, fileId, fileName, status, createdOn',
                values=f'"{category}", "{item_name}", "{fileId}", "{file_name}", "{status}", "{datetime.now().strftime("%d/%m/%Y %H:%M")}"')

        except Exception as e:
            raise Exception(f'Download Control Error: {str(e)}')


    def moved_file(self, item_name:str, file_id: str, file_name:str, category:str):
        try:
            dir_download = os.getenv('PATH_DIR_DOWNLOAD')
            dir_target = f'{os.getenv("PATH_DIR_TARGET")}/{category}/{item_name}'
        
            self.opsys.create_dirs(dirname=dir_target)
            
            found_file = False
            for root, dirs, files in os.walk(dir_download, topdown=False):
                for name in files:
                    if name.split('.')[0] == file_name:
                        src = os.path.join(root, name)
                        # self.opsys.move_file(source=src, destiny=dst)
                        self.opsys.copy_file(source=src, destiny=dir_target)

                        time.sleep(3)
                        print(f'{datetime.now()} - Inserindo no controle de download ...')
                        self.download_control(category=category, item_name=item_name, fileId=file_id, file_name=name, status="Arquivo baixado")
                        found_file = True
                        self.opsys.delete_file(filename=src)
                        break

            if not found_file:
                raise Exception('Arquivo não localizado no diretorio Downloads')

        except Exception as e:
            raise Exception(f'Moved File Error: {str(e)}')


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
                ctg = [v for k, v in row.items() if k.startswith('subcategoria') and v]
                category = '/'.join(ctg)
                
                print(f'{datetime.now()} - Pesquisando {category} ...')
                self.search(driver=driver, row=row)
                
                time.sleep(5)
                records = driver.execute_script("return document.getElementsByClassName('item active')")
                txt_records_search = driver.execute_script("return document.querySelectorAll('.text-center h2')[0].textContent")
                
                total_records_search = int(re.findall(r'\d+', txt_records_search)[0])
                qtd_records_page = len(records)
                qtd_page = ceil(total_records_search / 30)
                idx = 0

                while qtd_records_page > 0:
                    print(f'{datetime.now()} - Selecionar registro {idx + 1} de {len(records)} ...')
                    records[idx].click()

                    time.sleep(3)
                    item_name = driver.execute_script("return document.querySelector('.item h3').textContent").strip()
                    print(f'{datetime.now()} - Item {item_name} ...')

                    download = driver.execute_script("return document.querySelectorAll('.item-download a')")
                    titulo = driver.execute_script("return document.getElementsByClassName('panel-footer title ellipsis')")

                    for index, item in enumerate(download):
                        try:
                            print(f'{datetime.now()} - Arquivo {index + 1} de {len(download)} ...')

                            name = titulo[index].text
                            file_name = unicodedata.normalize('NFD', name.strip()).encode('ascii', 'ignore').decode('utf8').replace('\n', '_').replace('"', "'").replace(' ', '+')
                            file_name = re.sub(r"m2+", "m²", file_name)

                            file_href = item.get_attribute('href')
                            file_id = re.sub(r"\D", "", file_href)

                            be_downloaded = self.db.select_filter(table='download_control', where=f'fileId == "{file_id}"')
                            if be_downloaded: 
                                print(f'{datetime.now()} - Arquivo ja baixado {name} ...')
                                continue

                            print(f'{datetime.now()} - Baixando {name} ...')
                            item.click()

                            print(f'{datetime.now()} - Aguardando carregamento do arquivo {file_name} ...')
                            time.sleep(120) # 2 minutos
                            print(f'{datetime.now()} - Movendo arquivo {file_name} ...')
                            self.moved_file(item_name=item_name, file_id=file_id, file_name=file_name, category=category)

                        except Exception as e:
                            error = str(e).replace('?', '')
                            print(error)
                            self.download_control(category=category, item_name=item_name, fileId=file_id, file_name=file_name, status=error)
                            continue
                    
                    print(f'{datetime.now()} - Voltando a pagina ...')
                    driver.find_element(By.XPATH, '//div[@id="hbreadcrumb"]/ol/li/a[@href="/"]').click()

                    if qtd_page > 1 and qtd_records_page == 1:
                        print(f'{datetime.now()} - Indo para proxima pagina ...')
                        next_page = driver.execute_script("return document.getElementsByClassName('fa fa-chevron-right')")
                        next_page[0].click()
                        
                        time.sleep(5)
                        records = driver.execute_script("return document.getElementsByClassName('item active')")
                        qtd_records_page = len(records)
                        qtd_page -= 1
                        idx = 0

                    else:
                        time.sleep(5)
                        qtd_records_page -= 1
                        idx += 1
                        records = driver.execute_script("return document.getElementsByClassName('item active')")

                    
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
                os.system("start C:\\bot-huntag\\devops\\start.ps1")
                driver.quit()
            except Exception:
                pass

bot = Robot()
bot.run()
