import os
import math
import random
import json

import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from tkinter import filedialog

from PIL import Image
from PIL import ImageTk
from PIL import ImageOps

def Save():

    imageToEdit.save("Test.png")

def TestTiling():

    tileImage = Image.new(mode="RGB", size=(imageToEdit.width * 3, imageToEdit.height * 3))

    for x in range(3):

        for y in range(3):

            tileImage.paste(imageToEdit, (x * imageToEdit.width, y * imageToEdit.height))

    tileImage.show()

def ChooseColor():

    global brushColor

    colorCode = colorchooser.askcolor(title="Choose Brush Color")[0]

    if colorCode:

        brushColor = colorCode

def SetBrushList():

    listbox.delete(0, tk.END)

    index = 0

    for folderName in os.listdir(brushesPath):

        folder = os.path.join(brushesPath, folderName)

        if os.path.isdir(folder):

            listbox.insert(index, folderName)
            index += 1

def ItemsSelected(event):

    global brushSelectedInList

    brushSelectedInList = listbox.get(listbox.curselection()[0])

def SelectButtonPressed():

    if brushSelectedInList:

        LoadBrush(brushSelectedInList)

def RoundToNearest2(num):

    return math.ceil(num / 2) * 2

def RoundToNearest(x, num):

    return math.ceil(num / x) * x

def GetImageOffset(sliderX, sliderY):

    return (round(sliderX.get()), round(sliderY.get()))

def ChangeImage():

    global unPannedImage
    global imageToEdit

    fileDir = filedialog.askopenfilename(initialdir="/", title="Open Image", filetypes=[('Png Files', '*.png')])

    if fileDir:

        unPannedImage = Image.open(fileDir).convert("RGB")
        imageToEdit = unPannedImage.copy()

        changeOffsetSliderX.configure(to=round(unPannedImage.width / 2))
        changeOffsetSliderY.configure(to=round(unPannedImage.height / 2))

def SaveImage():

    file = filedialog.asksaveasfile(filetypes=[('Png Files', '*.png')], defaultextension=[('Png Files', '*.png')])
    imageToEdit.save(file.name)

def ScatterBrush():

    for i in range(RoundToNearest2(scatterBrushSlider.get())):

        RandomBrush()
        randomCoords = (random.randint(0, unPannedImage.width), random.randint(0, unPannedImage.height))

        ApplyBrush(imageToEdit, randomCoords, brushTx, brushMaskTx, brushColor)
        ApplyBrush(unPannedImage, OffsetMouseCoords(imageOffsetX, imageOffsetY, randomCoords), brushTx, brushMaskTx, brushColor)

def FloodFill():

    imageToEdit.paste(brushColor, (0, 0, imageToEdit.width, imageToEdit.height))
    unPannedImage.paste(brushColor, (0, 0, unPannedImage.width, unPannedImage.height))

def CreateBrush():

    path = os.path.join(brushesPath, brushNameInputBox.get())

    os.mkdir(path)

    dataFile = open(os.path.join(path, "Data.json"), "x")

    dataToAppend = {"texture": "Texture.png", "mask": "Mask.png", "has-variants": False}

    json.dump(dataToAppend, dataFile)

    dataFile.close()

    imageToEdit.save(os.path.join(path, "Mask.png"))

    textureToSave = Image.new(mode="RGB", size=imageToEdit.size, color=(0, 0, 0))
    textureToSave.save(os.path.join(path, "Texture.png"))

def StrToInt(string):

    try:

        int(string)

        return True

    except:

        return False

def CheckRandomScaleSpinBoxes():

    minValue = minRandScaleBox.get()
    maxValue = maxRandScaleBox.get()

    minIsInt = StrToInt(minValue)
    maxIsInt = StrToInt(maxValue)

    if not minIsInt:

        minRandScaleBox.set(16)

    if not maxIsInt:

        maxRandScaleBox.set(64)

    minValue = minRandScaleBox.get()
    maxValue = maxRandScaleBox.get()

    if int(minValue) < 4 or int(minValue) > 256:

        minRandScaleBox.set(16)

    if int(maxValue) < 4 or int(maxValue) > 256:

        maxRandScaleBox.set(64)

    if int(maxValue) < int(minValue):

        maxRandScaleBox.set(int(minValue))

