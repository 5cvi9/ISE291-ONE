# main_hub.py

import os
import streamlit as st
import importlib.util

# ——————————————————————————————————————————————————————————————
# 1) CONFIGURE PAGE & TITLE
# ——————————————————————————————————————————————————————————————
st.set_page_config(page_title="ISE 291 Streamlit Hub")
st.title("ISE 291 Term 242 Section F22 Streamlit Hub")
st.markdown("Welcome GROUP1.")

# ——————————————————————————————————————————————————————————————
# 2) DISCOVER APPS DIRECTORY
# ——————————————————————————————————————————————————————————————
# apps are under <this file>/ISE291G1Hub/apps
BASE_DIR  = os.path.dirname(__file__)
APPS_DIR  = os.path.join(BASE_DIR, "apps", "ISE291_Project")

if not os.path.isdir(APPS_DIR):
    st.error(f"Apps directory not found:\n{APPS_DIR}")
    st.stop()

# ——————————————————————————————————————————————————————————————
# 3) SIDEBAR NAVIGATION
# ——————————————————————————————————————————————————————————————
st.sidebar.title("Navigation")

# Topics = subfolders under apps/
topics = [
    name for name in os.listdir(APPS_DIR)
    if os.path.isdir(os.path.join(APPS_DIR, name))
]
if not topics:
    st.error("No topics found in apps directory.")
    st.stop()

topic = st.sidebar.selectbox("Choose a Topic", topics)

# Sub-apps = .py files in that topic folder
topic_path = os.path.join(APPS_DIR, topic)
sub_apps = [
    fname for fname in os.listdir(topic_path)
    if fname.endswith(".py") and not fname.startswith("__")
]
if not sub_apps:
    st.error(f"No sub-apps found in {topic_path}")
    st.stop()

sub_app = st.sidebar.selectbox("Choose a Sub-App", sub_apps)

# ——————————————————————————————————————————————————————————————
# 4) LOAD & RUN THE SELECTED SUB-APP
# ——————————————————————————————————————————————————————————————
app_path = os.path.join(topic_path, sub_app)

# double-check our path
if not os.path.isfile(app_path):
    st.error(f"Could not find file:\n{app_path}")
    st.stop()

# dynamically load the module
spec = importlib.util.spec_from_file_location("sub_app", app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# call its entrypoint
if hasattr(module, "app"):
    module.app()
elif hasattr(module, "main"):
    module.main()
else:
    st.error(f"Module `{sub_app}` has no `app()` or `main()` function.")
