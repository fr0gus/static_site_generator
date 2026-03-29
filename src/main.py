import os
import shutil
from copy_static import copy_recursive
from markdown_blocks import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
