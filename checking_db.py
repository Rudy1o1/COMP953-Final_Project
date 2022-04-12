import sqlite3

def main():

    db_path = "C:\Temp\Final_Project\apod_images.db"
    image_sha256 = "a186ef73f20c1ef210e09c2676e644abe0fbe7624ed136fe3f54c04fc7535160"
    image_already_in_db(db_path, image_sha256)

def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 

    myConnection = sqlite3.connect("C:\\Temp\\Final_Project\\apod_images.db")
    myCursor = myConnection.cursor()

    hash = image_sha256

    selectStatement = ("""SELECT location_path FROM images
                    WHERE hash_value = \'""") + hash + "\'" 

    myCursor.execute(selectStatement)
    results = myCursor.fetchall()

    myConnection.close

    if (len(results)==0):
        a = False

    else:
        a= True
    

    return a

main()