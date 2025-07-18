##################
#MIT License
#
#Copyright (c) 2025 Froggy / FroggyCorp.
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#version 0.2


import os
from os import walk
from pathlib import Path
import os.path
import shutil

#config part

#define if you want more dir to be scanned. For example $HOME/Desktop to get wine or steam .desktop
installed_desktop_path = [str(Path.home()) + '/Desktop'] #['rep1', 'rep2']
#define where the basedir of menu should be save. Per default is $HOME/.config/menus/xdg_legacy_dir_menu_maker
start_menu_desktop_path = str(Path.home()) + '/.config/menus/xdg_legacy_dir_menu_maker'

#end of config

XDG_DATA_DIRS = os.getenv("XDG_DATA_DIRS").split(':')

installed_desktop_files = []
start_menu_desktop_files = []

config_delete = '_delete'
config_new = '_new'
config_directory = '_directory'
config_lost = '_lost'
config_hidden = '_hidden'
config_dir = [config_delete, config_new, config_directory, config_lost, config_hidden]
XDG_MENU_PREFIX = 'plasma-'
config_directory_folder_name = 'desktop-directories'
config_desktop_folder_name = 'applications'
config_applications_menu_file = str(Path.home()) + '/.config/menus/' + XDG_MENU_PREFIX + 'applications.menu'
config_applications_menu = "<!DOCTYPE Menu PUBLIC '-//freedesktop//DTD Menu 1.0//EN' 'http://www.freedesktop.org/standards/menu-spec/1.0/menu.dtd'>\n \
<Menu>\n \
 <Name>Applications</Name>\n \
 <LegacyDir>" + start_menu_desktop_path + "</LegacyDir>\n \
</Menu>\n"

def search_in_file(file_name, array):
    find = False
    with open(file_name, 'r') as file:
        for a in range(len(array)):
            if (array[a] in file.read()):
                find = True
                break
            file.seek(0)
    file.close()
    return find

def add_line_in_file(file_name, param):
#add param after [desktop entry]
    with open(file_name, 'r') as source:
        with open(file_name + '.new', 'w') as dest:
            for source_line in source:
                dest.write(source_line)
                if source_line.find('[Desktop Entry]') == 0:
                    dest.write(param + '\n')
        dest.close()
    source.close()
    os.replace(file_name + '.new', file_name)
    os.chmod(file_name, 0o700) 


def remove_line_in_file(file_name, array):
    if search_in_file(file_name, array) == True:
        with open(file_name, 'r') as source:
            with open(file_name + '.new', 'w') as dest:
                for source_line in source:
                    find = False
                    for a in range(len(array)):
                        if array[a] in source_line:
                            find = True
                    if find == False:
                        dest.write(source_line)
            dest.close()
        source.close()
        os.replace(file_name + '.new', file_name)
        os.chmod(file_name, 0o700) 

#regroup XDG_DATA_DIRS and installed_desktop_path
for a in range(len(XDG_DATA_DIRS)):
    installed_desktop_path.append(XDG_DATA_DIRS[a] + '/' + config_desktop_folder_name)

#create base directory if needed
if (os.path.isdir(start_menu_desktop_path)) == False:
    os.mkdir(start_menu_desktop_path)
for a in range(len(config_dir)):
    b = start_menu_desktop_path + '/' + config_dir[a]
    if (os.path.isdir(b)) == False:
        os.mkdir(b)

#define specific .directory of base directory
c = start_menu_desktop_path + '/' + config_hidden + '/.directory'
if (os.path.isfile(c)) == False:
    with open(c, 'w') as file:
        file.write('[Desktop Entry]\n' \
            'Icon=\n' \
            'Type=Directory\n' \
            'Hidden=true\n')
    file.close()
'''
c = start_menu_desktop_path + '/' + config_delete + '/.directory'
if (os.path.isfile(c)) == False:
    with open(c, 'w') as file:
        file.write('[Desktop Entry]\n' \
            'Icon=\n' \
            'Type=Directory\n' \
            'Hidden=true\n')
    file.close()
'''


#copy .directory inside _directorie, no matter if exist or not
for a in range(len(XDG_DATA_DIRS)):
    for (dir_path, dir_names, file_name) in walk(XDG_DATA_DIRS[a] + '/' + config_directory_folder_name + '/'):
        for b in range(len(file_name)):
            #select only .directory files
            if file_name[b].count('.directory') > 0:
                shutil.copyfile(dir_path + file_name[b], start_menu_desktop_path + '/' + config_directory + '/' + file_name[b])

#create defaut .directory file for each dir inside start_menu_desktop_path
for (dir_path, dir_names, file_name) in walk(start_menu_desktop_path):
        if len(dir_names) > 0:
            for b in range(len(dir_names)):
                c = dir_path + '/' + dir_names[b] + '/.directory' 
                if (os.path.isfile(c)) == False:
                    with open(c, 'w') as file:
                        file.write('[Desktop Entry]\n' \
                                'Icon=\n' \
                                'Type=Directory\n' \
                                'Name=' + dir_names[b] + '\n'\
                                'Comment=' + dir_names[b] + '\n')
                    file.close()

