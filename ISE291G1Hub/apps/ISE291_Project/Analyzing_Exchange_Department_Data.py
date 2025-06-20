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

- Top 5 Host Universities: Which universities hosted the most students.
- Top Majors: The most popular fields of study among exchange participants.
- GPA Distributions by Sponsor and Major: How student GPAs vary across different sponsors and academic majors.
- Comparisons Between Universities and Majors.
- Correlation Among Key Numerical Features: Relationships between metrics like GPA, completed credit hours, and language‐test scores.
- Performance Comparison (Host vs KFUPM): How students GPAs at their host universities compare to their GPAs at KFUPM.
""")

st.title("Exchange Program Data Analysis")

def load_datasets():
    # Set the base path
    base = os.path.join("ISE291G1Hub", "apps", "ISE291_Project")
    
    # Primary exchange data: try xlsx, then csv
    excel2 = os.path.join(base, "Book2.xlsx")
    csv2 = os.path.join(base, "Book2.csv")
    
    try:
        df2 = pd.read_excel(excel2)
    except FileNotFoundError:
        df2 = pd.read_csv(csv2)

    # Optional GPA file
    excel1 = os.path.join(base, "Book1_GPA.xlsx")
    try:
        df1 = pd.read_excel(excel1)
    except FileNotFoundError:
        df1 = None

    return df2, df1

df, df1 = load_datasets()



# Clean sponsor names
df['Sponsor Name'] = df['Sponsor Name'].replace({
    'Fully Sponsored by KFUPM': 'Fully KFUPM',
    'KFUPM-Partial Sponsor':  'Partialy KFUPM'
})
df["Name of Host University"]=df["Name of Host University"].replace("University of Arizona","Arizona State University")



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

- Colorado School of Mines hosted the largest share, roughly 26.8% of our sample.
- University of Florida follows with about 20%.
- Arizona State University accounts for 21%.
- University of North Texas and University of Georgia Tech round out the top five with 13% and 19%  respectively.

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

1. **Mechanical Engineering (ME)**
   
   - Colorado School of Mines **40** students.
   - North Texas **21** students.

2. **Electrical Engineering (EE)**
   - University of Cincinnati **21** students.
   - Georgia Tech **45** students.     


3. **Industrial & Systems Engineering (ISE)**
   - University of Florida **34** students.  
   - Arizona State University **30** students.  
   

4. **Chemical Engineering (CHE)**
   - University of Florida **24** students. 
   - Colorado School of Mines **27** students.  
  

5. **Petroleum Engineering (PETE)**
   - Colorado School of Mines **34** students.  
   



The lighter cells across many universities and majors show a long tail of smaller exchanges, indicating a broad but shallow spread beyond the core programs.

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
Strong in ME (40 students) and PETE (34).

- Georgia Tech
Host EE with 45 students, showcasing its leading electrical engineering department.

- Arizona State University
Host 30 ISE students and 19 ME.

- University of Florida
Has a balanced spread but is strongest in ISE (34) and CHE (24).

- University of North Texas
Host 15 FIN and 21 ME.
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

Sponsors like SAUDI ARAMCO and SABIC also show high median GPAs.

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
Median GPA ≈ 3.35
Most ME students cluster between roughly 3.3 and 3.6, with the central line right around 3.35.

2- Electrical Engineering (EE)
Median GPA ≈ 3.45
Reflecting a strong, consistent performance in EE.

3- Industrial & Systems Engineering (ISE)
Median GPA ≈ 3.25
Noticeably lower median than most majors; ISE GPAs spread from about 2.8 up to 3.4.

4- Chemical Engineering (CHE)
Median GPA ≈ 3.45
CHE sits in the mid-3’s, with most students between 3.0 and 3.6.

5- Petroleum Engineering (PETE)
Median GPA ≈ 3.60
Reflecting a tight cluster around the lower mid-3’s.

6- Software Engineering (SWE)
Median GPA ≈ 3.40
Also around the mid-3’s, but with a slightly wider spread down toward the high-2’s.

7- Financial Engineering (FIN)
Median GPA ≈ 3.40
One of the highest medians — FIN students tend to sit solidly in the upper-3’s.

8- Computer Science (CS)
Median GPA ≈ 3.55

9- Aerospace Engineering (AME)
Median GPA ≈ 3.20

10- Architectural Engineering (ARC)
Median GPA ≈ 3.65
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
    - A secondary bump appears around 65–75 hours.
    - The long tail to the right suggests a smaller group of (75–80 hours) who also participated.
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
        - IQR ~ 72–87: 50% of TOEFL scores span this 15-point.
        - Range ~ 61–107: Whiskers cover most scores; multiple outliers above 110 show some students achieve exceptionally high results.
        
    """)
