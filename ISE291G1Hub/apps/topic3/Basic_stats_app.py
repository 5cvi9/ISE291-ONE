import streamlit as st

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Set up the app
st.title("Basic Stats App")
st.write("Upload your dataset and perform basic statistical analysis.")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file:
    # Read the uploaded file into a DataFrame
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Here's a preview of your dataset:")
        st.dataframe(df)

        # Allow the user to select a column
        column = st.selectbox("Select a column to analyze:", df.columns)

        # Check the column type
        if df[column].dtype == "object":
            st.write(f"Column '{column}' is categorical.")
            
            # Categorical Histogram
            st.write("### Categorical Histogram")
            fig, ax = plt.subplots()
            df[column].value_counts().plot(kind="bar", ax=ax)
            ax.set_title(f"Histogram of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Count")
            st.pyplot(fig)

            # Pie chart
            st.write("### Pie Chart")
            fig, ax = plt.subplots()
            df[column].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax)
            ax.set_ylabel("")
            ax.set_title(f"Pie Chart of {column}")
            st.pyplot(fig)

            # Categorical Summary
            st.write("### Summary Statistics for Categorical Data")
            st.write(df[column].value_counts())

        else:
            st.write(f"Column '{column}' is numerical.")

            # Numerical Histogram
            st.write("### Numerical Histogram")
            bins = st.slider("Select number of bins for the histogram:", min_value=5, max_value=50, value=10)
            fig, ax = plt.subplots()
            df[column].plot(kind="hist", bins=bins, ax=ax)
            ax.set_title(f"Histogram of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

            # Summary Statistics
            st.write("### Summary Statistics for Numerical Data")
            st.write(f"Mean: {df[column].mean():.2f}")
            st.write(f"Median: {df[column].median():.2f}")
            st.write(f"Mode: {df[column].mode()[0]:.2f}")
            st.write(f"Standard Deviation: {df[column].std():.2f}")
            st.write(f"Minimum: {df[column].min():.2f}")
            st.write(f"Maximum: {df[column].max():.2f}")

            # Box Plot
            st.write("### Box Plot")
            fig, ax = plt.subplots()
            sns.boxplot(y=df[column], ax=ax)
            ax.set_title(f"Box Plot of {column}")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.write("Please upload a CSV file to proceed.")
