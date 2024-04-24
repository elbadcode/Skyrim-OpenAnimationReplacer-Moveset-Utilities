import json
import os
import random
import shutil
from typing import Dict

basepath = os.getcwd()
priorities = []
presetConditions = []
framework_paths=[]


def make_variant_dirs(submodPath):
    for _variant in variant_map:
        print(_variant)
        _variant_name = '_variants_' + _variant
        _variant_name = _variant_name.lower()
        if (_variant_name.endswith('attack')):
            mcocount = 0
            oldname = _variant_name
            while mcocount < 7:
                mcocount += 1
                _variant_name = oldname + (str)(mcocount)
                _variant_path = os.path.join(submodPath, _variant_name)
                os.makedirs(_variant_path, exist_ok=True)
                variant_paths.append(_variant_path)
        _variant_path = os.path.join(submodPath, _variant_name)
        os.makedirs(_variant_path, exist_ok=True)
        variant_paths.append(_variant_path)


def process_folders(directory):

    for root, dirs, files in os.walk(directory, topdown=True):
        matching_keys = []
        for file in files:
            file_path = os.path.join(root, file).lower()
            animations_found = False
            animation_list = []
            if file.endswith(".hkx"):
                animations_found = True
                animation_list.append(file_path)

            if animations_found:
                for key in file_path.split('\\'):
                    if key in grips or key in stances or key in keytraces:
                        matching_keys.append(key)


                for config_file in file_path:
                    config_file_path = os.path.join(file_path, config_file)
                    if config_file.endswith("config.json"):
                        data = json.loads(config_file_path)




def generate_preset(grip=None, stance=None, keytrace=None, weapon=None):
    generated_priority = int(1900000000)
    template = {
            "name": "",
            "priority": generated_priority,
            "interruptible": False,
            "shareRandomResults": False,
            "keepRandomResultsOnLoop": False,
            "conditions": [{
                    "condition": "IsActorBase",
                    "requiredVersion": "1.0.0.0",
                    "Actor base": {
                            "pluginName": "Skyrim.esm",
                            "formID": "7"
                    }
            },
            ]
    }

    if grip:
        generated_priority = int(generated_priority) + int(2000000)
        if grip == "1H":
            generated_priority += 2000
            template["conditions"].append(grip_mapping_1H)
        if grip == "2H":
            generated_priority += 3000
            template["conditions"].append(grip_mapping_2H)
        if grip == "DW":
            generated_priority += 66000
            template["conditions"].append(grip_mapping_DW)

    if stance:
        generated_priority = int(generated_priority) + int(200000)
        template["conditions"].append(
                {
                        "condition": "HasPerk",
                        "requiredVersion": "1.0.0.0",
                        "Perk": {
                                "pluginName": "Stances - Dynamic Weapon Movesets SE.esp",
                                "formID": stance_mapping[stance],
                        }
                }
        )
    if keytrace:
        generated_priority = int(generated_priority) + int(20000)
        generated_priority = int(generated_priority) + int(keytrace_mapping[keytrace])
        template["conditions"].append(
                {
                        "condition": "OR",
                        "requiredVersion": "1.0.0.0",
                        "Conditions": [
                                {
                                        "condition": "HasMagicEffect",
                                        "requiredVersion": "1.0.0.0",
                                        "Magic effect": {
                                                "pluginName": "Keytrace.esp",
                                                "formID": keytrace_mapping[keytrace],
                                        },
                                        "Active effects only": False,
                                },
                                {
                                        "condition": "IsMovementDirection",
                                        "requiredVersion": "1.0.0.0",
                                        "Direction": {
                                                "value": keytrace_mapping2[keytrace]
                                        }
                                }
                        ]
                }
        )
    if weapon:
        generated_priority = generated_priority + int(12000000)
        generated_priority = generated_priority + weapon_priorities[weapon]
        notweapons = []
        for _weapon in weapons:
            if _weapon == weapon:
                pass
            elif _weapon == 'Greatsword' and (weapon == 'Spear' or weapon == 'Sword' or weapon == 'Katana'):
                pass
            elif _weapon == 'Dagger' and weapon == 'Claw':
                pass
            else:
                notweapons.append(_weapon)
        for notweapon in notweapons:
                template["conditions"].append(weapon_mapping3[notweapon])
        template["conditions"].append(weapon_mapping2[weapon])

    template["conditions"].append(
            {
                    "condition": "Random",
                    "requiredVersion": "1.0.0.0",
                    "Random value": {
                            "min": 0.0,
                            "max": 1.0
                    },
                    "Comparison": "<",
                    "Numeric value": {
                            "value": 0.86
                    }
            }
    )
    template["name"] = " ".join(filter(None, [grip, stance, keytrace]))
    while generated_priority in priorities:
        generated_priority += 1
    priorities.append(generated_priority)
    template["priority"] = generated_priority
    with open("presets.txt", "a") as log_file:
        print(f"New: {template}", file=log_file)
    return template


