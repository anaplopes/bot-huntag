# -*- coding: utf-8 -*-
import time
from datetime import datetime
from selenium import webdriver
from unidecode import unidecode
from utils.dirfile import DirFileUtil
from selenium.webdriver.common.by import By
from database.db_connection import DbConnection
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DownloadQueue:

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
        # driver.maximize_window()
        return driver


    def login(self, driver):
        # login
        try:
            driver.get('https://app.huntag.com.br/Login')
            driver.find_element(By.ID, 'Email').send_keys('diana.godoi@grupotj.com.br')
            driver.find_element(By.ID, 'Password').send_keys('Tj123456!')
            driver.find_element(By.XPATH, '//input[@type="submit"][@value="Login"]').submit()

        except Exception as e:
            raise Exception(f'Login Error: {e}')


    def moved_file(self, row, filename):
        try:
            dir_download = 'C:/Users/diana/Downloads'
            dir_hd = f'E:/HUNTAG/{row["category"]}/{row["file_name"]}'
            
            self.dirfile.create_dirs(dirname=dir_hd)

            self.dirfile.unzip_file(
                dirname=dir_hd, 
                zipname=f'{dir_download}/{filename}.zip')

            time.sleep(10)
            print(f'{datetime.now()} - Atualizando controle ...')
            self.db.update(
                table='download_control',
                col_val='status = "kit baixado"',
                where=f'id = {row["id"]}')
            
            time.sleep(5)
            self.dirfile.delete_file(filename=f'{dir_download}/{filename}.zip')

        except Exception as e:
            raise Exception(f'Moved File Error: {e}')


    def run(self):
        try:
            print(f'{datetime.now()} - Configurando o driver ...')
            driver = self.config()

            print(f'{datetime.now()} - Fazendo login ...')
            self.login(driver=driver)

            print(f'{datetime.now()} - Acessando fila de downloads ...')
            driver.find_element(By.XPATH, '//div/ul/li/a[@href="/DownloadQueue"]').click()

            print(f'{datetime.now()} - Buscando controle de download ...')
            rows = self.db.select_filter(table='download_control', where='status = "kit na fila"')
            if not rows:
                print(f'{datetime.now()} - Nenhum download pendente')

            for row in rows:
                print(f'{datetime.now()} - Filtrando arquivos para download ...')
                records = driver.execute_script("return document.querySelectorAll('.row')")
                _id = '[id^="downloadButton_"]'
                button = driver.execute_script(f"return document.querySelectorAll('{_id}')")

                print(f'{datetime.now()} - Localizando arquivo ...')
                count_records = len(records)
                idx_rec = 0
                idx_btn = 0
                while count_records > 0:
                    txt = records[idx_rec].text

                    file_name = txt.find(row['file_name'])
                    if file_name == -1:
                        idx_rec += 5
                        idx_btn += 1
                        continue
                    
                    created_on = txt.find(row['created_on'])
                    if created_on == -1:
                        idx_rec += 5
                        idx_btn += 1
                        continue
                    
                    print(f'{datetime.now()} - Baixando arquivo ...')
                    button[idx_btn].click()

                    filename = unidecode(row['file_name']).replace(' ', '+')
                    # filename = row['file_name'].replace('ç', 'c').replace(' ', '+')
                    print(f'{datetime.now()} - Movendo arquivo {filename} ...')
                    time.sleep(60)
                    self.moved_file(row=row, filename=filename)

                    time.sleep(10)
                    break
            
            print('Finalizado')

        except Exception as e:
            print(f'Error: {e}')
            return f'Error: {e}'

        finally:
            try:
                self.db.finish()
                driver.close()
                driver.quit()
            except Exception:
                pass

robot = DownloadQueue()
robot.run()
