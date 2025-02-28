import streamlit as st
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="CAMCOM",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the futuristic cyberpunk style
st.markdown("""
<style>
    body {
        background-color: #000000;
        color: #00ffcc;
        font-family: Arial, sans-serif;
    }
    .stApp {
        background-color: #000000;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
        text-shadow: 0px 0px 10px #00ffcc;
    }
    .stButton>button {
        border: 2px solid #00ffcc;
        background-color: transparent;
        color: #00ffcc;
        border-radius: 8px;
        font-size: 0.9em;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        box-shadow: 0px 0px 15px #00ffcc;
        padding: 10px 15px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00ffcc;
        color: black;
        transform: scale(1.05);
        box-shadow: 0px 0px 25px #00ffcc;
    }
    .camera-container, .output-container {
        border: 4px solid #00ffcc;
        border-radius: 15px;
        box-shadow: 0px 0px 20px #00ffcc;
        background: rgba(0, 0, 0, 0.8);
        padding: 20px;
        margin-bottom: 20px;
        height: 450px;
    }
    .output-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-size: 1.5em;
    }
    .project-name {
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 0px 0px 10px #00ffcc;
        color: #00ffcc;
        text-align: right;
        padding-right: 20px;
        margin-bottom: 20px;
    }
    .system-status {
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        border-radius: 5px;
        padding: 5px 10px;
        background-color: rgba(0, 255, 204, 0.1);
        margin-top: 10px;
    }
    .timestamp {
        font-family: 'Courier New', monospace;
        font-size: 1em;
        color: #00ffcc;
        margin-top: 10px;
        text-align: center;
    }
    .camera-placeholder {
        width: 100%;
        height: 330px;
        background: rgba(0, 30, 20, 0.5);
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid rgba(0, 255, 204, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Project title
st.markdown('<div class="project-name">CAMCOM</div>', unsafe_allow_html=True)

# Initialize session state variables
if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False
if 'image_captured' not in st.session_state:
    st.session_state.image_captured = False
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'system_log' not in st.session_state:
    st.session_state.system_log = ["System initialized"]

# Functions for camera controls
def toggle_camera():
    st.session_state.camera_on = not st.session_state.camera_on
    st.session_state.image_captured = False
    status = "activated" if st.session_state.camera_on else "deactivated"
    st.session_state.system_log.append(f"Camera {status}")

def capture_image():
    if st.session_state.camera_on:
        st.session_state.image_captured = True
        st.session_state.system_log.append("Image captured")

# Layout with two columns
col1, col2 = st.columns(2)

# Camera section
with col1:
    st.markdown('<div class="camera-container">', unsafe_allow_html=True)
    
    # Display camera status
    status = "ACTIVE" if st.session_state.camera_on else "INACTIVE"
    st.markdown(f'<div class="system-status">CAMERA STATUS: {status}</div>', unsafe_allow_html=True)
    
    # Camera display area
    if st.session_state.camera_on and not st.session_state.image_captured:
        camera_image = st.camera_input("", key="camera", label_visibility="collapsed")
        if camera_image is not None:
            st.session_state.captured_image = camera_image
    elif st.session_state.image_captured and st.session_state.captured_image is not None:
        st.image(st.session_state.captured_image, use_column_width=True)
    else:
        st.markdown(
            """
            <div class="camera-placeholder">
                <p style="color:#00ffcc;">CAMERA OFFLINE</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Display timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f'<div class="timestamp">{current_time}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Camera control buttons
    st.markdown("### CONTROL PANEL")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("ON/OFF"):
            toggle_camera()
    with c2:
        st.button("VIDEO")
    with c3:
        if st.button("CAPTURE"):
            capture_image()
    with c4:
        st.button("AUDIO")
    with c5:
        st.button("SETTINGS")

# Output section
with col2:
    st.markdown('<div class="output-container">', unsafe_allow_html=True)
    
    # Show the CAMCOM logo/text
    st.markdown("<h2>CAMCOM SYSTEM</h2>", unsafe_allow_html=True)
    
    # System log section
    st.markdown("<h3>SYSTEM LOG</h3>", unsafe_allow_html=True)
    
    # Display log entries (most recent first)
    log_entries = ""
    for entry in reversed(st.session_state.system_log[-8:]):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entries += f"<p style='font-family: monospace; margin: 5px 0; font-size: 0.9em;'>[{timestamp}] {entry}</p>"
    
    st.markdown(log_entries, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# System footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 10px; color: #00ffcc; font-size: 0.8em; font-family: monospace;">
        CAMCOM SYSTEM v1.0 | SECURE CONNECTION ESTABLISHED
    </div>
    """, 
    unsafe_allow_html=True
)