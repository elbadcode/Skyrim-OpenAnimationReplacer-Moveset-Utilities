#!/usr/bin/env python
import asyncio
import os
import shutil
from collections import namedtuple
from json import JSONDecodeError
import time
import FreeSimpleGUI as sg
import json
import numpy
import subprocess
import ctypes
import re
import base64
import pyjsonviewer
import glob
from pathlib import Path, PurePath, PosixPath
from annotation_edit import replace_regex,replace_annotations

regex_stances = r"(\"Stances \- Dynamic Weapon Movesets SE\.esp\")(?:\,\n\W+\"formID\")\W*(\d+)"

mco_bfco_filepaths = list()


try:
    user_theme = sg.user_settings_get_entry('theme')
except JSONDecodeError:
    user_theme = "dark teal 5"
sg.theme(user_theme)

# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'
notices_encode = "ew0KICAgICJBY2NlcHRlZCI6IGZhbHNlLA0KICAgICJWZXJzaW9uIjogIjEuMC4wIiwNCiAgICAiQXBwbGljYXRpb25OYW1lIjogIk9BUiBVdGlsIE1hc3RlciIsDQogICAgIkF1dGhvciI6ICJMb2JvdG9teXggYWthIGVsYmFkY29kZSIsDQogICAgIlN0clBvcHVwIjogIkkgdW5kZXJzdGFuZCB0aGF0IHRoaXMgdG9vbCBjYW4gbWFrZSBwZXJtYW5lbnQgY2hhbmdlcyB0byBmaWxlcyBhbmQgaXMgYSB3b3JrIGluIHByb2dyZXNzIHRoYXQgaGFzIG5vdCBiZWVuIGV4dGVuc2l2ZWx5IHRlc3RlZCBvdXRzaWRlIHRoZSBjcmVhdG9yJ3MgaGFyZHdhcmUuIEkgaGF2ZSBhbHJlYWR5IG1hbnVhbGx5IGJhY2tlZCB1cCB0aGUgZmlsZXMgSSB3aWxsIHJ1biB0aGlzIHNjcmlwdCBhZ2FpbnN0IG9yIEkgcGxhbiB0byB1c2UgdGhlIGluIGFwcCBiYWNrdXAgbWV0aG9kIHdpdGggdGhlIHVuZGVyc3RhbmRpbmcgdGhhdCBpdCBtYXkgZmFpbC4gSWYgSSBmYWlsIHRvIHZlcmlmeSBteSBiYWNrdXBzIGFuZCB0aGlzIHByb2dyYW0gY2F1c2VzIGlycmV2ZXJzaWJsZSBsb3NzIG9mIGRhdGEgSSBhY2tub3dsZWRnZSB0aGF0IGl0IGlzIG15IG93biBmYXVsdCBhbmQgZG8gbm90IGhvbGQgdGhlIGNyZWF0b3IgYWNjb3VudGFibGUiLA0KICAgICJQU0dMaWNlbnNlIjogIkNvcHlyaWdodCAyMDIzIFB5U2ltcGxlU29mdCwgSW5jLiBhbmQvb3IgaXRzIGxpY2Vuc29ycy4gQWxsIHJpZ2h0cyByZXNlcnZlZC4gXG5SZWRpc3RyaWJ1dGlvbiwgbW9kaWZpY2F0aW9uLCBvciBhbnkgb3RoZXIgdXNlIG9mIFB5U2ltcGxlR1VJIG9yIGFueSBwb3J0aW9uIHRoZXJlb2YgaXMgc3ViamVjdCB0byB0aGUgdGVybXMgb2YgdGhlIFB5U2ltcGxlR1VJIExpY2Vuc2UgQWdyZWVtZW50IGF2YWlsYWJsZSBhdCBodHRwczovL2V1bGEucHlzaW1wbGVndWkuY29tLlxuWW91IG1heSBub3QgcmVkaXN0cmlidXRlLCBtb2RpZnkgb3Igb3RoZXJ3aXNlIHVzZSBQeVNpbXBsZUdVSSBvciBpdHMgY29udGVudHMgZXhjZXB0IHB1cnN1YW50IHRvIHRoZSBQeVNpbXBsZUdVSSBMaWNlbnNlIEFncmVlbWVudC4iDQp9"
Windows = []


# case insensitive
def i_equals(str1, str2):
    try:
        return str1.lower() == str2.lower()
    except ValueError:
        return str(str1).lower() is str(str2).lower()


