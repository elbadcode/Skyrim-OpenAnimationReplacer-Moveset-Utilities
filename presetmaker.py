import json
import os

basepath = os.getcwd()
priorities = []
priority_map = []
presetConditions = []
framework_paths = []
variant_paths = ['']

grip_priority_mappings = {
        "2H": 1000000,
        "1H": 150000000,
        "DW": 290000000
}

kt_priority_mappings = {
        "Forward": 250000000,
        "Left": 200000100,
        "Right": 200000000,
        "Backward": 300000000
}

stance_priority_mappings = {
        "Low": 70000000,
        "Mid": 50000000,
        "High": 35000000,
}


weapon_priority_mappings = {
        "Axe": 100000,
        "Blunt": 200000,
        "Claw": 800000,
        "Dagger": 700000,
        "Greatsword": 900000,
        "Katana": 990000,
        "Quarterstaff": 850000,
        "Rapier": 980000,
        "Scythe": 750000,
        "Shield": 420000,
        "Spear": 620000,
        "Sword": 500000,
        "Unarmed": 140000,
        "Whip": 330000
}


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
                        },
                        {
                                "condition": "IsEquippedType",
                                "requiredVersion": "1.0.0.0",
                                "Type": {
                                        "value": 10.0
                                }
                        },
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
                "condition": "IsEquippedType",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Type": {
                        "value": 2
                },
        },

        "Greatsword": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "EldenSkyrim.esp",
                                        "editorID": "WeaponTypeRimExGreatsword",
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
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "PluginName": "kcf.esm",
                                        "editorID": "WeapTypeKatana"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "EldenSkyrim.esp",
                                        "editorID": "WeaponTypeRimKatana",
                                }
                        },
                ]
        },
        "Quarterstaff": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "PluginName": "kcf.esm",
                                        "editorID": "WeapTypeQuarterStaff"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "EldenSkyrim.esp",
                                        "editorID": "WeaponTypeRimTwinblade",
                                }
                        },
                ]
        },
        "Rapier": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "PluginName": "kcf.esm",
                                        "editorID": "WeapTypeRapier"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "EldenSkyrim.esp",
                                        "editorID": "WeaponTypeRimRapier",
                                }
                        },
                ]
        },
        "Scythe": {
                "condition": "OR",
                "requiredVersion": "1.0.0.0",
                "negated": False,
                "Conditions": [
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "WeapTypeScythe"
                                },

                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "Smooth Weapon.esm",
                                        "editorID": "WeapTypeScythe"
                                },

                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "WeapTypeHalberd"
                                },

                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "Keyword": {
                                        "pluginName": "Smooth Weapon.esm",
                                        "editorID": "WeapTypeHalberd"
                                },

                        },
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
                                        "pluginName": "kcf.esm",
                                        "editorID": "WeapTypePike"
                                }
                        },

                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "pluginName": "kcf.esm",
                                        "editorID": "WeapTypeSpear"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "pluginName": "Smooth Weapon.esm",
                                        "editorID": "WeapTypePike"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "pluginName": "Smooth Weapon.esm",
                                        "editorID": "WeapTypeSpear"
                                }
                        },
                        {
                                "condition": "IsEquippedHasKeyword",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Keyword": {
                                        "pluginName": "Smooth Weapon.esm",
                                        "editorID": "WeapTypeJavelin"
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
                                        "pluginName": "EldenSkyrim.esp",
                                        "editorID": "WeapTypeRimSpear"
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
                        },

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
                "condition": "IsEquippedType",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Type": {
                        "value": 2
                },
                "Left hand": False
        },
        "Greatsword": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Keyword": {
                        "PluginName": "kcf.esm",
                        "editorID": "WeapTypeGreatsword",
                }
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
        "Scythe":
            {
                    "condition": "IsEquippedHasKeyword",
                    "requiredVersion": "1.0.0.0",
                    "negated": True,
                    "Keyword": {
                            "pluginName": "kcf.esm",
                            "editorID": "WeapTypeScythe"
                    }
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
                                                "pluginName": "Spear of Skyrim.esp",
                                                "formID": "A88"
                                        }
                                }
                        },
                ]
        },
        "Sword": {
                "condition": "IsEquippedHasKeyword",
                "requiredVersion": "1.0.0.0",
                "negated": True,
                "Keyword": {
                        "pluginName": "kcf.esm",
                        "editorID": "OneHandSword"
                }
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
                        "value": 11.0
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

twohanders = [
        "Greatsword",
        "Spear",
        "Scythe",
        "Quarterstaff"
]

onehanders = [
        "Dagger",
        "Claw",
        "Whip",
        "Rapier",
        "Unarmed"
]
grip_mapping = {"2H": "gripMode ==1", "1H": "gripMode == 2", "DW": "gripMode == 3"}
grip_mapping2 = {"2H": True, "1H": False, "DW": True}
stance_mapping = {"High": "42518", "Mid": "42519", "Low": "4251A"}
stance_mapping2 = {"High": "806", "Mid": "805", "Low": "803"}
keytrace_mapping = {"Forward": "801", "Left": "802", "Right": "804", "Backward": "803"}
keytrace_mapping2 = {"Forward": 1, "Left": 4, "Right": 2, "Backward": 3}

grip_mapping_1H = {
                                "condition": "OR",
                                "requiredVersion": "1.0.0.0",
                                "negated": False,
                                "Conditions": [
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
                                        },
                                        {
                                                "condition": "IsEquippedType",
                                                "requiredVersion": "1.0.0.0",
                                                "negated": False,
                                                "Type": {
                                                        "value": 0
                                                },
                                                "Left Hand": True,
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
                                                        "graphVariableType": "Int",
                                                }
                                        },
                                }
                        }
        ]
}
grip_mapping_2H = {
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
                        ]
                }
        ]
}

