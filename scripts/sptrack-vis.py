from PyQt5.QtCore import *
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
import math
import json
# Only needed for access to command line arguments
import sys
import time
import os

mainWindow = None

turn_alpha = math.pi/180*15
turn_beta = math.pi/180*15

sc = 10000

def main():
    app = QApplication(sys.argv)
 
    # create the instance of our Window
    mainWindow = MainWindow()
    mainWindow.fileNameLineEdit.setText("data/greedy_data_9.json")
    mainWindow.boxRotLineEdit.setText("15 15 0")
    # showing the window
    mainWindow.show()
 
    # start the app
    sys.exit(app.exec())

def get_svg_code(fileName, image_size, boxrot):
    #fileName = mainWindow.fileNameLineEdit.getText()

    path = {}
    # open the file and read the contents as json
    with open(fileName, 'r') as myfile:
        data=myfile.read()
        # convert the json to a python dictionary
        path = json.loads(data)


    # computer center of all sats that need to be plotted
    center = [0,0,0]
    for sat in path:
        for i in range(3):
            center[i] += sat["pos"][i]
    
    for i in range(3):
        center[i] /= len(path)

    # compute the dims for the path
    dims = 0
    for sat in path:
        for i in range(3):
            dims = max(dims, abs(sat["pos"][i] - center[i]))
    dims = dims * 1.1

    # create a box around the path
    box = []
    box.append([+dims, +dims, +dims])
    box.append([-dims, +dims, +dims])
    box.append([-dims, -dims, +dims])
    box.append([+dims, -dims, +dims])

    box.append([+dims, +dims, -dims])
    box.append([-dims, +dims, -dims])
    box.append([-dims, -dims, -dims])
    box.append([+dims, -dims, -dims])

    # transform the sat coords to the center, rotate them and store them in sat_path
    sat_path = []
    for sat in path:
        for i in range(3):
            sat["pos"][i] = sat["pos"][i] - center[i]
        sat_path.append(rotatec(sat["pos"], boxrot))
    
    # rotate the box
    new_box = []
    for corner in box:
        new_box.append(rotatec(corner, boxrot))

    # compute new center of box new_box
    new_center = [0,0,0]
    for corner in new_box:
        for i in range(3):
            new_center[i] += corner[i]

    for i in range(3):
        new_center[i] /= len(new_box)
    
    # compute the dimensions of the new_box
    dims = 0
    for corner in new_box:
        for i in range(3):
            dims = max(dims, abs(corner[i] - new_center[i]))
    
    dims = dims * 1.1
    
    # compute the scale factor
    sc = image_size / dims / 2.05

    # scale the sat_path coords
    for sat in sat_path:
        for i in range(3):
            sat[i] = int((sat[i] - new_center[i]) * sc + image_size/2.0)

    # scale the box coords
    for corner in new_box:
        for i in range(3):
            corner[i] = int((corner[i] - new_center[i]) * sc + image_size/2.0)


    box_center = [int(image_size/2.0) for i in range(3)]

    # create the svg code
    my_svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" >
        <g color="green">
        <rect x="0" y="0" width="{image_size}" height="{image_size}" fill="white" stroke="gray"/>"""
    
    # braw a 3D box between center +- dims
    # 1
    #boxrot = [0,0,0]
    # print(image_size, center, dims, boxrot)
    
    # line between 0 and 1, 1 and 2, 2 and 3, 3 and 0
    my_svg_code += f"""<line x1="{new_box[0][0]}" y1="{new_box[0][1]}" x2="{new_box[1][0]}" y2="{new_box[1][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[1][0]}" y1="{new_box[1][1]}" x2="{new_box[2][0]}" y2="{new_box[2][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[2][0]}" y1="{new_box[2][1]}" x2="{new_box[3][0]}" y2="{new_box[3][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[3][0]}" y1="{new_box[3][1]}" x2="{new_box[0][0]}" y2="{new_box[0][1]}" stroke="gray" />"""

    # line between 4 and 5, 5 and 6, 6 and 7, 7 and 4
    my_svg_code += f"""<line x1="{new_box[4][0]}" y1="{new_box[4][1]}" x2="{new_box[5][0]}" y2="{new_box[5][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[5][0]}" y1="{new_box[5][1]}" x2="{new_box[6][0]}" y2="{new_box[6][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[6][0]}" y1="{new_box[6][1]}" x2="{new_box[7][0]}" y2="{new_box[7][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[7][0]}" y1="{new_box[7][1]}" x2="{new_box[4][0]}" y2="{new_box[4][1]}" stroke="gray" />"""

    # line between 0 and 4, 1 and 5, 2 and 6, 3 and 7
    my_svg_code += f"""<line x1="{new_box[0][0]}" y1="{new_box[0][1]}" x2="{new_box[4][0]}" y2="{new_box[4][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[1][0]}" y1="{new_box[1][1]}" x2="{new_box[5][0]}" y2="{new_box[5][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[2][0]}" y1="{new_box[2][1]}" x2="{new_box[6][0]}" y2="{new_box[6][1]}" stroke="gray" />"""
    my_svg_code += f"""<line x1="{new_box[3][0]}" y1="{new_box[3][1]}" x2="{new_box[7][0]}" y2="{new_box[7][1]}" stroke="gray" />"""

    psat = box_center
    for sat in sat_path:
        # compute the color based on the sat[2]
        colorDepth = int((dims-sat[2])/dims*255)
        color = f"#FF{colorDepth:02X}{colorDepth:02X}"
        
        # radius of the circle based on sat[2]
        radius = int((sat[2])/dims*20)


        my_svg_code += f"""<circle cx="{sat[0]}" cy="{sat[1]}" r="{radius}" fill="{color}"/>"""
        # line between pcoords and coords <line x1="0" y1="80" x2="100" y2="20" stroke="black" />
        my_svg_code += f"""<line x1="{psat[0]}" y1="{psat[1]}" x2="{sat[0]}" y2="{sat[1]}" stroke="blue" />"""
        psat = sat
        
    my_svg_code += """ </g>
        </svg>"""

    return my_svg_code

class MainWindow(QDialog):
 
    # constructor
    def __init__(self):
        super(MainWindow, self).__init__()
 
        # setting window title
        self.setWindowTitle("Space Track Visualizer")
 
        # setting geometry to the window
        self.setGeometry(0, 0, 800, 800)
 
        self.formGroupBox = QGroupBox("Visualizer")
        self.fileNameLineEdit = QLineEdit()
        self.outFileNameEdit = QLineEdit()
        self.boxRotLineEdit = QLineEdit()
        

        self.svgBox = QSvgWidget()

        self.svgBox.setGeometry(0,0,800,800)
        #self.svgBox.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.svgBox.setFixedSize(800,800)
        

        # calling the method that create the form
        self.createForm()
 
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
 
        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.updateImage)
        #self.buttonBox.clicked.connect(self.updateImage)
        # adding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)


        self.rotLeftButton = QPushButton("Left")
        self.rotLeftButton.clicked.connect(self.rotLeft)
        self.rotRightButton = QPushButton("Right")
        self.rotRightButton.clicked.connect(self.rotRight)
        self.rotUpButton = QPushButton("Up")
        self.rotUpButton.clicked.connect(self.rotUp)
        self.rotDownButton = QPushButton("Down")
        self.rotDownButton.clicked.connect(self.rotDown)

        self.saveFileButton = QPushButton("Save File")
        self.saveFileButton.clicked.connect(self.saveFile)
        # creating a vertical layout
        mainLayout = QVBoxLayout()
 
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
 
        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)
        
        mainLayout.addWidget(self.rotLeftButton)
        mainLayout.addWidget(self.rotRightButton)
        mainLayout.addWidget(self.rotUpButton)
        mainLayout.addWidget(self.rotDownButton)
        mainLayout.addWidget(self.saveFileButton)

        # setting lay out
        self.setLayout(mainLayout)
 
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        size = self.geometry()
        self.image_size = min(size.width(), size.height()-150) - 100
        self.svgBox.setFixedSize(self.image_size,self.image_size)
       
        return super().resizeEvent(a0)
    
    def rotLeft(self):
        boxRot = self.boxRotLineEdit.text().split()
        if len(boxRot)==3:
            boxRot[0] = int(boxRot[0]) + 5
            self.boxRotLineEdit.setText(f"{boxRot[0]} {boxRot[1]} {boxRot[2]} ")    
            self.updateImage()

    def rotRight(self):
        boxRot = self.boxRotLineEdit.text().split()
        boxRot[0] = int(boxRot[0]) - 5
        self.boxRotLineEdit.setText(f"{boxRot[0]} {boxRot[1]} {boxRot[2]} ")    
        self.updateImage()

    def rotUp(self):
        boxRot = self.boxRotLineEdit.text().split()
        if len(boxRot)==3:
            boxRot[1] = int(boxRot[1]) + 5
            self.boxRotLineEdit.setText(f"{boxRot[0]} {boxRot[1]} {boxRot[2]} ")    
            self.updateImage()

    def rotDown(self):
        boxRot = self.boxRotLineEdit.text().split()
        if len(boxRot)==3:
            boxRot[1] = int(boxRot[1]) - 5
            self.boxRotLineEdit.setText(f"{boxRot[0]} {boxRot[1]} {boxRot[2]} ")    
            self.updateImage()

    def saveFile(self):
        outFileName = self.outFileNameEdit.text()
        
        # if outfileName is empty, generate it using fileNameLineEdit and change extension to svg
        if (outFileName == ""): 
            base_name, _ = os.path.splitext(self.fileNameLineEdit.text())
            outFileName = f"{base_name}.svg"

        boxRot = self.boxRotLineEdit.text().split()
        for i in range(len(boxRot)):
            boxRot[i] = float(boxRot[i])
            boxRot[i] = math.pi/180*boxRot[i]
        
        svg_code = get_svg_code(self.fileNameLineEdit.text(), self.image_size, boxRot)
        
        with open(outFileName, 'w') as file:
            file.write(svg_code)
    # -- end of function

    # get info method called when form is accepted
    def updateImage(self):
        # get the boxrot
        boxRot = self.boxRotLineEdit.text().split()
        for i in range(len(boxRot)):
            boxRot[i] = float(boxRot[i])
            boxRot[i] = math.pi/180*boxRot[i]

        svg_bytes = bytearray(get_svg_code(self.fileNameLineEdit.text(), self.image_size,  boxRot), encoding='utf-8')
        self.svgBox.renderer().load(svg_bytes)
        

 
    # create form method
    def createForm(self):
 
        # creating a form layout
        overallLayout = QGridLayout()
        layout = QFormLayout()
 
        # box center, dims and line edit
        layout.addRow(QLabel("File Name"), self.fileNameLineEdit)
        layout.addRow(QLabel("Out File Name"), self.outFileNameEdit)
        layout.addRow(QLabel("Box Rot"), self.boxRotLineEdit)
        #layout.addRow(self.rotLeftButton)


        # SVG Box
        overallLayout.addWidget(self.svgBox, 1, 0)
        overallLayout.addLayout(layout, 0, 0)
        overallLayout.setColumnStretch(1, 0)

        #layout.addRow(QLabel("Box Rot"), self.boxRotLineEdit)
        # setting layout
        self.formGroupBox.setLayout(overallLayout)
 
def tr(coords, sz, pcenter, dims, rot, name="POINT"):
    x = coords[0]
    y = coords[1]
    z = coords[2]

    print(f"-- {name} Input {x:.2f},{y:.2f},{z:.2f}, {sz} {pcenter} {dims} {rot}")
    distxy = math.sqrt(x**2 + y**2)
    alphaxy = math.atan2(y, x)
    #print (f"distxy {alphaxy} + {rot[0]}")
    x1 = distxy * math.cos(alphaxy + rot[0])
    y1 = distxy * math.sin(alphaxy + rot[0])
    z1 = z

    print(f"First {x1:.2f},{y1:.2f},{z1:.2f}")

    distyz = math.sqrt(y1**2 + z1**2)
    alphayz = math.atan2(z1, y1)

    x2 = x1
    y2 = distyz * math.cos (alphayz + rot[1])
    z2 = distyz * math.sin (alphayz + rot[1])

    print(f"Second {x2:.2f},{y2:.2f},{z2:.2f}")



    sc = dims

    new_coords = [x2,y2,z2]
    for i in range(3):
        new_coords[i] = int((new_coords[i]-pcenter[i]) * sz/sc/2.0 + sz/2.0)
    
    print (f"-- Output {new_coords}")
    return new_coords

def rotatec(coords, rot):
    x = coords[0]
    y = coords[1]
    z = coords[2]

    print(f"-- Input {x:.2f},{y:.2f},{z:.2f}, {rot}")
    distxy = math.sqrt(x**2 + y**2)
    alphaxy = math.atan2(y, x)
    
    x1 = distxy * math.cos(alphaxy + rot[0])
    y1 = distxy * math.sin(alphaxy + rot[0])
    z1 = z

    print(f"First {x1:.2f},{y1:.2f},{z1:.2f}")

    distyz = math.sqrt(y1**2 + z1**2)
    alphayz = math.atan2(z1, y1)

    x2 = x1
    y2 = distyz * math.cos (alphayz + rot[1])
    z2 = distyz * math.sin (alphayz + rot[1])

    print(f"Second {x2:.2f},{y2:.2f},{z2:.2f}")

    distxz = math.sqrt(x2**2 + z2**2)
    alphaxz = math.atan2(z2, x2)

    x3 = distxz * math.cos (alphaxz + rot[2])
    y3 = y2
    z3 = distxz * math.sin(alphaxz + rot[2]) 
    
    print(f"Third {x3:.2f},{y3:.2f},{z3:.2f}")
    return [x3, y3, z3]

if __name__ == '__main__':
    main()