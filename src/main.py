import os
import shutil

def copy_static(source_dir, dest_dir):
    try:
        contents = os.listdir(source_dir)
        for item in contents:
            source_path = os.path.join(source_dir, item)
            dest_path = os.path.join(dest_dir, item)
            
            if os.path.isfile(source_path):
                print(f"Copying file: {source_path}")
                shutil.copy(source_path, dest_path)
            elif os.path.isdir(source_path):
                print(f"Processing directory: {source_path}")
                os.mkdir(dest_path)
                copy_static(source_path, dest_path)
    except Exception as e:
        print(f"Error during copy: {e}")
        raise

def main():
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Get the project root directory (one level up from script_dir)
        project_root = os.path.dirname(script_dir)
        
        # Define paths relative to project root
        static_dir = os.path.join(project_root, "static")
        public_dir = os.path.join(project_root, "public")

        if os.path.exists(public_dir):
            shutil.rmtree(public_dir)
        os.mkdir(public_dir)
        copy_static(static_dir, public_dir)
        return 0
    except Exception as e:
        print(f"Error in main: {e}")
        return 1

if __name__ == "__main__":
    exit(main())