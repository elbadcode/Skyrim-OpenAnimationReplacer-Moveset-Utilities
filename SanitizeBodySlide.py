import os
import re
import FreeSimpleGUI as sg
import shutil
import xml.etree.ElementTree as ET

def make_key(key):
	"""
    Returns a dictionary that is used to pass parameters to an Input element.
    Another approach could be to return an Input element. The downside to that approach is
    the lack of parameters and associated docstrings when creating the layout.

    :param key:
    :return: Dict
    """
	return {'default_text':sg.user_settings_get_entry(key, ''), 'key':key}
# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'
Windows = []




def create_backup(file_path):
	bs_path = locate_bs_path(file_path)
	dest_root = f"{bs_path}_backup"
	print(dest_root)
	if not os.path.exists(dest_root):
		os.makedirs(dest_root)
	os.chdir(dest_root)
	print(f"dest_root {dest_root}")
	path_from_bs = file_path.split('SliderPresets\\')[1]
	dest= os.path.join(dest_root, path_from_bs)
	print (dest)
	print(path_from_bs)
	dest_dir = os.path.dirname(dest)
	if not os.path.exists(dest_dir):
		os.makedirs(dest_dir)
	if os.path.isdir(file_path):
		shutil.copytree(file_path,dest,dirs_exist_ok=True)
	elif os.path.isfile(file_path) and not os.path.isfile(dest):
		shutil.copyfile(file_path,dest)


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




def recurse_count(folder):
	folder_ct = 0
	for file_entry in os.scandir(folder):
		file = file_entry.name
		fullname = os.path.join(folder, file)
		if os.path.isfile(fullname):
			if file.endswith('.xml'):
				folder_ct += 1
		elif os.path.isdir(fullname):
			folder_ct += recurse_count(fullname)
	print(f"{folder}: {folder_ct}")
	return folder_ct


def locate_presets_path(starting_path):
	for dirpath in os.walk(starting_path):
		try_path = dirpath[0]
		print(try_path)
		if try_path.endswith('SliderPresets'):
			return try_path
		elif 'SliderPresets' in try_path:
			while not (try_path.endswith('SliderPresets')):
				try_path = os.path.abspath(os.path.join(try_path, '..'))
			return try_path
		else:
			return



def locate_bs_path(starting_path):
	for dirpath in os.walk(starting_path):
		try_path = dirpath[0]
		print(try_path)
		if try_path.endswith('CalienteTools'):
			preset_path= locate_presets_path(try_path)
			return try_path,preset_path
		elif 'CalienteTools' in try_path:
			while not (try_path.endswith('CalienteTools')):
				try_path = os.path.abspath(os.path.join(try_path, '..'))
			preset_path = locate_presets_path(try_path)
			return try_path,preset_path
		else:
			return


def set_start_path():
	try:
		starting_path = sg.user_settings_get_entry('-bodyslidepath-')
	except Exception as e:
		starting_path = os.getcwd()


	layout = [[sg.Text('Pick Mod Location')],
							[sg.InputText(size=(50, 1), key='-bodyslidepath-'), sg.FileBrowse()],
							[sg.Button('Go'), sg.Button('Exit')]]
	event1, values1 = sg.Window('Normal Filename', layout).read(close=True)
	bs_path = locate_bs_path(starting_path)
	return bs_path


regex = r"\<SetSlider\Wname\=\"(\w+)\"\Wsize\=\"big\"\Wvalue\=\"(\d*)\"\/\>\n*\W+\<SetSlider\Wname=\"(\w+)\"\Wsize\=\"small\"\Wvalue\=\"(\d*)\""
regex_small = r"\<SetSlider\Wname\=\"(\w+)\"\Wsize\=\"small\"\Wvalue\=\"(\d*)\"\/\>"


def set_divisor():
	divideby = 1
	action_window = sg.Window("Choose Action",
							  [[sg.Text("This will ensure no low weight sliders exceed high weights. You can match them or divide by n")],
							   [sg.Button('Match Weights'), sg.Button('Divide Low Weights'), sg.Cancel()]
							   ])
	event, values = action_window.read()
	if event == 'Match Weights':
		sg.Popup('Matching Erroneous Weights')
		divideby = 1
	elif event == 'Divide Low Weights':
		divideby = 2
		while divideby not in range(1,10):
			layout2 = [[sg.Text('Enter Divisor:')],
					   [sg.Input('', enable_events=True, key='-INPUT-')],
					   [sg.Button('Ok', key='-OK-'), sg.Button('Cancel')]]
			window2 = sg.Window('Pick weight divisor', layout2, keep_on_top=True,force_toplevel=True)
			event2, values2 = window2.read()
			print(event2, values2)
			if event2 == sg.WIN_CLOSED or event2 == 'Exit':
				break
			if event2 == '-INPUT-' and len(values2['-INPUT-']) and values2['-INPUT-'][-1] not in ('0123456789'):
				sg.Popup("Whoa there buddy what the heck did you type")
				window2['-INPUT-'].update(values2['-INPUT-'][:-1])
			elif values2['-INPUT-'][-1] in ('0123456789'):
				divideby = values2['-INPUT-']
		window2.close()
		return divideby


def resolve_xml_paths(f):
	print(f"f {f}")
	if f.endswith('.xml'):
		print("here")
		return f
	elif os.path.isdir(f):
		for file_entry in os.path.scandir(f):
			file = file_entry.name
			fullname = os.path.join(f, file)
			if fullname.endswith('.xml'):
				print("here")
				return fullname

def offset_weights(f):
	fullname = resolve_xml_paths(f)
	offset_weights_file(fullname)

def offset_weights_file(fullname):
	with open(
			+
				except IndexError:
					print('Something is funky with your selection')
			elif event == 'Make Backup':
				for item in selected_items:
					create_backup(item)
			elif event == 'Offset Weights':
				for f in selected_items:
					if (f.endswith('.xml')):
						offset_weights(f)
			elif event == 'Change Directory':
				window.close()
				Windows.append(Windows.pop(0))
				main()
		except IndexError:
			print('index error')


		try:
			print(event, values)
		except UnicodeEncodeError:
			print('check text encoding')



treedata = sg.TreeData()

with open("bodyslidechangelog.txt", "w") as log_file:
	main()
