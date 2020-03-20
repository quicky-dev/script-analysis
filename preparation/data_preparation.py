import os


class ScriptData():
    '''
    Script Data class for storing data of one given script
    '''

    def __init__(self, packages=[]):
        '''
        initialize a ScriptData object with a set of packages
        '''
        self.packages = set()
        self.add_packages(packages)

    def size(self):
        return len(self.packages)

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

    def __init__(self, folder_path, ignore_path=None):
        self.folder_path = folder_path
        # array to store all script data objects
        self.data = []

        # create a set to store packages that might accidentally be added by
        # the interpreter
        self.ignore = set(['caskroom/cask'])
        # add the ignore values from this text file if
        if ignore_path is not None:
            self.get_ignored_package_names(ignore_path)

    def get_macos_files(self, path='scripts/macos/'):
        '''
        retrieve all file paths from macos subdirectory and return a list of
        paths
        '''
        if path[-1] != '/':
            path += '/'
        files = os.listdir(path)
        return [path + file_name for file_name in files]

    def get_ubuntu_files(self, path='scripts/ubuntu/'):
        '''
        retrieve all file paths from ubuntu subdirectory and return a list of
        paths
        '''
        if path[-1] != '/':
            path += '/'
        files = os.listdir(path)
        return [path + file_name for file_name in files]

    def read_macos_files(self):
        '''
        calls get_macos_files to get all macos file paths then calls
        interpret_macos_file to convert each file to a ScriptData object.
        '''
        for file_path in self.get_macos_files():
            self.interpret_macos_file(file_path)

    def get_file_lines(self, path):
        f = open(path)
        lines = f.read().splitlines()
        f.close()
        return lines

    def interpret_macos_file(self, path):
        '''
        interpret a single macos file given its filepath, create a
        ScriptData object that contains the data from the file, then add the
        data to self.data.
        '''
        # create a script data object to store the scrips data
        script_data = ScriptData()
        # add the script data object to self.data
        self.data.append(script_data)

        # get all lines from the file
        lines = self.get_file_lines(path)
        for line in lines:
            # if the line is empty continue
            if len(line) == 0:
                continue
            # split the line by the first space
            split_line = line.split(' ', maxsplit=1)
            # if the first word of this line is not brew continue to th next
            if split_line[0] != 'brew':
                continue
            # split the remainder of the line by spaces. The last word will be
            # the package name
            package = split_line[1].split(' ')[-1]
            # if the package name should be ignored continue
            if package in self.ignore:
                continue
            # add the package to script_data object once it passes all filters
            script_data.add_package(package)

    def interpret_ubuntu_file(self, path):
        '''
        interpret a single ubuntu file given its filepath, create a
        ScriptData object that contains the data from the file, then add the
        data to self.data.
        '''
        pass

    def get_ignored_package_names(self, ignore_path):
        '''
        add all words from a file file to self.ignore set of package names to
        ignore or package names that are mistaken as packages by the
        interpreter
        '''
        for package_name in self.get_file_lines(ignore_path):
            self.ignore.add(package_name)


if __name__ == '__main__':
    s = ScriptInterpreter('hello')
    ubuntu_files = s.get_ubuntu_files()
    lines = s.get_file_lines(ubuntu_files[0])
    [print(line) for line in lines]
    # s.interpret_macos_file(macos_files[0])
    # print()
    # print('Retrieved packages:')
    # [print(package) for package in s.data[0].packages]
