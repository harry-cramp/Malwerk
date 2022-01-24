import os
import re
import sys

from tqdm import tqdm
from collections import Counter

# TRENDFINDER analyses apktool outputs to find trends in malware and benign samples
malware_api_keywords = set()
benign_api_keywords = set()

if len(sys.argv) != 4:
	raise Exception("Must specify both directories of analysis output files to analyse as well as the split factor as float!")

benign_analysis_path = sys.argv[1]
malware_analysis_path = sys.argv[2]
split_factor = float(sys.argv[3])

redundant_chars = ["*", "/", "(", ")", "[", "]", ";", "\\", ":"]

class ApiData:

	def __init__(self):
		self.api_words_dict = {
			"Possible root detection": {},
			"References to apks": {},
			"SMS or telephony": {},
			"No location api": {},
			"Interesting API references": {},
			"Possible crypto stuff": {},
			"Possible client / communication": {},
			"Possible camera api calls": {},
			"stuff found in strings": {},
			"stuff found in methods": {},
			"Looking for private / public": {},
			"Native libraries found": {},
			"Assets found": {}
		}

def process_tokens(line):
	for char in redundant_chars:
		line = line.replace(char, " ")
	return set(line.split(" "))

def process_analysis(apidata, analysis_path):
	files = os.listdir(analysis_path)
	titles = apidata.api_words_dict.keys()
	print(f"Analysing output files in {analysis_path}...")
	for file_index in tqdm(range(len(files))):
		analysis_file = files[file_index]
		if not os.path.isfile(os.path.join(analysis_path, analysis_file)):
			continue
		f = open(os.path.join(analysis_path, analysis_file))
		lines = f.readlines()
		processing = False
		collecting_title = ""
		noted_apis = {}
		for line in lines:
			if not processing:
				if not re.match("\[\*\].*", line):
					continue
				for title in titles:
					if title in line:
						processing = True
						collecting_title = title
			else:
				line = line.strip()
				if line == "": 
					processing = False
					continue
				if re.match("\[\*\].*", line):
					continue
				line = line.split(".")[0]
				try:
					noted_apis[line]
				except KeyError:
					if line not in apidata.api_words_dict[collecting_title].keys():
						apidata.api_words_dict[collecting_title][line] = 1
					else:
						apidata.api_words_dict[collecting_title][line] += 1
					noted_apis[line] = True
	return (apidata, len(files))

malware_apidata, malware_count = process_analysis(ApiData(), malware_analysis_path)
benign_apidata, benign_count = process_analysis(ApiData(), benign_analysis_path)
					
print("ANALYSIS RESULTS:\n")
for title in benign_apidata.api_words_dict.keys():
	if title == "Looking for private / public":
		continue
	print(f"{title.upper()}\n")
	counter = Counter(malware_apidata.api_words_dict[title])
	for data in counter.most_common(20):
		percentage = (data[1] / malware_count) * 100
		compare_msg = ""
		if data[0] in benign_apidata.api_words_dict[title].keys():
			benign_data = benign_apidata.api_words_dict[title][data[0]]
			benign_percentage = (benign_data / benign_count) * 100
			compare_msg = " vs. {:.2f}% for benign samples".format(benign_percentage)
			if abs(percentage - benign_percentage) >= split_factor:
				print("{} - {:.2f}%{}".format(data[0], percentage, compare_msg))
				
	print("\n\n")