def i_in(str1, str2):
    try:
        flag = False
        for _str in str1:
            if _str.lower() in str(str2.lower()):
                flag = True
        return flag
    except IndexError:
        pass
    try:
        return str1.lower() in str2.lower()
    except AttributeError:
        return str(str1).lower() in str(str2).lower()


def i_endswith(str1, str2):
    try:
        flag = False
        for _str in str2:
            if str1.lower().endswith(_str.lower()):
                flag = True
        return flag
    except IndexError:
        pass
    return str1.lower().endswith(str2.lower())


def ext_change(file_path, ext):
    try:
        return os.path.splitext(file_path)[0] + ext
    except TypeError:
        p = str(file_path).rsplit('.')[0] + ext
    return p


def make_theme_window(theme=None):
    if theme:
        sg.theme(theme)
    # -----  Layout & Window Create  -----
    layout = [[sg.T('This is your layout')], [sg.Button('Ok'), sg.Button('Change Theme'), sg.Button('Exit')]]

    return sg.Window('Pattern for changing theme', layout)


def set_user_theme():
    windowtheme = make_theme_window()

    while True:
        e, v = windowtheme.read()
        if e == sg.WINDOW_CLOSED or e == 'Exit':
            break
        if e == 'Change Theme':  # Theme button clicked, so get new theme and restart window
            e, v = sg.Window('Choose Theme', [
                    [sg.Combo(sg.theme_list(), keep_on_top=True, force_toplevel=True, readonly=True, k='-THEME LIST-'),
                     sg.OK(), sg.Cancel()]]).read(
                    close=True)
            print(e, v)
            user_theme = str('-THEME LIST-')
            print(user_theme)
            sg.user_settings_set_entry('theme', 'user_theme')
            if e == 'OK':
                windowtheme.close()
                return

    windowtheme.close()


def display_notices(notice_data, notices_file):
    popup_text = ''
    for k, v in notice_data:
        if k == "StrPopup":
            popup_text = v
    notice_window = sg.Window("Important Notices",
                              [[sg.Text(popup_text)],
                               [sg.Button('I Agree to the Terms'), sg.Button('Display License'), sg.Cancel()]
                               ])
    event, values = notice_window.read()
    if event == 'I Agree to the Terms':
        sg.Popup('Terms Accepted, this window will not show again unless you remove notices.json')
        notice_data["Accepted"] = True
        with open(notices_file, "w") as f:
            json.dump(notice_data, f)
        return
    elif event == 'Cancel':
        return


def check_notices():
    notices_file = os.path.join(os.path.dirname(__file__), "notices.json")
    notice_data = dict()
    try:
        with open(notices_file, 'r+') as f:
            notice_data = json.load(f)
            try:
                if notice_data['Accepted'] is True:
                    print(notice_data['Accepted'])
                    return
                else:
                    display_notices(notice_data, notices_file)
            except ValueError:
                pass
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No notices file found... will create one for you', keep_on_top=True,
                               background_color='red', text_color='white')
        decoded_notice = base64.standard_b64decode(notices_encode)
        with open(notices_file, 'w') as f:
            json.dumps(decoded_notice, f)
        display_notices(decoded_notice, notices_file)
        return


def locate_oar_path(starting_path):
    if os.path.isfile(starting_path):
        starting_path = os.path.dirname(starting_path)
    for dirpath in os.walk(starting_path):
        try_path = dirpath[0]
        if i_endswith(try_path, 'OpenAnimationReplacer'):
            return try_path
        elif i_in('OpenAnimationReplacer', try_path):
            while not (i_endswith(try_path, 'OpenAnimationReplacer')):
                try_path = os.path.abspath(os.path.join(try_path, '..'))
            return try_path
        elif i_in('animations', try_path):
            while not (i_endswith(try_path, 'OpenAnimationReplacer')):
                try_path = os.path.abspath(os.path.join(try_path, '..'))
            return try_path
        elif dirpath[0].endswith('DynamicAnimationReplacer'):
            sg.popup("Ok", "DAR to OAR converter not implemented yet but you really should use one...",
                keep_on_top=True)
            return os.path.abspath(dirpath[0])


def set_starting_path():
    starting_path = sg.popup_get_folder('Select mod folder')
    oar_path = locate_oar_path(starting_path)
    return oar_path


