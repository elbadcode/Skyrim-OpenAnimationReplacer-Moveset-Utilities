import os
import json
import random
import numpy 
import shutil

formIDs = ['42519','42518', '4251A']


def create_backup(file_path):
    baknum = 0
    backup_path = file_path + ".bak" + str(baknum)
    while os.path.exists(backup_path):
        baknum = baknum+1
        backup_path = file_path + ".bak" + str(baknum)
    shutil.copyfile(file_path, backup_path)


def isAttackRelated(file):
    attacks = ["mco","attack","skysa","combat","sword","block", "r1hm", "h2h", "hvy","combo","atk"]
    for attack in attacks:
        if attack in file:
            return True
    return False

def noStance(conditions):
    _conditions = json.dumps(conditions)
    if 'Stances'in _conditions:
        return False
    for _id in formIDs:
        if _id in _conditions:
            return False
    return True





def modify_config_files():
    oar_path = os.path.join(os.path.dirname(__file__), "Meshes", "Actors", "Character", "Animations", "OpenAnimationReplacer")
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



def insert_cons(config_data, config_file):
    conditions = config_data["conditions"]
    pos = list(config_data.keys()).index('conditions')
    params = list(config_data.items())
    additions = [
    ("interruptible", True),
    ("replaceOnLoop", False),
    ("shareRandomResults", True),
    ("keepRandomResultsOnLoop", False),
    ("ignoreDontConvertAnnotationsToTriggersFlag", True)]
    for param in additions:
        if param not in params:
            params.insert(pos,param)
            pos = list(config_data.keys()).index('conditions')
        else:
            params.update(pos,param)
    config_data = dict(params)
    random_condition = {
        "condition": "Random",
        "requiredVersion": "1.0.0.0",
        "Random value": {
            "min": 0.0,
            "max": 1.0
        },
        "Comparison": "<",
        "Numeric value": {
            "value": 0.7
        }
    }

    
    dice = numpy.random.choice(numpy.arange(0,3), p=[0.34, 0.33, 0.33])
    _formID = formIDs[dice]
    stance = {
            "condition": "HasPerk",
            "requiredVersion": "1.0.0.0",
            "Perk": {
              "pluginName": "Stances - Dynamic Weapon Movesets SE.esp",
              "formID": _formID
                }
            }

    stance_random = {
              "condition": "OR",
              "requiredVersion": "1.0.0.0",
              "Conditions": [ stance, random_condition]
              }                                            
    try:           
        if (noStance(conditions)):
            config_data["conditions"].append(stance_random)
            print(f"Assigned stance {_formID} to {config_file_path}",file=log_file)
        else:
            print(f"Stances already in {config_file_path}",file=log_file)

        config_file.seek(0)  
        json.dump(config_data, config_file, indent=2)
        config_file.truncate() 
    except KeyError:
        print("oops")

if __name__ == "__main__":
    modify_config_files()
