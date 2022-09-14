
# NRMM DETECTION FROM HIGH RESOLUTION SATELLITE IMAGERY USING THE YOLOV4

# SECTION 1: xView_geojson_to_yolo.py 

xView provide bounding box annotations for the objects in their dataset in a GeoJSON format.

This code was developed to select only the annotations associated with NRMM objects, and convert their format from GeoJSON to YOLO.

This involves converting the coordinates of the bounding boxes from image pixel coordinates to YOLO coordinates.

## Directory Formatting:
Create a main folder to house the other directories. In the code given, this folder is called 'DATA_FOR_DIS'

- Within this folder, create a folder called 'Annotations'. Put the GeoJSON file from xView here.

- Additionally, create a folder called 'All_images'. Put all xView images here.

- Additionally, create an empty folder called 'Useful_images'. This will eventually contain the images containing NRMM objects.

## Setting Paths:
Change the following directory paths:

'path' (~line 25) -> set path to 'Annotations' directory
'image_link' (~line 96) -> adapt path to 'All_images' directory
'writing_link' (~line 295) -> adapt path to 'Useful_images' directory
Old_image_link / new_image_link (~line 306) -> adapt 'All_images' and 'Useful_images' paths.


## Annotations
The annotation file supplied by xView is 372.2MB which was too large for a 2019 Macbook Pro to process, therefore this file was split into 90MB chunks using the following terminal command:

split -b 90m file_name

This resulted in 21 smaller geoJSON files which were then manually editted to make sure that no annotations were cut off mid way through.

This process may not be required if computing resources allow. If so, adjust code accordingly.

## Running the code:
This code was developed and tested using Pycharm.


## Expected Outcome:
After running the code, the 'Useful_Images' directory should become populated with satellite images that contain NRMM objects. For each image there should also be a text document with the same name as its associated image.

Each text file will contain a line for each object it contains. The first value is the object label (0 = NRMM). The following values are the bounding box coordinates for that object in YOLO format.



### SECTION 2: plot_annotations_on_images.py
- This file will plot an image and a given set of bounding box coordinates 

# Requirements: 

- All NRMM images will need to be in the 'Useful_images' directory (aka the xView_geojson_to_yolo.py file will already need to have been run) 

- Image numbers and associated coordinates can be found in the original xView geojson file.
    - Image numbers are found under the "image_id" key. 
    - Bounding box coordinates are found under the "bounds_imcoords" key. 
    
- The user needs to set the parameters given in Lines 21 - 23 (image number, path to file, coordinates).

