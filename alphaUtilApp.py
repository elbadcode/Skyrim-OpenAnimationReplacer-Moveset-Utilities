#!/usr/bin/env python
import os
import shutil
from collections import namedtuple
import PySimpleGUI as sg
import json
import numpy
import subprocess
import ctypes
import re

sg.theme('light brown 8')

"""
    Copyright 2023 PySimpleSoft, Inc. and/or its licensors. All rights reserved.

    Redistribution, modification, or any other use of PySimpleGUI or any portion thereof is subject to the terms of the PySimpleGUI License Agreement available at https://eula.pysimplegui.com.

    You may not redistribute, modify or otherwise use PySimpleGUI or its contents except pursuant to the PySimpleGUI License Agreement.
"""

# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

Windows = []


def set_starting_path():
    starting_path = sg.popup_get_folder('Select mod folder')
    print
    for dirpath in os.walk(starting_path):
        try_path = dirpath[0]
        print(try_path)
        if try_path.endswith('OpenAnimationReplacer'):
            starting_path = try_path
            break
        elif 'OpenAnimationReplacer' in try_path:
            while not (try_path.endswith('OpenAnimationReplacer')):
                try_path = os.path.abspath(os.path.join(try_path, '..'))
            starting_path = try_path
        elif dirpath[0].endswith('DynamicAnimationReplacer'):
            sg.popup("Ok", "DAR to OAR converter not implemented yet but you really should use one...",
                     keep_on_top=True)
            starting_path = os.path.abspath(dirpath[0])
    return starting_path


