import os, shutil

def main():
    setup_public_directory()

def setup_public_directory():
    if os.path.exists("public"):
        shutil.rmtree("public")
        os.mkdir("public")

    copy_dir("static", "public")

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