grip_mapping = {"2H": "gripMode < 2", "1H": "gripMode != 1", "DW": "gripMode == 3"}
grip_mapping2 = {"2H": True, "1H": False, "DW": True}
stance_mapping = {"High": "42518", "Mid": "42519", "Low": "4251A"}
keytrace_mapping = {"Forward": "801", "Left": "802", "Right": "804", "Backward": "803"}
keytrace_mapping2 = {"Forward": 1, "Left": 4, "Right": 2, "Backward": 3}

grip_mapping_1H= {
        "condition": "OR",
        "requiredVersion": "1.0.0.0",
        "negated": False,
        "Conditions": [
                {
                        "condition": "MathStatement",
                        "requiredPlugin": "OpenAnimationReplacer-Math",
                        "requiredVersion": "1.0.0.0",
                        "Math Statement": {
                                "expression": "gripMode == 2",
                                "variables": {
                                        "gripmode": {
                                                "graphVariable": "iDynamicGripMode",
                                                "graphVariableType": "Int",
                                        }
                                },
                        }
                },
                {
                        "condition": "AND",
                        "requiredVersion": "1.0.0.0",
                        "negated": False,
                        "Conditions": [
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 3",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                                {
                                        "condition": "IsEquippedType",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Type": {
                                                "value": 5
                                        },
                                        "Left Hand": True,
                                },
                                {
                                        "condition": "IsEquippedType",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Type": {
                                                "value": 1
                                        },
                                        "Left Hand": True,
                                },
                                {
                                        "condition": "IsEquippedType",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Type": {
                                                "value": 2
                                        },
                                        "Left Hand": True,
                                },
                                {
                                        "condition": "IsEquippedType",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Type": {
                                                "value": 3
                                        },
                                        "Left Hand": True,
                                },
                                {
                                        "condition": "IsEquippedType",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Type": {
                                                "value": 4
                                        },
                                        "Left Hand": True,
                                },
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 1",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                        ]
                }

        ]
}
grip_mapping_2H= {
        "condition": "OR",
        "requiredVersion": "1.0.0.0",
        "negated": False,
        "Conditions": [
                {
                        "condition": "MathStatement",
                        "requiredPlugin": "OpenAnimationReplacer-Math",
                        "requiredVersion": "1.0.0.0",
                        "Math Statement": {
                                "expression": "gripMode == 1",
                                "variables": {
                                        "gripmode": {
                                                "graphVariable": "iDynamicGripMode",
                                                "graphVariableType": "Int",
                                        }
                                },
                        }
                },
                {
                        "condition": "AND",
                        "requiredVersion": "1.0.0.0",
                        "negated": False,
                        "Conditions": [
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 3",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 2",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                        ]
                },
                {
                        "condition": "AND",
                        "requiredVersion": "1.0.0.0",
                        "negated": False,
                        "Conditions": [
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 3",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 2",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                                {
                                        "condition": "IsEquippedType",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": False,
                                        "Type": {
                                                "value": 5
                                        },
                                        "Left Hand": False,
                                },
                        ]
                }

        ]
}

