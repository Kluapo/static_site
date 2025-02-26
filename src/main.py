import os
import shutil
from markdown_blocks import *

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    # Read the files
    with open(from_path, 'r') as md_file:
        markdown_content = md_file.read()
    
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Get the title from markdown
    title = extract_title(markdown_content)
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    final_content = template_content.replace("{{ Title }}", title)
    final_content = final_content.replace("{{ Content }}", html_content)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final content to the destination
    with open(dest_path, 'w') as output_file:
        output_file.write(final_content)
        print("writing to destination")

def main():
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Get the project root directory (one level up from script_dir)
        project_root = os.path.dirname(script_dir)
        
        # Define paths relative to project root
        static_dir = os.path.join(project_root, "static")
        public_dir = os.path.join(project_root, "public")
        content_path = os.path.join(project_root, "content", "index.md")
        template_path = os.path.join(project_root, "template.html")
        output_path = os.path.join(public_dir, "index.html")

        # Clean and recreate public directory
        if os.path.exists(public_dir):
            shutil.rmtree(public_dir)
        os.mkdir(public_dir)
        
        # Copy static files
        copy_static(static_dir, public_dir)
        
        # Generate the page
        generate_page(content_path, template_path, output_path)
        
        return 0
    except Exception as e:
        print(f"Error in main: {e}")
        return 1

if __name__ == "__main__":
    exit(main())