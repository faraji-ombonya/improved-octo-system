import os

class DeepFaceImage():
    
    def __init__(self, image_path: str, image_name: str) -> None:
        self.image_path = image_path
        self.image_name = image_name
        
    def rename(self, new_name: str) -> None:
        # Get the directory path and the current file extension
        dir_path, old_name = os.path.split(self.image_path)
        base_name, file_extension = os.path.splitext(old_name)
        
        # Create the new file name by combining the new name and the existing extension
        new_file_name = f"{new_name}{file_extension}"
        
        # Create the new full path for the renamed image
        new_image_path = os.path.join(dir_path, new_file_name)
        
        try:
            # Check if the source file exists before renaming
            if os.path.exists(self.image_path):
                # Check if the destination file already exists
                if os.path.exists(new_image_path):
                    print(f"Destination file '{new_image_path}' already exists. Rename operation aborted.")
                else:
                    # Rename the image file
                    os.rename(self.image_path, new_image_path)
                    self.image_path = new_image_path
                    self.image_name = new_file_name
            else:
                print(f"Source file '{self.image_path}' does not exist. Rename operation aborted.")
        except OSError as e:
            print(f"Failed to rename the image: {str(e)}")

    def append_user_id(self, user_id: str) -> None:
        # Get the directory path and the current file extension
        dir_path, old_name = os.path.split(self.image_path)
        base_name, file_extension = os.path.splitext(old_name)
        
        # Create a new file name by appending the user ID to the existing name
        new_file_name = f"{base_name}_{user_id}{file_extension}"
        
        # Create the new full path for the renamed image
        new_image_path = os.path.join(dir_path, new_file_name)
        
        try:
            # Check if the source file exists before renaming
            if os.path.exists(self.image_path):
                # Check if the destination file already exists
                if os.path.exists(new_image_path):
                    print(f"Destination file '{new_image_path}' already exists. Rename operation aborted.")
                else:
                    # Rename the image file
                    os.rename(self.image_path, new_image_path)
                    self.image_path = new_image_path
                    self.image_name = new_file_name
            else:
                print(f"Source file '{self.image_path}' does not exist. Rename operation aborted.")
        except OSError as e:
            print(f"Failed to rename the image: {str(e)}")

    def append_user_id_to_image_name(self):
        # Extract the user ID from the image name (assuming it's in the format "image_name_user_id.ext")
        base_name, file_extension = os.path.splitext(self.image_name)
        parts = base_name.split('_')
        if len(parts) == 2:
            user_id = parts[1]
            self.append_user_id(user_id)
        else:
            print("Image name doesn't contain a valid user ID.")

img = DeepFaceImage("/home/faraji/Developer/Personal/improved-octo-system/", "les.jpg")
print(f"{img.image_path}{img.image_name}")