grip_mapping_DW = {
        "condition": "OR",
        "requiredVersion": "1.0.0.0",
        "negated": False,
        "Conditions": [
                {
                        "condition": "MathStatement",
                        "requiredPlugin": "OpenAnimationReplacer-Math",
                        "requiredVersion": "1.0.0.0",
                        "Math Statement": {
                                "expression": "gripMode > 2",
                                "variables": {
                                        "gripmode": {
                                                "graphVariable": "iDynamicGripMode",
                                                "graphVariableType": "Int",
                                        }
                                },
                        }
                }
            ]
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

presets = []


def make_variant_dirs(_submodPath):
    for _variant in variant_map:
        print(_variant)
        _variant_name = '_variants_' + _variant
        _variant_name = _variant_name.lower()
        if (_variant_name.endswith('attack')):
            mcocount = 0
            oldname = _variant_name
            while mcocount < 7:
                mcocount += 1
                _variant_name = oldname + str(mcocount)
                _variant_path = os.path.join(_submodPath, _variant_name)
                os.makedirs(_variant_path, exist_ok=True)
                variant_paths.append(_variant_path)
        _variant_path = os.path.join(_submodPath, _variant_name)
        os.makedirs(_variant_path, exist_ok=True)
        variant_paths.append(_variant_path)


def generate_preset(grip=None, stance=None, keytrace=None, weapon=None):
    generated_priority = int(1613474836)
    isAttacking = (keytrace is not None)
    RandomVal = 0.5
    if grip:
        generated_priority += grip_priority_mappings[grip]
        RandomVal += 0.2
    if stance:
        generated_priority += stance_priority_mappings[stance]
        RandomVal += 0.2
    if keytrace:
        generated_priority += kt_priority_mappings[keytrace]
        RandomVal += 0.1
    template = {
            "name": "",
            "priority": generated_priority,
            "interruptible": False,
            "shareRandomResults": True,
            "keepRandomResultsOnLoop": False,
            "conditions": [{
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
                                    "value": RandomVal
                            }
                    },
                    {
                            "condition": "IsInAir",
                            "requiredVersion": "1.0.0.0",
                            "negated": True
                    },
            ]
    }
    if isAttacking:
        template["conditions"].append({
            "condition": "IsAttacking",
            "requiredVersion": "1.0.0.0",
            "negated": False,
        })
    if grip == None:
        generated_priority -= 100000000
    elif grip == "1H":
        if weapon in twohanders:
            generated_priority += 20000000
        template["conditions"].append(grip_mapping_1H)
    elif grip == "2H":
        if weapon in onehanders:
            print("skipping" + weapon)
        elif weapon not in onehanders:
            template["conditions"].append(grip_mapping_2H)
    elif grip == "DW":
        template["conditions"].append(grip_mapping_DW)

    if stance == None:
        generated_priority -= 100000000
    else:
        template["conditions"].append(
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
                                        "Magic effect": {
                                                "pluginName": "StancesNG.esp",
                                                "formID": stance_mapping2[stance],
                                        }
                                }
                        ]
                }

        )
    if keytrace == None:
        generated_priority -= 10000000
    elif keytrace:
        template["conditions"].append(
                {
                        "condition": "HasMagicEffect",
                        "requiredVersion": "1.0.0.0",
                        "Magic effect": {
                                "pluginName": "Keytrace.esp",
                                "formID": keytrace_mapping[keytrace],
                        },
                        "Active effects only": False,
                }
        )
    if weapon:
        generated_priority += weapon_priority_mappings[weapon]
        notweapons = []
        for _weapon1 in weapons:
            if _weapon1 == weapon:
                pass
            elif _weapon1 == 'Dagger' and weapon == 'Claw':
                pass
            elif _weapon1 != weapon:
                notweapons.append(_weapon1)
        for notweapon in notweapons:
            template["conditions"].append(weapon_mapping3[notweapon])
        template["conditions"].append(weapon_mapping2[weapon])
        notweapons = []

    template["name"] = " ".join(filter(None, [grip, stance, keytrace]))
    generated_priority = int(generated_priority)
    if generated_priority < 0:
        return
    elif generated_priority >  int(2180278640):
        generated_priority -= 400278640
    while generated_priority in priorities:
        generated_priority += 1
    priorities.append(generated_priority)
    template["priority"] = generated_priority
    with open("presets.txt", "a") as log_file:
        print(f"New: {template}", file=log_file)

    return template


# add options to generate weapon agnostic folders with higher priority
for _weapon in weapons:
    config_name = "4D Combat " + str(_weapon)
    weapon_path = os.path.join(basepath, config_name)
    try:
        _weapon_conditions = weapon_mapping2[_weapon]
        if _weapon in onehanders:
            grips = ["1H", "DW"]
        else:
            grips = ["1H", "2H", "DW"]
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
                    submodPath = os.path.join(weapon_path, preset['name'])
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
                submodPath = os.path.join(weapon_path, preset['name'])
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
# process_folders(testpath, presets)
print(sorted(priorities))