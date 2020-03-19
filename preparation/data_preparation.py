import os


class ScriptData():
    '''
    Script Data class for storing data of one given script
    '''

    def __init__(self, packages):
        self.packages = set()
        self.add_packages(packages)

    def add_package(self, package):
        self.packages.add(package)

    def add_packages(self, packages):
        for package in packages:
            self.add_package(package)


class ScriptInterpreter():
    '''
    Interpreter class for interpreting scripts from a script folder
    Currently customized for macos and ubuntu subdirectories.

    It only requires a path to the script.
    Keep in mind if this is called from another directory, change the os
    directory before calling.
    '''

    def __init__(self, folder_path):
        self.folder_path = folder_path
        # array to store all script data objects
        self.data = []

    def get_macos_files(self, path='scripts/macos'):
        '''
        retrieve all file paths from macos subdirectory and return a list of
        paths
        '''
        files = os.listdir(path)
        return [path + file_name for file_name in files]

    def get_ubuntu_files(self, path='script/ubuntu'):
        '''
        retrieve all file paths from ubuntu subdirectory and return a list of
        paths
        '''
        files = os.listdir(path)
        return [path + file_name for file_name in files]

    def read_macos_files(self):
        '''
        calls get_macos_files to get all macos file paths then calls
        interpret_macos_file to convert each file to a ScriptData object.
        '''
        for file_path in self.get_macos_files():
            self.interpret_macos_file(file_path)

    def interpret_macos_file(self, path):
        '''
        interpret a single macos file given its filepath, create a
        ScriptData object that contains the data from the file, then add the
        data to self.data.
        '''
        pass

    def interpret_ubuntu_file(self, path):
        '''
        interpret a single ubuntu file given its filepath, create a
        ScriptData object that contains the data from the file, then add the
        data to self.data.
        '''
        pass
