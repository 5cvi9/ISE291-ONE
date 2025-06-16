import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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

# Resolve data path relative to this script
def load_dataset():
    base = os.path.dirname(__file__)
    excel_path = os.path.join(base, 'Book2.xlsx')
    csv_path = os.path.join(base, 'Book2.csv')
    try:
        return pd.read_excel(excel_path)
    except FileNotFoundError:
        return pd.read_csv(csv_path)

# Load data
df = load_dataset()

st.subheader("Raw Data Preview")
st.dataframe(df.sample(5))

# Clean sponsor names
df['Sponsor Name'] = df['Sponsor Name'].replace({
    'Fully Sponsored by KFUPM': 'Fully KFUPM',
    'KFUPM-Partial Sponsor': 'Partialy KFUPM'
})

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
ax2.set_ylabel('Major')
ax2.set_xlabel('Number of Students')
st.pyplot(fig2)


st.subheader("Heatmap: Top 7 Universities vs. Majors")
st.markdown("""
    
    This heatmap shows how the top seven host institutions distribute students across all majors.

1. Mechanical Engineering (ME)

Georgia Tech leads, hosting 45 ME students.
Colorado School of Mines follows with 40.
University of Florida then takes 34.
Smaller ME cohorts scatter among Cincinnati, North Texas, and Arizona State.

2. Electrical Engineering (EE)

University of Florida is the top EE destination with 34 students.
Colorado School of Mines hosts 27 EE students.
University of North Texas comes next at 15.
A handful of EE students also go to Georgia Tech and Cincinnati.

3. Industrial & Systems Engineering (ISE)

Colorado School of Mines again leads for ISE with 34 students.
University of Florida hosts 24 ISE students.
Georgia Tech follows at 16.
The remainder are spread across Cincinnati, North Texas, and Arizona State.

4. Chemical Engineering (CHE)

University of Florida hosts 24 CHE students.
University of Cincinnati takes 21.
Georgia Tech hosts 7 CHE students.
Colorado and North Texas each host a small number (3–4) of CHE majors.

5. Petroleum Engineering (PETE)

Colorado School of Mines is the primary PETE destination with 34 students.
University of Florida hosts 8 PETE students.
Georgia Tech and Cincinnati each take a handful (2–4) of PETE majors.

The lighter cells across many universities and majors show a long tail of smaller exchanges, indicating a broad but shallow spread beyond the core programs.

(All counts sum to the same 700-student sample.)
""")


# 4. Top 5 Universities vs Top 5 Majors (Clustered Bar)
st.subheader("Top 5 Universities vs Top 5 Majors")
top5_unis = top_unis.index
top5_majors = top_majors.index
data = df[df['Name of Host University'].isin(top5_unis) & df['Major'].isin(top5_majors)]
cluster_df = data.groupby(['Name of Host University', 'Major']).size().unstack(fill_value=0)
fig4 = cluster_df.plot(kind='bar', figsize=(10, 6)).get_figure()
plt.xticks(rotation=45, ha='right')
st.pyplot(fig4)

st.markdown("""

This clustered bar chart compares the distribution of students in the five most popular majors—CHE, EE, ISE, ME, and PETE—across our top five host institutions:

- Colorado School of Mines
Strong in ME (40 students) and PETE (34), reflecting its well-known engineering and petroleum programs.
Also hosts 27 EE and 11 CHE students, with a smaller presence in ISE.

- Georgia Tech
Dominates EE with 45 students, showcasing its leading electrical engineering department.
Welcomes 16 ME and 7 CHE students, but very few in ISE and PETE.

- University of Cincinnati
Attracts 21 CHE students and 11 ME, with a modest number (6) of EE students and very few PETE or ISE.

- University of Florida
Has a balanced spread but is strongest in ISE (34) and ME (24), underlining its interdisciplinary engineering strengths.
Also hosts 14 CHE and 8 EE students, with minimal PETE representation.

- University of North Texas
Draws 21 ME students and 6 EE students.
PETE (2) and CHE (1) are niche offerings here, with almost no ISE placements.
""")

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
st.subheader("GPA vs. Sponsor")
st.markdown("""
        We compare the GPA profiles of students across our seven most-common sponsorship categories

        From the visualizations you’ll notice:

Fully KFUPM students tend to have higher GPAs overall (median around 3.7–3.8) with fewer low-end scores.

KFUPM Fund shows a slightly lower median (around 3.3–3.4) and a wider spread, indicating more variability.

Sponsors like SAUDI ARAMCO and SABIC also show high median GPAs (3.7–3.9).

Self-funded and Ministry of Education categories can have wider ranges and lower minimums, suggesting a broader mix of academic performance.

""")
# 7. GPA Distribution by Major (Top 10) - Box & Violin
top10_majors = df['Major'].value_counts().head(10).index