formIDs = ['42519', '42518', '4251A']
pluginname = {"Stances - Dynamic Weapon Movesets SE.esp", "StancesNG.esp"}
stance_mapping = {"High": "42518", "Mid": "42519", "Low": "4251A"}
stance_mapping2 = {"High": "806", "Mid": "805", "Low": "803"}
conversion = {
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

# smaller than a dict and better suited for holding immutable data. Must be instantiated with name author description
# defaults=None allows only one optional/nullable field, in this case conditionpresets
ModCfg = namedtuple("Mod", "name author description ConditionPresets", defaults=None)

SubmodCfg = namedtuple("Submod", "name priority optionals conditions", defaults=None)

show_Expanded = False

ModCfgs = []
SubmodCfgs = []




def create_backup(file_path):
    baknum = 0
    backup_path = file_path + ".bak" + str(baknum)
    while os.path.exists(backup_path):
        baknum = baknum + 1
        backup_path = file_path + ".bak" + str(baknum)
    shutil.copyfile(file_path, backup_path)



def convert_stances(oar_path):
    with open("stancedistri_log.txt", "a") as log_file:
        for root, dirs, files in os.walk(oar_path):
            for file in files:

                config_file_path = os.path.join(root, "config.json")
                if os.path.exists(config_file_path):
                    create_backup(config_file_path)
                    with open(config_file_path, "r+") as config_file:  # Open in read/write mode
                        _config_data = json.load(config_file)

                        text = """{
                            "condition": "HasPerk",
                            "requiredVersion": "1.0.0.0",
                            "Perk": {
                                "pluginName": "Stances - Dynamic Weapon Movesets SE.esp",
                                "formID": "                                   "
                            }
                        }"""

                        {
                                "name": "Low Left",
                                "priority": 2003786449,
                                "interruptible": false,
                                "shareRandomResults": true,
                                "keepRandomResultsOnLoop": false,
                                "conditions": [
                                        {
                                                "condition": "IsActorBase",
                                                "requiredVersion": "1.0.0.0",
                                                "Actor base": {
                                                        "pluginName": "Skyrim.esm",
                                                        "formID": "7"
                                                }
                                        },
                                        {
                                                "condition": "Random",
                                                "requiredVersion": "1.0.0.0",
                                                "Random value": {
                                                        "min": 0.0,
                                                        "max": 1.0
                                                },
                                                "Comparison": "<",
                                                "Numeric value": {
                                                        "value": 0.89
                                                }
                                        },
                                        {
                                                "condition": "IsInAir",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true
                                        },
                                        {
                                                "condition": "OR",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": false,
                                                "Conditions": [
                                                        {
                                                                "condition": "HasPerk",
                                                                "requiredVersion": "1.0.0.0",
                                                                "Perk": {
                                                                        "pluginName": "Stances - Dynamic Weapon Movesets SE.esp",
                                                                        "formID": "4251A"
                                                                }
                                                        },
                                                        {
                                                                "condition": "HasMagicEffect",
                                                                "requiredVersion": "1.0.0.0",
                                                                "Magic effect": {
                                                                        "pluginName": "StancesNG.esp",
                                                                        "formID": "803"
                                                                }
                                                        }
                                                ]
                                        },
                                        {
                                                "condition": "HasMagicEffect",
                                                "requiredVersion": "1.0.0.0",
                                                "Magic effect": {
                                                        "pluginName": "Keytrace.esp",
                                                        "formID": "802"
                                                },
                                                "Active effects only": false
                                        },
                                        {
                                                "condition": "AND",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": false,
                                                "Conditions": [
                                                        {
                                                                "condition": "IsEquippedType",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Type": {
                                                                        "value": 3.0
                                                                }
                                                        },
                                                        {
                                                                "condition": "IsEquippedHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Keyword": {
                                                                        "editorID": "WeapTypeAxe"
                                                                }
                                                        }
                                                ]
                                        },
                                        {
                                                "condition": "AND",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": false,
                                                "Conditions": [
                                                        {
                                                                "condition": "IsEquippedType",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Type": {
                                                                        "value": 4.0
                                                                }
                                                        },
                                                        {
                                                                "condition": "IsEquippedHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Keyword": {
                                                                        "editorID": "WeapTypeMace"
                                                                }
                                                        }
                                                ]
                                        },
                                        {
                                                "condition": "AND",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": false,
                                                "Conditions": [
                                                        {
                                                                "Keyword": {
                                                                        "form": {
                                                                                "pluginName": "NewArmoury.esp",
                                                                                "formID": "19aab4"
                                                                        }
                                                                },
                                                                "Left hand": false,
                                                                "condition": "IsEquippedRightHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true
                                                        },
                                                        {
                                                                "Keyword": {
                                                                        "form": {
                                                                                "pluginName": "NewArmoury.esp",
                                                                                "formID": "19aab4"
                                                                        }
                                                                },
                                                                "Left hand": true,
                                                                "condition": "IsEquippedLeftHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true
                                                        }
                                                ]
                                        },
                                        {
                                                "condition": "IsEquippedType",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Type": {
                                                        "value": 2
                                                },
                                                "Left hand": false
                                        },
                                        {
                                                "condition": "IsEquippedHasKeyword",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Keyword": {
                                                        "PluginName": "kcf.esm",
                                                        "editorID": "WeapTypeGreatsword"
                                                }
                                        },
                                        {
                                                "condition": "IsEquippedHasKeyword",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Keyword": {
                                                        "PluginName": "kcf.esm",
                                                        "editorID": "WeapTypeKatana"
                                                }
                                        },
                                        {
                                                "condition": "IsEquippedHasKeyword",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Keyword": {
                                                        "editorID": "WeaptypeQuarterstaff",
                                                        "pluginName": "kcf.esm"
                                                }
                                        },
                                        {
                                                "condition": "IsEquippedHasKeyword",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Keyword": {
                                                        "PluginName": "kcf.esm",
                                                        "editorID": "WeapTypeRapier"
                                                }
                                        },
                                        {
                                                "condition": "IsEquippedHasKeyword",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Keyword": {
                                                        "pluginName": "kcf.esm",
                                                        "editorID": "WeapTypeScythe"
                                                }
                                        },
                                        {
                                                "condition": "IsEquippedType",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Type": {
                                                        "value": 11.0
                                                }
                                        },
                                        {
                                                "condition": "AND",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": false,
                                                "Conditions": [
                                                        {
                                                                "condition": "IsEquippedHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Keyword": {
                                                                        "editorID": "WeaptypePike"
                                                                }
                                                        },
                                                        {
                                                                "condition": "IsEquippedHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Keyword": {
                                                                        "editorID": "WeaptypeSpear"
                                                                }
                                                        },
                                                        {
                                                                "condition": "IsEquipped",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Form": {
                                                                        "pluginName": "Sekiro - Ashina General.esp",
                                                                        "formID": "1DAD"
                                                                }
                                                        },
                                                        {
                                                                "condition": "IsEquippedHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Keyword": {
                                                                        "form": {
                                                                                "pluginName": "SkyrimSpearMechanic.esp",
                                                                                "formID": "D62"
                                                                        }
                                                                }
                                                        },
                                                        {
                                                                "condition": "IsEquippedHasKeyword",
                                                                "requiredVersion": "1.0.0.0",
                                                                "negated": true,
                                                                "Keyword": {
                                                                        "form": {
                                                                                "pluginName": "Spear of Skyrim.esp",
                                                                                "formID": "A88"
                                                                        }
                                                                }
                                                        }
                                                ]
                                        },
                                        {
                                                "condition": "IsEquippedHasKeyword",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Keyword": {
                                                        "pluginName": "kcf.esm",
                                                        "editorID": "OneHandSword"
                                                }
                                        },
                                        {
                                                "condition": "IsEquippedType",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": true,
                                                "Type": {
                                                        "value": 0
                                                },
                                                "Left hand": false
                                        },
                                        {
                                                "condition": "IsEquippedHasKeyword",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": false,
                                                "Keyword": {
                                                        "editorID": "WeapTypeWhip"
                                                }
                                        }
                                ]
                        }

                        replacement = r"""{
                          "condition": "OR",
                          "requiredVersion": "\1",
                          "Conditions": [
                            {
                              "condition": "HasPerk",
                              "requiredVersion": "\1",
                              "Perk": {
                                "pluginName": "\2",
                                "formID": "\3"
                              }
                            },
                            {
                              "condition": "HasSpell ",
                              "requiredVersion": "\1",
                              "Spell": {
                                "pluginName": "StancesNG.esp",
                                "formID": "805"
                              },
                              "Active effects only": false
                            }
                          ]
                        }"""

                        result = re.sub(pattern, replacement, text, flags=re.VERBOSE)

        with open("stancedistri_log.txt", "a") as log_file:
            print(f"Stances already in {config_file_path}", file=log_file)

        config_file.seek(0)
        json.dump(config_data, config_file, indent=2)
        config_file.truncate()



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

        try:
            if int(base_filename):
                continue
            continue
        # This must look insane if you don't know the difference between pass and continue in python
        except ValueError:
            pass

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


