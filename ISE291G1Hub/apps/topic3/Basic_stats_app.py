import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style="whitegrid")
st.markdown("""
# Exchange Program Data Analysis

We took a sample of students from various years—about 700 in total—to get a simple overview of how the exchange program works.

This application visualizes data from the KFUPM exchange program.
Below, you’ll find interactive charts that help you understand:

- **Top 5 Host Universities**: Which universities hosted the most students.
- **Top Majors**
- **GPA Distributions** by sponsor and major.
- **Comparisons** between universities and majors.
- **Correlation** among key numerical features.


""")


st.title("Exchange Program Data Analysis")

# File uploader
uploaded = st.file_uploader("Upload your dataset (Excel or CSV)", type=["xlsx", "xls", "csv"])
if uploaded:
    # Load data
    if uploaded.name.endswith(("xlsx", "xls")):
        df = pd.read_excel(uploaded)
    else:
        df = pd.read_csv(uploaded)

    st.subheader("Raw Data Preview")
    st.dataframe(df.sample(5))

    # 1. Top 5 Host Universities (Pie Chart)
    st.subheader("Top 5 Host Universities")
    top_unis = df['Name of Host University'].value_counts().head(5)
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    ax1.pie(top_unis, labels=top_unis.index, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig1)

    # 12. Top 7 Host Universities (Table & Bar)
    st.subheader("Top 7 Host Universities")
    top7 = df['Name of Host University'].value_counts().head(7)
    st.table(top7.to_frame('Count'))
    fig10, ax10 = plt.subplots()
    top7.plot(kind='bar', ax=ax10)
    ax10.set_xlabel('University')
    ax10.set_ylabel('Count')
    st.pyplot(fig10)

    st.subheader("Context")
    st.markdown("""
    
   We drew a random sample of 700 exchange students from various enrolment years to understand the distribution of host universities. All percentages and counts below refer to this cohort.

Colorado School of Mines hosted the largest share, roughly 29% of our sample (≈ 203 students).
University of Florida follows with about 22% (≈ 155 students).
Georgia Tech accounts for 21% (≈ 147 students).
University of North Texas and University of Cincinnati round out the top five with 15% (≈ 105) and 13% (≈ 91) respectively.

-Together, these five institutions represent the vast majority of placements, with Colorado School of Mines being the top university attended by students.
""")
    

    # 13. Heatmap: Top 7 Universities vs Majors
    st.subheader("Heatmap of Top 7 Universities vs Majors")
    filt = df[df['Name of Host University'].isin(top7.index)]
    mat = filt.groupby(['Name of Host University', 'Major']).size().unstack(fill_value=0)
    fig11, ax11 = plt.subplots(figsize=(12, 6))
    sns.heatmap(mat, annot=True, fmt='d', cmap='YlGnBu', linewidths=.5, ax=ax11)
    st.pyplot(fig11)

  

    # 2. Top 10 Majors (Bar Chart)
    st.subheader("Top 10 Majors")
    top_majors = df['Major'].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top_majors.values, y=top_majors.index, ax=ax2)
    ax2.set_xlabel("Number of Students")
    st.pyplot(fig2)

    # 3. GPA by Sponsor (Box Plot Top 7)
    st.subheader("GPA Distribution by Sponsor (Top 7)")
    top_sponsors = df['Sponsor Name'].value_counts().head(7).index
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df[df['Sponsor Name'].isin(top_sponsors)], x='Sponsor Name', y='GPA', ax=ax3)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig3)

    # 4. Top 5 Universities vs Top 5 Majors (Clustered Bar)
    st.subheader("Top 5 Universities vs Top 5 Majors")
    top5_unis = df['Name of Host University'].value_counts().head(5).index
    top5_majors = df['Major'].value_counts().head(5).index
    cluster_df = df[df['Name of Host University'].isin(top5_unis) & df['Major'].isin(top5_majors)]
    data = cluster_df.groupby(['Name of Host University', 'Major']).size().unstack(fill_value=0)
    fig4 = data.plot(kind='bar', figsize=(10, 6)).get_figure()
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig4)

    # 5. Correlation Heatmap of Numerical Features
    st.subheader("Correlation Heatmap of Numerical Features")
    num_cols = df[['GPA', 'Total Completed Hours', 'IELTS/TOEFL Score']]
    fig5, ax5 = plt.subplots(figsize=(6, 5))
    sns.heatmap(num_cols.corr(), annot=True, cmap='coolwarm', ax=ax5)
    st.pyplot(fig5)

    # 6. Tagging Test Type
    st.subheader("Tag Test Type: IELTS vs TOEFL")
    df['Test Type'] = df['IELTS/TOEFL Score'].apply(lambda x: 'IELTS' if x <= 9.5 else 'TOEFL')
    st.write(df['Test Type'].value_counts())

    # 7. GPA Distribution by Major (Top 10) - Box Plot
    st.subheader("GPA Distribution by Major (Top 10)")
    top10_majors = df['Major'].value_counts().head(10).index
    fig6, ax6 = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df[df['Major'].isin(top10_majors)], x='Major', y='GPA', ax=ax6)
    ax6.set_xticklabels(ax6.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig6)

    # 8. GPA Violin Plot by Major (Top 10)
    st.subheader("GPA Violin Plot by Major (Top 10)")
    fig7, ax7 = plt.subplots(figsize=(12, 5))
    sns.violinplot(data=df[df['Major'].isin(top10_majors)], x='Major', y='GPA', ax=ax7)
    ax7.set_xticklabels(ax7.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig7)

    # 9. Distribution of Completed Hours
    st.subheader("Total Completed Hours Distribution")
    fig8, ax8 = plt.subplots(figsize=(8, 4))
    sns.histplot(df['Total Completed Hours'], bins=20, kde=True, ax=ax8)
    st.pyplot(fig8)

    # 10. Count of Students per Major (Top 10)
    st.subheader("Count of Students per Major (Top 10)")
    fig9, ax9 = plt.subplots(figsize=(10, 5))
    sns.countplot(x='Major', data=df[df['Major'].isin(top10_majors)], ax=ax9)
    ax9.set_xticklabels(ax9.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig9)

    # 11. Histograms of All Numeric Columns
    st.subheader("Histograms of Numeric Columns")
    for col in df.select_dtypes(include='number').columns:
        fig, ax = plt.subplots()
        sns.histplot(df[col], bins=10, ax=ax)
        ax.set_title(f'Histogram of {col}')
        st.pyplot(fig)

  

    # 14. GPA by Sponsor: Fully vs Partially KFUPM
    st.subheader("GPA Distributions by Sponsor (KFUPM)")
    for sponsor in ['Fully KFUPM', 'Partialy KFUPM']:
        sub = df[df['Sponsor Name'] == sponsor]
        fig_hist, ax_hist = plt.subplots()
        sns.histplot(sub['GPA'], bins=15, kde=True, ax=ax_hist)
        ax_hist.set_title(f'GPA Histogram – {sponsor}')
        st.pyplot(fig_hist)
        fig_box, ax_box = plt.subplots()
        sns.boxplot(y=sub['GPA'], ax=ax_box)
        ax_box.set_title(f'GPA Boxplot – {sponsor}')
        st.pyplot(fig_box)