grip_mapping_DW= {
        "condition": "OR",
        "requiredVersion": "1.0.0.0",
        "negated": False,
        "Conditions": [
                {
                        "condition": "MathStatement",
                        "requiredPlugin": "OpenAnimationReplacer-Math",
                        "requiredVersion": "1.0.0.0",
                        "Math Statement": {
                                "expression": "gripMode == 3",
                                "variables": {
                                        "gripmode": {
                                                "graphVariable": "iDynamicGripMode",
                                                "graphVariableType": "Int",
                                        }
                                },
                        }
                },
                {
                        "condition": "AND",
                        "requiredVersion": "1.0.0.0",
                        "negated": False,
                        "Conditions": [
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 1",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                                {
                                        "condition": "MathStatement",
                                        "requiredPlugin": "OpenAnimationReplacer-Math",
                                        "requiredVersion": "1.0.0.0",
                                        "negated": True,
                                        "Math Statement": {
                                                "expression": "gripMode == 2",
                                                "variables": {
                                                        "gripmode": {
                                                                "graphVariable": "iDynamicGripMode",
                                                                "graphVariableType": "Int",
                                                        }
                                                },
                                        }
                                },
                        ]
                }

        ]
}



weapon_mapping = {
    "Axe": "Axe.json",
    "Blunt": "Blunt.json",
    "Claw": "Claw.json",
    "Dagger": "Dagger.json",
    "Greatsword": "Greatsword.json",
    "Katana": "Katana.json",
    "Quarterstaff": "Quarterstaff.json",
    "Rapier": "Rapier.json",
    "Scythe": "Scythe.json",
    "Shield": "Shield.json",
    "Spear": "Spear.json",
    "Sword": "Sword.json",
    "Unarmed": "Unarmed.json",
    "Whip": "Whip.json",
}

variant_map = [
    "mco_attack",
    "mco_powerattack",
    "mco_sprintattack",
    "mco_sprintpowerattack",
    "1hm_idle",
    "2hm_idle",
    "2hw_idle",
    "dw1hm1hmidle",
    "mt_sprintforwardsword",
    "mco_weaponart"
]

variant_paths = ['']

allkeys = grip_mapping
allkeys = allkeys | stance_mapping
allkeys = allkeys | keytrace_mapping
allkeys = allkeys | weapon_mapping

grips = ["2H", "1H", "DW"]
stances = ["High", "Low", "Mid"]
keytraces = ["Forward", "Left", "Right", "Backward"]
weapons = [
    "Axe",
    "Blunt",
    "Claw",
    "Dagger",
    "Greatsword",
    "Katana",
    "Quarterstaff",
    "Rapier",
    "Scythe",
    "Shield",
    "Spear",
    "Sword",
    "Unarmed",
    "Whip",
]

weapon_priorities = {
        "Axe": 3,
        "Blunt": 4,
        "Claw": 2431333,
        "Dagger": 1134,
        "Greatsword": 1337,
        "Katana": 112,
        "Quarterstaff": 8343,
        "Rapier": 1866654,
        "Scythe": 4432424,
        "Shield": 15,
        "Spear": 12123332,
        "Sword": 118877,
        "Unarmed": 4,
        "Whip": 7121123,
}

