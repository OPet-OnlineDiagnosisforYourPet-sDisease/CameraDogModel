import uvicorn
from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
import shutil
from pydantic import BaseModel
import mysql

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = FastAPI()  # create a new FastAPI app instance

# port = int(os.getenv("PORT"))
port = 8080

model = tf.keras.models.load_model('SkinDisease.h5')

def predict(file):
    img = image.load_img(file, target_size=(150,150))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)


    images = np.vstack([x]) 
    classes = model.predict(images) 
    print(classes[0]) 

    result = np.argmax(classes[0])
    
    resmessage = ""
    if result == 0:
        resmessage = 'Flea Allergy'
    elif result == 1:
        resmessage = 'Hot Spot'
    elif result == 2:
        resmessage = 'Mange'
    elif result == 3:
        resmessage = 'Ringworm'

    return resmessage


# GCS Section
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json"

def uploadtogcs(file):
    from google.cloud import storage
    client = storage.Client()
    bucket = client.get_bucket('modelkamera')
    blob = bucket.blob(file)
    blob.upload_from_filename(file)
    return blob.public_url

def updatemysql(userID, petID, url):
    print(userID, petID, url)
    import mysql.connector

    mydb = mysql.connector.connect(
        host='35.222.154.226', 
        user='root', 
        password='rahman552', 
        database='imagediagnosis' 
    )

    cursor = mydb.cursor()

    query = "INSERT INTO tabelkamera (userID, petID, url) VALUES (%s, %s, %s)"
    values = (userID, petID, url)
    cursor.execute(query, values)
    mydb.commit()

    return str(userID) + " " + str(petID) + " " + str(url)

    # return the index of inserted data
    return cursor.lastrowid

@app.get("/")
def hello_world():
    return ("hello world")

@app.post("/imageclassify")
def imageclassify(input: UploadFile = File(...)):
    savefile = input.filename
    with open(savefile, "wb") as buffer:
        shutil.copyfileobj(input.file, buffer)
    result = predict(savefile)
    gcs_url = uploadtogcs(savefile)
    os.remove(savefile)
    return (result, gcs_url)

class Item(BaseModel):
    userID: int
    petID: int
    gcs_url: str


@app.post("/updatedb")
def updatedb(item: Item):
    updateddb = updatemysql(item.userID, item.petID, item.gcs_url)
    return updatedb

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=port, timeout_keep_alive=1200)