def RandomBrush():

    global brushMaskTx
    global brushTx
    global brushDiameter
    global brushRotation

    if brushHasVariants:

        choiceIndex = random.randint(0, len(brushMaskList) - 1)

        brushMaskTx = brushMaskList[choiceIndex]
        brushTx = brushList[choiceIndex]

    if randomScalingEnabled:

        CheckRandomScaleSpinBoxes()

        brushDiameter = RoundToNearest2(random.randint(int(minRandScaleBox.get()), int(maxRandScaleBox.get())))

    if randomRotationEnabled:

        brushRotation = random.randint(0, 360)

def EnableStamp():

    global stampEnabled

    if stampEnabled:

        stampBtn.config(text="Enable Stamp")
        stampEnabled = False

    else:

        stampBtn.config(text="Disable Stamp")
        stampEnabled = True

def EnableRandomRotation():

    global randomRotationEnabled

    if randomRotationEnabled:

        randomRotationBtn.config(text="Enable Random Rotation")
        randomRotationEnabled = False

    else:

        randomRotationBtn.config(text="Disable Random Rotation")
        randomRotationEnabled = True

def EnableRandomScaling():

    global randomScalingEnabled

    if randomScalingEnabled:

        randomScalingBtn.config(text="Enable Random Scaling")
        randomScalingEnabled = False

    else:

        randomScalingBtn.config(text="Disable Random Scaling")
        randomScalingEnabled = True

window = tk.Tk()

menuBar = tk.Menu(window)

fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Save", command=SaveImage)
fileMenu.add_command(label="Open", command=ChangeImage)

toolsMenu = tk.Menu(menuBar, tearoff=0)
toolsMenu.add_command(label="Choose Color", command=ChooseColor)
#toolsMenu.add_command(label="Test Tiling", command=TestTiling)

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Tools", menu=toolsMenu)

canvas = tk.Canvas(window, bg="#1c1c1c", highlightthickness=0)
canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

toolbox = ttk.Frame(window)
toolbox.pack(expand=True, fill=tk.BOTH)

rows = []

for i in range(10):

    row = tk.Frame(toolbox)
    row.pack(side=tk.TOP)

    sep = ttk.Separator(toolbox, orient="horizontal")
    sep.pack(side=tk.TOP, fill=tk.X)
    
    rows.append(row)

listboxParent = tk.Frame(rows[0])
listboxParent.pack(side=tk.TOP)

listbox = tk.Listbox(
    listboxParent,
    width=25,
    height=6,
    selectmode=tk.EXTENDED
)

listbox.pack(side=tk.LEFT)
listbox.bind('<<ListboxSelect>>', ItemsSelected)

listboxScrollbar = ttk.Scrollbar(
    listboxParent,
    orient=tk.VERTICAL,
    command=listbox.yview
)

listbox['yscrollcommand'] = listboxScrollbar.set

listboxScrollbar.pack(side=tk.RIGHT, expand=True, fill=tk.Y)

selectBrushBtn = ttk.Button(rows[1], text="Select", command=SelectButtonPressed)
selectBrushBtn.pack(side=tk.LEFT)

refreshBrushBtn = ttk.Button(rows[1], text="Refresh", command=SetBrushList)
refreshBrushBtn.pack(side=tk.LEFT)

changeBrushDiameterText = tk.Label(rows[2], text="Brush Scale: ")
changeBrushDiameterText.pack(side=tk.TOP)

changeBrushDiameterSlider = ttk.Scale(rows[2], from_=4, to=256, orient=tk.HORIZONTAL)
changeBrushDiameterSlider.set(64)
changeBrushDiameterSlider.pack(side=tk.TOP)

brushRotationText = tk.Label(rows[2], text="Brush Rotation: ")
brushRotationText.pack(side=tk.TOP)

brushRotationSlider = ttk.Scale(rows[2], from_=0, to=360, orient=tk.HORIZONTAL)
brushRotationSlider.set(0)
brushRotationSlider.pack(side=tk.TOP)

changeOffsetText = tk.Label(rows[3], text="Image Offset: (0, 0) ")
changeOffsetText.pack(side=tk.TOP)

