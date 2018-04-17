from pathlib import Path
import json
import csv


def interpret_year(year_str):
    year = int(year_str)
    if year <= 20:
        return 2000 + year
    else:
        return 1900 + year


csv_dict = {}
no_header_list = []
path_list = Path('../json').glob('**/*.json')
for path in path_list:
    path_str = str(path)
    parsed_path = path_str.split("/")
    conference = parsed_path[2]
    if conference not in csv_dict:
        csv_dict[conference] = {}
    year = interpret_year(parsed_path[3].replace(conference, ''))
    if year not in csv_dict[conference]:
        csv_dict[conference][year] = {}
    with open(path_str) as content:
        publication = json.loads(content.read())
        if publication['algorithms']['algorithm'][0]["@name"] == 'SectLabel':
            if "author" in publication['algorithms']['algorithm'][0]["variant"]:
                authors = publication['algorithms']['algorithm'][0]["variant"]["author"]
                if isinstance(authors, dict):
                    authors = [authors]
                for author in authors:
                    if author['#text'] not in csv_dict[conference][year]:
                        csv_dict[conference][year][author['#text']] = 0
                    csv_dict[conference][year][author['#text']] += 1
        elif publication['algorithms']['algorithm'][1]["@name"] == 'ParsHed':
            if "author" in publication['algorithms']['algorithm'][0]["variant"]:
                authors = publication['algorithms']['algorithm'][0]["variant"]["author"]
                if isinstance(authors, dict):
                    authors = [authors]
                for author in authors:
                    if author['#text'] not in csv_dict[conference][year]:
                        csv_dict[conference][year][author['#text']] = 0
                    csv_dict[conference][year][author['#text']] += 1
        else:
            no_header_list.append(path_str)

aggregated_dict_list = []
for conference in csv_dict:
    for year in sorted(csv_dict[conference]):
        for author in sorted(csv_dict[conference][year]):
            aggregated_dict_list.append([conference, year, author.encode(), csv_dict[conference][year][author]])

with open('author_publication.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["Conference", "Year", "Author Name", "Publication"])
    writer.writerows(aggregated_dict_list)