def launch_organizer(folder_path):
    print(folder_path)
    directory = folder_path
    print(f"Selected mod at: {folder_path}", file=log_file)
    directories = [os.path.abspath(x[0]) for x in os.walk(directory)]
    try:
        directories.remove(os.path.abspath(directory))  #
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


# Execute the command.  Will not see the output from the command until it completes.

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


def recurse_count(folder):
    folder_ct = 0
    for file in os.listdir(folder):
        fullname = os.path.join(folder, file)
        if os.path.isfile(fullname):
            if file.endswith('.hkx'):
                folder_ct += 1
        elif os.path.isdir(fullname):
            folder_ct += recurse_count(fullname)
    print(f"{folder}: {folder_ct}")
    return folder_ct


def add_files_in_folder(parent, dirname):
    files = os.listdir(dirname)
    for f in files:
        fullname = os.path.join(dirname, f)
        if os.path.isdir(fullname):  # if it's a folder, add folder and recurse
            folder_ct = recurse_count(fullname)
            treedata.Insert(parent, fullname, f, values=[folder_ct], icon=folder_icon)
            add_files_in_folder(fullname, fullname)
        elif f.endswith(('.hkx', '.json')):
            treedata.Insert(parent, fullname, f, values=[], icon=file_icon)


def main(starting_path=None):
    if starting_path is None:
        starting_path = set_starting_path()
    add_files_in_folder('', starting_path)
    layout1 = [[sg.Text('Choose Mod Folder')],
               [sg.Tree(data=treedata,
                        headings=['Anim Count', ],
                        auto_size_columns=True,
                        select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                        num_rows=20,
                        col0_width=40,
                        key='-TREE-',
                        show_expanded=True,
                        enable_events=True,
                        expand_x=True,
                        expand_y=True,
                        )],
               [sg.Button('Organize into Variants'), sg.Button('Rename Submods'), sg.Button('Add Stances')],
               [sg.Button('Open Config.json'), sg.Button('Reprioritize'), sg.Button('Change Directory'),
                sg.Button('Exit'), sg.Sizegrip()]]

    Windows.insert(0, sg.Window('Choose Mod Folder', layout1, keep_on_top=False, resizable=True, finalize=True))
    window = Windows[0]
    selected_items = [""]
    base_mods = filter(os.path.isdir,
                       [os.path.join(starting_path, arg) for arg in os.listdir(starting_path)])
    while True:  # Event Loop
        event, values = window.read()
        print(values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Change Directory':
            sg.popup("Ok", "It will append the new directory. Close and restart to actually change")
            window.close()
            Windows.append(Windows.pop(0))
            main()
        elif event == 'Organize into Variants':
            args = values['-TREE-']
            for arg in args:
                if arg in base_mods:
                    print(f"\nITEM: {arg}")
                    launch_organizer(arg)
            sg.popup("Ok", f"Done organizing folders")
            treedata.tree_dict.update()
            window.refresh()
            window.read()
        elif event == 'Rename Submods':
            sg.popup("Ok", "Coming soon")
        elif event == 'Add Stances':
            convert_stances(starting_path)
        elif event == 'Open Config.json':
            args = values['-TREE-']
            for arg in args:
                if arg in base_mods:
                    print(f"\nITEM: {arg}")
                    if 'config.json' in arg:
                        shell32 = ctypes.windll.shell32

                        filepath = os.path.join(os.getcwd(), arg)
                        shell32.ShellExecuteA(0, "open", filepath, 0, 0, 5)

        try:
            print(event, values)
        except UnicodeEncodeError:
            print('check text encoding')


treedata = sg.TreeData()
with open("variant_log.txt", "w") as log_file:
    main()