changeOffsetSliderX = ttk.Scale(rows[3], from_=0, to=256, orient=tk.HORIZONTAL)
changeOffsetSliderX.pack(side=tk.TOP)

changeOffsetSliderY = ttk.Scale(rows[3], from_=0, to=256, orient=tk.HORIZONTAL)
changeOffsetSliderY.pack(side=tk.TOP)

scatterBrushText = tk.Label(rows[4], text="Scatter Amount: ")
scatterBrushText.pack(side=tk.TOP)

scatterBrushSlider = ttk.Scale(rows[4], from_=4, to=256, orient=tk.HORIZONTAL)
scatterBrushSlider.set(16)
scatterBrushSlider.pack(side=tk.TOP)

scatterBrushBtn = ttk.Button(rows[5], text="Add Scatter", command=ScatterBrush)
scatterBrushBtn.pack(side=tk.LEFT)

floodFillBtn = ttk.Button(rows[5], text="Flood Fill", command=FloodFill)
floodFillBtn.pack(side=tk.LEFT)

createBrushText = tk.Label(rows[6], text="Create Brush")
createBrushText.pack(side=tk.TOP)

brushNameText = tk.Label(rows[6], text="Brush Name: ")
brushNameText.pack(side=tk.TOP)

brushNameInputBox = ttk.Entry(rows[6])
brushNameInputBox.pack(side=tk.TOP)

createBrushBtn = ttk.Button(rows[6], text="Add to Brushes", command=CreateBrush)
createBrushBtn.pack(side=tk.TOP)

stampBtn = ttk.Button(rows[7], text="Enable Stamp", command=EnableStamp)
stampBtn.pack(side=tk.TOP)

brushRateText = tk.Label(rows[7], text="Painting Rate: ")
brushRateText.pack(side=tk.TOP)

brushRateSlider = ttk.Scale(rows[7], from_=0, to=24, orient=tk.HORIZONTAL)
brushRateSlider.set(24)
brushRateSlider.pack(side=tk.TOP)

randomRotationBtn = ttk.Button(rows[8], text="Enable Random Rotation", command=EnableRandomRotation)
randomRotationBtn.pack(side=tk.TOP)

randomScalingBtn = ttk.Button(rows[8], text="Enable Random Scaling", command=EnableRandomScaling)
randomScalingBtn.pack(side=tk.TOP)

randomScalingText = tk.Label(rows[9], text="Random Scaling Range")
randomScalingText.pack(side=tk.TOP)

randScaleSpinboxes = tk.Frame(rows[9])
randScaleSpinboxes.pack(side=tk.TOP)

randomScalingMinText = tk.Label(randScaleSpinboxes, text="Min:")
randomScalingMinText.pack(side=tk.LEFT)

minRandScaleBox = ttk.Spinbox(randScaleSpinboxes, from_=4, to=256, width=5)
minRandScaleBox.set(16)
minRandScaleBox.pack(side=tk.LEFT)

randomScalingMaxText = tk.Label(randScaleSpinboxes, text="Max:")
randomScalingMaxText.pack(side=tk.LEFT)

maxRandScaleBox = ttk.Spinbox(randScaleSpinboxes, from_=4, to=256, width=5)
maxRandScaleBox.set(64)
maxRandScaleBox.pack(side=tk.LEFT)

window.config(menu=menuBar)

mouseDown = False
mouseOverImg = False
mouseCoords = (0, 0)

currentImage = None
currentImageCanvas = None

def OnImageMotion(event):

    global mouseCoords

    mouseCoords = (event.x, event.y)

def OnImageEnter(event):

    global mouseOverImg

    mouseOverImg = True

def OnImageLeave(event):

    global mouseOverImg

    mouseOverImg = False

def MouseDown(event):

    global mouseDown

    if brushSelected:

        RandomBrush()

    mouseDown = True

def MouseUp(event):

    global mouseDown

    if brushSelected and stampEnabled and mouseDown and mouseOverImg:

        ApplyBrush(imageToEdit, mouseCoords, brushTx, brushMaskTx, brushColor)
        ApplyBrush(unPannedImage, OffsetMouseCoords(imageOffsetX, imageOffsetY, mouseCoords), brushTx, brushMaskTx, brushColor)

    mouseDown = False

