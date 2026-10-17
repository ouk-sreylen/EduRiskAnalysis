import streamlit as st
import pandas as pd

# Step 7. Replace your old `st.set_page_config()` code with:
st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
)

def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()

# 8. Replace your old `student_df` code with:
student_df = load_student_data()


# 9. Add the following function to calculate risk level based on score and attendance
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"
    
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)
    
# 10. Add a new column to the DataFrame to store the risk level for each student
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

# 11. Add a sidebar for navigation
with st.sidebar:
    st.title("EduRisk Menu")
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )

# 12. Update the main app code to display different content based on the selected page
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")

    if st.button("Click Me"):
        st.write("Welcome to my page! ")

#  13. Add the following code to display the student data in a table format
elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")

    st.write(
        "This dashboard gives a quick overview of student performance "
        "using data loaded from students.csv."
    )

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

    st.subheader("Student Records")
    st.write("This table shows student data loaded from students.csv.")
    st.dataframe(student_df)

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Score Chart")
        score_chart = student_df.set_index("Student Name")["Score"]
        st.bar_chart(score_chart)

    with chart_col2:
        st.write("Course Count")
        course_count = student_df["Course"].value_counts()
        st.bar_chart(course_count)

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )
    
    # 14. Add the following code to allow users to filter the student data by course
    selected_course = st.selectbox(
        "Select Course",
        ["All"] + list(student_df["Course"].unique())
    )
    
    # 15. Add the following code to allow users to filter the student data by risk level
    selected_risk = st.selectbox(
        "Select Risk Level",
        ["All", "Low Risk", "Medium Risk", "High Risk"]
    )
    
    # 16. Add the following code to allow users to filter the student data by minimum attendance
    min_attendance = st.slider(
        "Minimum Attendance",
        0,
        100,
        0
    )
    
    # 17. Add minimum score filter
    min_score = st.slider(
        "Minimum Score",
        0,
        100,
        0
    )
    
    # 18. Add filtering logic 
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]
    
    # 19. Update the metrics based on the filtered data
    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)
        
    # 20. Add a checkbox to show/hide the filtered dataset
    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Filtered Student Dataset")
        st.dataframe(filtered_df)
        # 21. Add a download button for the filtered dataset
        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Filtered dataset is hidden.")
        
    # 22. Add a section to display charts based on the filtered data  
    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if len(filtered_df) > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.warning("No data available for score chart.")
            
    # 23. Add a chart for risk level distribution      
    with chart_col2:
        st.write("Risk Level Count")

        if len(filtered_df) > 0:
            risk_count = filtered_df["Risk Level"].value_counts()
            st.bar_chart(risk_count)
        else:
            st.warning("No data available for risk chart.")

# 24. Add a new page for student data         
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)
    
# 25. Add a download button for the full dataset
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")

# 26. Add an About page
else:
    st.title("About")

    st.write("This app is part of Lab 03.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Data Loading, Layout, and Frontend Prototype")

    st.info(
        "This frontend prototype loads real data from students.csv "
        "and displays it using Streamlit and Pandas."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )
