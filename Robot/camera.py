import cv2
import base64

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    check, frame = camera.read()
    frame = cv2.flip(frame, 1)
    img = cv2.imencode('.JPEG', frame)[1]
    data = base64.urlsafe_b64encode(img)
    # print(data)
    cv2.imshow("TEST", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
