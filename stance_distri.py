import os
import json
import random
import numpy 
import shutil

formIDs = ['42519','42518', '4251A']
pluginname = {"Stances - Dynamic Weapon Movesets SE.esp", "StancesNG.esp"}
stance_mapping = {"High": "42518", "Mid": "42519", "Low": "4251A"}
stance_mapping2 = {"High": "806", "Mid": "805", "Low": "803"}
conversion = {
        "42518": "806",
        "42519": "805",
        "4251A": "803"
}

def create_backup(file_path):
    baknum = 0
    backup_path = file_path + ".bak" + str(baknum)
    while os.path.exists(backup_path):
        baknum = baknum+1
        backup_path = file_path + ".bak" + str(baknum)
    shutil.copyfile(file_path, backup_path)


def isAttackRelated(file):
    attacks = ["mco","attack","skysa","combat","sword","block", "r1hm","1hm", "2hw", "h2h", "hvy","combo","atk"]
    for attack in attacks:
        if attack in file:
            return True
    return False

def noStance(conditions):
    _conditions = json.dumps(conditions)
    if 'Stances - Dynamic Weapon Movesets SE.esp'in _conditions:
        _conditions.replace('Stances - Dynamic Weapon Movesets SE.esp', 'StancesNG.esp')

        try:
            for k,v in conversion:
                _conditions.replace( k, v)
        except KeyError:
            return False
        return False
    for _id in formIDs:
        if _id in _conditions:
            return False
    return True





def add_stances():
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

def insert_cons(config_data, config_file, config_file_path=None, conversion=None):
    conditions = config_data["conditions"]
    pos = list(config_data.keys()).index('conditions')
    params = list(config_data.items())
    dice = numpy.random.choice(numpy.arange(0,3), p=[0.34, 0.33, 0.33])
    _formID = formIDs[dice]
    stance = (
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
                                            "formID": stance_mapping[stance],
                                    }
                            },
                            {
                                    "condition": "HasMagicEffect",
                                    "requiredVersion": "1.0.0.0",
                                    "Magic Effect": {
                                            "pluginName": "StancesNG.esp",
                                            "formID": stance_mapping2[stance],
                                    }
                            }
                    ]
            }

    )

    stance_random = {
            "condition": "OR",
            "requiredVersion": "1.0.0.0",
            "Conditions": [ stance, random_condition]
    }
    try:
        if (noStance(conditions)):
            config_data["conditions"].append(stance_random)
            with open("stancedistri_log.txt", "a") as log_file:
                print(f"Assigned stance {_formID} to {config_file_path}",file=log_file)
        else:
            for k,v in config_data.items():
                if k in ["pluginName"]:
                    if v == "Stances - Dynamic Weapon Movesets SE.esp":
                        config_data.update({"pluginName": "StancesNG.esp"})
                elif k in ["formID"]:
                    if v == "42518":
                        v = "806"
                elif v == "42519":
                    v = "805"
                elif v == "4251A":
                    v = "803"


            with open("stancedistri_log.txt", "a") as log_file:
                print(f"Stances already in {config_file_path}",file=log_file)

        config_file.seek(0)
        json.dump(config_data, config_file, indent=2)
        config_file.truncate()
    except KeyError:
        print("oops")

def insert_cons(config_data, config_file, config_file_path=None, conversion=None):
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
            "value": 0.8
        }
    }


    dice = numpy.random.choice(numpy.arange(0,3), p=[0.34, 0.33, 0.33])
    _formID = formIDs[dice]
    stance = (
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
                                                "formID": stance_mapping[stance],
                                        }
                                },
                                {
                                        "condition": "HasMagicEffect",
                                        "requiredVersion": "1.0.0.0",
                                        "Magic Effect": {
                                                "pluginName": "StancesNG.esp",
                                                "formID": stance_mapping2[stance],
                                        }
                                }
                        ]
                }

        )

    stance_random = {
              "condition": "OR",
              "requiredVersion": "1.0.0.0",
              "Conditions": [ stance, random_condition]
              }                                            
    try:           
        if (noStance(conditions)):
            config_data["conditions"].append(stance_random)
            with open("stancedistri_log.txt", "a") as log_file:
                print(f"Assigned stance {_formID} to {config_file_path}",file=log_file)
        else:
            for k,v in config_data.items():
                if k in ["pluginName"]:
                    if v == "Stances - Dynamic Weapon Movesets SE.esp":
                        config_data.update({"pluginName": "StancesNG.esp"})
                elif k in ["formID"]:
                    if v == "42518":
                        v = "806"
                elif v == "42519":
                    v = "805"
                elif v == "4251A":
                    v = "803"


            with open("stancedistri_log.txt", "a") as log_file:
                print(f"Stances already in {config_file_path}",file=log_file)

        config_file.seek(0)  
        json.dump(config_data, config_file, indent=2)
        config_file.truncate() 
    except KeyError:
        print("oops")

if __name__ == "__main__":
    add_stances()
