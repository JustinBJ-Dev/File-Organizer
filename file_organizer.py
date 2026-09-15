import os
import shutil
from pathlib import Path

# Define the mapping of extensions to folder names
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xlsx", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".bat", ".sh"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".json", ".xml"],
}

def organize_folder(target_dir):
    """
    Organizes files in the given directory into category-based folders.
    """
    path = Path(target_dir)
    
    if not path.exists() or not path.is_dir():
        print(f"Error: The path '{target_dir}' is not a valid directory.")
        return

    print(f"Organizing: {path.absolute()}")
    
    files_moved = 0
    
    # Iterate through all items in the directory
    for item in path.iterdir():
        # Skip directories, we only want to move files
        if item.is_dir():
            continue
            
        # Get the file extension in lowercase
        extension = item.suffix.lower()
        
        # Determine the category
        category = "Others"
        for cat, extensions in FILE_CATEGORIES.items():
            if extension in extensions:
                category = cat
                break
        
        # Create the category folder if it doesn't exist
        category_path = path / category
        category_path.mkdir(exist_ok=True)
        
        # Define the destination path
        destination = category_path / item.name
        
        # Handle name collisions (if file already exists in destination)
        if destination.exists():
            stem = item.stem
            suffix = item.suffix
            counter = 1
            while destination.exists():
                destination = category_path / f"{stem}_{counter}{suffix}"
                counter += 1
        
        try:
            shutil.move(str(item), str(destination))
            files_moved += 1
            print(f"Moved: {item.name} -> {category}/")
        except Exception as e:
            print(f"Could not move {item.name}: {e}")

    print(f"\nFinished! Moved {files_moved} files.")

if __name__ == "__main__":
    print("--- Python File Organizer ---")
    user_path = input("Enter the full path of the folder to organize (or press Enter for current directory): ").strip()
    
    if not user_path:
        user_path = "."
        
    organize_folder(user_path)
