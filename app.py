import streamlit as st
import cv2
from deepface import DeepFace
import os

st.title("🔐 Face Unlock System")

KNOWN_FACES_DIR = "known_faces"

# Session state
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""

# 🔓 After login UI
if st.session_state.auth:
    st.success(f"✅ Welcome {st.session_state.user}")
    st.title("🏠 Dashboard")

    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

else:
    run = st.button("Start Camera")

    FRAME_WINDOW = st.image([])

    if run:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("❌ Camera not opening")
        else:
            ret, frame = cap.read()

            if ret:
                FRAME_WINDOW.image(frame, channels="BGR")

                temp_path = "temp.jpg"
                cv2.imwrite(temp_path, frame)

                name = "Unknown"

                for file in os.listdir(KNOWN_FACES_DIR):
                    try:
                        result = DeepFace.verify(
                            temp_path,
                            os.path.join(KNOWN_FACES_DIR, file),
                            enforce_detection=False
                        )

                        if result["verified"]:
                            name = file.split('.')[0]
                            break
                    except:
                        pass

                if name != "Unknown":
                    st.success(f"✅ Access Granted: {name}")

                    st.session_state.auth = True
                    st.session_state.user = name

                    cap.release()
                    st.rerun()

                else:
                    st.error("❌ Access Denied")

            cap.release()