st.subheader("GPA Distribution by Major (Top 10)")
fig6, ax6 = plt.subplots(figsize=(12, 5))
sns.boxplot(
    data=df[df['Major'].isin(top10_majors)],
    x='Major', y='GPA', ax=ax6
)
ax6.set_xticklabels(ax6.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig6)

st.subheader("GPA Violin Plot by Major (Top 10)")
fig7, ax7 = plt.subplots(figsize=(12, 5))
sns.violinplot(
    data=df[df['Major'].isin(top10_majors)],
    x='Major', y='GPA', ax=ax7
)
ax7.set_xticklabels(ax7.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig7)

st.subheader("GPA vs. Majors")
st.markdown("""
    Below are the median GPA values for each of the top 10 majors (in order of descending popularity), based on our 700-student sample. The median is the “middle” score — half of students in that major scored above it and half below:

1- Mechanical Engineering (ME)
Median GPA ≈ 3.45
Most ME students cluster between roughly 3.3 and 3.6, with the central line right around 3.45.

2- Electrical Engineering (EE)
Median GPA ≈ 3.45
Very similar to ME, reflecting a strong, consistent performance in EE.

3- Industrial & Systems Engineering (ISE)
Median GPA ≈ 3.00
Noticeably lower median than most majors; ISE GPAs spread from about 2.8 up to 3.4.

4- Chemical Engineering (CHE)
Median GPA ≈ 3.30
CHE sits in the mid-3’s, with most students between 3.0 and 3.6.

5- Petroleum Engineering (PETE)
Median GPA ≈ 3.35
Very similar to CHE, reflecting a tight cluster around the lower mid-3’s.

6- Software Engineering (SWE)
Median GPA ≈ 3.35
Also around the mid-3’s, but with a slightly wider spread down toward the high-2’s.

7- Financial Engineering (FIN)
Median GPA ≈ 3.60
One of the highest medians — FIN students tend to sit solidly in the upper-3’s.

8- Computer Science (CS)
Median GPA ≈ 3.60
On a par with FIN, indicating strong performance in CS.

9- Aerospace Engineering (AME)
Median GPA ≈ 3.30
Similar to CHE/PETE/SWE, but with a slightly narrower interquartile range.

10- Architectural Engineering (ARC)
Median GPA ≈ 3.75
The highest median of all ten majors, suggesting ARC students generally achieve the top GPAs in our sample.
""")

# 9. Distribution of Completed Hours
st.subheader("Total Completed Hours Distribution")
fig8, ax8 = plt.subplots(figsize=(8, 4))
sns.histplot(df['Total Completed Hours'], bins=20, kde=True, ax=ax8)
st.pyplot(fig8)


st.subheader("Total Completed Hours Distribution")
st.markdown("""
    - The bulk of students have completed 30–45 hours, with a clear peak around 36–40 hours.
    - A secondary bump appears around 65–75 hours, representing upper-class students who went later in their studies.
    - The long tail to the right suggests a smaller group of very senior students (75–85 hours) who also participated.
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

st.subheader("IELTS Score Distribution")
st.markdown("""
        - Median ≈ 7.0: Half of our IELTS students scored above 7.0 and half below.
        - IQR ~ 6.8–7.5: 50% of scores lie in this band, showing a tight clustering around the mid-7’s.
        - Range ~ 6.0–8.5: Most scores fall within these whiskers, with a few high-end outliers touching 8.5.
        
    """)
st.subheader("TOEFL Score Distribution")
st.markdown("""
     
        - Median ≈ 78: The middle TOEFL score is around 78.
        - IQR ~ 72–87: 50% of TOEFL scores span this 15-point window
        - Range ~ 61–107: Whiskers cover most scores; multiple outliers above 110 show some students achieve exceptionally high results.
        
    """)
