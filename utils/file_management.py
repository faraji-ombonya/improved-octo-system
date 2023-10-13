import os
import shutil


def create_user_database_folder(name):
    # Define the base directory where you want to create the folder
    base_directory = "user/database"

    # Combine the base directory and the name to create the full path
    folder_path = os.path.join(base_directory, name)

    try:
        # Create the folder if it doesn't exist
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except OSError as e:
        print(f"Error creating folder '{folder_path}': {str(e)}")


def move_image_to_user_database(name, image_filename):
    # Define the source directory (uploads directory)
    source_directory = "uploads"

    # Define the destination directory (user-specific directory within user/database)
    destination_directory = os.path.join("user/database", name)

    try:
        # Create the user-specific directory if it doesn't exist
        os.makedirs(destination_directory, exist_ok=True)

        # Build the source and destination file paths
        source_path = os.path.join(source_directory, image_filename)
        destination_path = os.path.join(destination_directory, image_filename)

        # Move the image file
        shutil.move(source_path, destination_path)
        print(f"Image '{image_filename}' moved to '{destination_path}' successfully.")
    except OSError as e:
        print(f"Error moving image '{image_filename}': {str(e)}")



def delete_pickle_file():
    file_path = "user/database/representations_vgg_face.pkl"

    try:
        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        else:
            print(f"File '{file_path}' does not exist.")
    except OSError as e:
        print(f"Error deleting file '{file_path}': {str(e)}")