pluginname = {"Stances - Dynamic Weapon Movesets SE.esp", "StancesNG.esp"}
stance_mapping = {"High": "42518", "Mid": "42519", "Low": "4251A"}
stance_mapping2 = {"High": "806", "Mid": "805", "Low": "803"}
stance_conv = {
        "42518": "806",
        "42519": "805",
        "4251A": "803"
}

keytrace_mapping = {
        801: "forward",
        802: "left",
        803: "backward",
        804: "right",
}

kt_bfco_mapping = {
        801: "forward",
        802: "left",
        803: "backward",
        804: "right",
}


def start_bfco_rename_noregex(folder_path):
    st = time.time()
    remap = {"mco": "BFCO", "sprintpowerattack":"SprintAttackPower","sprintattack":"SprintAttack", "powerattack":"PowerAttack", "attack":"Attack", "weaponart":"PowerAttackComb" }
    for file_path in Path(folder_path).glob('**/*.hkx'):
        p = Path(file_path)
        for k in remap:
            if k in p.parent:
                new_name = p.parent.replace(k, remap[k])
                new_path = Path.joinpath(p.parent.parent, new_name, p.name)
                try:
                    os.rename(p, new_path)
                    if os.path.exists(new_name):
                        et = time.time()
                        elap = et - st
                        print(f'Execution time: ', elap, ' seconds')
                except FileExistsError:
                    pass
            elif k in p:
                new_name = p.name.replace(k, remap[k])
                new_path = Path.joinpath(p.parent, new_name)
                try:
                    os.rename(p, new_path)
                    if os.path.exists(new_name):
                        et = time.time()
                        elap = et - st
                        print(f'Execution time: ', elap, ' seconds')
                except FileExistsError:
                    pass


def start_bfco_rename(folder_path):
    st = time.time()
    regex_var = r"^(.+)(_variants_|\\)(mco)(_)(?:(sprint)?((?(5)powerattack|power))?(?:(power)*(Attack)(\d*))|(weaponart))((\\)*(\d+)?(\.hkx)?)$"

    regex2 = r"^(.+)(_variants_(BFCO|mco)_)(weaponart)$"
    subst = "\\g<2>BFCO\\g<4>\\g<6>\\g<5>\\g<8>\\g<7>\\g<9>\\g<10>\\g<12>\\g<13>\\g<14>"
    remap = {"mco": "BFCO", "sprintpowerattack":"SprintAttackPower","sprintattack":"SprintAttack", "powerattack":"PowerAttack", "attack":"Attack", "weaponart":"PowerAttackComb" }
    
    wp_art = "_variants_BFCO_weaponart"
    wp_art_sub = "\\g<2>PowerAttackComb\\g<5>"
    if not os.path.isdir(folder_path):
        folder_path = Path(folder_path).parent
    os.chdir(folder_path)
    path = Path.cwd()
    #files = (p.resolve().relative_to(Path.cwd()) for p in Path(path).glob("**/*") if p.suffix in {".json", ".txt", ".bat", ".hkx"})
    for file_path in Path(path).glob('**/*.hkx'):
        p = Path(file_path)
        xml = str(p).split('.hkx')[0] + '.xml'

        cmd = f'hkxconv convert -v xml "{p}" "{xml}"'
        cmdstr = str(cmd)
        print(cmdstr)
        print(cmd)
        subprocess.run(cmdstr)
        pp = PurePath(p)
        if p.exists():
            print(f"og name:{p}")
            

            new_name = re.sub(regex_var, subst, str(p), 0, re.IGNORECASE | re.MULTILINE)
            new_name = str(new_name)
            print(new_name)
            if 'weaponart' in new_name:
                new_name = re.sub(regex2, wp_art, new_name, 0, re.IGNORECASE)
                print(new_name)
            renamed = False
            pparent = pp.parent
            if p.is_file():
                if str(p.name).lower().startswith('mco'):
                    os.chdir(pparent)
                    new_path = PurePath.joinpath(pparent,new_name)
                    try:
                        os.rename(p, new_name)
                    except FileExistsError:
                        pass
                    if Path.exists(Path(new_name)):
                        print(f"renamed {new_name}")
                        et = time.time()
                        elap = et - st
                        print(f'Execution time: ', elap, ' seconds')
                elif '_variants' in str(pparent):
                    pparent = pparent.parent
                    os.chdir(pparent)
                    new_path = Path.joinpath(pparent,new_name).parent
                    print(f"new_path:{new_path}")
                    print(f"pparent:{pparent}")
                    try:
                        os.rename(p.parent,new_path)
                    except FileExistsError:
                        pass
                    if os.path.exists(new_name):
                        print(f"renamed {new_name}")
                        et = time.time()
                        elap = et - st
                        print(f'Execution time: ', elap, ' seconds')
                    else:
                        try:
                            Path.mkdir(new_path)
                            et = time.time()
                            elap = et - st
                            print(f'Execution time: ', elap, ' seconds')
                        except FileExistsError:
                            pass
                        try:
                            shutil.copyfile(file_path, new_name)
                            et = time.time()
                            elap = et - st
                            print(f'Execution time: ', elap, ' seconds')
                        except FileExistsError:
                            pass
                        except FileNotFoundError:
                            pass
    




