import pytesseract
import pyautogui
from PIL import Image
from PIL import ImageGrab
import sqlite3
import time
import tkinter as tk
from tkinter import ttk
import ctypes
from datetime import date



pytesseract.pytesseract.tesseract_cmd= r"C:\Program Files\Tesseract-OCR\tesseract"
day = date.today()
today = day.strftime("%d_%m_%Y")
newfile=open('%s.csv' % today, 'w',encoding='utf-8')
newfile.write("Item"+ "," + "price x1" + "," + "price x10" + "," + "price x100" + "," + "chosen price" + ","+ "\n")    

# Windows API constants for keypress simulation
KEYEVENTF_KEYUP = 0x0002
VK_1 = 0x31  # Virtual key code for "1"
VK_a = 0x41  # Virtual key code for "a"
VK_esc=0x1B  # Virtual key code for "escape"

HDVS = [
    {"NOM_HDV":"HDV_RESSOURCES", "coordinates": (280, 500, 920, 240), "zaapi_position":15 },
    {"NOM_HDV":"HDV_BUCHERONS", "coordinates": (765, 570, 550, 200), "zaapi_position":7 },
    {"NOM_HDV":"HDV_ANIMAUX", "coordinates": (0, 0, 0, 0), "zaapi_position":2 },
    {"NOM_HDV":"HDV_MINEURS", "coordinates": (275, 475, 100, 200), "zaapi_position":11 },
    {"NOM_HDV":"HDV_PAYSANS", "coordinates": (688, 608, 470, 500), "zaapi_position":13 },
    {"NOM_HDV":"HDV_BOUCHERS_CHASSEURS", "coordinates": (761, 610, 55, 30), "zaapi_position":4 },
    {"NOM_HDV":"HDV_POISSONIERS_PECHEURS", "coordinates": (320, 630, 740, 150), "zaapi_position":14 },
    {"NOM_HDV":"HDV_ALCHIMISTES", "coordinates": (1100, 440, 930, 350), "zaapi_position":1 },
    {"NOM_HDV":"HDV_BOULANGERS", "coordinates": (425, 440, 430, 150), "zaapi_position":5 },
    {"NOM_HDV":"HDV_RUNES", "coordinates": (205, 650, 210, 450), "zaapi_position":15 },
    {"NOM_HDV":"HDV_BIJOUTIERS", "coordinates": (470, 400, 100, 580), "zaapi_position":3 },
    {"NOM_HDV":"HDV_TAILLEURS", "coordinates": (470, 440, 330, 350), "zaapi_position":18 },
    {"NOM_HDV":"HDV_COORDONNIERS", "coordinates": (465, 535, 660, 300), "zaapi_position":8 },
    {"NOM_HDV":"HDV_FORGERONS", "coordinates": (205, 570, 700, 430), "zaapi_position":10 },
    {"NOM_HDV":"HDV_SCULPTEURS", "coordinates": (650, 360, 1080, 240), "zaapi_position":17 },
    {"NOM_HDV":"HDV_BRICOLEURS", "coordinates": (0, 0, 0, 0), "zaapi_position":6 },
    {"NOM_HDV":"HDV_AMES", "coordinates": (600, 220, 400, 310), "zaapi_position":19 },
    {"NOM_HDV":"MILICE", "coordinates": (0, 0, 660, 281), "zaapi_position":20 },
]
HDV_dict = {hdv["NOM_HDV"]: (hdv["coordinates"], hdv["zaapi_position"]) for hdv in HDVS}

i=1
k=1

delta_t_debut=3
delta_t=0.05
delta_t_mouse_move=0.1
currentmap="HDV_FORGERONS"

def init_index():
    global i,k
    i=1
    k=1

def TESSERACT_GET_NUMBER():
    get_number_image= ImageGrab.grab(bbox=(300, 680, 540, 710))
    raw_number_string = pytesseract.image_to_string(get_number_image, config='')
    get_number = int(raw_number_string.partition(' ')[0])
    return get_number

