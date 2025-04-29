import os
import sys
import argparse

def get_directory_structure(path, prefix="", is_last=False, ignore_hidden=True):
    """
    Generate a visual directory structure tree starting from the given path.
    
    Args:
        path (str): Path to the directory to visualize
        prefix (str): Prefix for the current line (used for recursion)
        is_last (bool): Whether this is the last item in its parent directory
        ignore_hidden (bool): Whether to ignore hidden files/folders (starting with .)
        
    Returns:
        str: Formatted string representation of the directory structure
    """
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."
    
    # Get the base directory name for the root level
    base_name = os.path.basename(path.rstrip(os.sep))
    
    # Start with the root directory name
    if prefix == "":
        result = f"{base_name}/\n"
        new_prefix = "│\n"
    else:
        # For recursive calls, use the provided prefix
        connector = "└── " if is_last else "├── "
        result = f"{prefix}{connector}{base_name}/\n"
        new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
        
    # Get all items in the directory
    try:
        items = os.listdir(path)
        # Sort items: directories first, then files
        dirs = []
        files = []
        
        for item in items:
            if ignore_hidden and item.startswith('.'):
                continue
                
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                files.append(item)
                
        dirs.sort()
        files.sort()
        all_items = dirs + files
        
        # Process each item
        for i, item in enumerate(all_items):
            full_path = os.path.join(path, item)
            is_current_last = (i == len(all_items) - 1)
            
            if os.path.isdir(full_path):
                # Recursively process directories
                result += get_directory_structure(
                    full_path, 
                    new_prefix, 
                    is_current_last,
                    ignore_hidden
                )
            else:
                # Add files
                connector = "└── " if is_current_last else "├── "
                result += f"{new_prefix}{connector}{item}\n"
                
        return result
        
    except PermissionError:
        return f"{new_prefix}├── [Permission Denied]\n"
    except Exception as e:
        return f"{new_prefix}├── [Error: {str(e)}]\n"

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Generate a directory structure tree')
    parser.add_argument('path', nargs='?', default=os.getcwd(),
                      help='Path to the directory (defaults to current directory)')
    parser.add_argument('--show-hidden', action='store_true',
                      help='Show hidden files and directories')
    
    args = parser.parse_args()
    
    # Generate and print directory structure
    structure = get_directory_structure(
        args.path, 
        prefix="", 
        is_last=False, 
        ignore_hidden=not args.show_hidden
    )
    
    print(structure)

if __name__ == "__main__":
    main()