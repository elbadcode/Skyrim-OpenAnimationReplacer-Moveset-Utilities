from lxml import etree as ET
import time
import re
import subprocess

def replace_annotations(path):
    st = time.time()
    xml_file = path
    anno_rep = {"PIE.@SGVI|MCO_nextattack|": "BFCO_NextIsAttack",
                "PIE.@SGVI|MCO_nextpowerattack|": "BFCO_NextIsPowerAttack", "MCO_WinOpen": "BFCO_NextWinStart",
                "MCO_recovery": "BFCO_Recovery", "MCO_PowerWinOpen": "BFCO_NextPowerWinStart",
                "MCO_PowerWinClose": "BFCO_DIY_EndLoop", "MCO_WinClose": "BFCO_DIY_EndLoop"}
    xml_content = str(xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    annotations = tree.xpath('//hkparam[@name="annotations"]')
    for annotation in annotations:
        hkobjects = annotation.findall('.//hkobject')
        for hkobject in hkobjects:
            hkparams = hkobject.findall('.//hkparam[@name="text"]')
            for hkparam in hkparams:
                # Get the text of the hkparam tag
                try:
                    text = hkparam.text
                    # If the text is in anno_rep, replace it
                    if text in anno_rep:
                        try:
                            print(text)
                            print(anno_rep[text])
                            hkparam.text = anno_rep[text]
                        except Exception as e:
                            print(e)
                    elif text.startswith("PIE"):
                        try:
                            print(text)
                            print(anno_rep[text])
                            hkparam.text = anno_rep[text]
                        except Exception as e:
                            print(e)
                    else:
                        pass
                except Exception as e:
                    print(e)
    modified_xml_content = ET.tostring(tree)
    modified_xml_content = modified_xml_content.decode('utf-8')
    with open(path, "w") as xml_file:
        xml_file.write(modified_xml_content)
        hkx = str(path).split('.xml')[0] + '.hkx'
        cmd = f'hkxconv convert -v hkx "{path}" "{hkx}"'
        cmdstr = str(cmd)
        print(cmdstr)
        print(cmd)
        subprocess.run(cmdstr)
        et = time.time()
        elap = et - st
        print('Execution time: ', elap, ' seconds')
        return elap


def replace_regex(path):
    st = time.time()
    # Define the regex patterns and their replacements
    regex_anno = r"(?:PIE\.\@SGVI)?(?:\|MCO_(next))?(power)*(Attack)?(?:\|)"
    subst_anno = "BFCO_\\g<1>is\\g<2>"
    # Perform the regex replacements
    with open(path, "r+", encoding='us-ascii') as xml_file:
        xml_content = xml_file.read()
        xml_content = re.sub(regex_anno, subst_anno, xml_content)
        print(xml_content, file=xml_file)  # Parse the modified XML content
        hkx = str(path).split('.xml')[0] + '.hkx'
        cmd = f'hkxconv convert -v hkx "{path}" "{hkx}"'
        cmdstr = str(cmd)
        print(cmdstr)
        print(cmd)
        subprocess.run(cmdstr)
        et = time.time()
        elap = et - st
        print('Execution time: ', elap, ' seconds')
        return elap

# def replace_regex(path):
#     st = time.time()
#     # Define the regex patterns and their replacements
#     regex_anno = [r"(?:PIE\.\@SGVI)?(?:\|MCO_(next))?(power)*(Attack)?(?:\|)", r"(?:MCO_)(.*Win)(?:Open)",
#                   r"(?:MCO_)(.*Win)(?:Close)"]
#     subst_anno = ["BFCO_\\g<1>is\\g<2>", "BFCO_Next\\g<1>Start", "BFCO_DIY_EndLoop"]
#     # Perform the regex replacements
#     with open(path, "r+", encoding='us-ascii') as xml_file:
#         xml_content = xml_file.read()
#         for regex, subst in zip(regex_anno, subst_anno):
#             xml_content = re.sub(regex, subst, xml_content)
#             print(xml_content, file=xml_file)  # Parse the modified XML content
#             hkx = str(path).split('.xml')[0] + '.hkx'
#             cmd = f'hkxconv convert -v hkx "{path}" "{hkx}"'
#             cmdstr = str(cmd)
#             print(cmdstr)
#             print(cmd)
#             subprocess.run(cmdstr)
#             et = time.time()
#             elap = et - st
#             print('Execution time: ', elap, ' seconds')
#             return elap