def HDV_PNJ_choice(state,HDV):
        if (state == "fullscreen"):
            print("position x PNJ",HDV,str(HDV_dict[HDV][0][0]))
            print("position y PNJ",HDV,str(HDV_dict[HDV][0][1]))
            pos_x=HDV_dict[HDV][0][0]
            pos_y=HDV_dict[HDV][0][1]
        pyautogui.moveTo(pos_x,pos_y,delta_t_mouse_move,pyautogui.easeInOutQuad)
        pyautogui.click(pos_x,pos_y)
        time.sleep(delta_t)
        pyautogui.moveTo(pos_x+60,pos_y+100,delta_t_mouse_move,pyautogui.easeInOutQuad)
        pyautogui.click(pos_x+60,pos_y+100)
        time.sleep(delta_t)

def HDV_RESSOURCES_TYPE_MENU():
    pyautogui.moveTo(470,200,delta_t_mouse_move/10,pyautogui.easeInOutQuad)
    HDV_CLICK(1)
    time.sleep(delta_t)

def HDV_RESSOURCES_FIRST_TYPE(nb):
    HDV_RESSOURCES_TYPE_MENU()
    pos_x, pos_y = pyautogui.position()
    pyautogui.moveTo(pos_x,pos_y+(40*nb),delta_t_mouse_move/10,pyautogui.easeInOutQuad)
    HDV_CLICK(1)
    time.sleep(delta_t)

def HDV_MOUSE_UP(nb):
    pos_x, pos_y = pyautogui.position()
    pyautogui.moveTo(pos_x,pos_y-(36*nb),delta_t_mouse_move/10,pyautogui.easeInOutQuad)
    time.sleep(delta_t)

def HDV_RESSOURCES_CHOOSE_TYPES(nb):
    global i
    print("type mis à (i)" +str(nb))
    if(nb<13):
        HDV_RESSOURCES_TYPE_MENU()
        pos_x, pos_y = pyautogui.position()
        pyautogui.moveTo(pos_x,(pos_y+(36*nb)),delta_t_mouse_move/10,pyautogui.easeInOutQuad)
        HDV_CLICK(1)
    else:
        HDV_RESSOURCES_SCROLL_TYPES(i)
        pyautogui.moveTo(pos_x,(pos_y+(36*nb)),delta_t_mouse_move/10,pyautogui.easeInOutQuad)
        HDV_CLICK(1)
    time.sleep(delta_t)
    i=i+1


def HDV_RESSOURCES_SCROLL_TYPES(nb):
    global i
    i=1
    HDV_RESSOURCES_TYPE_MENU()
    pos_x, pos_y = pyautogui.position()
    pyautogui.moveTo(pos_x,(pos_y+36),delta_t_mouse_move/10,pyautogui.easeInOutQuad)
    HDV_TYPE_SCROLL(nb+1)
    if (nb>14):
        HDV_ITEM_SLIDE(nb-14)
    HDV_CLICK(1)
    HDV_RESSOURCES_FIRST_ITEM(1)
    HDV_CLICK(1)
    time.sleep(delta_t)

def HDV_RESSOURCES_FIRST_ITEM(nb):
    pyautogui.moveTo(100,260,delta_t_mouse_move/10,pyautogui.easeInOutQuad)
    time.sleep(delta_t)


def HDV_CLICK(nb):
    pos_x, pos_y = pyautogui.position()
    pyautogui.click(pos_x, pos_y)
    time.sleep(delta_t)

def HDV_RESSOURCES_SCROLL(nb):
    pyautogui.scroll(-36*nb)
    time.sleep(delta_t)

def HDV_TYPE_SCROLL(nb):
    pyautogui.scroll(-36*nb)
    time.sleep(delta_t)


