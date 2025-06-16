import streamlit as st
import os
import importlib.util

# — DEBUGGING INFO ——————————————————————————————————————————————————————
st.write("Current working directory:", os.getcwd())
BASE_DIR = os.path.dirname(__file__)
st.write("Script (__file__) lives in:", BASE_DIR)

# now build APPS_DIR
APPS_DIR = os.path.join(BASE_DIR, "apps")
st.write("Scanning for topics in:", APPS_DIR)
st.write("Contents of APPS_DIR:", os.listdir(APPS_DIR))
# — end DEBUGGING INFO ——————————————————————————————————————————————————————

st.title("ISE 291 Term 242 Section F22 Streamlit Hub")
st.markdown("Welcome GROUP1.")

# Sidebar Navigation
st.sidebar.title("Navigation")

topics = [
    name for name in os.listdir(APPS_DIR)
    if os.path.isdir(os.path.join(APPS_DIR, name))
]
st.write("Discovered topics:", topics)

topic = st.sidebar.selectbox("Choose a Topic", topics)

topic_path = os.path.join(APPS_DIR, topic)
sub_apps = [f for f in os.listdir(topic_path) if f.endswith(".py")]
st.write(f"Discovered sub-apps in {topic}:", sub_apps)

sub_app = st.sidebar.selectbox("Choose a Sub-App", sub_apps)

app_path = os.path.join(topic_path, sub_app)
spec = importlib.util.spec_from_file_location("sub_app", app_path)
sub_app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sub_app_module)
