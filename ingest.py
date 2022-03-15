#!/usr/bin/python3
from terminusdb_client import WOQLClient
import re
import csv
import json
import math
import os
import urllib.parse
from pprint import pprint

team = 'admin'
client = WOQLClient(f"http://localhost:6363/")
# make sure you have put the token in environment variable
# https://docs.terminusdb.com/v10.0/#/terminusx/get-your-api-key
client.connect(user=team, team=team, key='root')

dbid = "nmdc"
label = "NMDC"
description = "."
prefixes = {'@base' : 'http://nmdc/',
            '@schema' : 'http://nmdc#',
            'gold' : "https://gold.jgi.doe.gov/biosample?id="}

def import_schema(client):
    # Opening JSON file
    schema = open('nmdc.json',)
    schema_objects = json.load(schema)

    client.message = "Adding NMDC Schema"
    results = client.insert_document(schema_objects,
                                     graph_type="schema")
    print(f"Added schema: {results}")

if __name__ == "__main__":
    exists = client.get_database(dbid)

    if exists:
        client.delete_database(dbid, team=team, force=True)

    client.create_database(dbid,
                           team,
                           label=label,
                           description=description,
                           prefixes=prefixes)

    # client.author="Gavin Mendel-Gleason"
    import_schema(client)
    documents =[
        { "@type" : "EcosystemSubtype",
          "@capture" : "Ecosystem_1",
          "name" : "Endosphere",
          "uri" : "http://foo/Endosphere" },

        { "@type" : "Habitat",
          "@capture" : "Habitat_1",
          "name" : "Populus endosphere",
          "uri" : "http://foo/Populus_endosphere" },

        { "@type" : "Study",
          "@capture" : "Study_1",
          "websites":["https://pmiweb.ornl.gov/pmi-project-aims/"],
          "id":"gold:Gs0103573",
          "description":"This study is part of the Plant-Microbe Interfaces Science Focus Area, which aims to gain a deeper understanding of the diversity and functioning of mutually beneficial interactions between plants and microbes in the rhizosphere. Ongoing efforts focus on characterizing and interpreting such interfaces using systems comprising plants and microbes, in particular the poplar tree (Populus) and its microbial community in the context of favorable plant microbe interactions.",
          "doi":"https://doi.org/10.25585/1488096",
          "has_credit_associations":[
              { "@type" : "CreditAssociation",
                "applied_roles":["Principal Investigator","Conceptualization"],
                "applies_to_person":{
                    "@type" : "Person",
                    "name":"Mitchel J. Doktycz",
                    "email":"doktyczmj@ornl.gov",
                    "orcid":"orcid:0000-0003-4856-8343"}
               },
              { "@type" : "CreditAssociation",
                "applied_roles":["Conceptualization","Data curation",
                                 "Formal Analysis",
                                 "Funding acquisition",
                                 "Investigation",
                                 "Methodology",
                                 "Validation",
                                 "Visualization",
                                 "Writing – original draft",
                                 "Writing – review & editing"
                                 ],
                "applies_to_person":{
                    "@type" : "Person",
                    "name":"Josh Michener",
                    "email":"michenerjk@ornl.gov",
                    "orcid":"orcid:0000-0003-2302-8180"}}
              ],
          "principal_investigator": {"@type" : "Person",
                                     "name":"Mitchel J. Doktycz",
                                     "profile_image_url":"https://portal.nersc.gov/project/m3408/profile_images/doktycz_mitchel.jpg",
                                     "orcid":"orcid:0000-0003-4856-8343"},
          "publications":["https://doi.org/10.1128/mSystems.00045-18"],
          "title":"Defining the functional diversity of the Populus root microbiome",
          "name":"Populus root and rhizosphere microbial communities from Tennessee, USA"
         },

        { "@type" : "Biosample",
          "ecosystem_subtype" : {"@ref" : "Ecosystem_1"},
          "habitat" : {"@ref" : "Habitat_1" },
          "geo_loc_name": {
              "@type" : "LocationName",
              "has_raw_value":"USA: Tennessee"
          },
          "id":"gold:Gb0115838",
          "lat_lon": { "@type" : "LatLon",
                       "has_raw_value":"35.8443 -83.9607",
                       "latitude":35.8443,
                       "longitude":-83.9607},
          "add_date":"2015-06-23",
          "part_of":[ { "@ref" : "Study_1" } ],
          "name":"Populus endosphere microbial communities from Tennessee, USA - Endosphere MetaG P. deltoides DD176-1"
         }
    ]

    result = client.insert_document(documents)
    print(f"Added Documents: {result}")

    [eco, hab, study, bio] = result

    bio_document = client.get_document(bio)
    print("bio document\n")
    pprint(bio_document)

    study_document = client.get_document(bio_document['part_of'][0])
    print("study document\n")
    pprint(study_document)