def HDV_ITEM_SLIDE(nb):
    pos_x, pos_y = pyautogui.position()
    pyautogui.moveTo(pos_x, pos_y+(36*nb),delta_t_mouse_move/10,pyautogui.easeInOutQuad)
    time.sleep(delta_t/10)

def HDV_ITEM_MOVETO_CENTER():
    pyautogui.moveTo(250, 500,delta_t_mouse_move/10,pyautogui.easeInOutQuad)
    time.sleep(delta_t/10)


def ITEM_PRICING(price1,price10,price100):
    if (price100==0):
        if(price10==0):
            return price1
        else:
            return price10
    else:
        return price100


def HDV_ITEMS_GO_THROUGH_TWELVE(nb):
    for j in range(nb):
        HDV_CLICK(1)
        print("number of iterations :"+str(nb))
        time.sleep(delta_t)
        print("clicked on :")
        title_img = ImageGrab.grab(bbox=(590, 112, 1090, 154))
        title_text = pytesseract.image_to_string(title_img, config='', lang='fra')
        title_text=title_text.replace("\n", "")
        title_text=title_text.rstrip()
        print(title_text+"\n")
        price_1_img = ImageGrab.grab(bbox=(662, 522, 785, 553))
        price_1_text = pytesseract.image_to_string(price_1_img, config='')
        if (price_1_text==""):
            price_1_text = pytesseract.image_to_string(price_1_img, config='--psm 10')
            price_1_text=price_1_text.strip()
        if (price_1_text=="-"):
            price_1_text="0.00"
        price_1_text=price_1_text.replace(" ", "")
        price_1_text=price_1_text.replace("\n", "")
        if (price_1_text==""):
            price_1_text="0.00"
        price_1_text=''.join(c for c in price_1_text if c.isdigit())
        price_10_img = ImageGrab.grab(bbox=(830, 522, 942, 553))
        price_10_text = pytesseract.image_to_string(price_10_img, config='')
        price_10_text=price_10_text.replace(" ", "")
        price_10_text=price_10_text.replace("\n", "")
        if (price_10_text==""):
            price_10_text="0.00"
        price_10_text=''.join(c for c in price_10_text if c.isdigit())
        price_100_img = ImageGrab.grab(bbox=(973, 522, 1100, 553))
        price_100_text = pytesseract.image_to_string(price_100_img, config='')
        price_100_text=price_100_text.replace(" ","")
        price_100_text=price_100_text.replace("\n", "")
        if (price_100_text==""):
            price_100_text="0.00"       
        price_100_text=''.join(c for c in price_100_text if c.isdigit())
        chosen_price=ITEM_PRICING(float(price_1_text),float(price_10_text)/10,float(price_100_text)/100)
        newfile.write(title_text+ "," + str(float(price_1_text)) + "," + str(float(price_10_text)/10) + "," +str(float(price_100_text)/100)+"," + str(chosen_price) + "\n")    
        print(j)
        if (j!=11):
            HDV_ITEM_SLIDE(1)

def HDV_ITEMS_GO_THROUGH(nb):
    global k
    HDV_RESSOURCES_FIRST_ITEM(1)
    buffer=nb
    if(nb<12):
        print ("nb est inférieur à 12")
        HDV_ITEMS_GO_THROUGH_TWELVE(nb)
    else:
        print ("nb est supérieur à 12")
        HDV_ITEMS_GO_THROUGH_TWELVE(12)
        buffer=buffer-12
        while (buffer>0):
            if(buffer<12):
                HDV_MOUSE_UP(buffer)
                HDV_RESSOURCES_SCROLL(14)
                HDV_ITEM_SLIDE(1)
                HDV_ITEMS_GO_THROUGH_TWELVE(buffer)                
            else:
                HDV_MOUSE_UP(11)
                HDV_RESSOURCES_SCROLL(14)
                HDV_ITEMS_GO_THROUGH_TWELVE(12)
                '''HDV_ITEM_SLIDE(1)'''
            buffer=buffer-12
        HDV_ITEM_MOVETO_CENTER()
        HDV_RESSOURCES_SCROLL(-nb)
    k=k+1
    print("k="+str(k))
    time.sleep(delta_t)
  
