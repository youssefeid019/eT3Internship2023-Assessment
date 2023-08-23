# imports
import glob
import os
import datetime
import csv


# Move and rename function
def refactorFunction(oldPath, newPath):
    # Get List of all images
    files = glob.glob(oldPath + '/**/*.jpg', recursive=True)
    count = 0

    # For each image
    for file in files:
        # Get the file extension
        fileExtension = os.path.splitext(file)[1]

        # Generate the new filename with the format "imageX.jpg"
        newFilename = f"image{count + 1}{fileExtension}"

        # Construct the destination path
        destination = os.path.join(newPath, newFilename)

        # Check if the source file exists before attempting to rename
        if os.path.exists(file):
            # Rename the file with os.rename
            os.rename(file, destination)
            count += 1
        else:
            print(f"Source file not found: {file}")


# Image info function

def getImagesInfo(imagesPath):
    imagesInfoList = []  # Initialize an empty list to store image information

    allImages = os.listdir(imagesPath)
    # Sort the list of image filenames numerically
    allImages.sort(key=lambda x: int(x.split('image')[1].split('.jpg')[0]))
    for image in allImages:
        # Construct the full path to the image
        imagePath = os.path.join(imagesPath, image)

        # Get image size in bytes
        imageSize = os.path.getsize(imagePath)

        # Get the last modification date and time as a timestamp
        modificationTime = os.path.getmtime(imagePath)

        # Convert the timestamp to a readable date and time
        modificationDate = datetime.datetime.fromtimestamp(modificationTime)
        modificationDateStr = modificationDate.strftime('%a %b %d %H:%M:%S %Y')

        # Create a dictionary for the image information
        imageInfo = {'Name': image, 'Size (bytes)': imageSize, 'Last Modification Date': modificationDateStr}

        # Add the image info dictionary to the list
        imagesInfoList.append(imageInfo)

    return imagesInfoList


# Save to csv function

def saveToCsv(imagesInfoList, csvFileName):
    if imagesInfoList:
        # Define the column names
        columnNames = ['Name', 'Size (bytes)', 'Last Modification Date']

        # Open the CSV file for writing
        with open(csvFileName, mode='w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=columnNames)

            # Write the header row
            writer.writeheader()

            # Write the image information
            for imageInfo in imagesInfoList:
                writer.writerow(imageInfo)


# Define old path & new path
# Location of images
oldPath = "./dairies/"
# Location to move images to
newPath = "./allImages/"

refactorFunction(oldPath, newPath)
imagesInforList = getImagesInfo(newPath)
saveToCsv(imagesInforList, "imagesInfo.csv")
