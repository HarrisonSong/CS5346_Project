import json
import xmltodict
import glob
import os
import tarfile
from io import open


def py_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".xml":
            yield tarinfo


# for zip_file in os.listdir('../CS5346_project_data'):
#     if os.path.splitext(zip_file)[1] == ".tgz":
#         tar = tarfile.open('../CS5346_project_data/' + zip_file)
#         tar.extractall('./xml', members=py_files(tar))
#         tar.close()


for filename in glob.iglob('xml/W/W14/**/*.xml', recursive=True):
    print(filename)
    # name_pair = os.path.split(filename)
    # new_path = name_pair[0].replace("xml/", "json/")
    # new_name = name_pair[1].replace(".xml", ".json")
    # if not os.path.exists(new_path):
    #     os.makedirs(new_path)
    # xml_to_json(filename, new_path + '/' + new_name)
    with open(filename, 'r', encoding="utf-8") as f:
        xmlString = f.read()
    jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
    name_pair = os.path.split(filename)
    new_path = name_pair[0].replace("xml/", "json/")
    new_name = name_pair[1].replace(".xml", ".json")
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    with open(new_path + '/' + new_name, 'w') as f:
        f.write(jsonString)
