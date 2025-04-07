import os

def save_uploaded_files(uploaded_files, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    paths = []
    for file in uploaded_files:
        path = os.path.join(folder, file.name)
        with open(path, "wb") as f:
            f.write(file.read())
        paths.append(path)
    return paths
