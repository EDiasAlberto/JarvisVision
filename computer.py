from cv2 import *
import xerox

#handles any interactions with the computer
# for now this includes the following:
#   - clipboard management (for code snippets)
#   - file management (for suggested designs/ideas)
#   - webcam management (for computer vision)

class Computer:

    def __init__(self):
        self.cam = VideoCapture(0)

    def takePhoto(self):
        s, img = self.cam.read()
        if s:
            return img

    def saveTextFile(self, contents, path):
        with open(path, "w") as openFile:
            openFile.write(contents)

    def getClipboardContents(self):
        contents = xerox.paste()
        if not contents:
            print("NOTHING TO PASTE IN CLIPBOARD")
            return
        return contents

