# florapyr-scraper

## What is this

This is a scraper designed to extract species observations information from http://www.atlasflorapyrenaea.eu/. Given a list of species, the program will obtain all their observations and, for each of those, it will extract their _id_, _year_, _town_, _altitude_, _utm1x1_ and _utm10x10_, as obtained per the usual manual process from the website.

## How to use

### Download Python3
https://www.python.org/downloads/

### Clone this project
Command line: `git clone https://github.com/jcasado94/florapyr-scraper.git your-desired-directory`

Or simply download the zip: https://github.com/jcasado94/florapyr-scraper/archive/refs/heads/main.zip

### Fill input_get_observations.txt
With a newline-separated list of species IDs from FloraPyr, as obtained from the site in *Taxons > Fiches Taxons*, and as exemplified in the following screenshot,
![How to obtain species IDs](./images/speciesIDs.png)

(There is a _hidden functionality_ to let the user input the species names instead of the species IDs, as I thought that'd be easier for them. Nevertheless, it relies on string comparison between given taxa names and FloraPyr accepted names, and therefore it is not robust enough and not recommended to use. It can be triggered by changing `inputAsSpeciesName = False` to `inputAsSpeciesName = True` in `get_observations.py`. Manually fetching species IDs from FloraPyr is way more stable.)

### Execute!
`python3 get_observations.py`

### Read your observations
The retrieved observations will be written to `out_observations.csv` and `out_observations.json`. Choose whichever you prefer :).