import pickle
import os, uuid, tempfile
def_files = ["default.icon.png"]
def_folders = ["assets"]
tempdir = tempfile.gettempdir()

def store_data():
    global def_files, def_folders
    files = {}
    folders = {}
    for i in def_files:
        with open(i, "rb+") as f:
            files[i] = f.read()
    for i in def_folders:
        fol = os.listdir(i)
        folders[i] = {}
        for j in fol:
            path = i+"/"+j
            with open(path, "rb+") as f:
                folders[i][path] = f.read()
    db = {}
    db["gameid"] = uuid.uuid1()
    db['files'] = files
    db['folders'] = folders
    
    # Its important to use binary mode
    dbfile = open('assets.pkg', 'wb+')
    
    # source, destination
    pickle.dump(db, dbfile)                    
    dbfile.close()

def load_data():
    # for reading also binary mode is important
    dbfile = open('assets.pkg', 'rb')    
    db = pickle.load(dbfile)
    if not os.path.isdir(os.path.join(tempdir, str(db["gameid"]))):
        try: os.makedirs(os.path.join(tempdir, str(db["gameid"])))
        except FileExistsError: pass
        for i in db["files"].keys():
            with open(os.path.join(tempdir, os.path.join(str(db["gameid"]), i)), "wb+") as f:
                f.write(db["files"][i])
        for i in db["folders"].keys():
            print(os.path.join(tempdir, os.path.join(str(db["gameid"]), i)))
            try: os.makedirs(os.path.join(tempdir, os.path.join(str(db["gameid"]), i)))
            except FileExistsError: pass
            for j in db["folders"][i].keys():
                with open(os.path.join(tempdir, os.path.join(str(db["gameid"]), j)), "wb+") as f:
                    f.write(db["folders"][i][j])
    else:
        print("already exists")
    os.chdir(os.path.join(tempdir, str(db["gameid"])))
    print(os.getcwd())
    dbfile.close()


if __name__ == '__main__':
    store_data()
    load_data()
