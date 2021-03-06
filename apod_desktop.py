""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date        Author    Description
  2022-03-11  J.Dalby   Initial creation
  2022-03-24  Rudra Patel Script working
  2022-04-12  Rudra Patel Script completion 
"""
from sys import argv, exit
from datetime import datetime, date,time
from hashlib import sha256
import hashlib
from os import path
import os
import sqlite3
import requests
import ctypes

def main():

    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_info_dict = get_apod_info(apod_date)
    
    # Download today's APOD
    #image_url from apod_dict
    image_url = apod_info_dict['url']         

    #image_msg which get from the downloading the image
    image_msg = download_apod_image(image_url) 

    #image path
    image_path = get_image_path(image_url, image_dir_path)

    #image size
    image_size = len(image_msg)

    #image Download date
    image_download_date = datetime.now()

    #Counting The hash of the image
    image_sha256 = hashlib.sha256(image_msg).hexdigest()

    # Print APOD image information
    print_apod_info(image_url, image_path, image_size, image_sha256)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256,image_download_date)
        
    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
    if len(argv) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
    last_part_url = image_url.rsplit("/")[-1:]

    last_part = last_part_url[0]
    
    final_image_path = dir_path+"\\"+last_part

    return final_image_path

def get_apod_info(date):    
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """    

    print("Getting APOD information from NASA...sucess")
    apod_date= date

    URL = 'https://api.nasa.gov/planetary/apod'

    API_KEY = '4JxrLgSaoFPKS9Xd8lXugyeMjYAN7aOOyfH0EQ5I'
    
    params={
        'api_key':API_KEY,
        'date':apod_date
    }

    response = requests.get(URL,params=params)
    
    return response.json()

def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD

    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    print("APOD Information:")
    
    print("\tURL:",image_url)
    print("\tFile Path:",image_path)
    print("\tFile Size:",image_size,"bytes")
    print("\tSHA-256:",image_sha256)

    return None

def download_apod_image(image_url):
    """
    Downloads an image from a specified URL.

    :param image_url: URL of image
    :returns: Response message that contains image data
    """

    print("Downloading the APOD...sucess")
    image_data = requests.get(image_url).content
    
    return image_data

def save_image_file(image_msg, image_path):     
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """

    with open(image_path, 'wb') as handler:
        handler.write(image_msg)

    return None

def create_image_db(db_path):
    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """

    #connect to the databse for retreving the connection object
    myConnection = sqlite3.connect('apod_images.db')

    myCursor = myConnection.cursor()

    #sql query to create our database table

    createImageTable = """ CREATE TABLE IF NOT EXISTS images(
                            location_path text NOT NULL,
                            file_size int NOT NULL,
                            hash_value text NOT NULL,
                            date_time datetime NOT NULL
                        );"""
    
    myCursor.execute(createImageTable)
    myConnection.commit()
    myConnection.close()
    return None 

def add_image_to_db(db_path, image_path, image_size, image_sha256,date):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """

    myConnection = sqlite3.connect(db_path)

    myCursor = myConnection.cursor()

    addImageQuery = """INSERT INTO images(
                        location_path,
                        file_size,
                        hash_value,
                        date_time
                        )
                    VALUES (?,?,?,?);"""
    addData = (image_path,
                image_size,
                image_sha256,
                datetime.date(date)
                )
    
    myCursor.execute(addImageQuery,addData)

    myConnection.commit()
    myConnection.close()
    return None

def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 

    myConnection = sqlite3.connect(db_path)
    myCursor = myConnection.cursor()

    hash = image_sha256

    selectStatement = ("""SELECT location_path FROM images
                    WHERE hash_value = \'""") + hash + "\'" 

    myCursor.execute(selectStatement)
    results = myCursor.fetchall()

    myConnection.close

    if (len(results)==0):
        a = False

        print("New Image Not in chache.")
        print("Saving Image File...sucess")
        print("Adding Image to DB...sucess")
        

    else:
        a= True

        print("Image is already in chache.")

    return a

def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """

    print("Setting desktop wallpaper...sucess")

    SPI_SETDESKWALLPAPER = 20
    path = os.path.abspath(image_path).encode()
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0,path , 0)
    
    return None

main()