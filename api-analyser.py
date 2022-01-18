import os
import time
from tqdm import tqdm

# read all files in malware_samples directory
samples_path = "../testbatchmal"
output_path = "../testbatch-out"
files = os.listdir(samples_path)
for i in tqdm(range(len(files))):
	file = files[i].strip()
	file_path = os.path.join(samples_path, file)
	if os.path.isfile(file_path):
		# execute apk analysis and store output appropriately
		os.system(f"./run-apktool.sh {file_path} {output_path} {file}")
		
