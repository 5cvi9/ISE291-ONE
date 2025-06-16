import streamlit as st
import os
import importlib.util

st.title("ISE 291 Term 242 Section F22 Streamlit Hub")
st.markdown("Welcome GROUP1.")

# ─── Replace this ──────────────────────────────────────────────────────────────
# APPS_DIR = "ISE291G1Hub/apps"
# ────────────────────────────────────────────────────────────────────────────────

# ─── With these two lines ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)                # ← location of main_hub.py
APPS_DIR = os.path.join(BASE_DIR, "apps")           # ← points to <repo>/ISE291G1Hub/apps
# Optional debug: show us exactly what folder we’re scanning
st.write("Scanning for topics in:", APPS_DIR)
st.write(os.listdir(APPS_DIR))
# ────────────────────────────────────────────────────────────────────────────────

# Sidebar Navigation
st.sidebar.title("Navigation")

# List topics (subfolders in 'apps')
topics = [
    f for f in os.listdir(APPS_DIR)
    if os.path.isdir(os.path.join(APPS_DIR, f))
]
topic = st.sidebar.selectbox("Choose a Topic", topics)

# List sub-apps in the selected topic folder
topic_path = os.path.join(APPS_DIR, topic)
sub_apps = [f for f in os.listdir(topic_path) if f.endswith(".py")]

sub_app = st.sidebar.selectbox("Choose a Sub-App", sub_apps)

# Load and run the selected sub-app
app_path = os.path.join(topic_path, sub_app)
spec = importlib.util.spec_from_file_location("sub_app", app_path)
sub_app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sub_app_module)
