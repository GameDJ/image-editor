# This is a sample Python script.
import math
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#https://note.nkmk.me/en/python-numpy-image-processing/
#https://pillow.readthedocs.io/en/stable/handbook/tutorial.html

import sys
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
# from matplotlib import pyplot as plt

# Load an image
def load_image(path: str) -> np.ndarray:
    # image = Image.open(path).convert('L')  # Convert to grayscale
    image = Image.open(path).convert('RGB')  # Convert to RGB
    return np.array(image)
# def load_image(path: str) -> (list, int):
#     # image = Image.open(path).convert('L')  # Convert to grayscale
#     image = Image.open(path).convert('RGB')  # Convert to RGB
#     imageList = list(image.getdata())
#     image_2d = []
#     cur_row = []
#     # for row_index in range(image.height):
#     #     image_2D.append(imageList[image.width: row_index * image.width])
#     for i in range(len(imageList)):
#         # convert current row to a list of lists (row of RGBs)
#         cur_row.append([imageList[i][0], imageList[i][1], imageList[i][2]])
#         # add end of row, add it to the full 2D array
#         if i % image.width == i:
#             image_2d.append(cur_row)
#             cur_row = []
#     return image_2d

# Save a 2D array as an image
def save_image(array: np.ndarray, path: str):
    image = Image.fromarray(array)
    image.save(path)

# def save_image(array: list, path: str):
#     for row in array:
#         print("[", end="")
#         for pixel in row:
#             print("[", end="")
#             print(hex(pixel[0]) + "," + hex(pixel[1]) + "," + hex(pixel[1]), end="")
#             print("] ", end="")
#         print("]")


# Invert an image (RGB)
def invert_image(image_array: np.ndarray) -> np.ndarray:
    return 255 - image_array

def quinn_test(image_array: np.ndarray) -> np.ndarray:
    # return np.flip(image_array, axis = 0) # flip vertical (flip rows)
    return np.flip(image_array, axis = 1) # flip horizontal (flip columns)

def addison_test(image_array: np.ndarray) -> np.ndarray:
    return image_array

def will_test(image_array: np.ndarray) -> np.ndarray:
    return image_array

# def invert_image(image_array: list) -> list:
#     for row in image_array:
#         for pixel in row:
#             for channel_index in range(3):
#                 pixel[channel_index] = 255 - pixel[channel_index]
#     return image_array

# # Apply a threshold to an RGB image (per channel)
# def threshold_image(image_array: np.ndarray, threshold: int) -> np.ndarray:
#     return np.where(image_array > threshold, 255, 0).astype(np.uint8)
#
# # Apply a custom filter to an RGB image
# def apply_filter(image_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
#     from scipy.signal import convolve2d
#     # Initialize an empty array to store the filtered channels
#     filtered_image = np.zeros_like(image_array)
#     # Apply the filter to each channel
#     for i in range(3):  # 3 channels for RGB
#         filtered_image[:, :, i] = convolve2d(image_array[:, :, i], kernel, mode='same', boundary='fill', fillvalue=0).astype(np.uint8)
#     return filtered_image

# def redden(image_array: np.ndarray, shift: int) -> np.ndarray:
#     with np.nditer(image_array, op_flags=["readwrite"]) as iterator:
#         for x in iterator:
#             x += shift
#     return image_array

def show_image(image_array: np.ndarray):
    # convert array to PIL Image
    image = Image.fromarray(image_array)
    # initialize toplevel tkinter widget
    window = tk.Tk()
    window.title("Image Processor")

    # use ImageTk library to convert PIL image to Tk image
    tk_image = ImageTk.PhotoImage(image)

    # create a label to hold the image
    img_preview = tk.Label(window, image=tk_image)
    # give the widget to the packer (geometry manager)
    img_preview.pack()

    def handle_button_press():
        window.destroy()

    def invert():
        my_image_array = invert_image(image_array)
        my_image = Image.fromarray(my_image_array)
        my_tk_image = ImageTk.PhotoImage(my_image)
        # update the image label
        img_preview.config(image=my_tk_image)
        # prevent garbage collector from deleting image?
        img_preview.image = my_tk_image
        
    def quinn():
        my_image_array = quinn_test(image_array)
        my_image = Image.fromarray(my_image_array)
        my_tk_image = ImageTk.PhotoImage(my_image)
        # update the image label
        img_preview.config(image=my_tk_image)
        # prevent garbage collector from deleting image?
        img_preview.image = my_tk_image
        
    def addison():
        my_image_array = addison_test(image_array)
        my_image = Image.fromarray(my_image_array)
        my_tk_image = ImageTk.PhotoImage(my_image)
        # update the image label
        img_preview.config(image=my_tk_image)
        # prevent garbage collector from deleting image?
        img_preview.image = my_tk_image
        
    def will():
        my_image_array = will_test(image_array)
        my_image = Image.fromarray(my_image_array)
        my_tk_image = ImageTk.PhotoImage(my_image)
        # update the image label
        img_preview.config(image=my_tk_image)
        # prevent garbage collector from deleting image?
        img_preview.image = my_tk_image

    button = tk.Button(text="Invert", command=invert)
    button.pack()
    button = tk.Button(text="Quinn", command=quinn)
    button.pack()
    button = tk.Button(text="Addison", command=addison)
    button.pack()
    button = tk.Button(text="Will", command=will)
    button.pack()

    button = tk.Button(text="Close window", command=handle_button_press)
    button.pack()

    # display the window
    window.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # Load the image
    # img_array = load_image('grd.png')
    img_array = load_image(sys.argv[1])
    # print(sys.argv)
    # try changing first pixel
    new_img_array = img_array
    if len(sys.argv) > 2:
        if sys.argv[2] == "invert":
            new_img_array = invert_image(img_array)
        elif sys.argv[2] == "quinn":
            new_img_array = quinn_test(img_array)
        elif sys.argv[2] == "addison":
            new_img_array = addison_test(img_array)
        new_file_name = sys.argv[1]
        save_image(new_img_array, '.png')
    else:
        # no direct command given; bring up GUI
        show_image(new_img_array)
    # elif sys.argv[2] == "redden":
    #     new_img_array = redden(img_array, int(sys.argv[3]))

    # this previews a blown-up version of the image but has a white margin...
    # plt.rcParams['toolbar'] = 'None'
    # plt.imshow(new_img_array, interpolation='nearest')
    # plt.axis('off')
    # plt.tight_layout()
    # plt.show()

    # this previews the image in the OS image viewer...
    # img_preview = Image.fromarray(new_img_array)
    # img_preview.show()


    #save_image(new_img_array, 'filtered_image.png')

    # # Invert the image
    # inverted_image = invert_image(img_array)
    # save_image(inverted_image, 'inverted_image.jpg')
    #
    # # Apply thresholding
    # thresholded_image = threshold_image(img_array, 128)
    # save_image(thresholded_image, 'thresholded_image.jpg')
    #
    # # Apply a simple edge detection filter
    # edge_detection_kernel = np.array([[-1, -1, -1],
    #                                   [-1, 8, -1],
    #                                   [-1, -1, -1]])
    # filtered_image = apply_filter(img_array, edge_detection_kernel)
    # save_image(filtered_image, 'filtered_image.jpg')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
