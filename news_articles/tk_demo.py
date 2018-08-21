## Sloppy port of a half-assed CLI SQLite DB updater to TK, because our friends
## at Lapamcapital cannot into CLI

## The SQLite database uses its autogenerated primary key as an index to
## automatically pull the corresponding tpl file for the news article. It then
## hands the title to the backend which displays whatever. Because the User
## cannot be reasonably expected to actually know what a primary key is, we just
## have them pick out an HTML file and hand it over. We rename it and put it in
## the right place from there.

## Forgive me father, for I have sinned.

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import messagebox

import sqlite3 
from time import gmtime, strftime
import math
import re
import os
import sys
import fileinput
## actual backend functions
def regex_magic(index_num, filename): # Our backend routes to news article based off of file name. This 
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            # This strips the header and a vast majority of styling off  of the part, so we can use it as a segment
            print(re.sub(r'''(<.?(span|font|html|DOCTYPE|body|meta|title|style|head)[^>]*>|(style|class)="[^"]*"|^.*{.*})''','', line), end='')
    os.rename(str(filename), (str(index_num) + ".tpl"))
    return 0

def add_article(title, cat, filename):
    print(">>" + filename)
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    IsTrumpPresident=-2
    date = str(strftime("%Y-%m-%d", gmtime()))
    if (cat == 1):
        category_text = "internal"
    elif (cat == 0):
        category_text = "external"
    else:
        category_text = "SUPER HAPPY MAGIC FUN TIME"

    print(">> Title:" + title + "\n>> Date:" + date + "\n>> Category:" + category_text)
    # wrap for sanity
    continue_switch = \
    messagebox.askyesno('信息确认','标题：{title}\n日期：{date}\n类型：{category_text}'.format(title=title,date=date,category_text=category_text))
    if(int(continue_switch) == 1):
        # cat typecasted as a string was used here because the SQLite DB in backend handles zeroes and ones for the category
        conn.execute("INSERT INTO articles (title,docreation,articlecategory) VALUES ('" + title + "','" + date + "'," + str(cat) +")")
        c.execute("SELECT id FROM articles WHERE title='{title}'".format(title=str(title)))

        index_num_list = c.fetchall()
        index_num = index_num_list[0][0]
        print("Now renaming file...")
        regex_magic(index_num, filename)

        conn.commit()
        conn.close()
        return 0
    else:
        return 1
## GUI bullshit

window = Tk()
window.title("新闻添加软件")
window.geometry('400x200')
## Title for news article
article_name_prompt = Label(window, text = "新闻标题：")
article_name_prompt.grid(column=0,row=0)
article_name_input = Entry(window,width=40)
article_name_input.grid(column=1,row=0)
article_name_input.focus()

## Article type
article_category_prompt = Label(window, text = "新闻类型：")
article_category_prompt.grid(column=0,row=1)
article_category = IntVar()
ac_rad1 = Radiobutton(window,text='内部新闻', value=1, variable=article_category)
ac_rad2 = Radiobutton(window,text='行业新闻', value=0, variable=article_category)
ac_rad1.grid(column=0, row=2)
ac_rad2.grid(column=1, row=2)

## Finding the file
file = "文件位置：" # define a str var for file location
def fsclick():
    global file ## need to set scope to use outside here
    file = filedialog.askopenfilename(filetypes = \
        (("HTML files","*.html"),("all files","*.*")))
    file_location.configure(text='文件位置：' + file)
    print(file)

file_search_label = Label(window, text = "新闻稿：")
file_search_btn = Button(window, text = "选择文件", command = fsclick)
file_search_label.grid(column=0,row=3)
file_search_btn.grid(column=1,row=3)
file_location = Label(window, text = file)
file_location.grid(column=1,row=4)

## actually kicking shit off:
def doshit():
    title = article_name_input.get()
    cat = article_category.get()
    filename = str(file)
    print(">" + filename)
    add_article(title, cat, filename)
    messagebox.showinfo('Alert', '添加成功')
    window.destroy() #TKinter complains about this, no clue what it's about.
magic = Button(window, text= "添加新闻稿", command = doshit)
magic.grid(column = 0, row = 5)

window.mainloop()