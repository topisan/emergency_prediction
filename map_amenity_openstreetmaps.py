#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import time
import overpy
overpass_url = "http://overpass-api.de/api/interpreter"


# In[2]:


# extracting all boundaries of the municipios, 
# 3600349048 responds to canary islands area code
overpass_query = """
  area(3600349048);
(
  node(area);
  <;
) -> .a;
(
  rel.a["boundary"="administrative"]["admin_level"="8"];
);
out body;
"""  

result = overpy.Overpass().query(overpass_query)


# In[3]:


#extracting ids and meta information into separate lists
list_of_relations=[]
rel_ids=[]
names=[]
for i in range(0, len(result.relations)):
    rel_ids.append(result.relations[i].id)
    list_of_relations.append(result.relations[i].tags)
    names.append(result.relations[i].tags['name'])


# In[4]:


# create dict with ids as keys and meta info as values
dictionary = dict(zip(rel_ids,zip(names,list_of_relations)))
with open('relations_data.json', 'w') as fp:
    json.dump(dictionary, fp)


# In[5]:


this_id=rel_ids[55]+3600000000
overpass_query = """
        [out:json];
        area(%s);(
        node["amenity"="bar"](area);
        way["amenity"="bar"](area);
        rel["amenity"="bar"](area);); out center;
        """  % this_id 

result = overpy.Overpass().query(overpass_query)


# In[6]:


amount_of_bars=[]
for x in rel_ids:
    this_id=x+3600000000
    overpass_query = """
        [out:json];
        area(%s);(
        node["amenity"="bar"](area);
        way["amenity"="bar"](area);
        rel["amenity"="bar"](area);); out center;
        """  % this_id 

    response = requests.get(overpass_url, 
                             params={'data': overpass_query})
    data = response.json()
    amount_of_bars.append(len(data['elements']))
    time.sleep(1)


# In[7]:


# create dict with ids as keys and amount of bars as values
dictionary = dict(zip(rel_ids,zip(names,amount_of_bars)))
with open('relations_data.json', 'w') as fp:
    json.dump(dictionary, fp)

