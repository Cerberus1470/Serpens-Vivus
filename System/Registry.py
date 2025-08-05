"""
Module Registry. Houses the Registry class and static methods.
"""
import os
from System import Loading


class Registry:
    """
    Class to test out the registry. Currently, storing system settings.
    """

    class Directory:
        """
        Class to create a Registry directory. Houses name.
        """

        def __init__(self, name: str = "default"):
            self.name = name

        def __repr__(self):
            return "Directory with name {name}".format(name=self.name)

        def __iter__(self):
            return [self.__getattribute__(i) for i in list(self.__dict__.keys())
                    if (isinstance(self.__getattribute__(i), Registry.Key)) or (isinstance(self.__getattribute__(i), Registry.Directory))]

    class Key:
        """
        Class to create a Registry key. Houses name and value.
        """

        def __init__(self, name: str = "default", value: str = "default"):
            self.name = name
            self.value = value

        def __repr__(self):
            return "Key with name {name} and value {value}".format(name=self.name, value=self.value)

    def __init__(self, path: str = "\\", elevate=None):
        """
        This method is to iteratively read through the registry and create a directory-key structure that is intuitive and easy to manipulate in memory.
        """
        self.elevate = elevate
        self.base_path = path+'\\'
        for subdir, dirs, files in os.walk(path):  # Iterating through the Registry folder.
            for file in files:
                if file[len(file) - 5:] == "svkey":  # Making sure the files are svkeys.
                    file = "{subdir}\\{file}".format(subdir=subdir, file=file)  # Specifying the file path + name.
                    value = list(open(file, "r"))[0]  # Acquiring the value of the key.
                    self.add_key(file.replace(path+"\\", "").replace(".svkey", ""), value)  # Using the add_key method to add the key!

    def __repr__(self):
        return "Registry with {vars} directories/keys.".format(vars=len(self.__iter__()))

    def __iter__(self):
        return [self.__getattribute__(i) for i in list(self.__dict__.keys())
                if (isinstance(self.__getattribute__(i), Registry.Key)) or (isinstance(self.__getattribute__(i), Registry.Directory))]

    def add_key(self, key: str = "", value=0):
        """
        This is a method to add keys to the volatile registry stored in local memory.
        DANGER: There is no security for this method. Using this, anyone can add keys anywhere in the local registry.
        :param key: The key to add. Must be in the format {dir}\\{subdir}\\{key} to work.
        :param value: The value to set the new key to.
        :return: 0 if successful, 1 if the key exists, 2 if the value is not formatted correctly.
        """
        if self.find_key(self, key) != (None, None):  # Try to find if the key exists.
            Loading.returning("That key already exists.", 2)
            return 1
        else:  # If it doesn't exist...
            try:
                # First, iteratively create directories that aren't present.
                target = self
                path = key.split("\\")
                for i in range(len(path) - 1):
                    try:
                        if isinstance(target.__getattribute__(path[i]), Registry.Directory):
                            target = target.__getattribute__(path[i])
                        else:  # If there exists a key with the name of the path element already...
                            Loading.returning("There is already a key under that path.", 2)
                            return 1
                    except AttributeError:
                        target.__setattr__(path[i], Registry.Directory(path[i]))
                        target = target.__getattribute__(path[i])
                # Once necessary directories are made/found, create the key.
                key_name = path[-1]
                target.__setattr__(key_name, Registry.Key(key_name, value))
                return 0
            except AttributeError:
                Loading.returning("The key is not formatted correctly.", 2)
                return 2

    def get_key(self, key: str = ""):
        """
        This is a method to get values for keys in the volatile registry. This does not read from keys stored on the disk.
        :param key: The key whose value to get. Must be in the format {dir}\\{subdir}\\{key} to work.
        :return: The value of the key specified, 1 if the key was not found.
        """
        try:
            (key, _) = Registry.find_key(self, key)
            if key:
                return key.value
            else:
                raise AttributeError
        except AttributeError:
            Loading.returning("The specified key was not found.", 2)
            return 1

    def set_key(self, key: str = "", value: str = ""):
        """
        This is a method to set values for keys in the volatile registry. This does not set values to keys stored on the disk.
        :param key: The key whose value to get. Must be in the format {dir}\\{subdir}\\{key} to work.
        :param value: The value to set.
        :return: 0 if successful, 1 if the specified key is not a key, 2 if the key was not found.
        """
        try:
            (key, _) = Registry.find_key(self, key)
            if isinstance(key, Registry.Key):
                key.__setattr__("value", value)
                return 0
            else:
                Loading.returning("The specified key is not a key.", 2)
                return 1
        except AttributeError:
            Loading.returning("The specified key was not found.", 2)
            return 2

    def delete_key(self, key: str = ""):
        """
        This is a method to delete keys stored in the volatile registry. This does not delete keys stored on the disk.
        :param key: The key to delete. Must be in the format {dir}\\{subdir}\\{key} to work.
        :return: 0 if successful, 1 if the key was not found.
        """
        try:
            key, path = Registry.find_key(self, key)
            if key and path:
                target = self
                path = path[:-1]
                for i in path:
                    target = target.__getattribute__(i)
                target.__delattr__(key.name)
                return 0
            else:
                Loading.returning("The specified key was not found.", 2)
                return 1
        except AttributeError:
            Loading.returning("The specified key was not found.", 2)
            return 2

    def add_svkey(self, key: str = "", value=0):
        """
        This is a method to add to the global registry keys stored on the local disk. Also changes the local registry.
        DANGER: There is no security for this method. Using this, anyone can add to the registry and break the OS.
        :param key: The svkey file to add. Must be in the format {dir}\\{subdir}\\{key} to work.
        :param value: The value for the key.
        :return: 0 if successful, 1 if the key exists, 2 if the value is not formatted correctly, 3 if the key is not formatted corretly.
        """
        if (not key.rpartition("\\")[2]) or not (all(i in Loading.ALPHABET for i in key.rpartition("\\")[2])):
            Loading.returning("Please enter a key name with no escape characters.", 2)
            return 3
        try:
            key = key.replace(".svkey", "")
            val = self.add_key(key, value)
            if val in (1, 2):
                return val
            os.makedirs("System\\REGISTRY\\{path}".format(path=key.rpartition("\\")[0]), exist_ok=True)
            with open("System\\REGISTRY\\{path}.svkey".format(path=key), 'w') as file:
                file.write(str(value))
            return 0
        except (FileNotFoundError, FileExistsError, OSError, TypeError):
            Loading.returning("The registry failed to add the specified key. Please reboot and try again.", 3)

    def get_svkey(self, key: str = ""):
        """
        This is a method to get values from the global registry keys stored on the local disk.
        DANGER: There is no security for this method. Using this, anyone can add to the registry and break the OS.
        :param key: The svkey file to add. Must be in the format {dir}\\{subdir}\\{key} to work.
        :return: 0 if successful, 1 if unsuccessful.
        """
        (_, path) = Registry.find_key(self, key.replace(".svkey", ""))
        try:
            key = list(open("System\\REGISTRY\\{path}.svkey".format(path='\\'.join(path)), 'r'))
            if key:
                return key[0]
            else:
                raise FileNotFoundError
        except (FileNotFoundError, FileExistsError, OSError, TypeError):
            Loading.returning("The registry failed to find the key specified. Please reboot and try again.", 2)
            return 1

    def set_svkey(self, key: str = "", value=0):
        """
        This is a method to modify the global registry keys stored on the local disk. Also changes the local registry.
        :param key: The svkey file to modify. Must be in the format {dir}\\{subdir}\\{key} to work.
        :param value: The new value for the key.
        :return: 0 if successful, 1 if unsuccessful.
        """
        if not self.elevate():
            return 1
        try:
            key = key.replace(".svkey", "")
            self.set_key(key, value)
            (target, path) = self.find_key(self, key)
            with open("System\\REGISTRY\\{path}.svkey".format(path="\\".join(path)), 'w') as file:
                file.write(str(value))
            return 0
        except (FileNotFoundError, FileExistsError, OSError, TypeError):
            Loading.returning("The registry failed to write to the key specified. Please reboot and try again.", 3)
            return 1

    def delete_svkey(self, key: str = ""):
        """
        This is a method to delete keys from the global registry keys stored on the local disk. Also changes the local registry.
        :param key: The svkey file to modify. Must be in the format {dir}\\{subdir}\\{key} to work.
        :return: 0 if successful, 1 if unsuccessful.
        """
        if not self.elevate():
            return 1
        try:
            key = key.replace(".svkey", "")
            (_, path) = Registry.find_key(self, key)
            self.delete_key(key)
            os.remove("System\\REGISTRY\\{path}.svkey".format(path="\\".join(path)))
            return 0
        except (FileNotFoundError, FileExistsError, OSError, TypeError):
            Loading.returning("The registry failed to delete the key specified. Please reboot and try again.", 3)
            return 1

    @staticmethod
    def find_key(self, key: str = "", path: list = None):
        """
        This is a helper method to locate keys requested by other methods using only their name.
        :param self: The target object. Can be a Registry or Directory Object.
        :param key: The name of the requested key.
        :param path: Path variable to append to.
        :return: The requested key, None if it isn't found.
        :raises: AttributeError if the key attribute is not found.
        """
        if path is None:
            path = []
        if key.rpartition("\\")[0]:  # User has provided path!
            try:
                target = self
                for i in key.split("\\"):
                    target = target.__getattribute__(i)
                if isinstance(target, Registry.Key):
                    return target, key.split("\\")
                else:
                    return None, None
            except AttributeError:
                return None, None  # Path could not be found.
        for i in self.__iter__():
            if isinstance(i, Registry.Directory):
                (potential_key, path) = Registry.find_key(i, key)
                path = [] if path is None else path  # Making sure path stays a list.
                if potential_key:
                    path.insert(0, i.name)
                    return potential_key, path
            elif isinstance(i, Registry.Key):
                if i.name == key:
                    path.insert(0, i.name)
                    return i, path
        return None, None

    def find_keys(self, keys: list = None):
        """
        This is a helper method to find multiple keys at once, provided a list with proper Key Names.
        :param keys: The list of key names
        :return: The list of keys.
        """
        if keys is None:
            keys = []
        found_keys = []
        for i in keys:
            try:
                found_keys.append(Registry.find_key(self, i))
            except AttributeError:
                found_keys.append(None)
        return found_keys

    def verify_build(self, required_keys: list = None):
        """
        This is a modular method to check that the registry has the required keys. If not, adds the required keys to the global and local Registry.
        :param required_keys: The list of required keys. Must be a list of path-like objects.
        :return: True if all keys are found. False if writing to a key failed.
        """
        if required_keys is None:
            required_keys = []
        for i in required_keys:
            if Registry.find_key(self, i) == (None, None):  # Does the key exist?
                Loading.returning("Registry verification failed.", 2)
                return False
        return True
