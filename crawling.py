from html.parser import HTMLParser
import urllib.request


class MyHTMLParser(HTMLParser):
    file_list = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.file_list.append(value)


response = urllib.request.urlopen('http://acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-parscit/')
html = response.read().decode("utf-8")
parser = MyHTMLParser()
parser.feed(html)
filtered_list = [name for name in parser.file_list if name.find(".tgz") != -1 or name.find(".txt") != -1]
print(filtered_list)
for file in filtered_list:
    urllib.request.urlretrieve('http://acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-parscit/' + file, file)
