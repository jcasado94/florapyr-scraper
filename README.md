# florapyr-scraper

## What is this

This is a scraper designed to extract species observations information from http://www.atlasflorapyrenaea.eu/. Given a list of species IDs, the program will obtain all their observations and, for each of those, it will extract their _id_, _year_, _town_, _altitude_, _utm1x1_ and _utm10x10_, as obtained per the usual manual process from the website.

You input [this](examples/input_get_observations_example.txt)

and you get [this](examples/out_observations_example.json) and [this](examples/out_observations_example.csv).


## How to use

### Download Python3
https://www.python.org/downloads/

### Clone this project
Command line: `git clone https://github.com/jcasado94/florapyr-scraper.git your-desired-directory`

Or simply download the zip and extract it: https://github.com/jcasado94/florapyr-scraper/archive/refs/heads/main.zip

### Fill `input_get_observations.txt`
Write a newline-separated list of species IDs from FloraPyr into `input_get_observations.txt` (see the example in [input_get_observations_example.txt](examples/input_get_observations_example.txt)), as obtained from the site in *Taxons > Fiches Taxons*, and as exemplified in the following screenshot
![How to obtain species IDs](./images/speciesIDs.png)

(There is a _hidden functionality_ to let the user input the species names instead of the species IDs, as I thought that'd be easier for them. Nevertheless, it currently relies on string comparison between given taxa names and FloraPyr accepted names, and therefore it is not robust enough and not recommended to use (it will misbehave with discordant taxa, especially subspecies). It can be triggered by changing `inputAsSpeciesName = False` to `inputAsSpeciesName = True` in `get_observations.py`. Manually fetching species IDs from FloraPyr is way more stable and reliable.)

### Execute!
`python3 get_observations.py`

### Read your observations
The retrieved observations will be written to `out_observations.csv` and `out_observations.json`. Choose whichever you prefer :).