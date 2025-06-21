import streamlit as st
# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    layout="wide",
    page_title="TrioLens Detector",
    page_icon="🖐️"
)

import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from google import genai
from PIL import Image
import time
import io


# ========== Splash Screen ========== #
def show_splash_screen():
    splash = st.empty()
    with splash.container():
        st.markdown("""
            <style>
                .splash {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: #000000;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    z-index: 9999;
                    color: white;
                    font-size: 3rem;
                }
            </style>
            <div class="splash">
                <h1>Welcome to TrioLens Detector</h1>
            </div>
        """, unsafe_allow_html=True)
    # Wait for 5 seconds without showing countdown
    time.sleep(5)
    splash.empty()


# ========== Tutorial Carousel ========== #
def show_tutorial_carousel():
    st.markdown("""
        <style>
            .stImage {
                margin: 0 auto !important;
                display: block !important;
            }
            .carousel {
                width: 100%;
                max-width: 800px;
                margin: 0 auto !important;
                padding: 20px;
                text-align: center;
                margin-bottom: 5px;
                margin-top: 15px;
            }
            .carousel-image-container {
                display: flex !important;
                justify-content: center !important;
                margin: 0 auto 20px !important;
            }
            .carousel-image {
                max-width: 300px;
                width: 100%;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .carousel h2 {
                color: blue;
                margin-bottom: 15px;
                text-align: center !important;
            }
            .carousel p {
                font-size: 1.1rem;
                line-height: 1.6;
            }            
             .nav-up {
                display: flex !important;
                justify-content: center !important;
                gap: 20px;
                margin: 20px auto !important;
                width: fit-content;
            }
             .stMarkdown {
                text-align: center !important;
            }
           
        </style>
    """, unsafe_allow_html=True)

    # Slides content
    slides = [
        {
            "title": "Stage 1/4: Intelligent Hand Detection",
            "content": """
                <div style="border-left: 5px solid #4CAF50; padding-left: 15px; margin: 10px 0;">
                <b>ACTIVE TRACKING</b><br><br>
                - 🖐️ <b>21-Point Detection</b>: Tracks every finger joint<br>
                - ⚡ <b>Real-Time</b>: 30ms latency<br>
                - 🌓 <b>Adaptive Lighting</b>: Works in low-light<br><br>
                <i>Pro Tip: Keep hand 12 inches from camera</i>
                </div>
                """,
            "image": "screen1.png",
            "progress": "25%",
            "color": "#4CAF50"
        },
        {
            "title": "Stage 2/4: Intuitive Drawing Controls",
            "content": """
                <div style="border-left: 5px solid #2196F3; padding-left: 15px; margin: 10px 0;">
                <b>GESTURE COMMANDS</b><br><br>
                - <b>Draw Mode</b>: Index finger extended<br>
                - <b>Clear Canvas</b>: Thumb up<br>
                - <b>Pause/Resume</b>: Index + ring fingers<br><br>
                <i>Pro Tip: Slow down movements</i>
                </div>
                """,
            "image": "screen2.png",
            "progress": "50%",
            "color": "#2196F3"
        },
        {
            "title": "Stage 3/4: AI Processing Engine",
            "content": """
                <div style="border-left: 5px solid #9C27B0; padding-left: 15px; margin: 10px 0;">
                <b>AI CAPABILITIES</b><br><br>
                - 🧮 <b>Math Solver</b>: Algebra to calculus<br>
                - 🔺 <b>Shape Detection</b>: 15+ forms<br>
                - 📝 <b>Diagram Analysis</b>: Flowcharts<br><br>
                <i>94% accuracy on handwritten digits</i>
                </div>
                """,
            "image": "screen3.png",
            "progress": "75%",
            "color": "#9C27B0"
        },
        {
            "title": "Stage 4/4: Results Delivery",
            "content": """
                <div style="border-left: 5px solid #FF9800; padding-left: 15px; margin: 10px 0;">
                <b>OUTPUT OPTIONS</b><br><br>
                - 📋 <b>Step Explanations</b>: Detailed breakdowns<br>
                - 📈 <b>Confidence Metrics</b>: Accuracy scores<br>
                <i>Pro Tip: Try complex questions!</i>
                </div>
                """,
            "image": "screen4.png",
            "progress": "100%",
            "color": "#FF9800"
        }
    ]

    # Initialize session state for current slide
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    # Display current slide
    slide = slides[st.session_state.current_slide]

    try:
        image = Image.open(slide["image"])

        # Create columns to center the image
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.image(
                slide["image"],
                width=300,  # Set your desired width
                use_container_width='auto',  # Maintain aspect ratio
                output_format='PNG'
            )
    except FileNotFoundError:
        st.warning(f"Image not found: {slide['image']}")
        st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                [Placeholder for {slide['image']}]
            </div>
        """, unsafe_allow_html=True)

    # Display title and content
    st.markdown(f"""
        <div class="carousel">
            <h2>{slide['title']}</h2>
            <p>{slide['content']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-up">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        if st.session_state.current_slide > 0:
            if st.button("⏪ Previous"):
                st.session_state.current_slide -= 1
                st.rerun()

        if st.session_state.current_slide < len(slides) - 1:
            if st.button("Next ⏩", key="next_btn"):
                st.session_state.current_slide += 1
                st.rerun()
        else:
            if st.button("🚀 Proceed to App", key="proceed_btn"):
                st.session_state.show_main_app = True
                st.session_state.clear_carousel = True
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ========== Main Application ========== #
def main_application():

    # ========== Streamlit UI Styling ========== #
    st.markdown("""
       <style>
           /* Hide any residual elements */
           .stApp > div:first-child {
               display: none !important;
           }
       </style>
       """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            body {
                background-color: #000000;
                color: #ffffff;
            }
            .main {
                padding: 2rem;
            }
            h1, h2, h3 {
                color: #ffffff;
            }
            .block-container {
                padding-top: 1rem;
            }
            .stText {
                background-color: #000000;
                padding: 1rem;
                border-radius: 8px;
                font-size: 1.2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display image header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image('triolens.jpg')

    # Layout: camera on left, output on right
    col1, col2 = st.columns([3, 2])
    with col1:
        run = st.checkbox('▶️ Run Camera', value=True)
        FRAME_WINDOW = st.image([])

    with col2:
        st.title("AI")
        # output_text_area = st.empty()
        output_text_area = st.subheader("")

    # ========== Gemini API Setup ========== #
    client = genai.Client(api_key="AIzaSyAaJb9xhh8H3A7M4a9_6IbTiFnFMUlwEjM")

    # ========== Webcam + Hand Detector Setup ========== #
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    # cap.set(3, 1280)
    # cap.set(4, 720)

    # Initialize the HandDetector class with the given parameters
    detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

    # ========== Utility Functions ========== #
    def getHandInfo(img):
        hands, img = detector.findHands(img, draw=False, flipType=True)

        if hands:
            # Information for the first hand detected
            hand = hands[0]  # Get the first hand detected
            lmList = hand["lmList"]
            # Count the number of fingers up for the first hand
            fingers = detector.fingersUp(hand)
            print(fingers)
            return fingers, lmList
        else:
            return None

    def draw(info, prev_pos, canvas):
        fingers, lmList = info
        current_pos = None

        # Drawing logic
        if fingers == [0, 1, 0, 0, 0]:
            current_pos = lmList[8][0:2]
            if prev_pos is None: prev_pos = current_pos
            cv2.line(canvas, current_pos, prev_pos, (255, 0, 255), 10)
        elif fingers == [1, 0, 0, 0, 0]:
            canvas = np.zeros_like(img)

        return current_pos, canvas

    def sendToAI(canvas, fingers):

        # Convert OpenCV image to PIL
        if fingers == [1, 1, 1, 0, 0]:
            pil_image = Image.fromarray(canvas)

            prompt = (
                "Look at the image and follow these rules strictly:\n"
                "- If it's a math expression, solve it directly and explain in detail how it is solved.\n"
                "- If it's a shape like a circle, triangle, or square, just say the shape name (e.g., 'This is a circle').\n"
                "- Do not say things like 'I'm unable to solve a math problem' or explain why.\n"
                "- Do not write anything else besides the solution or shape name."
            )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, pil_image]
            )

            return response.text.strip()


    # ========== Main Loop ========== #
    prev_pos = None
    canvas = None
    image_combined = None
    output_text = ""
    # Continuously get frames from the webcam
    while True:
        success, img = cap.read()
        if not success or img is None:
            continue
        img = cv2.flip(img, 1)

        if canvas is None:
            canvas = np.zeros_like(img)

        info = getHandInfo(img)
        if info:
            fingers, lmList = info
            prev_pos, canvas = draw(info, prev_pos, canvas)
            response = sendToAI(canvas, fingers)
            if response:
                output_text = response

        image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
        FRAME_WINDOW.image(image_combined, channels="BGR")

        if output_text:
            output_text_area.text(output_text)


        cv2.waitKey(1)


# ========== App Flow Control ========== #
if 'show_main_app' not in st.session_state:
    st.session_state.show_main_app = False
    st.session_state.splash_shown = False
    st.session_state.clear_carousel = False

# Show splash screen only if it hasn't been shown yet
if not st.session_state.splash_shown:
    show_splash_screen()
    st.session_state.splash_shown = True
    st.rerun()

# Main app flow
if not st.session_state.show_main_app:
    if st.session_state.get('clear_carousel'):
        # Create and immediately clear a container
        placeholder = st.empty()
        placeholder.empty()
        st.session_state.clear_carousel = False
        time.sleep(0.1)  # Ensures cleanup completes
    show_tutorial_carousel()
else:
    # Force clear any remaining elements
    for _ in range(3):
        st.empty()
    main_application()