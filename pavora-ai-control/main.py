"""PAVORA AI CONTROL — local Windows 11 webcam hand mouse. No uploads or recording."""
import argparse
import time
import cv2
import mediapipe as mp
import pyautogui
from gesture_logic import Point, classify

pyautogui.FAILSAFE=True
pyautogui.PAUSE=0.015

def run(camera_index: int):
    cap=cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Webcam not available. Connect webcam or try --camera 1")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,540)
    w,h=pyautogui.size()
    enabled=False
    mx=my=None
    last_click=last_scroll=0.0
    scroll_anchor=None
    last_frame=time.monotonic()
    try:
        with mp.solutions.hands.Hands(max_num_hands=1,model_complexity=0,
            min_detection_confidence=.65,min_tracking_confidence=.60) as hands:
            while True:
                ok,frame=cap.read()
                if not ok:
                    if time.monotonic()-last_frame>2:
                        print("Webcam feed lost: stopping")
                        break
                    continue
                last_frame=time.monotonic()
                frame=cv2.flip(frame,1)
                rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                result=hands.process(rgb)
                points=None
                gesture="no hand"
                if result.multi_hand_landmarks:
                    landmarks=result.multi_hand_landmarks[0]
                    points=[Point(p.x,p.y) for p in landmarks.landmark]
                    gesture=classify(points)
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame,landmarks,mp.solutions.hands.HAND_CONNECTIONS)
                if enabled and points:
                    if gesture=="stop":
                        enabled=False
                        mx=my=scroll_anchor=None
                    elif gesture in ("pointer","click"):
                        scroll_anchor=None
                        x=max(0,min(1,(points[8].x-.12)/.76))*(w-1)
                        y=max(0,min(1,(points[8].y-.12)/.76))*(h-1)
                        mx=x if mx is None else mx*.72+x*.28
                        my=y if my is None else my*.72+y*.28
                        pyautogui.moveTo(round(mx),round(my),duration=0)
                        if gesture=="click" and time.monotonic()-last_click>.65:
                            pyautogui.click()
                            last_click=time.monotonic()
                    elif gesture=="scroll":
                        fy=(points[8].y+points[12].y)/2
                        if scroll_anchor is not None and time.monotonic()-last_scroll>.09:
                            if abs(fy-scroll_anchor)>.022:
                                pyautogui.scroll(-2 if fy>scroll_anchor else 2)
                                scroll_anchor=fy
                                last_scroll=time.monotonic()
                        elif scroll_anchor is None:
                            scroll_anchor=fy
                    else:
                        scroll_anchor=None
                else:
                    scroll_anchor=None
                cv2.rectangle(frame,(0,0),(frame.shape[1],73),(15,20,32),-1)
                status="ACTIVE" if enabled else "PAUSED"
                cv2.putText(frame,f"PAVORA AI CONTROL | {status} | {gesture}",
                    (12,29),cv2.FONT_HERSHEY_SIMPLEX,.65,(90,230,150) if enabled else (0,200,255),2)
                cv2.putText(frame,"E enable/pause | Open palm pause | Q/ESC quit",
                    (12,57),cv2.FONT_HERSHEY_SIMPLEX,.48,(230,230,230),1)
                cv2.imshow("PAVORA AI CONTROL",frame)
                key=cv2.waitKey(1)&0xff
                if key in (ord("q"),27): break
                if key==ord("e"):
                    enabled=not enabled
                    mx=my=scroll_anchor=None
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--camera",type=int,default=0)
    args=parser.parse_args()
    try:
        run(args.camera)
    except pyautogui.FailSafeException:
        print("Emergency corner fail-safe triggered")
    except KeyboardInterrupt:
        print("Stopped")
    except Exception as exc:
        print("Error:",exc)
        raise SystemExit(1)
