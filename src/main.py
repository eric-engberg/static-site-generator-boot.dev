import os, shutil, sys
from gencontent import generate_pages_recursively

def main():
    if len(sys.argv) != 2:
        basepath = "/"
    basepath = sys.argv[1]
    if not basepath.endswith("/"):
        basepath += "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    setup_docs_directory()
    generate_pages_recursively("content", "template.html", "docs", basepath)

def setup_docs_directory():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
        os.mkdir("docs")

    copy_dir("static", "docs")

def copy_dir(src_dir, dest_dir):
    for file in os.listdir(src_dir):
        full_src_path = os.path.join(src_dir, file)
        full_dest_path = os.path.join(dest_dir, file)
        if os.path.isfile(full_src_path):
            print(f"Copying {full_src_path} to {full_dest_path}")
            shutil.copy(full_src_path, full_dest_path)
        else:
            os.mkdir(full_dest_path)
            copy_dir(full_src_path, full_dest_path)

if __name__ == "__main__":
    main()
