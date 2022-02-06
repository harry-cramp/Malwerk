import re
import os
import sys

perm_labels = []
api_labels = []

output_file_path = sys.argv[1]

perms = {}
api_calls = {}

def load_sample_data(sample_path):
	with open(sample_path) as sample_file:
		lines = sample_file.readlines()
		for line in lines:
			line = line.strip()
			regex_search = re.search("<uses\-permission android:name=\"(android\.permission\..*)\"/>", line)
			if regex_search:
				perms[regex_search.group(1)] = 1
			else:
				line = line.split(".")[0]
				for label in api_labels:
					if line == label:
						api_calls[line] = 1

# load permissions from file
with open("data/permissions.txt") as perm_file:
	lines = perm_file.readlines()
	for line in lines:
		perm_labels.append(line.strip())
	perm_file.close()
	
# load API calls from file
with open("data/api-calls.txt") as api_file:
	lines = api_file.readlines()
	for line in lines:
		api_labels.append(line.strip())
	api_file.close()

for label in perm_labels:
	perms[label] = 0
for label in api_labels:
	api_calls[label] = 0

load_sample_data(output_file_path)

feature_vector = ""
for perm in perm_labels:
	feature_vector += str(perms[perm])
for api_call in api_labels:
	feature_vector += str(api_calls[api_call])
	
path_elements = output_file_path.split("/")
file_name = path_elements[-1].replace(".txt", "_fv.txt")
folder_path = "/".join(path_elements[:-1])

with open(os.path.join(folder_path, file_name), "w") as fv_file:
	fv_file.write(feature_vector)
	fv_file.close()
