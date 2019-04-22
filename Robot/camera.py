import cv2
import base64

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    check, frame = camera.read()
    frame = cv2.flip(frame, 1)
    try:
        img = cv2.imencode('.jpg', frame)[1]
    except Exception as e:
        print('Camera is not available')
        exit(0)
    data = base64.b64encode(img)
    # print(data)
    cv2.imshow("TEST", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
