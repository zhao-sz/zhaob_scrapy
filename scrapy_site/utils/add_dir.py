import os


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("--- new folder " + path)
    else:
        print("--- there is this folder" + path)