canvas.bind("<Motion>", OnImageMotion)
canvas.bind("<ButtonPress-1>", MouseDown)
canvas.bind("<ButtonRelease-1>", MouseUp)

def LoadImageToScreen(image):

    global currentImage
    global currentImageCanvas

    currentImage = ImageTk.PhotoImage(image)

    if currentImageCanvas:

        canvas.coords(currentImageCanvas, imagePosOffsetX, imagePosOffsetY)
        canvas.itemconfig(currentImageCanvas, image=currentImage)

    else:

        currentImageCanvas = canvas.create_image(imagePosOffsetX, imagePosOffsetY, image=currentImage, anchor=tk.NW)

        canvas.tag_bind(currentImageCanvas, "<Enter>", OnImageEnter)
        canvas.tag_bind(currentImageCanvas, "<Leave>", OnImageLeave)

def ApplyBrush(image, coords, brush, brushMask, color):

    scopeX = image.width
    scopeY = image.height

    midX = coords[0]
    posX = coords[0] + scopeX
    negX = coords[0] - scopeX

    midY = coords[1]
    posY = coords[1] + scopeY
    negY = coords[1] - scopeY

    xPlots = [midX, posX, negX]
    yPlots = [midY, posY, negY]

    coloredBrush = ImageOps.colorize(brush, black=color, white=(255, 255, 255))

    resizedBrushMask = brushMask.copy().resize((brushDiameter, brushDiameter)).rotate(brushRotation, expand=True)
    resizedBrush = coloredBrush.copy().resize((brushDiameter, brushDiameter)).rotate(brushRotation, expand=True)

    rotatedDiameter = resizedBrushMask.width

    for x in xPlots:

        for y in yPlots:

            image.paste(resizedBrush, (RoundToNearest(brushSnap, (x - imagePosOffsetX)) - round(rotatedDiameter / 2), RoundToNearest(brushSnap, (y - imagePosOffsetY)) - round(rotatedDiameter / 2)), resizedBrushMask)

def BrushVariants(image, variantSize):

    sizeX = variantSize[0]
    sizeY = variantSize[1]

    imgSizeX = image.width
    imgSizeY = image.height

    framesX = math.floor(imgSizeX / sizeX)
    framesY = math.floor(imgSizeY / sizeY)

    variants = []

    for x in range(framesX):

        for y in range(framesY):

            variants.append(image.crop((x * sizeX, y * sizeY, x * sizeX + sizeX, y * sizeY + sizeY)).convert("L"))

    return variants

def LoadBrush(brushName):

    global brushMaskList, brushList, brushMaskTx, brushTx, brushSelected, brushHasVariants

    specifiedBrush = os.path.join(brushesPath, brushName)
    dataFile = open(os.path.join(specifiedBrush, "Data.json"))

    data = json.load(dataFile)

    dataFile.close()

    maskImg = Image.open(os.path.join(specifiedBrush, data["mask"]))
    textureImg = Image.open(os.path.join(specifiedBrush, data["texture"]))

    brushHasVariants = data["has-variants"]

    if brushHasVariants:

        rawVariantSize = data["variant-size"]
        variantSize = (rawVariantSize["x"], rawVariantSize["y"])

        brushMaskList = BrushVariants(maskImg, variantSize)
        brushList = BrushVariants(textureImg, variantSize)

        brushMaskTx = brushMaskList[0]
        brushTx = brushList[0]

    else:

        brushMaskTx = maskImg.convert("L")
        brushTx = textureImg.convert("L")

    brushSelected = True

def OffsetImage(x, y):

    global imageToEdit

    pannedImage = Image.new(mode="RGB", size=imageToEdit.size)
    
    scopeX = imageToEdit.width
    scopeY = imageToEdit.height

    croppedImageRightSide = unPannedImage.crop((x, 0, scopeX, scopeY))
    croppedImageLeftSide = unPannedImage.crop((0, 0, x, scopeY))
    
    pannedImage.paste(croppedImageRightSide, (0, 0))
    pannedImage.paste(croppedImageLeftSide, (scopeX - x, 0))

    croppedImageBottomSide = pannedImage.crop((0, y, scopeX, scopeY))
    croppedImageTopSide = pannedImage.crop((0, 0, scopeX, y))

    pannedImage.paste(croppedImageBottomSide, (0, 0))
    pannedImage.paste(croppedImageTopSide, (0, scopeY - y))

    imageToEdit = pannedImage

