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
no_citation_list = []
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
        last_index = len(publication['algorithms']['algorithm']) - 1
        if publication['algorithms']['algorithm'][last_index]["@name"] == 'ParsCit':
            print(path_str)
            if publication['algorithms']['algorithm'][last_index]["citationList"] is not None:
                citation_list = publication['algorithms']['algorithm'][last_index]["citationList"]["citation"]
                if isinstance(citation_list, dict):
                    citation_list = [citation_list]
                for citation in citation_list:
                    if citation["@valid"] == "true":
                        if "authors" in citation:
                            authors = citation["authors"]["author"]
                            if isinstance(authors, str):
                                authors = [authors]
                            for author in authors:
                                if author not in csv_dict[conference][year]:
                                    csv_dict[conference][year][author] = 0
                                csv_dict[conference][year][author] += 1

        else:
            no_citation_list.append(path_str)

print(len(no_citation_list))

aggregated_dict_list = []
for conference in csv_dict:
    for year in sorted(csv_dict[conference]):
        for author in csv_dict[conference][year]:
            aggregated_dict_list.append([conference, year, author.encode(), csv_dict[conference][year][author]])

with open('author_inCitation.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["Conference", "Year", "Author Name", "No. of inCitations"])
    writer.writerows(aggregated_dict_list)
