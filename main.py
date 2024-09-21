import cv2
from cvzone.HandTrackingModule import HandDetector

camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)
detector = HandDetector(detectionCon=0.65)

rect_width, rect_height = 150, 100

class DragRect():
    def __init__(self, posCenter, size=[150, 100]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
                cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

rect = DragRect([250, 100])

def close_window():
    camera.release()
    cv2.destroyAllWindows()
    exit()

def draw_rectangle(frame, rect):
    cx, cy = rect.posCenter
    w, h = rect.size
    cv2.rectangle(frame, (cx - w // 2, cy - h // 2),
                  (cx + w // 2, cy + h // 2), (255, 0, 255), cv2.FILLED)

def draw_pointer(frame, x, y):
    cv2.circle(frame, (x, y), 10, (0, 255, 0), cv2.FILLED)

def main():
    global rect
    
    while True:
        success, frame = camera.read()
        if not success:
            break

        hands, frame = detector.findHands(frame, flipType=False)
        if hands:
            for hand in hands:
                lm_list = hand["lmList"]
                finger_tip_x, finger_tip_y = lm_list[8][:2]
                draw_pointer(frame, finger_tip_x, finger_tip_y)
                rect.update((finger_tip_x, finger_tip_y))

        draw_rectangle(frame, rect)
        cv2.imshow("Virtual Drag and Drop", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            close_window()

if __name__ == "__main__":
    main()