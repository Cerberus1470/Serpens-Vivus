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
                    if (self.__getattribute__(i).__class__ == Registry.Key) or (self.__getattribute__(i).__class__ == Registry.Directory)]

    class Key:
        """
        Class to create a Registry key. Houses name and value.
        """

        def __init__(self, name: str = "default", value: str = "default"):
            self.name = name
            self.value = value

        def __repr__(self):
            return "Key with name {name} and value {value}".format(name=self.name, value=self.value)

    def __init__(self, path: str = "\\"):
        """
        This method is to iteratively read through the registry and create a directory-key structure that is intuitive and easy to manipulate in memory.
        """
        for subdir, dirs, files in os.walk(path):  # Iterating through the Registry folder.
            for file in files:
                if file[len(file) - 5:] == "svkey":  # Making sure the files are svkeys.
                    file = "{subdir}\\{file}".format(subdir=subdir, file=file)  # Specifying the file path + name.
                    value = list(open(file, "r"))[0]  # Acquiring the value of the key.
                    self.add_key(file[16:len(file) - 6], value)  # Using the add_key method to add the key!

    def __repr__(self):
        return "Registry with {vars} directories/keys.".format(vars=len(self.__iter__()))

    def __iter__(self):
        return [self.__getattribute__(i) for i in list(self.__dict__.keys())
                if (self.__getattribute__(i).__class__ == Registry.Key) or (self.__getattribute__(i).__class__ == Registry.Directory)]

    def add_key(self, key: str = "", value=0):
        """
        This is a method to add keys to the volatile registry stored in local memory.
        DANGER: There is no security for this method. Using this, anyone can add keys anywhere in the local registry.
        :param key: The key to add. Must be in the format {dir}\\{subdir}\\{key} to work.
        :param value: The value to set the new key to.
        :return: 0 if successful, 1 if the key exists, 2 if the key is not formatted correctly.
        """
        try:
            self.__getattribute__(key)  # Try to find if the key exists.
            Loading.returning("That key already exists.", 2)
            return 1
        except AttributeError:  # If it doesn't exist...
            try:
                # First, iteratively create directories that aren't present.
                target = self
                path = key.split("\\")
                for i in range(len(path) - 1):
                    try:
                        if target.__getattribute__(path[i]).__class__ == Registry.Directory:
                            target = target.__getattribute__(path[i])
                        else:
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
            (key, _) = Registry.find_key(self, key.rpartition("\\")[2])
            if key.__class__ == Registry.Key:
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
            key, path = Registry.find_key(self, key.rpartition("\\")[2])
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
        :return: 0 if successful, 1 if unsuccessful.
        """
        try:
            key = key.replace(".svkey", "")
            self.add_key(key, value)
            os.makedirs("System\\REGISTRY\\{path}".format(path=key.rpartition("\\")[0]), exist_ok=True)
            file = open("System\\REGISTRY\\{path}.svkey".format(path=key), 'w')
            file.write(str(value))
            file.close()
            return 0
        except (FileNotFoundError, FileExistsError, OSError):
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
        except (FileNotFoundError, FileExistsError, OSError):
            Loading.returning("The registry failed to find the key specified. Please reboot and try again.", 2)
            return 1

    def set_svkey(self, key: str = "", value=0):
        """
        This is a method to modify the global registry keys stored on the local disk. Also changes the local registry.
        DANGER: There is no security for this method. Using this, anyone can modify the registry and break the OS.
        :param key: The svkey file to modify. Must be in the format {dir}\\{subdir}\\{key} to work.
        :param value: The new value for the key.
        :return: 0 if successful, 1 if unsuccessful.
        """
        try:
            key = key.replace(".svkey", "")
            self.set_key(key, value)
            (target, path) = self.find_key(self, key)
            file = open("System\\REGISTRY\\{path}.svkey".format(path="\\".join(path)), 'w')
            file.write(str(value))
            file.close()
            return 0
        except (FileNotFoundError, FileExistsError, OSError):
            Loading.returning("The registry failed to write to the key specified. Please reboot and try again.", 3)
            return 1

    def delete_svkey(self, key: str = ""):
        """
        This is a method to delete keys from the global registry keys stored on the local disk. Also changes the local registry.
        DANGER: There is no security for this method. Using this, anyone can modify the registry and break the OS.
        :param key: The svkey file to modify. Must be in the format {dir}\\{subdir}\\{key} to work.
        :return: 0 if successful, 1 if unsuccessful.
        """
        try:
            key = key.replace(".svkey", "")
            (key, path) = Registry.find_key(self, key)
            self.delete_key(key)
            os.remove("System\\REGISTRY\\{path}.svkey".format(path="\\".join(path)))
            return 0
        except (FileNotFoundError, FileExistsError, OSError):
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
            target = self
            for i in key.split("\\"):
                target = target.__getattribute__(i)
            if target.__class__ == Registry.Key:
                return target, key.split("\\")
            else:
                return None, None
        for i in self.__iter__():
            if i.__class__ == Registry.Directory:
                (potential_key, path) = Registry.find_key(i, key)
                if potential_key:
                    path.insert(0, i.name)
                    return potential_key, path
            elif i.__class__ == Registry.Key:
                if i.name == key:
                    path.insert(0, i.name)
                    return i, path
        return None, None

    def find_keys(self, keys : list = None):
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
            try:
                Registry.find_key(self, i)  # Does the key exist?
            except AttributeError:
                match i.rpartition("\\")[2]:  # Default values for keys.
                    case 'Resolution':
                        value = "10x40"
                    case 'Recovery':
                        value = "recovery"
                    case 'Speed':
                        value = "1.0"
                    case 'Start':
                        value = "alphabetical"
                    case _:
                        value = "None"
                self.add_svkey(i, value)
        return True