def ESCAPE_MENU():
    print("excape button pressed")
    ctypes.windll.user32.keybd_event(VK_esc, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_esc, 0, KEYEVENTF_KEYUP, 0)


def GET_CURRENT_MAP():
    ctypes.windll.user32.keybd_event(VK_1, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_1, 0, KEYEVENTF_KEYUP, 0)

def GO_TO_HDV(next_hdv):
    global currentmap
    print("current map", currentmap)
    print("next map", next_hdv)
    if (currentmap=="RANDOM" or currentmap=="MILICE"): #will consume bonta potion then go to ressources market from the milicia
        ctypes.windll.user32.keybd_event(VK_1, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_1, 0, KEYEVENTF_KEYUP, 0)
        print("current map is: ",currentmap, "and next map is",next_hdv)
        currentmap="MILICE"
        time.sleep(0.5)
        pyautogui.moveTo(HDV_dict[currentmap][0][2],HDV_dict[currentmap][0][3],delta_t_mouse_move,pyautogui.easeInOutQuad)#zaapi_click
        pyautogui.click()
        print("first click")
        pyautogui.moveTo((HDV_dict[currentmap][0][2]+30),(HDV_dict[currentmap][0][3]+50),0.01,pyautogui.easeInOutQuad)#zaapi_click2
        time.sleep(0.1)
        pyautogui.click()
        print("moving to zaapi")
        time.sleep(2)#moving to zaapi
        pyautogui.moveTo(574,165,delta_t_mouse_move,pyautogui.easeInOutQuad)#hdv_tab
        pyautogui.click()
        if (HDV_dict[next_hdv][1]>10):
            print("cas 1 order of hdv is :",str(HDV_dict[next_hdv][1]))
            pyautogui.moveTo(650,450,delta_t_mouse_move,pyautogui.easeInOutQuad)#center mouse
            time.sleep(0.2)
            pyautogui.scroll(-2000)
            time.sleep(0.2)
            pyautogui.moveTo(622,463,delta_t_mouse_move,pyautogui.easeInOutQuad)#hdv_ressources
            pyautogui.moveTo(650,250+45*(HDV_dict[next_hdv][1]-10),delta_t_mouse_move,pyautogui.easeInOutQuad)#get to the next_hdv after scrolling
        else:
            print("cas 2")
            pyautogui.moveTo(650,250+45*(HDV_dict[next_hdv][1]-1),delta_t_mouse_move,pyautogui.easeInOutQuad)#get to the next_hdv
        pyautogui.click()
        currentmap=next_hdv
    elif (currentmap==next_hdv):
        print("cas3 on est sur la bonne map")
        currentmap=next_hdv
    else: 
        print("moveto"+ str(HDV_dict[currentmap][0][2])+ str(HDV_dict[currentmap][0][3]))
        print(currentmap)
        pyautogui.moveTo(HDV_dict[currentmap][0][2],HDV_dict[currentmap][0][3],delta_t_mouse_move,pyautogui.easeInOutQuad)#zaapi_click
        pyautogui.click()
        pyautogui.moveTo(HDV_dict[currentmap][0][2]+30,HDV_dict[currentmap][0][3]+50,delta_t_mouse_move,pyautogui.easeInOutQuad)#zaapi_click2
        pyautogui.click()
        time.sleep(2)#moving to zaapi
        pyautogui.moveTo(574,165,delta_t_mouse_move,pyautogui.easeInOutQuad)#hdv_tab
        pyautogui.click()
        if (HDV_dict[next_hdv][1]>10):
            print("cas 4")
            pyautogui.moveTo(650,450,delta_t_mouse_move,pyautogui.easeInOutQuad)#center mouse
            pyautogui.scroll(-2000)
            pyautogui.moveTo(622,463,delta_t_mouse_move,pyautogui.easeInOutQuad)#hdv_ressources
            pyautogui.moveTo(650,250+45*(HDV_dict[next_hdv][1]-10),delta_t_mouse_move,pyautogui.easeInOutQuad)#get to the next_hdv after scrolling
        elif (HDV_dict[next_hdv][1]<=10 and HDV_dict[next_hdv][1]>HDV_dict[currentmap][1]):
            print("cas 5")
            pyautogui.moveTo(650,250+45*(HDV_dict[next_hdv][1]-2),delta_t_mouse_move,pyautogui.easeInOutQuad)#get to the next_hdv
        else:
            print("cas 6")
            print(currentmap)
            pyautogui.moveTo(650,250+45*(HDV_dict[next_hdv][1]-1),delta_t_mouse_move,pyautogui.easeInOutQuad)#get to the next_hdv
        pyautogui.click()
        currentmap=next_hdv
    time.sleep(0.5)

