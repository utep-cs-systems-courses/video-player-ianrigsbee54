import cv2
import threading
import base64
import queue

class pcQueue():
    def __init__(self):
        self.sem = threading.Semaphore(10)
        self.que = queue.Queue()
    def put(self):

    def get(self):

def convertToGray():

def extractFrames():

def displayFrame():
    
producerQ = pcQueue()
consumerQ = pcQueue()

convertThread = threading.Thread()
extractThread = threading.Thread()
displayThread = threading.Thread()

convertThread.start()
extractThread.start()
displayThread.start()
