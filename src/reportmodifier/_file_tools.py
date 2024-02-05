import os


def get_files_in_folder(top_level_dir, condition_callback=None, recursive=True):
    """ Similar to the a bit overloaded function list_files_in_folder(). The result is basically the same: A dict with
    the base file name as key and the full file path as value. But this function eliminates an unpleasant flaw of
    list_files_in_folder(), if its argument name_as_key is True: It lists truly ALL files. If a file appears in
    multiple sub-directories with the same name, list_files_in_folder() lists it only once, any other appearance is
    being ignored. This function lists those files anyway by prefixing the base file with the sub-directory name.
    Example: There are two files:
        D:\temp\1.txt
        D:\temp\subdir\1.txt
    list_files_in_folder(r'D:\temp', name_as_key=True) returns {'1.txt': 'D:\temp\subdir\1.txt'}
    get_files_in_folder(r'D:\temp') returns {'1.txt': 'D:\temp\1.txt', 'subdir\1.txt': 'D:\temp\subdir\1.txt'}
    Another feature of this function is to define a condition which is a callback function to check the file for
    validity. This callback function must take one parameter 'path' and must return True or False.
    """
    result = dict()
    for root, dirs, files in os.walk(top_level_dir):
        for f in files:
            path = os.path.join(root, f)
            if condition_callback is None or condition_callback(path):
                result[os.path.relpath(path, top_level_dir)] = os.path.normpath(path)
        if not recursive:
            return result
    return result