#get .desktop already present inside start menu, save in start_menu_desktop_files
for (dir_path, dir_names, file_name) in walk(start_menu_desktop_path):
    file_name = sorted(file_name, key=str.lower)
    for b in range(len(file_name)):
        size = os.path.getsize(dir_path + '/' + file_name[b])
        date = int(os.path.getctime(dir_path + '/' + file_name[b]))
        #on ajoute les repertoires s'il y a
       # if len(dir_names) > 0:
       #     dir_names = sorted(dir_names, key=str.lower)
       #     for c in range(len(dir_names)):
       #         start_menu_desktop_files.append([dir_path, dir_names[c], '', ''])
        #on ajoute que les .desktops
        if (file_name[b].count('.desktop') > 0):
            start_menu_desktop_files.append([dir_path, file_name[b], size, date])
print(str(len(start_menu_desktop_files)) + ' .desktop files in start menu')

#get all .desktop on system, refer to installed_desktop_path, save in installed_desktop.files
for a in range(len(installed_desktop_path)):
    for (dir_path, dir_names, file_name) in walk(installed_desktop_path[a]):
        for b in range(len(file_name)):
            #on ajoute que les .desktops
            if (file_name[b].count('.desktop') > 0):
                size = os.path.getsize(dir_path + '/' + file_name[b])
                date = int(os.path.getctime(dir_path + '/' + file_name[b]))
                installed_desktop_files.append([dir_path, file_name[b], size, date])
print(str(len(installed_desktop_files)) + ' .desktop files found on system')
#print(*installed_desktop_files, sep="\n")
#print(*start_menu_desktop_files, sep="\n")

#Compare & copy new .desktop files. Remove category, hidden and onlyshow parameter
for a in range(len(installed_desktop_files)):
    present = 0
    for b in range(len(start_menu_desktop_files)):
        if installed_desktop_files[a][1] == start_menu_desktop_files[b][1] :
            present = 1
    if present == 0:    #File don't exist, we copy it
        source = installed_desktop_files[a][0] + "/" + installed_desktop_files[a][1]
        dest = start_menu_desktop_path + "/" + config_new + '/' + installed_desktop_files[a][1]

#        with open(source, 'r') as origin_file:
            #we search if we need to remove some part
#            if search_in_file(source, ['NoDisplay=', 'Categories=', 'OnlyShowIn=', 'NotShowIn=']):
            #if ('NoDisplay=' in origin_file.read()) or ('Categories=' in origin_file.read()) or ('OnlyShowIn=' in origin_file.read()) or ('NotShowIn=' in origin_file.read()):
                #yes, so we remove them
#                with open(dest, 'w') as destination_file:
#                    for origin_line in origin_file:
                        #remove some config on .desktop so LegacyDir can work
#                        if origin_line.count('NoDisplay=') == 0 and origin_line.count('Categories=') == 0 and origin_line.count('OnlyShowIn=') == 0 and origin_line.count('NotShowIn') == 0 :
#                            destination_file.write(origin_line)
#                destination_file.close()
#            else:
#        origin_file.close()

        shutil.copyfile(source, dest)
        os.chmod(dest, 0o700) 


#We organise .desktop option depending on their position in start menu architecture
#remove option for all dir (need optimization ?)
for (dir_path, dir_names, file_name) in walk(start_menu_desktop_path):
    for a in range(len(file_name)):
        source = dir_path + "/" + file_name[a]
        if os.path.isfile(source) and '.desktop' in source:
            if search_in_file(source, ['NoDisplay=', 'Categories=', 'OnlyShowIn=', 'NotShowIn=', 'Hidden=']):
                remove_line_in_file(source, ['NoDisplay=', 'Categories=', 'OnlyShowIn=', 'NotShowIn=', 'Hidden='])


#add hidden or notshow for _delete and _hidden
for (dir_path, dir_names, file_name) in walk(start_menu_desktop_path):
    if config_delete in dir_path:
        for a in range(len(file_name)):
            if '.desktop' in file_name[a]:
                if search_in_file(dir_path + '/' + file_name[a], ['Hidden=']) == False:
                    add_line_in_file(dir_path + '/' + file_name[a], 'Hidden=true')
    if config_hidden in dir_path:
        for a in range(len(file_name)):
            if '.desktop' in file_name[a]:
                if search_in_file(dir_path + '/' + file_name[a], ['NoDisplay']) == False:
                    add_line_in_file(dir_path + '/' + file_name[a], 'NoDisplay=true')
                

#create menu file 
with open(config_applications_menu_file, 'w') as file:
    for line in config_applications_menu:
        file.write(line)
file.close()
