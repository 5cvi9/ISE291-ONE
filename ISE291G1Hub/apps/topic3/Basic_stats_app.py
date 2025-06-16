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
- **Top Majors**n- **GPA Distributions** by sponsor and major.
- **Comparisons** between universities and majors.
- **Correlation** among key numerical features.
""")

st.title("Exchange Program Data Analysis")

# Load data directly from Book2.xlsx or Book2.csv
try:
    df = pd.read_excel('Book2.xlsx')
except FileNotFoundError:
    df = pd.read_csv('Book2.csv')

st.subheader("Raw Data Preview")
st.dataframe(df.sample(5))

# Clean sponsor names
df['Sponsor Name'] = df['Sponsor Name'].replace({'Fully Sponsored by KFUPM': 'Fully KFUPM',
                                                 'KFUPM-Partial Sponsor': 'Partialy KFUPM'})

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

# Context
st.subheader("Context")
st.markdown("""
We drew a random sample of 700 exchange students from various enrolment years to understand the distribution of host universities. All percentages and counts below refer to this cohort.

- Colorado School of Mines hosted the largest share, roughly 29% of our sample (≈ 203 students).
- University of Florida follows with about 22% (≈ 155 students).
- Georgia Tech accounts for 21% (≈ 147 students).
- University of North Texas and University of Cincinnati round out the top five with 15% (≈ 105) and 13% (≈ 91) respectively.

Together, these five institutions represent the vast majority of placements, with Colorado School of Mines being the top university attended by students.
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
st.ylabel('Major')
st.xlabel('Number of Students')
st.pyplot(fig2)

# 4. Top 5 Universities vs Top 5 Majors (Clustered Bar)
st.subheader("Top 5 Universities vs Top 5 Majors")
top5_unis = top_unis.index
top5_majors = top_majors.index
data = df[df['Name of Host University'].isin(top5_unis) & df['Major'].isin(top5_majors)]
cluster_df = data.groupby(['Name of Host University', 'Major']).size().unstack(fill_value=0)
fig4 = cluster_df.plot(kind='bar', figsize=(10, 6)).get_figure()
plt.xticks(rotation=45, ha='right')
st.pyplot(fig4)

# 3. GPA by Sponsor (Box Plot Top 7)
st.subheader("GPA Distribution by Sponsor (Top 7)")
top_sponsors = df['Sponsor Name'].value_counts().head(7).index
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df[df['Sponsor Name'].isin(top_sponsors)], x='Sponsor Name', y='GPA', ax=ax3)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig3)

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

# 7. GPA Distribution by Major (Top 10) - Box & Violin
st.subheader("GPA Distribution by Major (Top 10)")
fig6, ax6 = plt.subplots(figsize=(12, 5))
sns.boxplot(data=df[df['Major'].isin(top_majors)], x='Major', y='GPA', ax=ax6)
ax6.set_xticklabels(ax6.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig6)

st.subheader("GPA Violin Plot by Major (Top 10)")
fig7, ax7 = plt.subplots(figsize=(12, 5))
sns.violinplot(data=df[df['Major'].isin(top_majors)], x='Major', y='GPA', ax=ax7)
ax7.set_xticklabels(ax7.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig7)

# 9. Distribution of Completed Hours
st.subheader("Total Completed Hours Distribution")
fig8, ax8 = plt.subplots(figsize=(8, 4))
sns.histplot(df['Total Completed Hours'], bins=20, kde=True, ax=ax8)
st.pyplot(fig8)
st.markdown("""
- Peak around 36–40 hours.
- Secondary bump at 65–75 hours.
- Long tail up to 85 hours.
""")

# Tag Test Type & Score Distribution
st.subheader("Test Type Tagging & Score Distribution")
df['Test Type'] = df['IELTS/TOEFL Score'].apply(lambda x: 'IELTS' if x <= 9.5 else 'TOEFL')
st.write(df['Test Type'].value_counts())
for ttype in ['IELTS', 'TOEFL']:
    fig_score, ax_score = plt.subplots()
    sns.boxplot(y=df[df['Test Type'] == ttype]['IELTS/TOEFL Score'], ax=ax_score)
    ax_score.set_title(f'{ttype} Score Distribution')
    st.pyplot(fig_score)

st.markdown("""
### IELTS Score Insights
- Median ≈ 7.0
- IQR ~ 6.8–7.5
- Range ~ 6.0–8.5

### TOEFL Score Insights
- Median ≈ 78
- IQR ~ 72–87
- Range ~ 61–107
""")