def OffsetMouseCoords(offsetX, offsetY, coords):

    return (coords[0] + offsetX, coords[1] + offsetY)

def OnKeyDown(event):

    global imageMoveXSpeed
    global imageMoveYSpeed

    key = event.char

    if key == "w":

        imageMoveYSpeed = 1

    if key == "s":

        imageMoveYSpeed = -1

    if key == "a":

        imageMoveXSpeed = 1

    if key == "d":

        imageMoveXSpeed = -1

def OnKeyUp(event):

    global imageMoveXSpeed
    global imageMoveYSpeed

    key = event.char

    if key == "w":

        imageMoveYSpeed = 0

    if key == "s":

        imageMoveYSpeed = 0

    if key == "a":

        imageMoveXSpeed = 0

    if key == "d":

        imageMoveXSpeed = 0

window.bind('<KeyPress>', OnKeyDown)
window.bind('<KeyRelease>', OnKeyUp)

brushesPath = os.path.join(os.getcwd(), "Brushes")

brushSelectedInList = None

brushMaskList = None
brushList = None

brushMaskTx = None
brushTx = None

brushSelected = False
brushHasVariants = False

stampEnabled = False
randomRotationEnabled = False
randomScalingEnabled = False

brushColor = (0, 0, 0)
prevOffsetX = 0
prevOffsetY = 0

brushRotation = 0
brushDiameter = 64

brushSnap = 1

imageMoveXSpeed = 0
imageMoveYSpeed = 0

imagePosOffsetX = 0
imagePosOffsetY = 0

SetBrushList()
LoadBrush("Circle Brush")

unPannedImage = Image.new(mode="RGB", size=(512, 512), color=(255, 255, 255))
imageToEdit = unPannedImage.copy()

ticksPerOneBrush = 0
brushTick = 0

while True:

    imageOffsetX, imageOffsetY = GetImageOffset(changeOffsetSliderX, changeOffsetSliderY)

    if brushSelected:

        if mouseDown and mouseOverImg and stampEnabled == False:

            if brushTick >= ticksPerOneBrush:

                brushTick = 0
                ApplyBrush(imageToEdit, mouseCoords, brushTx, brushMaskTx, brushColor)
                ApplyBrush(unPannedImage, OffsetMouseCoords(imageOffsetX, imageOffsetY, mouseCoords), brushTx, brushMaskTx, brushColor)

    brushTick += 1

    LoadImageToScreen(imageToEdit)

    changeBrushDiameterText.configure(text="Brush Scale: {}".format(RoundToNearest2(changeBrushDiameterSlider.get())))
    scatterBrushText.configure(text="Scatter Amount: {}".format(RoundToNearest2(scatterBrushSlider.get())))
    brushRateText.configure(text="Painting Rate: {}".format(round(brushRateSlider.get())))
    brushRotationText.configure(text="Brush Rotation: {}".format(round(brushRotationSlider.get())))

    if prevOffsetX != imageOffsetX or prevOffsetY != imageOffsetY:

        OffsetImage(imageOffsetX, imageOffsetY)

        prevOffsetX = imageOffsetX
        prevOffsetY = imageOffsetY

        changeOffsetText.configure(text="Image Offset: ({}, {})".format(imageOffsetX, imageOffsetY))        

    brushDiameterSliderValue = RoundToNearest2(changeBrushDiameterSlider.get())

    if brushDiameterSliderValue != brushDiameter and randomScalingEnabled == False:

        brushDiameter = brushDiameterSliderValue

    brushRateSliderValue = 24 - round(brushRateSlider.get())

    if brushRateSliderValue != ticksPerOneBrush:

        ticksPerOneBrush = brushRateSliderValue

    brushRotationSliderValue = round(brushRotationSlider.get())

    if brushRotationSliderValue != brushRotation and randomRotationEnabled == False:

        brushRotation = brushRotationSliderValue

    imagePosOffsetX += imageMoveXSpeed
    imagePosOffsetY += imageMoveYSpeed

    window.update()