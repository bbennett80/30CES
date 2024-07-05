import shutil
import os

# Define the path to the content directory
content_directory = 'content'

# Check if the content directory exists
if os.path.exists(content_directory):
    # Iterate through all the subdirectories and files in the content directory
    for item in os.listdir(content_directory):
        item_path = os.path.join(content_directory, item)
        # If it's a directory, delete it and its contents
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        # If it's a file, delete the file
        else:
            os.remove(item_path)
else:
    print(f"The directory {content_directory} does not exist.")
