#!/usr/bin/python3
from terminusdb_client import WOQLClient
import re
import csv
import json
import math
import os
import urllib.parse

team = 'admin'
client = WOQLClient(f"http://localhost:6363/")
# make sure you have put the token in environment variable
# https://docs.terminusdb.com/v10.0/#/terminusx/get-your-api-key
client.connect(user=team, team=team, key='root')

dbid = "nmdc"
label = "NMDC"
description = "."
prefixes = {'@base' : 'http://nmdc/',
            '@schema' : 'http://nmdc#'}

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
