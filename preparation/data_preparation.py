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
        self.os_type = None

    def size(self):
        '''
        returns an int indicating the number of packages this script contains
        '''
        return len(self.packages)

    def set_os_type(self, os_type):
        '''
        set the os type of this scripts data
        '''
        self.os_type = os_type

    def contains(self, package):
        '''
        given a package (string), return a boolean indicating whether
        it exists in self.packages
        '''
        return package in self.packages

    def add_package(self, package):
        '''
        add a single package name (string) to self.packages
        '''
        self.packages.add(package)

    def add_packages(self, packages):
        '''
        add multiple packages (list of strings) to self.packages
        '''
        for package in packages:
            self.add_package(package)


class ScriptInterpreter():
    '''
    Interpreter class for interpreting scripts from a script folder
    Currently customized for macos and ubuntu subdirectories.

    It only requires a path to the script.
    Keep in mind if this is called from another directory, change the os
    directory before calling.

    It can also take an optional path to a file with keywords to ignore that
    the interpreter might mistake as packages names.
    '''

    def __init__(self, folder_path, ignore_path=None):
        '''
        initialize a ScriptInterpreter object with a folder path to its scripts
        and an optinal path to ignore file.
        '''
        # path to the scripts folder
        self.folder_path = folder_path
        # array to store all script data objects
        self.data = []
        # create a set to store unique packages
        self.unique_packages = set()

        # create a set to store packages that might accidentally be added by
        # the interpreter
        self.ignore = set(['caskroom/cask'])
        # add the ignore values from this text file if
        if ignore_path is not None:
            self.get_ignored_package_names(ignore_path)

    def _get_macos_files(self, path='scripts/macos/'):
        '''
        retrieve all file paths from macos subdirectory and return a list of
        paths
        '''
        if path[-1] != '/':
            path += '/'
        files = os.listdir(path)
        return [path + file_name for file_name in files]

    def _get_ubuntu_files(self, path='scripts/ubuntu/'):
        '''
        retrieve all file paths from ubuntu subdirectory and return a list of
        paths
        '''
        if path[-1] != '/':
            path += '/'
        files = os.listdir(path)
        return [path + file_name for file_name in files]

    def _get_file_lines(self, path):
        '''
        given a file path, return a list of all lines (strings) in the file
        '''
        f = open(path)
        lines = f.read().splitlines()
        f.close()
        return lines

    def read_macos_files(self):
        '''
        calls _get_macos_files to get all macos file paths then calls
        interpret_macos_file to convert each file to a ScriptData object
        containing the files packages.
        '''
        for file_path in self._get_macos_files():
            self.interpret_macos_file(file_path)

    def read_ubuntu_files(self):
        '''
        calls _get_ubuntu_files to get all ubuntu file paths then calls
        interpret_ubuntu_file to convert each file to a ScriptData object
        containing the files packages.
        '''
        for file_path in self._get_ubuntu_files():
            self.interpret_ubuntu_file(file_path)

    def interpret_macos_file(self, path):
        '''
        interpret a single macos file given its filepath, create a
        ScriptData object that contains the data from the file, then add the
        data to self.data.
        '''
        # create a script data object to store the scrips data
        script_data = ScriptData()
        # set the type to macos
        script_data.set_os_type('macos')
        # add the script data object to self.data
        self.data.append(script_data)

        # get all lines from the file
        lines = self._get_file_lines(path)
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

            # add the package to unique_packages set
            self.unique_packages.add(package)
            # add the package to script_data object once it passes all filters
            script_data.add_package(package)

    def interpret_ubuntu_file(self, path):
        '''
        interpret a single ubuntu file given its filepath, create a
        ScriptData object that contains the data from the file, then add the
        data to self.data.
        '''
        # create a script data object to store the scrips data
        script_data = ScriptData()
        # set the type to ubuntu
        script_data.set_os_type('ubuntu')
        # add the script data object to self.data
        self.data.append(script_data)

        # get all lines from the file
        lines = self._get_file_lines(path)
        for line in lines:
            # if the line is empty continue
            if len(line) == 0:
                continue
            if 'sudo' not in line:
                continue
            if 'install' not in line:
                continue
            # get the name of the package
            package = line.split(' ')[-1]
            # if the package name should be ignored continue
            if package in self.ignore:
                continue

            # add the package to unique_packages set
            self.unique_packages.add(package)
            # add the package to script_data object once it passes all filters
            script_data.add_package(package)

    def get_ignored_package_names(self, ignore_path):
        '''
        add all words from a file file to self.ignore set of package names to
        ignore or package names that are mistaken as packages by the
        interpreter
        '''
        for package_name in self._get_file_lines(ignore_path):
            self.ignore.add(package_name)


def test_interpret(test_type, index=0):
    '''
    test the interpreter on a file, and see the results it gives.
    this test cant be checked by a computer but can with the human eye.
    it will print out the lines of a script and then the packages it retrieves.

    testing requires a folder in the same directory as this function call. The
    folder should be called scripts with a subfolder called macos or ubuntu.
    '''
    assert test_type == 'MACOS' or test_type == 'UBUNTU'

    s = ScriptInterpreter('hello', 'ignore.txt')

    if test_type == 'MACOS':
        files = s._get_macos_files()
    if test_type == 'UBUNTU':
        files = s._get_ubuntu_files()

    # report if the index is out of range
    if index >= len(files):
        print(f'Index out of range. Max index: {len(files) - 1}')
        return

    # have the interpreter class interpret the first file
    if test_type == 'MACOS':
        s.interpret_macos_file(files[index])
    if test_type == 'UBUNTU':
        s.interpret_ubuntu_file(files[index])

    # print the file lines to the console
    lines = s._get_file_lines(files[index])
    [print(line) for line in lines]

    # print out the retrieved packages
    print()
    print('Retrieved packages:')
    [print(package) for package in s.data[0].packages]


if __name__ == '__main__':
    test_interpret('UBUNTU')
