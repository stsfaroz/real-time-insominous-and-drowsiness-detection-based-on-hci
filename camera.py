# camera.py
#F1YbN3SwfHKjFL0puCd2sAcPgC6SBFYNV32EsUgd
import PIL.Image
from PIL import Image
from twilio.rest import TwilioRestClient
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4a681eb1964c61bf14a5f6bea7ddadad'
auth_token = '6bd92f1b5edf42b5b039a64447d2866b'
whatsapp = TwilioRestClient(account_sid, auth_token)





client = TwilioRestClient(account_sid, auth_token)
thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
flag=0
def eye_aspect_ratio(eye):

    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release() 
    def get_frame(self):
        ret,frame= self.video.read()
        global flag
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)#converting to NumPy Array
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < thresh:
                flag += 1
                print("sleeping",flag)

                if flag >= frame_check:
                    message = whatsapp.messages.create(body='Driver is Sleeping',from_='whatsapp:+14155238886',to='whatsapp:+918681904046')
                    ff=open("log.txt","w")
                    ff.write(str(1))
                    ff.close()

                    cv2.putText(frame, "****************sleeping!****************", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "****************ALERT!****************", (10,325),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    #print ("Drowsy")
            else:
                ff=open("log.txt","w")
                ff.write(str(0))
                ff.close()
                print(" not sleeping",flag)
                flag = 0
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