def search_and_rename(root_dir):
    parent_path = os.getcwd()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            print(f"filename:{filename}")
            if i_in(filename, ('config.json', 'user.json')):
                new_dir = ''
                config_file_path = os.path.join(dirpath, filename)
                try:
                    with open(config_file_path, "r") as f:
                        pass
                except FileNotFoundError:
                    break
                with open(config_file_path, "r+") as _config_file:
                    create_backup(config_file_path)
                    config_data = json.load(_config_file)
                    _fields = ["name", "author", "description"]
                    _values = []
                    con_dict = config_data['conditions']
                    for k in con_dict:
                        print(f"dict: {con_dict}")
                        if k not in _fields:
                            _fields.append(k)
                        _values.append(k)
                        print(f"values: {_values}")

                    # try:
                    # _modCfg = ModCfg(filename, [_values])
                    #  ModCfgs.append(_modCfg)
                    #    print("its a mod not a submod")
                    #   except TypeError:
                    #    pass
                    else:
                        for field in _fields:
                            if i_in('conditions', field):
                                print(f"con: {field}")
                                _conditions = config_data['conditions']
                                submod_cons = ['']
                                newName = ''
                                for con in notableConditions:
                                    if con in _conditions:
                                        print(f"con: {con}")
                                        newName += con
                                        submod_cons.append(con, config_data[con])
                                        print(newName)
                                        print(submod_cons)

                                sg.popup_scrolled(config_data, title=f'Config File: {filename}', non_blocking=True)
                                layout2 = [[sg.Text('Enter new Name'), sg.Input(key='-newname-')]]

                                window2 = sg.Window('rename', layout2,
                                                    auto_size_text=True,
                                                    default_element_size=(10, 1),
                                                    text_justification='r',
                                                    return_keyboard_events=True,
                                                    keep_on_top=True,
                                                    grab_anywhere=True)


def create_backup(file_path):
    oar_path = locate_oar_path(file_path)
    dest_root = f"{oar_path}_backup"
    print(dest_root)
    if not os.path.exists(dest_root):
        os.makedirs(dest_root)
    os.chdir(dest_root)
    print(f"dest_root {dest_root}")
    path_from_oar = file_path.split('OpenAnimationReplacer\\')[1]
    dest = os.path.join(dest_root, path_from_oar)
    print(dest)
    print(path_from_oar)
    dest_dir = os.path.dirname(dest)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    if os.path.isdir(file_path):
        shutil.copytree(file_path, dest, dirs_exist_ok=True)
    elif os.path.isfile(file_path) and not os.path.isfile(dest):
        shutil.copyfile(file_path, dest)


def create_backup_file(file_path, dest):
    if os.path.isdir(file_path):
        for file_entry in os.scandir(file_path):
            try:
                file_name = os.path.join(file_path, file_entry.name)
                if os.path.exists:
                    create_backup(file_name)
            except FileExistsError:
                pass
    elif os.path.isfile(file_path):
        baknum = 0
        backup_path = file_path + ".bak" + str(baknum)
        while os.path.exists(backup_path):
            baknum = baknum + 1
            backup_path = file_path + ".bak" + str(baknum)
        shutil.copyfile(file_path, backup_path)


def isAttackRelated(file):
    attacks = ["mco", "attack", "skysa", "combat", "sword", "block", "r1hm", "1hm", "dw", "2hm", "2hw", "h2h", "hvy",
               "combo", "atk", "bfco"]
    for attack in attacks:
        if attack in file:
            return True
    return False