weapon_mapping2 = {
        "Axe": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 3.0
                                }
                        },
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 6.0
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "editorID": "WeapTypeAxe"
                                }
                        }
                ]
        },
        "Blunt": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 4.0
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "editorID": "WeapTypeMace"
                                }
                        }
                ]
        },
        "Claw": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "Keyword": {
                                        "form": {
                                                "pluginName": "NewArmoury.esp",
                                                "formID": "19aab4"
                                        }
                                },
                                "Left hand": False,
                                "condition": "IsEquippedRightHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False
                        },
                        {
                                "Keyword": {
                                        "form": {
                                                "pluginName": "NewArmoury.esp",
                                                "formID": "19aab4"
                                        }
                                },
                                "Left hand": True,
                                "condition": "IsEquippedLeftHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False
                        }
                ]
        },
        "Dagger": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Type": {
                                        "value": 2
                                },
                                "Left hand": True
                        },
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Type": {
                                        "value": 2
                                },
                                "Left hand": False
                        }
                ]
        },
        "Greatsword": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "AND",
                                "requiredVersion": "1.0.0.0",
                                "Conditions": [
                                        {
                                                "condition": "IsEquippedType",
                                                "requiredVersion": "1.0.0.0",
                                                "Type": {
                                                        "value": 1
                                                }
                                        },
                                        {
                                                "condition": "MathStatement",
                                                "requiredPlugin": "OpenAnimationReplacer-Math",
                                                "requiredVersion": "1.0.0.0",
                                                "Math Statement": {
                                                        "expression": "gripMode == 1",
                                                        "variables": {
                                                                "gripmode": {
                                                                        "graphVariable": "iDynamicGripMode",
                                                                        "graphVariableType": "Int"
                                                                }
                                                        }
                                                }
                                        }
                                ]
                        },
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 5
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "TwoHandSword"
                                }
                        }
                ]
        },
        "Katana": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Keyword": {
                        "PluginName": "kcf.esm",
                        "editorID": "WeapTypeKatana"
                }
        },
        "Quarterstaff": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Keyword": {
                        "editorID": "WeaptypeQuarterstaff",
                        "pluginName": "kcf.esm"
                }
        },
        "Rapier": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Keyword": {
                        "PluginName": "kcf.esm",
                        "editorID": "WeapTypeRapier"
                }
        },
        "Scythe": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 6.0
                                },
                                "Left hand": False
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "WeapTypeScythe"
                                }
                        }
                ]
        },
        "Spear": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "editorID": "WeaptypePike"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "editorID": "WeaptypeSpear"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "form": {
                                                "pluginName": "NewArmoury.esp",
                                                "formID": "E457E"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquipped",
                                "requiredVersion": "1.0.0.0",
                                "Form": {
                                        "pluginName": "Sekiro - Ashina General.esp",
                                        "formID": "1DAD"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "form": {
                                                "pluginName": "Smooth Weapon.esm",
                                                "formID": "801"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
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
                                "Keyword": {
                                        "form": {
                                                "pluginName": "Smooth Weapon.esm",
                                                "formID": "80A"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "form": {
                                                "pluginName": "Spear of Skyrim.esp",
                                                "formID": "A88"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "form": {
                                                "pluginName": "kcf.esm",
                                                "formID": "803"
                                        }
                                }
                        }
                ]
        },
        "Sword": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 1
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "OneHandSword"
                                }
                        },
                        {
                                "condition": "AND",
                                "requiredVersion": "1.0.0.0",
                                "Conditions": [
                                        {
                                                "condition": "IsEquippedType",
                                                "requiredVersion": "1.0.0.0",
                                                "Type": {
                                                        "value": 5
                                                }
                                        },
                                        {
                                                "condition": "MathStatement",
                                                "requiredPlugin": "OpenAnimationReplacer-Math",
                                                "requiredVersion": "1.0.0.0",
                                                "Math Statement": {
                                                        "expression": "gripMode == 2",
                                                        "variables": {
                                                                "gripmode": {
                                                                        "graphVariable": "iDynamicGripMode",
                                                                        "graphVariableType": "Int"
                                                                }
                                                        }
                                                }
                                        }
                                ]
                        },
                ]
        },
        "Unarmed": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 0
                                },
                                "Left hand": True
                        },
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 0
                                },
                                "Left hand": False
                        }
                ]
        },
        "Shield": {
                "condition": "IsEquippedType",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Type": {
                        "value": 10.0
                }
        },
        "Whip": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Keyword": {
                        "editorID": "WeapTypeWhip"
                }
        }
}

