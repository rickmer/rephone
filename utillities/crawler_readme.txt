To extract the relevant informations from the european parliament use the following command in your terminal to download a part form the website:
wget -r --no-parent --user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36" --limit-rate=150k http://www.europarl.europa.eu/meps/de/

After the download finished use the extractor.py to extract the information. Please set the mypath variable to the folder www.europarl.europa.eu/meps/de/.