def noStance(conditions):
    _conditions = json.dumps(conditions)
    if 'Stances - Dynamic Weapon Movesets SE.esp' in _conditions:
        _conditions.replace('Stances - Dynamic Weapon Movesets SE.esp', 'StancesNG.esp')
        try:
            for k, v in conversion:
                _conditions.replace(k, v)
        except KeyError:
            return False
        return False
    for _id in formIDs:
        if _id in _conditions:
            return False
    return True


def add_stances(oar_path):
    with open("stancedistri_log.txt", "a") as log_file:
        for root, dirs, files in os.walk(oar_path):
            for file in files:
                if file.endswith(".hkx") and isAttackRelated(file):
                    try:
                        config_file_path = os.path.join(root, "config.json")
                        if os.path.exists(config_file_path):
                            create_backup(config_file_path)
                            with open(config_file_path, "r+") as _config_file:  # Open in read/write mode
                                _config_data = json.load(_config_file)
                                insert_cons(_config_data, _config_file)
                            break

                    except FileExistsError:
                        try:
                            config_file_path = os.path.join(root, "user.json")
                            if os.path.exists(config_file_path):
                                create_backup(config_file_path)
                                with open(config_file_path, "r+") as _config_file:  # Open in read/write mode
                                    _config_data = json.load(_config_file)
                                    insert_cons(_config_data, _config_file)

                        except FileExistsError:
                            print('oop')


def insert_cons(config_data, config_file, config_file_path=None):
    conditions = config_data["conditions"]
    pos = list(config_data.keys()).index('conditions')
    params = list(config_data.items())
    dice = numpy.random.choice(numpy.arange(0, 3), p=[0.34, 0.33, 0.33])
    stance_mapping = {"42518", "42519", "4251A"}
    stance_mapping2 = {"806", "805", "803"}
    stancej = (
            {
                    "condition": "OR",
                    "requiredVersion": "1.0.0.0",
                    "negated": False,
                    "Conditions": [
                            {
                                    "condition": "HasPerk",
                                    "requiredVersion": "1.0.0.0",
                                    "Perk": {
                                            "pluginName": "Stances - Dynamic Weapon Movesets SE.esp",
                                            "formID": stance_mapping[dice],
                                    }
                            },
                            {
                                    "condition": "HasMagicEffect",
                                    "requiredVersion": "1.0.0.0",
                                    "Magic Effect": {
                                            "pluginName": "StancesNG.esp",
                                            "formID": stance_mapping2[dice],
                                    }
                            }
                    ]
            }

    )
    stancec = {
            "condition": "OR",
            "requiredVersion": "1.0.0.0",
            "Conditions": stancej
    }
    try:
        if (noStance(conditions)):
            config_data["conditions"].append(stancec)
            with open("stancedistri_log.txt", "a") as log_file:
                print(f"Assigned stance {stance_mapping[dice]} to {config_file_path}", file=log_file)
        else:
            for k, v in config_data.items():
                if k in "pluginName":
                    if v == "Stances - Dynamic Weapon Movesets SE.esp":
                        config_data.update({"pluginName": "StancesNG.esp"})
                elif k in "formID":
                    if v == "42518":
                        v = "806"
                    elif v == "42519":
                        v = "805"
                    elif v == "4251A":
                        v = "803"

            with open("stancedistri_log.txt", "a") as log_file:
                print(f"Stances already in {config_file_path}", file=log_file)

        config_file.seek(0)
        json.dump(config_data, config_file, indent=2)
        config_file.truncate()
    except KeyError:
        print("oops")


def organize_files(folder_path):
    """
    Scans a folder, moves files to corresponding variant folders,
    iterating for duplicates.
    """
    for filename in os.listdir(folder_path):
        # Extract base filename without extension
        base_filename, ext = os.path.splitext(filename)

        # Skip non-hkx files
        if ext.lower() != ".hkx":
            continue

        # Construct variant folder name
        variant_folder = f"_variants_{base_filename}"

        # Construct destination path with incrementing number for duplicates
        destination_path = os.path.join(variant_folder, "1.hkx")
        i = 1
        while os.path.exists(destination_path):
            i += 1
            destination_path = os.path.join(variant_folder, f"{i}.hkx")

        # Create variant folder if it doesn't exist
        if not os.path.exists(variant_folder):
            os.makedirs(variant_folder)

        # Move the file to the destination path
        source_path = os.path.join(folder_path, filename)
        os.rename(source_path, destination_path)

    print(f"Finished organizing files in {folder_path}")


