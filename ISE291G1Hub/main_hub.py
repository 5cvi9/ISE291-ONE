import streamlit as st
import os
import importlib.util

st.title("ISE 291 Term 242 Section F22 Streamlit Hub")
st.markdown("Welcome GROUP1.")

# Absolute path to the 'ISE291_Project' folder
APPS_DIR = "ISE291G1Hub/apps/ISE291_Project"

# Sidebar Navigation
st.sidebar.title("Navigation")

# List topics (subfolders in 'ISE291_Project')
topics = [f for f in os.listdir(APPS_DIR) if os.path.isdir(os.path.join(APPS_DIR, f))]
topic = st.sidebar.selectbox("Choose a Topic", topics)

# List sub-apps in the selected topic folder
topic_path = os.path.join(APPS_DIR, topic)
sub_apps = [f for f in os.listdir(topic_path) if f.endswith(".py")]

# Handle case where no sub-apps are found
if not sub_apps:
    st.sidebar.warning("No sub-apps found in this topic.")
else:
    sub_app = st.sidebar.selectbox("Choose a Sub-App", sub_apps)

    # Load and Run the Selected Sub-App
    app_path = os.path.join(topic_path, sub_app)
    spec = importlib.util.spec_from_file_location("sub_app", app_path)
    sub_app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sub_app_module)

    # Optionally, you could call a function from the sub_app_module if needed
