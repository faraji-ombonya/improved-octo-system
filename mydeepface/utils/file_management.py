import os
import shutil
import re


def move_image(source_path, destination_path):
    try:
        # Ensure the destination directory exists
        destination_directory = os.path.dirname(destination_path)
        os.makedirs(destination_directory, exist_ok=True)

        # Move the image file
        shutil.move(source_path, destination_path)
        print(f"Image '{source_path}' moved to '{destination_path}' successfully.")
    except OSError as e:
        print(f"Error moving image '{source_path}': {str(e)}")



def delete_file(file_path):
    try:
        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        else:
            print(f"File '{file_path}' does not exist.")
    except OSError as e:
        print(f"Error deleting file '{file_path}': {str(e)}")



def get_user_id_from_image_path(image_path):
    # Define a regular expression pattern to match the user ID (assuming it's a UUID format)
    pattern = r'/database/([0-9a-f-]+)/'

    # Use re.search to find the match
    match = re.search(pattern, image_path)

    # Check if a match was found
    if match:
        # Extract the user ID from the match
        user_id = match.group(1)
        return user_id
    else:
        return None


