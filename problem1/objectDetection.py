import torchvision
from torchvision.ops import nms
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from torchvision.transforms import functional as F
from PIL import Image
import os
import json

# images folder
fileDir=os.path.dirname(os.path.realpath(__file__))
imageFolder = os.path.join(fileDir, 'allImages')
txtFolder = 'ImagesTxtFiles'
# list of all images
images = [f for f in os.listdir(imageFolder) if os.path.isfile(os.path.join(imageFolder, f))]

def objDetection(images,imageFolder):
    # Load the pretrained model
    model = fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.COCO_V1)
    model.eval()
    count = 0

    for image in images:

        # Load image
        imagePath = os.path.join(imageFolder, image)
        img = Image.open(imagePath)

        # Apply transformations
        imageTensor = F.to_tensor(img)
        imageTensor = imageTensor.unsqueeze(0)  

        # Perform inference
        with torch.no_grad():
            predictions = model(imageTensor)

        # Extract bounding boxes, labels, and scores
        boxes = predictions[0]['boxes']
        labels = predictions[0]['labels']
        scores = predictions[0]['scores']
        filteredIndices = nms(boxes, scores, 0.2)
        filteredBoxes = boxes[filteredIndices]
        filteredLabels = labels[filteredIndices]
        filteredScores = scores[filteredIndices]

        # Display image
        plt.figure()
        plt.imshow(img)
        ax = plt.gca()

        result = torch.cat((filteredLabels.unsqueeze(1), filteredBoxes), dim=1)
        toTxt(result=result,index=count)

        # Add bounding boxes to the image
        for box, label in zip(filteredBoxes, filteredLabels):
            x, y, w, h = box
            rect = patches.Rectangle((x, y), w - x, h - y, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            plt.text(x, y, f'Label: {label}', color='r')

        plt.savefig(f"imagesResult/image{count+1}.jpg")

        count += 1
def toTxt(result,index): 
    #tensor to string
    resultList=result.tolist()
    resultStr = "\n".join([" ".join(map(str, row)) for row in resultList])

    # Write the string to a file
    with open(f"ImagesTxtFiles/image{index+1}.txt", "w") as file:
        file.write(resultStr)
def convertToJson(txtFolder):
    # List of all files
    txtFiles = [f for f in os.listdir(txtFolder) if f.endswith('.txt')]

    # Loop through the text files
    for txtFile in txtFiles:
        #full path to text file
        txtFilePath = os.path.join(txtFolder, txtFile)

        # Read the content of the text file
        with open(txtFilePath, 'r') as file:
            lines = file.readlines()

        # Create a JSON file with the same name as the text file but with a .json extension
        jsonFileName = os.path.splitext(txtFile)[0] + '.json'
        jsonFilePath = os.path.join(txtFolder, jsonFileName)

        # Extract data from the text file and create JSON data
        annotations = []
        for line in lines:
            values = line.strip().split()  # Split based on whitespace
            if len(values) >= 5:
                x, y, width, height = map(float, values[1:5])  # Extract data from the 2nd to 5th columns
                annotation = {
                    "result": [
                        {
                            "image_rotation": 0,
                            "value": {
                                "x": x,
                                "y": y,
                                "width": width,
                                "height": height,
                                "rotation": 0,
                                "rectanglelabels": ["object"]
                            }
                        }
                    ]
                }
                annotations.append(annotation)

        jsonData = {
            "annotations": annotations,
            "data": {
                "image": f"imagesResult/{os.path.splitext(txtFile)[0]}.jpg"  # Change this path as needed
            }
        }

        # Write the JSON data to the JSON file
        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(jsonData, jsonFile, indent=4)

        print(f'Created JSON file: {jsonFilePath}')
objDetection(images=images,imageFolder=imageFolder)
convertToJson(txtFolder=txtFolder)