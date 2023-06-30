# given a list of FloraPyr observation IDs, returns their information 
# (species, year, town, altitude, utm1x1, utm10x10)
import requests
import re
from bs4 import BeautifulSoup


observationInfoURL = "http://www.atlasflorapyrenaea.eu/src/taxon/obs-view.php?id="

pattern = re.compile(r'value=\\"([0-9]+)\\')

def getObservationsInfo(observationsDump):

  observations = []
  for match in pattern.finditer(observationsDump):
    obsID = match.group(1)
    obs = {"id": obsID}

    try:
      r = requests.get(observationInfoURL + obsID, timeout = 10)
    except requests.exceptions.Timeout:
      print("ObservationInfo timeout. Skipping observation" + obsID)
      continue
      
    html = BeautifulSoup(r.content, features="lxml")

    altitudeLabel = html.find("label", string="Altitude (m)")
    if altitudeLabel is None:
      altitudeLabel = html.find("label", string="Altitude calculée (m)")
    if altitudeLabel is not None:
      altitude = altitudeLabel.findNext("div").text
      obs["altitude"] = altitude
    
    utm1x1Label = html.find("label", string="Maille UTM 1 km")
    if utm1x1Label is not None:
      utm1x1 = utm1x1Label.findNext("div").text
      obs["utm1x1"] = utm1x1
    
    utm10x10Label = html.find("label", string="Maille UTM 10 km")
    if utm10x10Label is not None:
      utm10x10 = utm10x10Label.findNext("div").text
      obs["utm10x10"] = utm10x10
    
    townLabel = html.find("label", string="Commune")
    if townLabel is not None:
      town = townLabel.findNext("div").text
      obs["town"] = town  

    yearLabel = html.find("label", string="Année")
    if yearLabel is not None:
      year = yearLabel.findNext("div").text
      obs["year"] = year

    speciesLabel = html.find("label", string="Nom reconnu florapyr")
    if speciesLabel is not None:
      species = speciesLabel.findNext("div").text
      obs["species"] = " ".join(species.split()[:2])

    observations.append(obs)
  
  return observations