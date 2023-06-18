import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import ImageTk, Image

def selectPic():
    global img
    try:
        filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
                                              filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
        if filename:
            img = Image.open(filename)
            img = img.resize((200, 200), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            lbl_show_pic['image'] = img
            entry_pic_path.delete(0, END)
            entry_pic_path.insert(0, filename)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def process_image():
    try:
        img_path = entry_pic_path.get()
        if img_path:
            open = np.ones((5, 5))
            close = np.ones((20, 20))

            citra = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
           
            if citra is None:
                raise ValueError("Failed to read the image.")

            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Failed to read the image.")

            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([20, 255, 255])
            redmask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)

            lower_red2 = np.array([170, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            redmask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)

            redmask = redmask1 + redmask2
            maskOpen = cv2.morphologyEx(redmask, cv2.MORPH_OPEN, open)
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, close)

            maskFinal = maskClose
            cnt_r = 0
            for r in redmask:
                cnt_r += list(r).count(255)
            print("Merah ", cnt_r)
            cv2.imshow('BGR Merah', redmask)
            cv2.imshow('Merah', cnt_r)

            lower_green = np.array([50, 50, 50])
            upper_green = np.array([70, 255, 255])
            greenmask = cv2.inRange(hsv_img, lower_green, upper_green)

            cv2.imshow('BGR Hijau', greenmask)
            cnt_g = 0
            for g in greenmask:
                cnt_g += list(g).count(255)
            print("Hijau ", cnt_g)

            lower_yellow = np.array([120, 50, 50])
            upper_yellow = np.array([130, 255, 255])
            yellowmask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

            cv2.imshow('BGR Kuning', yellowmask)
            cnt_y = 0
            for y in yellowmask:
                cnt_y += list(y).count(255)
            print("Kuning", cnt_y)

            tot_area = cnt_r + cnt_y + cnt_g
            rperc = cnt_r / tot_area
            yperc = cnt_y / tot_area
            gperc = cnt_g / tot_area

            glimit = 0.5
            ylimit = 0.8

            if gperc > glimit:
                print("Buah Mentah")
                cv2.imshow("Buah Mentah", img)
            elif yperc > ylimit:
                print("Buah Setengah Matang")
                cv2.imshow("Buah Setengah Matang", img)
            else:
                print("Buah Matang")
                cv2.imshow("Buah Matang", img)

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
frame = tk.Frame(root, bg='#45aaf2')

lbl_pic_path = tk.Label(frame, text='Image Path:', padx=25, pady=25, font=('verdana', 16), bg='#45aaf2')
lbl_show_pic = tk.Label(frame, bg='#45aaf2')
entry_pic_path = tk.Entry(frame, font=('verdana', 16))
btn_browse = tk.Button(frame, text='Select Image', bg='grey', fg='#ffffff', font=('courier', 16))
btn_process = tk.Button(frame, text='Process', bg='grey', fg='#ffffff', font=('courier', 16))

root.title("Deteksi Kematangan Buah Tomat")

btn_browse['command'] = selectPic
btn_process['command'] = process_image

frame.pack()

lbl_pic_path.grid(row=0, column=0)
entry_pic_path.grid(row=0, column=1, padx=(0, 20))
lbl_show_pic.grid(row=1, column=0, columnspan=2)
btn_browse.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
btn_process.grid(row=3, column=0, columnspan=2, padx=10, pady=10)



root.mainloop()
