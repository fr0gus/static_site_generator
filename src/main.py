import os
import shutil
import sys
from copy_static import copy_recursive
from markdown_blocks import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main(basepath="/"):
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    if sys.argv[1]:
        basepath = sys.argv[1]

    copy_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()
