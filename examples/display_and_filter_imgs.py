import sys
import os
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                               QFileDialog, QMessageBox)
from PySide2.QtGui import QPixmap, QIcon, QKeySequence
from PySide2.QtCore import Qt

class ImageComparer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Comparer')
        self.setGeometry(100, 100, 1200, 600)
        
        self.detectionsDir = ''
        self.rawDir = ''
        self.saveDir = ''
        self.detections = []
        self.currentIndex = -1

        self.setupUI()
        self.show()

    def setupUI(self):
        layout = QVBoxLayout()

        # Directory selection buttons and labels
        dirsLayout = QHBoxLayout()
        self.detectionsBtn = QPushButton('Select Detections Directory')
        self.rawBtn = QPushButton('Select Raw Images Directory')
        self.saveBtn = QPushButton('Select Save Directory')
        self.detectionsLabel = QLabel('No path is selected')
        self.rawLabel = QLabel('No path is selected')
        self.saveLabel = QLabel('No path is selected')
        
        dirsLayout.addWidget(self.detectionsBtn)
        dirsLayout.addWidget(self.detectionsLabel)
        dirsLayout.addWidget(self.rawBtn)
        dirsLayout.addWidget(self.rawLabel)
        dirsLayout.addWidget(self.saveBtn)
        dirsLayout.addWidget(self.saveLabel)

        # Image display
        self.detectionImageLabel = QLabel('Detection Image')
        self.rawImageLabel = QLabel('Raw Image Not Available')
        self.detectionImageLabel.setScaledContents(True)
        self.rawImageLabel.setScaledContents(True)

        imagesLayout = QHBoxLayout()
        imagesLayout.addWidget(self.detectionImageLabel)
        imagesLayout.addWidget(self.rawImageLabel)

        # Feedback and Save
        self.feedbackLabel = QLabel('Feedback')
        self.saveButton = QPushButton('Save')
        feedbackLayout = QHBoxLayout()
        feedbackLayout.addWidget(self.feedbackLabel)
        feedbackLayout.addWidget(self.saveButton)

        layout.addLayout(dirsLayout)
        layout.addLayout(imagesLayout)
        layout.addLayout(feedbackLayout)
        self.setLayout(layout)

        # Connections
        self.detectionsBtn.clicked.connect(lambda: self.selectDirectory('detections'))
        self.rawBtn.clicked.connect(lambda: self.selectDirectory('raw'))
        self.saveBtn.clicked.connect(lambda: self.selectDirectory('save'))
        self.saveButton.clicked.connect(self.saveCurrentImage)

    def selectDirectory(self, dirType):
        dirPath = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirPath:
            if dirType == 'detections':
                self.detectionsDir = dirPath
                self.detectionsLabel.setText(dirPath)
                self.loadImages()
            elif dirType == 'raw':
                self.rawDir = dirPath
                self.rawLabel.setText(dirPath)
            elif dirType == 'save':
                self.saveDir = dirPath
                self.saveLabel.setText(dirPath)

    def loadImages(self):
        self.detections = [f for f in os.listdir(self.detectionsDir) if f.endswith(('jpg', 'jpeg', 'png'))]
        self.currentIndex = 0
        self.updateImages()

    def updateImages(self):
        if 0 <= self.currentIndex < len(self.detections):
            detectionImagePath = os.path.join(self.detectionsDir, self.detections[self.currentIndex])
            self.detectionImageLabel.setPixmap(QPixmap(detectionImagePath).scaled(self.detectionImageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            rawImagePath = os.path.join(self.rawDir, self.detections[self.currentIndex])
            if os.path.exists(rawImagePath):
                self.rawImageLabel.setPixmap(QPixmap(rawImagePath).scaled(self.rawImageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.rawImageLabel.setText('Raw Image Not Available')
            self.feedbackLabel.setText('')
        else:
            self.feedbackLabel.setText('End of images or start of images')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            if self.currentIndex < len(self.detections) - 1:
                self.currentIndex += 1
                self.updateImages()
        elif event.key() == Qt.Key_Left:
            if self.currentIndex > 0:
                self.currentIndex -= 1
                self.updateImages()
        elif event.key() == Qt.Key_S:
            self.saveCurrentImage()

    def saveCurrentImage(self):
        if self.saveDir and self.rawDir and 0 <= self.currentIndex < len(self.detections):
            sourcePath = os.path.join(self.rawDir, self.detections[self.currentIndex])
            if os.path.exists(sourcePath):
                destinationPath = os.path.join(self.saveDir, self.detections[self.currentIndex])
                shutil.copy(sourcePath, destinationPath)
                self.feedbackLabel.setText('Image saved.')
            else:
                self.feedbackLabel.setText('Raw image not available. Cannot save.')
        else:
            QMessageBox.warning(self, "Save Error", "Please ensure all directories are selected and valid.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageComparer()
    sys.exit(app.exec_())
