
import streamlit as st
import pandas as pd
from scipy.stats import shapiro, ttest_ind, mannwhitneyu

# Title
st.title("Hypothesis Testing App")
st.write("Upload your dataset and perform hypothesis tests.")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file:
    # Read the uploaded file into a DataFrame
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Here's a preview of your dataset:")
        st.dataframe(df)

        # Extract numerical columns
        numerical_columns = df.select_dtypes(include=['number']).columns

        if len(numerical_columns) < 2:
            st.error("The dataset must contain at least two numerical columns for hypothesis testing.")
        else:
            # Ask user to select columns for normality testing
            st.subheader("Shapiro-Wilk Test for Normality")
            selected_columns = st.multiselect(
                "Select columns to test for normality:", numerical_columns
            )

            if selected_columns:
                normality_results = {}
                for col in selected_columns:
                    stat, p_value = shapiro(df[col])
                    normality_results[col] = {
                        "Test Statistic": stat,
                        "P-value": p_value,
                        "Conclusion": "Data is not Normal" if p_value > 0.05 else "Data is Normal",
                    }

                st.write("### Normality Test Results")
                st.dataframe(pd.DataFrame.from_dict(normality_results, orient='index'))

            # Ask user to select two columns for difference in means testing
            st.subheader("Difference in Means Tests")
            col1 = st.selectbox("Select the first column:", numerical_columns)
            col2 = st.selectbox("Select the second column:", numerical_columns)

            if col1 and col2 and col1 != col2:
                st.write(f"Selected columns: {col1} and {col2}")

                # Test 1: Student's t-test
                st.write("### Student's t-test")
                variances_known = st.checkbox("Assume equal variances (default: unchecked)")
                t_stat, t_p_value = ttest_ind(df[col1], df[col2], equal_var=variances_known)
                t_conclusion = "Fail to Reject Null Hypothesis => The two population means are not significantly different" if t_p_value > 0.05 else "Reject Null Hypothesis => The two population means are significantly different"

                st.write(f"T-test Statistic: {t_stat:.4f}")
                st.write(f"P-value: {t_p_value:.4f}")
                st.write(f"Conclusion: {t_conclusion}")

                # Test 2: Mann-Whitney U Test
                st.write("### Mann-Whitney U Test")
                u_stat, u_p_value = mannwhitneyu(df[col1], df[col2])
                u_conclusion = "Fail to Reject Null Hypothesis => The two population means are not significantly different" if u_p_value > 0.05 else "Reject Null Hypothesis => The two population means are significantly different"

                st.write(f"U-test Statistic: {u_stat:.4f}")
                st.write(f"P-value: {u_p_value:.4f}")
                st.write(f"Conclusion: {u_conclusion}")

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.write("Please upload a CSV file to proceed.")
