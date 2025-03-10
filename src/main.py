print ("Script Start") 
import os
import shutil
import sys
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

def generate_page(from_path, template_path, dest_path, basepath):
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
    
    # Replace template variables - THIS WAS MISSING
    final_content = template_content.replace('{{ Title }}', title)
    final_content = final_content.replace('{{ Content }}', html_content)
    
    # Now replace base paths
    final_content = final_content.replace('href="/', f'href="{basepath}')
    final_content = final_content.replace('src="/', f'src="{basepath}')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final content to the destination
    with open(dest_path, 'w') as output_file:
        output_file.write(final_content)
        print("writing to destination")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"generate_pages_recursive called with: {dir_path_content}, {template_path}, {dest_dir_path}")

    # Check if dir_path_content is a file (base case for recursion)
    if os.path.isfile(dir_path_content) and dir_path_content.endswith('.md'):
        # It's a markdown file, so generate the HTML
        generate_page(dir_path_content, template_path, dest_dir_path,basepath)
        return
    
    # Otherwise, it's a directory, so process its contents
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(entry_path) and entry.endswith('.md'):
            # Calculate the corresponding HTML output path
            relative_path = os.path.relpath(entry_path, dir_path_content)
            dest_filename = os.path.splitext(relative_path)[0] + '.html'
            dest_file_path = os.path.join(dest_dir_path, dest_filename)
            
            # Make sure the directory exists
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            
            print(f"Generating page from {entry_path} to {dest_file_path} using {template_path}.")
            
            # Generate the HTML page
            generate_page(entry_path, template_path, dest_file_path,basepath)
        
        elif os.path.isdir(entry_path):
            # Create the corresponding output directory
            new_dest_dir = os.path.join(dest_dir_path, os.path.basename(entry_path))
            os.makedirs(new_dest_dir, exist_ok=True)
            
            # Recursively process this subdirectory
            generate_pages_recursive(entry_path, template_path, new_dest_dir, basepath)
def main():
    print("Main function started")
    try:
        # Determine the basepath from CLI arguments
        basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
        print(f"Basepath: {basepath}")

        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"script_dir: {script_dir}")
        
        # Get the project root directory (one level up from script_dir)
        project_root = os.path.dirname(script_dir)
        print(f"project_root: {project_root}")
        
        # Define paths relative to project root
        static_dir = os.path.join(project_root, "static")
        public_dir = os.path.join(project_root, "docs")
        content_dir = os.path.join(project_root, "content")
        template_path = os.path.join(project_root, "template.html")
        
        print(f"static_dir: {static_dir}")
        print(f"public_dir: {public_dir}")
        print(f"content_dir: {content_dir}")
        print(f"template_path: {template_path}")

        # Clean and recreate public directory
        print("About to clean and recreate public directory")
        if os.path.exists(public_dir):
            shutil.rmtree(public_dir)
        os.mkdir(public_dir)
        
        # Copy static files
        print("About to copy static files")
        copy_static(static_dir, public_dir)
        print("Finished copying static files")
        
        # Generate pages recursively
        print("About to generate pages recursively")
        generate_pages_recursive(content_dir, template_path, public_dir, basepath)     
        print("Finished generating pages recursively")
        
        return 0
    except Exception as e:
        print(f"Error in main: {e}")
        return 1
if __name__ == "__main__":
    main()