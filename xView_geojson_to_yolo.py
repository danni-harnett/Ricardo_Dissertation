# SEE 'README' FILE IN GITHUB BEFORE EDITTING.

import os
import re
import string
import numpy as np
from PIL import Image


path = "/Users/danniharnett/Desktop/DATA_FOR_DIS/Annotations"  # Set path for Annotation file
os.chdir(path)  # Change directory to correct file
files = os.listdir()  # Get list of all annotation files in directory (original geojson was split into ~21 mini docs)
path = (os.getcwd())

target_labels = [56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 32]  # Image labels that relate to NRMM objects.
# Full list of labels can be found here: https://github.com/DIUx-xView/data_utilities/blob/master/xview_class_labels.txt
# Last Accessed: 12/09/22

coords = []  # List of original image pixel coordinates (not converted)
yolo_list = []  # List of converted yolo coordinates


# function taken from: https://github.com/frankzhangrui/Darknet-Yolo/blob/master/convert.py. Last Accessed: 10/06/22
def convert(size, box):  # Convert pixel to YOLO coordinates
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh  # Bottom 4 lines normalise the yolo values

    return ([x,y,w,h])


def get_image(search_string):  # Get each image id from Geojson
    word = r"image_id"  # Search word
    start_index = re.search(word, search_string).start()  # Find index where search word starts
    image = search_string[start_index + 12: start_index + 16]  # Extract image id
    image = remove_punc(image)  # Clean up extracted image id (remove any punctuation)
    return image


def remove_punc(i):  # Remove punctuation from input string
    i = i.replace(',', ' ')  # Remove commas
    i = i.replace('.', '')  # Remove full stop
    i = i.replace('"', '')  # Remove speech markers -> leaves only the 4 image coordinates
    i = re.sub(r'[a-z]', '', i)  # Remove any alphabet characters
    return i


def get_image_coords(data, image): # input = full annotation, image number

    # Extract object coordinates and remove excess punctuation from the geojson
    word = r"bounds_imcoords"  # Search word
    search_string = data  # Look at one feature at a time

    if search_string == "":
        print("Annotation is empty")

    else:
        start_index = re.search(word, search_string).start()  # Find character index of where "BOUNDS_IMCOORDS" starts
        image_coord = search_string[start_index + 19:start_index + 38]  # Find coordinates using the known index of "bounds imcoords"
        image_coord = image_coord.replace('"', '')  # Clean up extraction
        image_coord = image_coord.split(',')

        # 4 coords should be produced (xmin, xmax, ymin, ymax)...
        if (len(image_coord)) == 5: # If split generates 5 items, delete the last one (blank)
            image_coord.pop()

        image_coord = [float(x) for x in image_coord]  # Convert coords from str to float
        coords.append(image_coord)  # append original pixel coords to list (for reference)

        xmin, ymin, xmax, ymax = image_coord  # separate out the values

        # Create link based on 'All_images' directory
        image_link = "/Users/danniharnett/Desktop/DATA_FOR_DIS/All_images/%s.jpeg" % (image)

        im = Image.open(image_link) # Open image and determine its width and height
        w = int(im.size[0])
        h = int(im.size[1])

        box = (xmin, xmax, ymin, ymax)  # put coords in the correct order for the 'convert' function

        yolo_coordinates = convert((w, h), box)  # Convert image coordinates to YOLO coordinates
        yolo_list.append(yolo_coordinates)  # Append to list of converted coords

    return yolo_coordinates


