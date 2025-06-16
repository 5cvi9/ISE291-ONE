import os
import streamlit as st
import importlib.util

# 1) compute base dir
BASE_DIR = os.path.dirname(__file__)

# 2) point at the apps folder next to main_hub.py
APPS_DIR = os.path.join(BASE_DIR, "apps")

st.set_page_config(page_title="ISE 291 Streamlit Hub")
st.title("ISE 291 Term 242 Section F22 Streamlit Hub")
st.markdown("Welcome GROUP1.")

if not os.path.isdir(APPS_DIR):
    st.error(f"Could not find apps folder at:\n{APPS_DIR}")
    st.stop()

# 3) navigation
st.sidebar.title("Navigation")
topics = [
    d for d in os.listdir(APPS_DIR)
    if os.path.isdir(os.path.join(APPS_DIR, d))
]
if not topics:
    st.error(f"No topics found in {APPS_DIR}")
    st.stop()

topic = st.sidebar.selectbox("Choose a Topic", topics)

topic_path = os.path.join(APPS_DIR, topic)
sub_apps = [
    f for f in os.listdir(topic_path)
    if f.endswith(".py") and not f.startswith("__")
]
if not sub_apps:
    st.error(f"No sub-apps found in {topic_path}")
    st.stop()

sub_app = st.sidebar.selectbox("Choose a Sub-App", sub_apps)

# 4) load & run
app_path = os.path.join(topic_path, sub_app)
if not os.path.isfile(app_path):
    st.error(f"Cannot find file:\n{app_path}")
    st.stop()

spec = importlib.util.spec_from_file_location("sub_app", app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if hasattr(module, "app"):
    module.app()
elif hasattr(module, "main"):
    module.main()
else:
    st.error(f"`{sub_app}` has no `app()` or `main()` function.")
