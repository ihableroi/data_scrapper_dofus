import pytesseract
import pyautogui
from PIL import Image
from PIL import ImageGrab
import sqlite3
import time
import tkinter as tk
from tkinter import ttk
import ctypes
import pyperclip

pytesseract.pytesseract.tesseract_cmd= r"C:\Program Files\Tesseract-OCR\tesseract"

newfile=open("recettes_marteaux.txt","w")

i=1
k=1

delta_t_debut=3
delta_t=0.05
delta_t_mouse_move=0.1
delta_y=108

# Windows API constants for keypress simulation
KEYEVENTF_KEYUP = 0x0002
VK_1 = 0x31  # Virtual key code for "1"
VK_a = 0x41  # Virtual key code for "1"
VK_c = 0x43  # Virtual key code for "1"
VK_v = 0x56  # Virtual key code for "1"
VK_ctrl = 0x11  # Virtual key code for "1"
VK_shift = 0x10  # Virtual key code for "1"
# Define Windows API functions and constants
CF_UNICODETEXT = 13
OpenClipboard = ctypes.windll.user32.OpenClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard



def CLICK_COPY(pos_x,pos_y):
    pyautogui.moveTo(pos_x, pos_y,delta_t_mouse_move,pyautogui.easeInOutQuad)
    ctypes.windll.user32.keybd_event(VK_shift , 0, 0, 0)
    time.sleep(delta_t*10)
    pyautogui.mouseDown()
    time.sleep(delta_t*10)
    pyautogui.mouseUp()
    time.sleep(delta_t*10)
    ctypes.windll.user32.keybd_event(VK_shift , 0, KEYEVENTF_KEYUP, 0)
    pyautogui.moveTo(1500, 1000,delta_t_mouse_move,pyautogui.easeInOutQuad)
    pyautogui.click(1500, 1000)
    ctypes.windll.user32.keybd_event(VK_ctrl, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_a, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_ctrl, 0, KEYEVENTF_KEYUP, 0)
    ctypes.windll.user32.keybd_event(VK_a, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(delta_t)
    #ctr+c
    ctypes.windll.user32.keybd_event(VK_ctrl, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_c, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_ctrl, 0, KEYEVENTF_KEYUP, 0)
    ctypes.windll.user32.keybd_event(VK_c, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(delta_t)
    ctypes.windll.user32.keybd_event(0x0D , 0, 0, 0) #press enter


def get_clipboard_text():
    OpenClipboard(None)
    handle = GetClipboardData(CF_UNICODETEXT)
    print("recette en cours de copie")
    print("handle= "+ str(handle))
    clipboard_content = pyperclip.paste()
    return clipboard_content  
    CloseClipboard()
    return None

def GET_ITEM_NAME(pos_x1,pos_y1,pos_x2,pos_y2):
    get_item_name= ImageGrab.grab(bbox=(pos_x1,pos_y1,pos_x2,pos_y2))
    item_name_string = pytesseract.image_to_string(get_item_name, config='--psm 10')
    print(item_name_string)
    '''newfile.write(item_name_string)   '''
    return item_name_string

def GET_ITEM_RECETTE(position):
    pyautogui.moveTo(160, 275+position*108,delta_t_mouse_move,pyautogui.easeInOutQuad)
    CLICK_COPY(160, 275+position*108)
    print("recette copiee")
    get_recette_raw = get_clipboard_text()
    print(get_recette_raw)
    newfile.write(get_recette_raw+"\n")   


def GET_ALL_RECETTES(metier,nombre):
    time.sleep(delta_t_debut)
    button.config(state="disabled")
    root.iconify()
    root.update() 

    for i in range(5):
        print(i)
        global delta_y
        GET_ITEM_NAME(192,263+(i*delta_y),672,283+(i*delta_y))
        GET_ITEM_RECETTE(i)
        pyautogui.moveTo(5, 800,delta_t_mouse_move,pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(delta_t_mouse_move)
    i=0
    for i in range(nombre):
        print(i)
        GET_ITEM_NAME(192,263+(3*delta_y),672,283+(3*delta_y))
        GET_ITEM_RECETTE(3)
        pyautogui.moveTo(5, 800,delta_t_mouse_move,pyautogui.easeInOutQuad)
        pyautogui.click()
        GET_ITEM_NAME(192,263+(4*delta_y),672,283+(4*delta_y))
        GET_ITEM_RECETTE(4)
        time.sleep(delta_t_mouse_move/10)
        pyautogui.moveTo(695, 791,delta_t_mouse_move,pyautogui.easeInOutQuad)
        pyautogui.mouseDown()
        time.sleep(delta_t_mouse_move/10)
        pyautogui.mouseUp()
        time.sleep(delta_t_mouse_move/10)
    button.config(state="normal")





# Create the main window
root = tk.Tk()
root.title("extracteurs de recettes")
root.geometry("300x250")  # Set the window size

# Create a label
label = tk.Label(root, text="Choisir une option:")
label.pack(pady=10)

# Create a drop-down list
options = ["forgeur de marteaux", "bijoutier", "mineur", "alchimiste"]
selected_option = tk.StringVar()
selected_option.set(options[0])  # Set the default value

dropdown = ttk.Combobox(root, textvariable=selected_option, values=options, state="readonly")
dropdown.pack(pady=10)


# Create a button
button = tk.Button(root, text="commencer", command=lambda: GET_ALL_RECETTES(selected_option.get(),90))
button.pack(pady=10)

# Run the main event loop
root.mainloop()