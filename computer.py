from cv2 import VideoCapture, imshow, imwrite, imencode
from base64 import b64encode
from time import sleep
import xerox

#handles any interactions with the computer
# for now this includes the following:
#   - clipboard management (for code snippets)
#   - file management (for suggested designs/ideas)
#   - webcam management (for computer vision)

class Computer:

    def __init__(self):
        self.cam = VideoCapture(0)

    def testCamera(self):
        s, img = self.cam.read()
        imshow("outputFrame", img)
        imwrite("output.jpg", img)
        sleep(10)

    def takePhoto(self):
        s, img = self.cam.read()
        if s:
            s, buffer = imencode(".jpg", img)
            b64 = b64encode(buffer).decode("utf-8")
            return b64

    def saveTextFile(self, contents, path):
        with open(path, "w") as openFile:
            openFile.write(contents)

    def copy(self, text):
        xerox.copy(text);

    def getClipboardContents(self):
        contents = xerox.paste()
        if not contents:
            print("NOTHING TO PASTE IN CLIPBOARD")
            return
        return contents


if __name__=="__main__":
    client = Computer()

    client.testCamera()
