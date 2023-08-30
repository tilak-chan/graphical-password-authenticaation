from tkinter import *
from tkinter.ttk import *
from random import shuffle, randint, seed
from functools import partial
from PIL import Image, ImageTk

users = {"user1":("RedBlackBlue", "White", "Red"),
         "":("WhiteWhiteWhite", "Black", "Green"),
         "user3":("RedWhiteBlackYellow", "White", "Black"),
         "user4":("BlackWhiteRed", "Red", "Violet")}

img_path = {"Black":"Black.png", "Red":"Red.png", "Blue":"Blue.png", "Orange":"Orange.png",
            "Green":"Green.png", "Yellow":"Yellow.png", "Pink":"Pink.png",
            "White":"White.png", "Violet":"Violet.png", "Purple":"Purple.png",
            "Maroon":"Maroon.png", "LightYellow":"LightYellow.png", "LightGreen":"LightGreen.png",
            "Grey":"Grey.png", "Cyan":"Cyan.png", "Brown":"Brown.png"}

root = Tk()
root.title("Graphical Password Authentication")
root.geometry("500x500")
images = dict()
for label, path in img_path.items():
    images[label] = Image.open(path)

pswd = ""
alt_images = dict()

grow = 4
gcol = 4
gd = [(i, j) for i in range(grow) for j in range(gcol)]

def alterimg():
    offangle = 90
    global alt_images, images
    seed()
    for label, image in images.items():
        alt_img_data = []
        for pixel in image.getdata():
            (r, g, b) = (pixel[0], pixel[1], pixel[2])
            if(randint(1, 10) == 5):
                r = (r + randint(-5, 5)) % 256
                g = (g + randint(-5, 5)) % 256
                b = (b + randint(-5, 5)) % 256
            alt_pix = (r, g, b)
            alt_img_data.append(alt_pix)
        alt_img = Image.new(image.mode, image.size)
        alt_img.putdata(alt_img_data)
        orient = randint(0, 3)
        angle = orient * offangle
        alt_images[label] = (ImageTk.PhotoImage(alt_img.rotate(angle)), orient)


def login_page():
    global frame1, idfield, gd, pos
    frame1 = Frame(root)
    frame1.pack()
    Label(frame1, text = "Login Page").pack(side = TOP)
    idframe = Frame(frame1)
    idframe.pack()
    Label(idframe, text = "User ID: ").grid(row = 0, column = 0)
    idfield = Entry(idframe)
    idfield.grid(row = 0, column = 1)
    pframe = Frame(frame1)
    pframe.pack()
    Label(pframe, text = "Password: ").grid(row = 0)

    b = list()
    shuffle(gd)
    i = 0

    alterimg()
    pos1 = dict()
    pos2 = dict()
    img_labels = list(images.keys())
    for x, y in gd:
        b.append(Button(pframe, text = img_labels[i], image = alt_images[img_labels[i]][0],
        command = partial(CatPass, img_labels[i]), cursor = "dot"))
        b[i].grid(row = x + 1, column = y)
        pos1[(x, y)] = img_labels[i]
        pos2[img_labels[i]] = (x, y)
        i += 1
    Button(frame1, text = "Login", command = partial(login, pos1, pos2)).pack(side = BOTTOM)

def CatPass(str):
    global pswd
    pswd = pswd + " " + str

def login(pos1, pos2):
    global frame1, frame2
    global idfield, pswd


    keypass = ""
    userid = idfield.get()
    userid = userid.strip()
    if(userid in users.keys()):
        hint1 = users[userid][1]
        orient1 = alt_images[hint1][1]
        hint2 = users[userid][2]
        orient2 = alt_images[hint2][1]

        ort1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        (m, n) = ort1[orient1]
        pswd = pswd.strip()
        passslice = pswd.split()
        for i in passslice:
            k = ((pos2[i][0] - m - m * orient2) % grow, (pos2[i][1] - n - n * orient2) % gcol)
            keypass += pos1[k]

        if(users[userid][0] == keypass):
            pswd = ""
            frame1.destroy()
            frame2.pack()
        else:
            pswd = ""
            frame1.forget()
            login_page()
            Label(frame1, text = "Incorrect Password. Try Again.").pack(side = BOTTOM)
    else:
        pswd = ""
        frame1.forget()
        login_page()
        Label(frame1, text = "Invalid User ID. Try Again.").pack(side = BOTTOM)

def logout():
    frame2.forget()
    login_page()

frame2 = Frame(root)
Label(frame2, text = "Logged In!").pack()
Button(frame2, text = "Logout", command = logout).pack()

login_page()

root.mainloop()