def get_label(data):
    labels = []
    images = []
    word = r"type_id"  # type_id is the object label (e.g. Haul Truck has type id: 61)

    for i in data:  # for each feature in the dataset
        search_string = i  # look at one feature at a time

        if search_string == "":
            break

        else:
            start_index = re.search(word, search_string).start()  # Find character index of where "type id" starts
            label = search_string[start_index + 10 : start_index + 12]  # Find label value and convert to integer
            label = remove_punc(label)

            if label == ' ':  # if label is blank -> ignore it
                continue

            label = int(label)

            if label in target_labels:  # If label is associated with a NRMM object
                label = convert_label_for_yolo(label)  # Convert all NRMM objects to have a label of 0.
                labels.append(label)
                image = get_image(search_string)  # Get associated image id
                image = int(image)
                images.append(image)
                coord = get_image_coords(search_string, image)  # Returns YOLO coords

    return (labels, images, coords)


def convert_label_for_yolo(label): # change object labels to 0 if they are NRMM.

    if label in target_labels:
        label = 0

    return label


# GeoJson document was split into 21 smaller files (numbered accordingly) so they could be processed by the computer.
# If computer can handle file size of unsplit geoJSON, keep only one of the following code segments:

# Open each of the split annotation files:
zero = open(path+"/"+str(files[0]), "r")
zero = zero.read()
zero = zero.split("]]]}},") # split each bounding box annotation into a separate entry
zero_labels, zero_images, zero_coords = get_label(zero)

one = open(path+"/"+str(files[1]), "r")
one = one.read()
one = one.split("]]]}},")
one_labels, one_images, one_coords = get_label(one)

two = open(path+"/"+str(files[2]), "r")
two = two.read()
two = two.split("]]]}},")
two_labels, two_images, two_coords = get_label(two)

three = open(path+"/"+str(files[3]), "r")
three = three.read()
three = three.split("]]]}},")
three_labels, three_images, three_coords = get_label(three)

four = open(path+"/"+str(files[4]), "r")
four = four.read()
four = four.split("]]]}},")
four_labels, four_images, four_coords = get_label(four)

five = open(path+"/"+str(files[5]), "r")
five = five.read()
five = five.split("]]]}},")
five_labels, five_images, five_coords = get_label(five)

six = open(path+"/"+str(files[6]), "r")
six = six.read()
six = six.split("]]]}},")
six_labels, six_images, six_coords = get_label(six)

seven = open(path+"/"+str(files[7]), "r")
seven = seven.read()
seven = seven.split("]]]}},")
seven_labels, seven_images, seven_coords = get_label(seven)

eight = open(path+"/"+str(files[8]), "r")
eight = eight.read()
eight = eight.split("]]]}},")
eight_labels, eight_images, eight_coords = get_label(eight)

nine = open(path+"/"+str(files[9]), "r")
nine = nine.read()
nine = nine.split("]]]}},")
nine_labels, nine_images, nine_coords = get_label(nine)

ten = open(path+"/"+str(files[10]), "r")
ten = ten.read()
ten = ten.split("]]]}},")
ten_labels, ten_images, ten_coords = get_label(ten)

eleven = open(path+"/"+str(files[11]), "r")
eleven = eleven.read()
eleven = eleven.split("]]]}},")
eleven_labels, eleven_images, eleven_coords = get_label(eleven)

twelve = open(path+"/"+str(files[12]), "r")
twelve = twelve.read()
twelve = twelve.split("]]]}},")
twelve_labels, twelve_images, twelve_coords = get_label(twelve)

thirteen = open(path+"/"+str(files[13]), "r")
thirteen = thirteen.read()
thirteen = thirteen.split("]]]}},")
thirteen_labels, thirteen_images, thirteen_coords = get_label(thirteen)

fourteen = open(path+"/"+str(files[14]), "r")
fourteen = fourteen.read()
fourteen = fourteen.split("]]]}},")
fourteen_labels, fourteen_images, fourteen_coords = get_label(fourteen)

fifteen = open(path+"/"+str(files[15]), "r")
fifteen = fifteen.read()
fifteen = fifteen.split("]]]}},")
fifteen_labels, fifteen_images, fifteen_coords = get_label(fifteen)

