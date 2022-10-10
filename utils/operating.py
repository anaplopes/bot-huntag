# -*- coding: utf-8 -*-
import os
import shutil
import zipfile


class OperatingSystem:
    
    def exists(self, path:str) -> bool:
        if os.path.exists(path=path):
            return True
        return False


    def create_dirs(self, dirname:str) -> None:
        _dir = self.exists(path=dirname)
        if not _dir:
            os.makedirs(name=dirname)


    def create_dir(self, dirname:str) -> None:
        _dir = self.exists(path=dirname)
        if not _dir:
            os.mkdir(path=dirname)

    
    def clear_dir(self, dirname:str) -> None:
        # topdown=False não permite excluir um diretório antes que ele esteja vazio
        for root, dirs, files in os.walk(dirname, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))


    def zip_file(self, zipname:str, dirname:str) -> None:
        _zip = zipfile.ZipFile(zipname, 'w', compression=zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(dirname):
            for file in files:
                _zip.write(f'{dirname}/{file}', file)
        _zip.close()

    
    def unzip_file(self, dirname:str, zipname:str) -> bool:
        _zipfile = self.exists(path=zipname)
        if _zipfile:
            _zip = zipfile.ZipFile(zipname)
            _zip.extractall(dirname)
            _zip.close()
            return True
        return False


    def move_file(self, source:str, destiny:str) -> bool:       
        _source = self.exists(path=source)
        if _source:
            os.rename(src=source, dst=destiny)
            return True
        return False


    def copy_file(self, source:str, destiny:str) -> bool:
        _source = self.exists(path=source)
        if _source:
            shutil.copy(src=source, dst=destiny)
            return True
        return False
    

    def delete_file(self, filename:str) -> bool:
        _file = self.exists(path=filename)
        if _file and os.path.isfile(path=filename):
            os.remove(path=filename)
            return True
        return False


    def delete_dir(self, dirname:str) -> bool:
        _dir = self.exists(path=dirname)
        if _dir and os.path.isdir(dirname):
            os.rmdir(path=dirname)
            return True
        return False


    def delete_tree(self, dirname:str) -> bool:
        _dir = self.exists(path=dirname)
        if _dir and os.path.isdir(dirname):
            shutil.rmtree(path=dirname)
            return True
        return False