def launch_organizer(folder_path):
    directory = folder_path
    print(f"Selected mod at: {folder_path}", file=log_file)
    directories = [os.path.abspath(x[0]) for x in os.walk(directory)]
    try:
        directories.remove(os.path.abspath(directory))  # removes parent folder
    except ValueError:
        pass
    print(directories)
    for i in directories:
        if 'variants' not in i:
            try:
                os.chdir(i)
                print(f"Organizing submod folder: {i}")
                print(f"Organizing submod folder: {i}", file=log_file)
                organize_files(i)
            except FileNotFoundError:
                pass
    print(f"Done organizing: {directories}", file=log_file)
    window = Windows[len(Windows) - 1]
    window.refresh()


def search_2(treedata, sub_string):
    result = []
    parents = ['']
    while parents:
        temp = []
        for parent in parents:
            children_nodes = treedata.tree_dict[parent].children
            temp += [children_node.key for children_node in children_nodes]
            result += [children_node.key for children_node in children_nodes if sub_string in children_node.key]
        parents = temp.copy()
    return result


anim_count_data = []


def recurse_count(folder, anim_list):
    folder_ct = 0
    for file_entry in os.scandir(folder):
        file = file_entry.name
        fullname = os.path.join(folder, file)
        if os.path.isfile(fullname):
            if file.endswith('.hkx'):
                folder_ct += 1
        elif os.path.isdir(fullname):
            folder_ct += recurse_count(fullname)
    print(f"{folder}: {folder_ct}")
    return folder_ct, anim_list


def add_files_in_folder(parent, dirname, modname=None):
    anim_list = []
    files = os.listdir(dirname)
    for f in files:
        fullname = os.path.join(dirname, f)
        if i_endswith(fullname, "OpenAnimationReplacer"):
            fullname = str(fullname) + str(modname)
        if os.path.isdir(fullname):
            folder_ct = recurse_count(fullname)
            treedata.Insert(parent, fullname, f, values=[folder_ct], icon=folder_icon)
            add_files_in_folder(fullname, fullname)
        elif i_endswith(f, '.hkx'):
            anim_list.append(fullname)
            treedata.Insert(parent, fullname, f, values=[], icon=file_icon)
        elif i_endswith(f,{'.json','txt'}):

            treedata.Insert(parent, fullname, f, values=[], icon=file_icon)

def make_xml(path):
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith('.hkx'):
                if os.path.isfile(file):
                    file_name = file.split('.hkx')[0]
                    file_out = file_name + '.xml'
                    cmd = f'hkxconv convert -v xml "{file}" "{file_out}"'
                    print(cmd)
                    subprocess.run(cmd)
        for dir in dirs:
            if os.path.isdir(dir):
                subprocess.run(f'hkxconv convert -v xml "{dir}" "{dir}"')

def make_json_viewer(f_path):
    print(f_path)
    with open(f_path, "r+") as f:
        config_data = json.load(f)
        print(config_data)

        sg.popup_scrolled(config_data, title=f'Config File: {f_path}', non_blocking=True)
        layout2 = [[sg.Text('Enter new Name'), sg.Input(key='-newname-')]]

        window2 = sg.Window('ConfigView', layout2,
                            auto_size_text=True,
                            default_element_size=(10, 1),
                            text_justification='left',
                            return_keyboard_events=True,
                            keep_on_top=True,
                            grab_anywhere=True,
                            force_toplevel=True,
                            right_click_menu=[],
                            )
        
def async build_anim_cache(anim_list):
    _queue = asyncio.Queue()
    _cache = {}
    for anim in anim_list:
        if anim not in _cache and os.path.exists(anim) and not os.path.exists(ext_change(anim, '.xml')):
            _queue.put(anim)


