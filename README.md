# Space Track Data Processing
This repository contains instructions for downloading Space Track Data for all objects in Space using the gp basicspacedata

The general perturbations (GP) class is an efficient listing of the newest SGP4 keplerian element set for each man-made earth-orbiting object tracked by the 18th Space Defense Squadron. It is designed to accommodate the expanded satellite catalog’s 9-digit identifiers. 

## Basic instructions
Here are a set of instructions for getting the latest data

1. Create a login to the space-track.org system
2. Login and navigate to the documentation api-restOperators page here https://www.space-track.org/documentation#api-restOperators
3. Scroll down to the gp section and locate the recommended URL. Right click and save the data to a file called gp-all-data.json. Or after you login you can right click on this URL and save the file https://www.space-track.org/basicspacedata/query/class/gp/decay_date/null-val/epoch/%3Enow-30/orderby/norad_cat_id/format/json
4. This is a long line JSON file. Run the format json python script. This will output the JSON into a human readable JSON file 

        $ convert-to-readable.py <INPUT JSON> <OUTPUT JSON>

## Create a Sample for study

Run the following to get a small data set with 3 objects of a type so you can read it

        $ create-sample.py <INPUT JSON> <SAMPLE OUTPUT JSON>

Study the output JSON to see what fields are available

## Getting Object Counts

Run the following command to get a count of each object type

        $ object-counts.py <INPUT JSON>

  
        Object Counts
        PAYLOAD          11472
        ROCKET BODY      2137
        DEBRIS           11078
        UNKNOWN          892
        ----------------------
        TOTAL            25579


