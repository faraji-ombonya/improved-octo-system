from deepface import DeepFace

# verification = DeepFace.verify(img1_path = "img_db/fj.jpeg", img2_path = "img_db/enzo.jpg", model_name = "VGG-Face")

# print(verification)

# verified = verification.get("verified")
# print(f"Verification Status: {verified}")


# print(dfs)

# res = DeepFace.extract_faces(img_path="img_db/enzo.jpg") 

# res = DeepFace.represent(img_path="img_db/fj.jpeg")

# print(res)




dfs = DeepFace.find(img_path="enzo.jpg", db_path="./img_db", enforce_detection=False)



for item in dfs:
    print(item)