def main(starting_path=None):
    if starting_path is None:
        starting_path = set_starting_path()
        if starting_path is None:
            starting_path = sg.user_settings_get_entry('-last filename-')
        else:
            sg.user_settings_set_entry('-last filename-', starting_path)
    
    
    anim_cache,anim_queue = build_anim_cache(anim_list)
    
    parentdir = os.path.abspath(os.path.dirname(starting_path))
    print(parentdir)
    modname = str(parentdir).split("mods\\")[1].split("\\meshes")[0]
    print(modname)
    # add_files_in_folder('', parentdir, modname)
    anim_list = add_files_in_folder('', starting_path)
    #make_xml(starting_path)
    tree1 = sg.Tree(data=treedata,
                    headings=['Anim Count', ],
                    auto_size_columns=True,
                    select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                    num_rows=20,
                    change_submits=True,
                    selected_row_colors=('black', 'lightgrey'),
                    col0_width=40,
                    key='-TREE-',
                    show_expanded=True,
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                    )
    layout1 = [[sg.Text('Choose Mod Folder'), sg.Text(key='-SELVIEW-')],
               [tree1],
               [sg.Button('View Config'), sg.Button('Open Folder'), sg.Button('Make Backups'),
                sg.Button('Add Directory'), sg.Button('Change Theme')],
               [sg.Button('Organize into Variants'), sg.Button('Rename Submods'), sg.Button('Add Stances'),
                sg.Button('Reprioritize'), sg.Button('Rename for BFCO'), sg.Button('Rename for BFCO regex'), sg.Button('Update Annotations for BFCO')],[sg.Button('Dump Annotations')],
               [sg.Button('Update Annotations Custom'), sg.Button('Convert DAR to OAR'), sg.Button('Exit'),
                sg.Sizegrip()]]

    Windows.insert(0, sg.Window('Choose Mod Folder', layout1, keep_on_top=True, resizable=True, finalize=True))
    window = Windows[0]
    selected_items = [""]
    base_mods = filter(os.path.isdir,
                       [os.path.join(starting_path, arg) for arg in os.listdir(starting_path)])
    while True:  # Event Loop
        event, values = window.read()
        print(values)
        selected_items = values['-TREE-']
        if len(selected_items) == 1:
            try:
                selected_item = selected_items[0].split("OpenAnimationReplacer\\")[1]
            except IndexError:
                selected_item = selected_items[0]
            window['-SELVIEW-'].update(f'Selected: {selected_item}')
        for item in selected_items:
            if item in anim_list and item not in anim_cache:
                put_in_cache(item)
        elif len(selected_items) > 1:
            window['-SELVIEW-'].update(f'Selected: Multiple Folders')
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Make Backup':
            for item in selected_items:
                create_backup(item)
        elif event == 'Change Theme':
            user_theme = set_user_theme()
            sg.user_settings_set_entry('-theme-', user_theme)
        elif event == 'Open Folder':
            drive = str(starting_path).split(":")[0]
            drive = str(drive) + str("://")
            os.chdir(drive)
            subprocess.run(f'explorer {selected_item}')
        elif event == 'Change Directory':
            window.close()
        elif event == 'Convert DAR to OAR':
            subprocess.run(f'dar2oar.exe convert {selected_item} --run-parallel --stdout')
        elif event == 'Organize into Variants':
            args = values['-TREE-']
            for arg in args:
                if arg in base_mods:
                    print(f"\nITEM: {arg}")
                    launch_organizer(arg)
            sg.popup("Ok", f"Done organizing folders")
            treedata.tree_dict.update()
            tree1.update()
            window.refresh()
            window.read()
        elif event == 'Rename Submods':
            args = values['-TREE-']
            for arg in args:
                print(f"\nITEM: {arg}")
                search_and_rename(arg)
        elif event == 'Add Stances':
            args = values['-TREE-']
            for arg in args:
                print(f"\nITEM: {arg}")
                add_stances(args)
        elif event == 'Update Annotations for BFCO':
            args = values['-TREE-']
            for arg in args:
                if i_in(('.hkx'), arg):
                    break
        elif event == 'Rename for BFCO':
            args = values['-TREE-']
            for arg in args:
                if os.path.exists(arg) and arg not in base_mods:
                    start_bfco_rename_noregex(arg)
        elif event == 'Rename for BFCO Regex':
            args = values['-TREE-']
            for arg in args:
                if os.path.exists(arg) and arg not in base_mods:
                    start_bfco_rename(arg)

        elif event == 'View Config':
            args = values['-TREE-']
            for arg in args:
                print(f"\nOpenConfig: {arg}")
                if i_in(('.json', '.txt'), arg):
                    f_path = os.path.abspath(arg)
                    print(f"\nOpenConfig: {f_path}")
                    make_json_viewer(f_path)

        try:
            print(event, values)
        except UnicodeEncodeError:
            print('check text encoding')


treedata = sg.TreeData()

with open("variant_log.txt", "w") as log_file:
    main()
