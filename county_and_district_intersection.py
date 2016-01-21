import json
from shapely.geometry import shape
import pandas as pd

#load geojsons, extract features and create dict of id:polygon
co = json.load(open(r'C:\Users\camden\Documents\python\work\kc\mapping\ga_counties.geojson', 'r'))
counties = {i['properties']['name']: shape(i['geometry']) for i in co['features']}
ho = json.load(open(r'C:\Users\camden\Documents\python\work\kc\legis_profiles\static\geojson\lower.geojson', 'r'))
se = json.load(open(r'C:\Users\camden\Documents\python\work\kc\legis_profiles\static\geojson\upper.geojson', 'r'))
house = {i['properties']['SLDLST']: shape(i['geometry']) for i in ho['features']}
senate = {i['properties']['SLDUST']: shape(i['geometry']) for i in se['features']}

#get the overlapping counties and districts
house_overlap=[]
for dist, dpoly in house.iteritems():
    for co, poly in counties.iteritems():
        if dpoly.intersection(poly).area > 0.0001:
            house_overlap.append([dist, co])
senate_overlap=[]
for dist, dpoly in senate.iteritems():
    for co, poly in counties.iteritems():
        if dpoly.intersection(poly).area > 0.0001:
            senate_overlap.append([dist, co])
county_overlap=[]
for co, poly in counties.iteritems():
    for dist, dpoly in senate.iteritems():
        if dpoly.intersection(poly).area > 0.0001:
            county_overlap.append([co, 'senate', dist])
    for dist, dpoly in house.iteritems():
        if dpoly.intersection(poly).area > 0.0001:
            county_overlap.append([co, 'house', dist])

#create df's and export to csv's
housedf = pd.DataFrame(house_overlap, columns = ['house_dist', 'county'])
housedf.to_csv(r'C:\Users\camden\Documents\python\work\kc\legis_profiles\static\csv\house_overlap.csv', index = False)
senatedf = pd.DataFrame(senate_overlap, columns = ['senate_dist', 'county'])
senatedf.to_csv(r'C:\Users\camden\Documents\python\work\kc\legis_profiles\static\csv\senate_overlap.csv', index = False)
countydf = pd.DataFrame(county_overlap, columns = ['county', 'dist_type', 'dist'])
countydf.to_csv(r'C:\Users\camden\Documents\python\work\kc\legis_profiles\static\csv\county_overlap.csv', index = False)