weapon_mapping3 = {
        "Axe": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Type": {
                                        "value": 3.0
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "editorID": "WeapTypeAxe"
                                }
                        }
                ]
        },
        "Blunt": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Type": {
                                        "value": 4.0
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "editorID": "WeapTypeMace"
                                }
                        }
                ]
        },
        "Claw": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "Keyword": {
                                        "form": {
                                                "pluginName": "NewArmoury.esp",
                                                "formID": "19aab4"
                                        }
                                },
                                "Left hand": False,
                                "condition": "IsEquippedRightHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True
                        },
                        {
                                "Keyword": {
                                        "form": {
                                                "pluginName": "NewArmoury.esp",
                                                "formID": "19aab4"
                                        }
                                },
                                "Left hand": True,
                                "condition": "IsEquippedLeftHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True
                        }
                ]
        },
        "Dagger": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Type": {
                                        "value": 2
                                },
                                "Left hand": False
                        }
                ]
        },
        "Greatsword": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Type": {
                                        "value": 5
                                }
                        }
                ]
        },
        "Katana": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Keyword": {
                        "PluginName": "kcf.esm",
                        "editorID": "WeapTypeKatana"
                }
        },
        "Quarterstaff": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Keyword": {
                        "editorID": "WeaptypeQuarterstaff",
                        "pluginName": "kcf.esm"
                }
        },
        "Rapier": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Keyword": {
                        "PluginName": "kcf.esm",
                        "editorID": "WeapTypeRapier"
                }
        },
        "Scythe": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Type": {
                                        "value": 6.0
                                },
                                "Left hand": False
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "WeapTypeScythe"
                                }
                        }
                ]
        },
        "Spear": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "editorID": "WeaptypePike"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "editorID": "WeaptypeSpear"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "form": {
                                                "pluginName": "NewArmoury.esp",
                                                "formID": "E457E"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquipped",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Form": {
                                        "pluginName": "Sekiro - Ashina General.esp",
                                        "formID": "1DAD"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "form": {
                                                "pluginName": "Smooth Weapon.esm",
                                                "formID": "801"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
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
                                "negated": True,
                                "Keyword": {
                                        "form": {
                                                "pluginName": "Smooth Weapon.esm",
                                                "formID": "80A"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "form": {
                                                "pluginName": "Spear of Skyrim.esp",
                                                "formID": "A88"
                                        }
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "form": {
                                                "pluginName": "kcf.esm",
                                                "formID": "803"
                                        }
                                }
                        }
                ]
        },
        "Sword": {
                "condition": "AND",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Type": {
                                        "value": 1
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": True,
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "OneHandSword"
                                }
                        },
                ]
        },
        "Unarmed": {
                            "condition": "IsEquippedType",
                            "requiredVersion": "1.0.0.0",
                            "negated": True,
                            "Type": {
                                    "value": 0
                            },
                            "Left hand": False
                    },
        "Shield": {
                "condition": "IsEquippedType",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Type": {
                        "value": 10.0
                }
        },
        "Whip": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Keyword": {
                        "editorID": "WeapTypeWhip"
                }
        }
}

onehanders = [
    "Dagger",
    "Claw",
    "Whip",
    "Rapier",
    "Unarmed"
]

presets = []

