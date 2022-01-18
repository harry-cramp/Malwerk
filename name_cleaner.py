import os
import re

def terminal_name_formatter(name):
	name = name.replace("(", "\(").replace(")", "\)").replace(",", "\,")
	return name

file_dir = "new_samples/"
files = os.listdir(file_dir)
for file_name in files:
	full_path = os.path.join(file_dir, file_name)
	terminal_full_path = terminal_name_formatter(full_path)
	if re.match(".*\([0-9]\)\.apk", file_name):
		print(f"Duplicate found: {file_name}. Removing...")
		print(f"rm {terminal_full_path}")
		os.system(f"rm {full_path}")
	if os.path.isfile(full_path):
		print(full_path)
		new_name = ".".join(file_name.split(".")[:3])
		if not re.match(".*\.apk", new_name):
			new_name += ".apk"
		new_full_path = os.path.join(file_dir, new_name)
		os.system(f"mv {terminal_full_path} {new_full_path}")