def REFRESH_TIMER():
    global currentmap
    print("refreshing")
    pyautogui.moveTo(930,380,delta_t_mouse_move,pyautogui.easeInOutQuad)#goes somewhere in the center of the map
    print("go to center")
    pyautogui.moveTo(HDV_dict[currentmap][0][2],HDV_dict[currentmap][0][3],delta_t_mouse_move,pyautogui.easeInOutQuad)#goes to zaapi
    pyautogui.click()
    print("click on current zaapi")
    pyautogui.moveTo(HDV_dict[currentmap][0][2]+30,HDV_dict[currentmap][0][3]+50,delta_t_mouse_move,pyautogui.easeInOutQuad)#goes to zaapi
    pyautogui.click()
    print("go to current zaapi")
    time.sleep(4)#moving to zaapi
    ESCAPE_MENU()#after opening the zaapi menu, escapes it


def process_selection(selected_option):
    print(f"Selected option: {selected_option}")
    button.config(state="disabled")
    root.iconify()
    root.update()  
    time.sleep(delta_t_debut)
    global currentmap
    match selected_option:
        case "HDV Ressources":
            GO_TO_HDV("HDV_RESSOURCES")
            HDV_PNJ_choice("fullscreen","HDV_RESSOURCES")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_SCROLL_TYPES(k)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            init_index()
            ESCAPE_MENU()
            REFRESH_TIMER()
            if checkbox_state.get():
                GO_TO_HDV("HDV_BUCHERONS")
                selected_option="HDV Bucherons"
                process_selection(selected_option)
        case "HDV Bucherons":
            HDV_PNJ_choice("fullscreen","HDV_BUCHERONS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(5):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            if checkbox_state.get():
                GO_TO_HDV("HDV_MINEURS")
                selected_option="HDV Mineurs"
                process_selection(selected_option)
        case "HDV Mineurs":
            HDV_PNJ_choice("fullscreen","HDV_MINEURS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(5):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            if checkbox_state.get():
                GO_TO_HDV("HDV_PAYSANS")
                selected_option="HDV Paysans"
                process_selection(selected_option)
        case "HDV Paysans":
            HDV_PNJ_choice("fullscreen","HDV_PAYSANS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(3):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            if checkbox_state.get():
                GO_TO_HDV("HDV_BOUCHERS_CHASSEURS")
                selected_option="HDV Bouchers et Chasseurs"
                process_selection(selected_option)
        case "HDV Bouchers et Chasseurs":
            HDV_PNJ_choice("fullscreen","HDV_BOUCHERS_CHASSEURS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(3):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            if checkbox_state.get():
                ESCAPE_MENU()

                GO_TO_HDV("HDV_POISSONIERS_PECHEURS")
                selected_option="HDV Poissoniers et Pecheurs"
                process_selection(selected_option)
        case "HDV Poissoniers et Pecheurs":
            HDV_PNJ_choice("fullscreen","HDV_POISSONIERS_PECHEURS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(3):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            if checkbox_state.get():
                ESCAPE_MENU()
                GO_TO_HDV("HDV_ALCHIMISTES")
                selected_option="HDV Alchimistes"
                process_selection(selected_option)
        case "HDV Alchimistes":
            HDV_PNJ_choice("fullscreen","HDV_ALCHIMISTES")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(4):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            HDV_RESSOURCES_CHOOSE_TYPES(6)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(8)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(9)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            HDV_RESSOURCES_CHOOSE_TYPES(10)
            HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
            init_index()
            ESCAPE_MENU()
            REFRESH_TIMER()
            if checkbox_state.get():
                ESCAPE_MENU()
                GO_TO_HDV("HDV_BOULANGERS")
                selected_option="HDV Boulangers"
                process_selection(selected_option)
        case "HDV Boulangers":
            HDV_PNJ_choice("fullscreen","HDV_BOULANGERS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(2):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            REFRESH_TIMER()
            if checkbox_state.get():
                ESCAPE_MENU()
                GO_TO_HDV("HDV_BIJOUTIERS")
                selected_option="HDV Bijoutiers"
                process_selection(selected_option)
        case "HDV Bijoutiers":
            HDV_PNJ_choice("fullscreen","HDV_BIJOUTIERS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(2):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            REFRESH_TIMER()
            if checkbox_state.get():
                ESCAPE_MENU()
                selected_option="HDV Forgerons"
                process_selection(selected_option)
        case "HDV Forgerons":
            GO_TO_HDV("HDV_FORGERONS")
            HDV_PNJ_choice("fullscreen","HDV_FORGERONS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(7):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            REFRESH_TIMER()
            if checkbox_state.get():
                ESCAPE_MENU()
                selected_option="HDV Tailleurs"
                process_selection(selected_option)
        case "HDV Tailleurs":
            GO_TO_HDV("HDV_TAILLEURS")
            HDV_PNJ_choice("fullscreen","HDV_TAILLEURS")
            HDV_RESSOURCES_CHOOSE_TYPES(1)
            HDV_RESSOURCES_FIRST_ITEM(1)
            for j in range(3):
                HDV_ITEMS_GO_THROUGH(TESSERACT_GET_NUMBER())
                HDV_RESSOURCES_CHOOSE_TYPES(i)
            init_index()
            ESCAPE_MENU()
            REFRESH_TIMER()
            '''if checkbox_state.get():
                ESCAPE_MENU()
                GO_TO_HDV("HDV_TAILLEURS")
                selected_option="HDV Tailleurs"
                process_selection(selected_option)'''

    button.config(state="normal")




# Create the main window
root = tk.Tk()
root.title("extracteurs de prix")
root.geometry("300x250")  # Set the window size

# Create a label
label = tk.Label(root, text="Choisir une option:")
label.pack(pady=10)

# Create a drop-down list
options = ["HDV Ressources", "HDV Mineurs", "HDV Bucherons", "HDV Paysans", "HDV Bouchers et Chasseurs","HDV Poissoniers et Pecheurs","HDV Alchimistes","HDV Boulangers","HDV Bijoutiers","HDV Forgerons","HDV Tailleurs"]
selected_option = tk.StringVar()
selected_option.set(options[0])  # Set the default value

dropdown = ttk.Combobox(root, textvariable=selected_option, values=options, state="readonly")
dropdown.pack(pady=10)

# Create a checkbox
checkbox_state = tk.BooleanVar()  # Variable to store the state of the checkbox
checkbox = tk.Checkbutton(root, text="Passer tous les HDV en revue (option 1)", variable=checkbox_state)
checkbox.pack(pady=10)

# Create a button
button = tk.Button(root, text="commencer", command=lambda: process_selection(selected_option.get()))
button.pack(pady=10)

# Run the main event loop
root.mainloop()