st.subheader("GPA Comparison (KFUPM vs Host)")

    # 1. Scatter plot
fig_scatter, ax_scatter = plt.subplots()
ax_scatter.scatter(df1['GPA'], df1['Host GPA'])
ax_scatter.set_title('KFUPM GPA vs Host GPA')
ax_scatter.set_xlabel('KFUPM GPA')
ax_scatter.set_ylabel('Host GPA')
st.pyplot(fig_scatter)
st.subheader("KFUPM GPA vs. Host GPA (Scatter Plot)")
st.markdown("""
     
        - Each dot represents one student’s KFUPM GPA (x-axis) and their host-university GPA (y-axis).
        - students grades at their host university tend to be a bit lower than at KFUPM.
        - The overall upward trend confirms that strong performers at KFUPM generally remain strong performers abroad.
        
    """)




    # 2. Compute difference stats
df1['GPA Difference'] = df1['GPA'] - df1['Host GPA']
diff_stats = df1['GPA Difference'].describe().to_frame().T
st.subheader("GPA Difference Statistics")
st.table(diff_stats)

    # 3. Histogram of GPA Difference
fig_hist, ax_hist = plt.subplots()
ax_hist.hist(df1['GPA Difference'].dropna(), bins=20)
ax_hist.set_title('Distribution of GPA Difference (KFUPM – Host)')
ax_hist.set_xlabel('GPA Difference')
ax_hist.set_ylabel('Frequency')
st.pyplot(fig_hist)


st.subheader("Distribution (Histogram)")
st.markdown("""
     
        - Most students differences cluster just above zero, confirming a small grade drop abroad for the majority.
        - A few students actually scored higher abroad (the bars left of zero).
        - A small number experienced a large drop (bars out toward +2 or +3).
        
    """)

    # 4. Box plot of GPA Difference
fig_box, ax_box = plt.subplots()
ax_box.boxplot(df1['GPA Difference'].dropna(), vert=True, patch_artist=True)
ax_box.set_title('Box Plot of GPA Difference (KFUPM – Host)')
ax_box.set_ylabel('GPA Difference')
st.pyplot(fig_box)

st.subheader("Box Plot of Differences")
st.markdown("""
     
        - The center line shows the median drop of about 0.37 GPA points.
        - The box covers the middle 50% of students, whose drops range from 0 up to about 0.84.
        - The whiskers stretch from roughly –1.2 (host GPA > home) to +2.1, showing most students full range.

        note: Any dots outside those whiskers are rare cases with unusually big changes.
        
    """)

st.subheader("OVERALL")
st.markdown("""
     
        Most students see a small drop in GPA when they go abroad about 0.4 points on average. Half of them lose between 0 and 0.8 points, a few actually improve ,Only a few students experience big changes in either direction.
        
    """)
st.markdown("""
# Recommandations:
""")
st.subheader("- Adding More Universities")
st.markdown("""
Most students tend to enroll in the same five universities: Colorado School of Mines, University of Florida, Georgia Tech, University of North Texas, and University of Cincinnati. These institutions host nearly all students majoring in Mechanical Engineering (ME), Electrical Engineering (EE), Industrial and Systems Engineering (ISE), Chemical Engineering (CHE), and Petroleum Engineering (PETE).

However, other majors, such as Software Engineering, Financial Engineering, Computer Science, and Architectural Engineering, send only a few students to these same five universities. By introducing more partner universities, a wider range of majors can participate in the exchange program, ensuring that all students find the best academic fit.
""")
st.subheader("- Early Warning System")
st.markdown("""Host universities should inform the department if an exchange student midterm GPA drops below a certain level. In response, the department should take steps like reducing the student's course load to help prevent small academic issues from becoming bigger problems by the end of the term.
""")

