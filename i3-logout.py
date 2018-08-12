#!/usr/bin/env python
import Tkinter as tk
from subprocess import Popen
from PIL import Image
import re
import ast
import os
import os.path

class i3exit(tk.Frame):

    # icon (item) class
    class Icon():
        def __init__(self, name = '', cmd = '', icon = ''):
            self.name = name
            self.cmd = cmd
            self.icon = icon
        name = ''
        cmd = ''
        icon = ''
        btn = tk.Button

    icons = [] # all icons should be kept here
    iconsCount = 0
    currentIconIndex = 0
    currentPath = '';

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg='#000000')
        root = self.master
        self.currentPath = os.path.dirname(os.path.realpath(__file__)) + '/';
        root.wm_attributes('-type', 'normal')
        root.wm_attributes('-fullscreen', True)
        root.attributes('-alpha', 1)
        root.update_idletasks()
        screenWidth, screenHeight = root.winfo_width(), root.winfo_height()
        self.config(width=screenWidth, height=screenHeight)
        self.grid(sticky='n')
        root.wait_visibility(root)
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-alpha", 0.9)
        root.config(bg='#000000')
        self.initIcons()
        self.initPanel()
        self.renderIcons()
        self.bindKeys()

    def initStatusIcon(self):
        return

    def bindKeys(self):
        self.master.bind('<Escape>', lambda e:self.quit())
        self.master.bind('<Right>', lambda e:self.nextIcon())
        self.master.bind('<Left>', lambda e:self.prevIcon())
        self.master.bind('<semicolon>', lambda e:self.nextIcon())
        self.master.bind('<j>', lambda e:self.prevIcon())
        self.master.bind('<Return>', lambda e:self.executeCommand(self.icons[self.currentIconIndex]))

    def renderIcon(self, icon, column):
        image = tk.PhotoImage(file=self.currentPath + icon.icon)
        btn = tk.Button(self.panel, text=icon.name, fg='#ffffff', bd=0, height=64, command=lambda icon=icon: self.executeCommand(icon), image=image, relief='flat', bg='#000000')
        btn.config(compound='left')
        btn.config(highlightbackground='#000000')
        btn.config(activebackground='#000000')
        btn.config(activeforeground='#ffffff')
        btn.config(highlightcolor='#ffffff')
        btn.config(highlightthickness=2)
        btn.image = image
        btn.grid(row=0, column=column, padx=10, pady=10)
        icon.button = btn
        return

    def iconFocus(self, index):
        self.currentIconIndex = index
        return

    def renderIcons(self):
        column = 0;
        for icon in self.icons:
            self.iconsCount = self.iconsCount + 1
            self.renderIcon(icon, column)
            if(column == 0):
                self.icons[0].button.focus_set()
                self.currentIconIndex = 0
            self.icons[column].index = column
            self.icons[column].button.bind('<FocusIn>', lambda e, index=column :self.iconFocus(index))
            column = column+1

    def focusButton(self, index):
        self.icons[index].button.focus_set()

    def nextIcon(self):
        self.currentIconIndex = self.currentIconIndex + 1
        if((self.currentIconIndex+1) > self.iconsCount):
            self.currentIconIndex = 0
        self.icons[self.currentIconIndex].button.focus_set()

    def prevIcon(self):
        self.currentIconIndex = self.currentIconIndex - 1
        if(self.currentIconIndex < 0):
            self.currentIconIndex = self.iconsCount - 1
        self.icons[self.currentIconIndex].button.focus_set()

    def executeCommand(self, icon):

        if(icon.cmd == 'app.quit'):
            self.quit()
            return

        if(icon.cmd):
            params = icon.cmd.split(" ")
            Popen(params)
            self.quit()
        return

    def initPanel(self):
        self.panel = tk.Frame(self.master, borderwidth=0, relief="sunken", bg='')
        self.panel.grid(row=0)

    # Add icons for lock, logout, suspend, hibernate, reboot and shutdown
    def initIcons(self):
        self.icons.append( self.Icon(name='Lock', icon='icon-lock.png', cmd='i3lock') )
        self.icons.append( self.Icon(name='Logout', icon='icon-logout.png', cmd='i3-msg exit') )
        self.icons.append( self.Icon(name='Suspend', icon='icon-suspend.png', cmd='lock & systemctl suspend') )
        self.icons.append( self.Icon(name='Hibernate', icon='icon-hibernate.png', cmd='lock & systemctl hibernate') )
        self.icons.append( self.Icon(name='Reboot', icon='icon-reboot.png', cmd='systemctl reboot') )
        self.icons.append( self.Icon(name='Shutdown', icon='icon-shutdown.png', cmd='systemctl poweroff') )

    def loadItemsFromConfig(self, config):
        tmp = config.get('Items', 'Items')
        items = ast.literal_eval(tmp)
        for item in items:
            newIcon = self.Icon()
            if('name' in item):
                newIcon.name = item['name']
            if('icon' in item):
                newIcon.icon = item['icon']
            if('cmd' in item):
                newIcon.cmd = item['cmd']
            self.icons.append( newIcon )
        return

app = i3exit()
app.master.title('i3-exit')
app.mainloop()
