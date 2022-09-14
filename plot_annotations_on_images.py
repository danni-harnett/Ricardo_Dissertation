# File used for plotting
# See README: Section 2.

from PIL import Image
import matplotlib.pyplot
import matplotlib.pyplot as plt


def convert(size, box):  # Convert pixel to YOLO coordinates // Input format: xmin, xmax, ymin, ymax
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    # Plotting does not require the normalisation seen in the other convert function
    return ([x,y,w,h])


# SET BY USER:
path = "/Users/danniharnett/Desktop/DATA_FOR_DIS/Useful_images/"  # path to useful_images directory
image_number = 2543
image_coords = (1126,1501,1158,1523)


# Prepare image
image_number = str(image_number)
path_to_image = path+("/%s.jpeg")%(image_number)
im = Image.open(path_to_image)
w = int(im.size[0])
h = int(im.size[1])

# Prepare coordinates
xmin, ymin, xmax, ymax = image_coords
b = (xmin, xmax, ymin, ymax)
bb = convert((w,h), b) # convert image coords to yolo



img = matplotlib.image.imread(path_to_image)
figure, ax = plt.subplots(1)

# matplotlib plots rectangles from the (xy) coords of the upper left corner. we have the centre (xy) so need to convert:
upper_left_x = (bb[0] - (bb[2]/2))  # x centre - (width / 2)
upper_left_y = (bb[1] + (bb[3]/2))  # y centre - (height / 2)


# plot rectangle using coordinates
rect = matplotlib.patches.Rectangle((upper_left_x, upper_left_y), bb[2], -(bb[3]), edgecolor='r', facecolor="none")
ax.imshow(img)
ax.add_patch(rect)
plt.gca().invert_yaxis()
plt.show()









