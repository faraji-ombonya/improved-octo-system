from deepface import DeepFace
from pprint import pprint
import utils.file_management as fm

import multiprocessing

# define background processes
background_delete_pickle_file = multiprocessing.Process(target=fm.delete_pickle_file)



# verification = DeepFace.verify(img1_path = "img_db/enzo_b.jpg", img2_path = "img_db/enzo_b.jpg", model_name = "VGG-Face")

# print(verification)

# verified = verification.get("verified")
# print(f"Verification Status: {verified}")


# print(dfs)

# res = DeepFace.extract_faces(img_path="img_db/enzo.jpg") 

# res = DeepFace.represent(img_path="img_db/fj.jpeg")

# print(res)


# background_delete_picker_file.start()


dfs = DeepFace.find(
    img_path="uploads/rjb.jpg", 
    db_path="user/database/", 
    enforce_detection=False,

    # model_name="VGG-Face",
    # distance_metric="cosine",
     
    model_name="Facenet512",
    distance_metric="euclidean"
    )

for df in dfs:
    data = df.to_dict()

    pprint(data)

    print(data['identity'][0][14:18])
   

# def create_pickle_file():
#     DeepFace.find(img_path="", db_path="user/database/", enforce_detection=False)

# background_create_pickle_file = multiprocessing.Process(target=create_pickle_file)

# background_create_pickle_file.start()
# Example usage:
# name = "0004"
# fm.create_user_database_folder(name)


# name = "0007"
# image_filename = "rja.jpg"
# fm.move_image_to_user_database(name, image_filename)
# background_delete_pickle_file.start()

# Example usage:


