# given a list of species IDs (preferred) or names in input.txt, returns information about the observations for each of them.

import requests
import json
from difflib import SequenceMatcher
from get_observations_info import getObservationsInfo

initalRequestURL = "http://www.atlasflorapyrenaea.eu/src/taxon/index.php?idma=11"
setSpeciesURL = "https://www.atlasflorapyrenaea.eu/src/commun/liste-taxon-process.php"
geoJsonURL = "http://www.atlasflorapyrenaea.eu/src/taxon/GEOJSON-consult.php?precision=0&repres_carto=1&annee_debut=&annee_fin="
getObservationsURL = "http://www.atlasflorapyrenaea.eu/src/taxon/obs-liste.php?sEcho=3&iColumns=13&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=99999999999999999&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=true&mDataProp_9=9&sSearch_9=&bRegex_9=false&bSearchable_9=true&bSortable_9=true&mDataProp_10=10&sSearch_10=&bRegex_10=false&bSearchable_10=true&bSortable_10=true&mDataProp_11=11&sSearch_11=&bRegex_11=false&bSearchable_11=true&bSortable_11=false&mDataProp_12=12&sSearch_12=&bRegex_12=false&bSearchable_12=true&bSortable_12=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&sRangeSeparator=~&id_acces=1"

# False: input as species FloraPyr ID (preferred)
# True: input as species name
inputAsSpeciesName = False

class Encoder(json.JSONEncoder):
  def default(self, o):
      return o.__dict__

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def findClosestName(speciesName, speciesList):
  bestScore = 0
  bestSpecies = ""
  for species in speciesList:
    score = similar(speciesName, species)
    if score > bestScore:
      bestScore = score
      bestSpecies = species
  return (bestScore, bestSpecies)

sps = []
with open("input_get_observations.txt", 'r') as f:
  inputSpecies = f.read().splitlines()
  if inputAsSpeciesName: # decision currently made upon string similarity - not good for some species, especially subsps.
      with open("species_list.json", 'r') as f:
        speciesDict = json.load(f)
        for speciesName in inputSpecies:
          speciesName = speciesName[:len(speciesName)-1] # remove \n
          closestMatch = findClosestName(speciesName, list(speciesDict.keys()))
          print("Closest match for " + speciesName + ": " + closestMatch[1] + "(" + str(closestMatch[0]) + ")")
          sps.append(speciesDict[closestMatch[1]])
  else:
    sps = inputSpecies

s = requests.Session()

# initial request to get the phdsession cookie
try:
  s.get(initalRequestURL, timeout = 10, verify = False)
except requests.exceptions.Timeout:
  print("InitialRequest Timeout")
  exit()

# set species for search
for sp in sps:
  try:
    r = s.post(setSpeciesURL, data = {'cd_ref_flpyr': sp, 'submit': '1'}, timeout = 10, verify = False)
  except requests.exceptions.Timeout:
    print("SetTaxon timeout. Skipping taxon" + str(sps))


# geoJSON URL. Apparently this is needed before obs-liste.
try:
  r = s.get(geoJsonURL, timeout = 10, verify = False)
except requests.exceptions.Timeout:
  print("GeoJSON timeout")
  exit()


# get observations
try:
  r = s.get(getObservationsURL, timeout = 10, verify = False)
except requests.exceptions.Timeout:
  print("GetObservations timeout")
  exit()

observations = getObservationsInfo(r.text)

# json output
out = open("out_observations.json", 'w')
out.write(json.dumps(observations, indent=4, cls=Encoder))
out.close()

# csv output
csv = "OBSERVATION_ID,SPECIES,YEAR,TOWN,ALTITUDE,UTM1X1,UTM10X10\n"
for obs in observations:
  csv = csv + obs["id"] + "," + obs["species"] + ","
  if "year" in obs:
    csv = csv + obs["year"] + ","
  else:
    csv = csv + ","
  if "town" in obs:
    csv = csv + obs["town"] + ","
  else:
    csv = csv + ","
  if "altitude" in obs:
    csv = csv + obs["altitude"] + ","
  else:
    csv = csv + ","
  if "utm1x1" in obs:
    csv = csv + obs["utm1x1"] + ","
  else:
    csv = csv + ","
  if "utm10x10" in obs:
    csv = csv + obs["utm10x10"] + "\n"
  else:
    csv = csv + "\n"

out = open("out_observations.csv", 'w')
out.write(csv)
out.close()

print("Found " + str(len(observations)) + " observations.")