for _weapon in weapons:
    config_name = "4D Combat " + str(_weapon)
    weapon_path = os.path.join(basepath,config_name)
    try:
        _weapon_conditions = weapon_mapping2[_weapon]
        if (_weapon in onehanders):
            grips = ["DW", "1H"]
        for _grip in grips:
            _gripPath = os.path.join(weapon_path, _grip)


            preset = generate_preset(_grip, None, None, _weapon)
            presets.append(preset)
            presetConditions.append(preset['conditions'])
            submodPath = os.path.join(weapon_path, preset['name'])
            os.makedirs(submodPath, exist_ok=True)
            framework_paths.append(submodPath)
            make_variant_dirs(submodPath)
            configPath = os.path.join(submodPath, "config.json")
            with open(configPath, "w") as f:
                json.dump(preset, f, indent=2)

            for _keytrace in keytraces:
                preset = generate_preset(_grip, None, _keytrace, _weapon)
                presets.append(preset)
                presetConditions.append(preset['conditions'])
                submodPath = os.path.join(weapon_path, preset['name'])
                os.makedirs(submodPath, exist_ok=True)
                make_variant_dirs(submodPath)
                framework_paths.append(submodPath)
                configPath = os.path.join(submodPath, "config.json")
                with open(configPath, "w") as f:
                    json.dump(preset, f, indent=2)

            for _stance in stances:
                preset = generate_preset(_grip, _stance, None, _weapon)
                presets.append(preset)
                presetConditions.append(preset['conditions'])
                submodPath = os.path.join(weapon_path, preset['name'])
                os.makedirs(submodPath, exist_ok=True)
                framework_paths.append(submodPath)
                make_variant_dirs(submodPath)
                configPath = os.path.join(submodPath, "config.json")
                with open(configPath, "w") as f:
                    json.dump(preset, f, indent=2)

                for _keytrace in keytraces:
                    preset = generate_preset(_grip, _stance, _keytrace, _weapon)
                    presets.append(preset)
                    presetConditions.append(preset['conditions'])
                    submodPath = os.path.join(weapon_path,preset['name'])
                    os.makedirs(submodPath, exist_ok=True)
                    framework_paths.append(submodPath)
                    make_variant_dirs(submodPath)
                    configPath = os.path.join(submodPath, "config.json")
                    with open(configPath, "w") as f:
                        json.dump(preset, f, indent=2)

        for _stance in stances:
            print(_weapon_conditions)
            preset = generate_preset(None, _stance, None, _weapon)
            presets.append(preset)
            presetConditions.append(preset['conditions'])
            submodPath = os.path.join(weapon_path, preset['name'])
            os.makedirs(submodPath, exist_ok=True)
            framework_paths.append(submodPath)
            make_variant_dirs(submodPath)
            configPath = os.path.join(submodPath, "config.json")
            with open(configPath, "w") as f:
                json.dump(preset, f, indent=2)

            for _keytrace in keytraces:
                print(_weapon_conditions)
                preset = generate_preset(None, _stance, _keytrace, _weapon)
                presets.append(preset)
                presetConditions.append(preset['conditions'])
                submodPath = os.path.join(weapon_path   , preset['name'])
                os.makedirs(submodPath, exist_ok=True)
                framework_paths.append(submodPath)
                make_variant_dirs(submodPath)
                configPath = os.path.join(submodPath, "config.json")
                with open(configPath, "w") as f:
                    json.dump(preset, f, indent=2)

        preset = generate_preset(None, None, None, _weapon)
        preset['name'] = 'base'
        presets.append(preset)
        presetConditions.append(preset['conditions'])
        submodPath = os.path.join(weapon_path, preset['name'])
        os.makedirs(submodPath, exist_ok=True)
        framework_paths.append(submodPath)
        make_variant_dirs(submodPath)
        configPath = os.path.join(submodPath, "config.json")
        with open(configPath, "w") as f:
            json.dump(preset, f, indent=2)


        config = {
            "name": config_name,
            "author": "lobotomyx",
            "description": "Weapon Grip Stance Keytrace",
            "ConditionPresets": presetConditions
        }
        configPath = os.path.join(weapon_path, "config.json")
        with open(configPath, "w") as f:
            json.dump(config, f, indent=2)
    except FileNotFoundError:
        print("file not found")

outputs = [
    {
        "name": "framework",
        "author": "lobotomyx",
        "description": "Weapon Grip Stance Keytrace"
    }
]
for _framework_path in framework_paths:
    make_variant_dirs(_framework_path)
with open("user.json", "w") as f:
    json.dump(outputs[0], f, indent=2)
#process_folders(testpath, presets)
