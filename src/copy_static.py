import os
import shutil


def copy_recursive(src, dst):
    if not os.path.exists(src):
        raise Exception(f"Invalid source path: {src}")

    if not os.path.exists(dst):
        os.mkdir(dst)

    contents = os.listdir(src)

    for item in contents:
        itempath = os.path.join(src, item)
        if os.path.isfile(itempath):
            print(f"copying {itempath}")
            shutil.copy(itempath, dst)
        elif os.path.isdir(itempath):
            dstpath = os.path.join(dst, item)
            if not os.path.exists(dstpath):
                os.mkdir(dstpath)

            copy_recursive(itempath, dstpath)
        else:
            raise Exception("Invalid object")
