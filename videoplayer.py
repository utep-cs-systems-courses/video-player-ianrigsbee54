import cv2
import threading
import queue

lock = threading.Lock()
class pcQueue():
    def __init__(self):
        self.sem = threading.Semaphore(10)#queue locked to holding only 10 frames
        self.que = queue.Queue()
    def put(self, frame):
        self.sem.acquire()
        lock.acquire()
        self.que.put(frame)
        lock.release()
    def get(self):
        self.sem.release()
        lock.acquire()
        frame = self.que.get()
        lock.release()
        return frame
    def isEmpty(self):
        lock.acquire()
        empty = self.que.empty()
        lock.release()
        return empty

def convertToGray(producer, consumer, maxFrames):
    count = 0
    while True:
        if pQ.isEmpty():#wait until pQ has frames
            continue
        Frame = producer.get()#dequeue from producer
        if count == maxFrames:
            break
        print(f'converting frame {count} to grayscale')
        grayScaleFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        consumer.put(grayScaleFrame)#enqueue into consumer
        count += 1
    print("conversion complete")
    
def extractFrames(producer, fileName, maxFrames):
    count = 0
    vidcap = cv2.VideoCapture(fileName)
    success, image = vidcap.read()
    while success and count < maxFrames:
        success, jpgImage = cv2.imencode('.jpg', image)
        producer.put(image)#place frames in producer queue
        success, image = vidcap.read()
        print(f'reading frame {count} {success}')
        count += 1
    print('Frame extraction complete')   
    
def displayFrames(consumer, maxFrames):
    count = 0
    while True:
        if consumer.isEmpty():
            continue
        if count == maxFrames:#terminate loop once done displaying
            break
        displayFrame = consumer.get()#dequeue from consumer
        print(f'displaying frame {count}')
        cv2.imshow('Video', displayFrame)
        if cv2.waitKey(42) and 0xFF == ord('q'):#wait 42ms 
            break
        count += 1
    print("display finished")
    cv2.destroyAllWindows()

#two pcQueues one for extracting and one for converting and displaying    
pQ = pcQueue()
cQ = pcQueue()
fileName = "clip.mp4"
maxFrames = 9999 #max frames of clip.mp4
extractThread = threading.Thread(target = extractFrames, args = (pQ, fileName, maxFrames))
convertThread = threading.Thread(target = convertToGray, args = (pQ, cQ, maxFrames))
displayThread = threading.Thread(target = displayFrames, args = (cQ, maxFrames))

extractThread.start()
convertThread.start()
displayThread.start()

