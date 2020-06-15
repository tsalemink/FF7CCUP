from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import sqlite3
import os
import glob
import numpy as np



def test_db():
    conn=sqlite3.connect('textures.db')
    c=conn.cursor()
    c.execute("SELECT *, filename FROM textures")
    print(c.fetchall())
    conn.close()

def initialize_db():
    conn = sqlite3.connect('textures.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS textures (
        filename text PRIMARY KEY,
        gname text,
        width integer,
        height integer,
        category text,
        text_element integer,
        shinra_logo integer,
        use_esrgan integer,
        ignore integer
        )""")
    c.execute("""CREATE TABLE IF NOT EXISTS saved (filename text)""")

    conn.commit()
    conn.close()

def entry_exists(file=""):
    filename=file[13:-4]
    conn=sqlite3.connect('textures.db')
    c = conn.cursor()
    c.execute("SELECT * FROM textures WHERE filename=?",(filename,))
    conn.close()
    return c.fetchall()

def get(file):
    filename=file
    attributes = []
    conn=sqlite3.connect('textures.db')
    conn.row_factory = sqlite3.Row
    c=conn.cursor()
    c.execute("SELECT * FROM textures WHERE filename=?", (filename,))
    result = c.fetchone()
    conn.close()
    return result[0:10]
    """if not result:
        print("Adding file to DB: "+filename)
        my_img = ImageTk.PhotoImage(Image.open(file))
        addRecord(file)
        attributes = [file, file, my_img.width(), my_img.height(), "New", 0,0,0,0]

    else:
        print(result)
        for attr in result:
            for i in range(0, 9):
                attributes.append(attr[i])
    return attributes"""
    
def addRecord(conn, file, width, height):
    c=conn.cursor()
    try:
        c.execute("""INSERT INTO textures VALUES (:filename, :gname, :width, :height, :category,
                  :text, :shinra, :esrgan, :ignore)""",
                {
                    'filename': file,
                    'gname': file,
                    'width': width,
                    'height': height,
                    'category': "New",
                    'text': 0,
                    'shinra': 0,
                    'esrgan': 0,
                    'ignore': 0
                })
        conn.commit()
        print(file+" added to database")
    except: pass
    

def getNewTextures():
    conn = sqlite3.connect('textures.db')
    c = conn.cursor()
    os.chdir("./masterdumps")
    imageList=[]

    print(os.getcwd())
    for png in glob.glob("*.png"):
        imageList.append(png)
        my_img = ImageTk.PhotoImage(Image.open(png))
        addRecord(conn, png, my_img.width(), my_img.height())
    os.chdir("..")
    print(os.getcwd())
    conn.close()

def updateRecord(attr, file):
    
    filename=file[13:]
    attributes=attr
    #print(attributes)
    conn=sqlite3.connect('textures.db')
    c=conn.cursor()
    c.execute("""UPDATE textures SET gname = ?, category = ?, text_element = ?, shinra_logo = ?, use_esrgan = ?,
                ignore = ? WHERE filename = ?""", attributes)
    conn.commit()
    conn.close()
    


def save(position):
    print(os.getcwd())
    filename=position

    conn = sqlite3.connect('textures.db')
    c = conn.cursor()
    try:
        c.execute("""UPDATE saved SET filename = ? WHERE oid = 1""", (filename, ))
        print("position saved @ "+filename)
    except:
        print("couldn't save")
    conn.commit()
    conn.close()
def save_init(position):
    print(os.getcwd())
    filename=position

    conn = sqlite3.connect('textures.db')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO saved SET filename = ? WHERE oid = 1""", (filename, ))
        print("position saved @ "+filename)
    except:
        print("couldn't save")
    conn.commit()
    conn.close()


def get_save():
    print(os.getcwd())
    #print("GETTING SAVE NOW")

    conn = sqlite3.connect('textures.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""SELECT *  FROM saved WHERE oid=1""")
    #print("PRINTING FETCHED POSITION \n")
    result = c.fetchone()
    #print(result['filename'])
    conn.close()
    for item in result:
        #print("2 "+result['filename'])
        return result['filename']
def getImageList():
    tx_list =  []
    conn=sqlite3.connect('textures.db')
    conn.row_factory = sqlite3.Row
    c=conn.cursor()
    c.execute("SELECT * FROM textures")
    results = c.fetchall()
    for result in results:
        tx_list.append(result['filename'])
    conn.close()
    return tx_list
    #return result['filename']
    #conn.commit()
    #conn.close()
def convertIndex(sav_pos):
    return int(str(sav_pos[0])[1:-1])
#def organize(attributes)
	#attributes[0] is filename
	#attributes[4] is category

"""   for image in imageList:
        my_img = ImageTk.PhotoImage(Image.open(image))
        c.execute("INSERT INTO textures VALUES (:file_hash, :filename, :width, :height, :category,
                  :text_element, :shinra_logo, :use_esrgan)",
                {
                    'filename': image[13:-4],
                    'gname': image[13:-4],
                    'width': my_img.width(),
                    'height': my_img.height(),
                    'category': "[unassigned]",
                    'text_element': "[unknown]",
                    'shinra_logo': "[unknown]",
                    'use_esrgan': "[unknown]"
                })"""

