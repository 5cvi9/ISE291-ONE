mport streamlit as st
import os
import importlib.util

st.title("ISE 291 Term 242 Section F22 Streamlit Hub")
st.markdown("Welcome GROUP1.")

# 1) Always point at the right folder:
BASE_DIR = os.path.dirname(__file__)
APPS_DIR = os.path.join(BASE_DIR, "apps")

# 2) (Optional) Debug what you’re actually scanning:
st.write("Scanning apps in:", APPS_DIR)
st.write(os.listdir(APPS_DIR))

# Sidebar
st.sidebar.title("Navigation")
topics = [d for d in os.listdir(APPS_DIR)
          if os.path.isdir(os.path.join(APPS_DIR, d))]
topic = st.sidebar.selectbox("Choose a Topic", topics)

topic_path = os.path.join(APPS_DIR, topic)
sub_apps = [f for f in os.listdir(topic_path) if f.endswith(".py")]
sub_app = st.sidebar.selectbox("Choose a Sub-App", sub_apps)

# Load & run
app_path = os.path.join(topic_path, sub_app)
spec = importlib.util.spec_from_file_location("sub_app", app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