sixteen = open(path+"/"+str(files[16]), "r")
sixteen = sixteen.read()
sixteen = sixteen.split("]]]}},")
sixteen_labels, sixteen_images, sixteen_coords = get_label(sixteen)

seventeen = open(path+"/"+str(files[17]), "r")
seventeen = seventeen.read()
seventeen = seventeen.split("]]]}},")
seventeen_labels, seventeen_images, seventeen_coords = get_label(seventeen)

eighteen = open(path+"/"+str(files[18]), "r")
eighteen = eighteen.read()
eighteen = eighteen.split("]]]}},")
eighteen_labels, eighteen_images, eighteen_coords = get_label(eighteen)

nineteen = open(path+"/"+str(files[19]), "r")
nineteen = nineteen .read()
nineteen = nineteen.split("]]]}},")
nineteen_labels, nineteen_images, nineteen_coords = get_label(nineteen)

twenty = open(path+"/"+str(files[20]), "r")
twenty = twenty.read()
twenty = twenty.split("]]]}},")
twenty_labels, twenty_images, twenty_coords = get_label(twenty)

# All labels associated with NRMM objects
all_labels = (zero_labels + one_labels + two_labels + three_labels + four_labels + five_labels + six_labels + seven_labels
              + eight_labels + nine_labels + ten_labels + eleven_labels + twelve_labels + thirteen_labels +
              fourteen_labels + fifteen_labels + sixteen_labels + seventeen_labels + eighteen_labels + nineteen_labels
              + twenty_labels)

# All image numbers associated with NRMM objects
all_images = (zero_images + one_images + two_images + three_images + four_images + five_images + six_images + seven_images
              + eight_images + nine_images + ten_images+ eleven_images+ twelve_images+ thirteen_images +
              fourteen_images + fifteen_images + sixteen_images+ seventeen_images + eighteen_images + nineteen_images
              + twenty_images)

# All YOLO coordinates associated with NRMM objects
all_coords = (zero_coords + one_coords + two_coords + three_coords + four_coords + five_coords + six_coords + seven_coords
              + eight_coords + nine_coords + ten_coords + eleven_coords + twelve_coords + thirteen_coords +
              fourteen_coords + fifteen_coords + sixteen_coords + seventeen_coords + eighteen_coords + nineteen_coords
              + twenty_coords)

all_images = np.array(all_images)


for i in set(all_images):  # For each image containing NRMM objects..

    indices = np.where(all_images == i)[0]  # Find indices for each image (for example image 5 might occur at [3] & [14] in the list)

    # Write text document formatted in YOLO style to list annotations.
    # Each image has an associated text file that lists the coordinates of any NRMM objects it contains.
    # These will be written in the folder that contains only the NRMM images ('Useful_Images')
    # YOLO style: <label> <x_center, y_center, width, height>

    i = str(i)

    # adapt path to 'Useful_images' directory:
    writing_link = "/Users/danniharnett/Desktop/DATA_FOR_DIS/Useful_images/%s.txt" %(i)

    with open(writing_link, 'w') as f:  # Write text files for each image
        for j in indices:
            label = str(all_labels[j])
            coords = yolo_list[j]
            f.write("%s %s %s %s %s \n" % (label, coords[0], coords[1], coords[2], coords[3]))

    # MOVE THE NRMM IMAGES from 'All_images' INTO 'Useful_images'
    old_image_link = "/Users/danniharnett/Desktop/DATA_FOR_DIS/All_images/%s.jpeg" % (i)
    new_image_link = "/Users/danniharnett/Desktop/DATA_FOR_DIS/Useful_images/%s.jpeg" % (i)
    os.replace(old_image_link, new_image_link)



# Additional functionality: Converts yolo coordinates BACK TO pixel coords -> useful for checking
def yolobbox2bbox(x,y,w,h):
    x1, y1 = x-w/2, y-h/2
    x2, y2 = x+w/2, y+h/2
    return x1, x2, y1, y2








