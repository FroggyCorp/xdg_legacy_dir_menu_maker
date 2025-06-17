# XDG LegacyDir Menu Maker

# Licence

MIT License

Copyright (c) 2025 Froggy / FroggyCorp.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Why that program

I started with KDE few weeks ago, and using kmenuedit and modifying applications-kmenuedit.menu is pain. Changing part of the menu, stay inside applications-kmenuedit.menu and become unreadable. I wanted to get back a start menu, easy to configure as the one under windows and using LegacyDir option.

# What to conf ?

You can do nothing or add directory to scan for .desktop file and change the saving path of the start menu structure.
If you already have a $HOME/.config/menus/plasma-applications.menu, you need to save it before launching

# How it works ?

1. Recreate the dir arch on the path you defined
2. Copy .directory files to _directory for easy use of icons and create .directory file in each dir for easy config
3. Search for .desktop files depending on XDG_DATA_DIRS and other directory you added
4. Compare with .desktop already present inside the start menu directory
5. Copy new file inside _new, remove some tag which don't show with <LegacyDir>.
6. Create plasma-applications.menu in $HOME/.config/menus which will override the one in /etc/xdg/menus
7. Move file, create dir to the arch you want to have. Launch again the prog to get automatic .directory files
8. In case of, launch "kbuildsycoca6  --menutest --noincremental" in console to update the menu

# Limitation :
_hidden & _delete are same. Put files inside if you don't want them to show in start menu. _delete should not show as well in search, but actually don't work.
Don't make a directory with extra char like &. Use .directory files to change the showed name
You can't have a .desktop file in 2 location. The second will "erase" the first declared.

# How to remove :
Delete $HOME/.config/menus/plasma-applications.menu
Run "kbuildsycoca6  --menutest --noincremental"

# Todo :
Compare deleted files from system, and move the one in start menu to _lost
Make _delete working

# Version :
0.1