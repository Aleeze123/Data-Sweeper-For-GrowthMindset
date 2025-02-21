import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
st.title('Growth Mindset Data Sweeper 🌱')
st.write("""
This app allows you to upload a dataset, clean it by handling missing values, 
removing duplicates, and then visualize the cleaned data. 
You can also choose columns to keep and convert your file to CSV or Excel format.
""")
# Upload CSV file
st.header("📂 Upload Your CSV File 📂")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    original_filename = uploaded_file.name.split('.')[0]
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Data Preview 🔍")
    st.write(df.head())
    # Data Cleaning
    st.header("🧹 Data Cleaning 🧹")
    handle_missing = st.selectbox('How would you like to handle missing values?', 
                                  ['Remove rows', 'Fill with zeros', 'Fill with mean'])
    df_cleaned = df.copy()
    if handle_missing == 'Remove rows':
        df_cleaned = df_cleaned.dropna()
    elif handle_missing == 'Fill with zeros':
        df_cleaned = df_cleaned.fillna(0)
    elif handle_missing == 'Fill with mean':
        numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
        df_cleaned[numeric_columns] = df_cleaned[numeric_columns].fillna(df_cleaned[numeric_columns].mean())
    remove_duplicates = st.checkbox('Remove duplicate rows', value=True)
    if remove_duplicates:
        df_cleaned = df_cleaned.drop_duplicates()
    st.header("📝 Choose Columns to Keep 📝")
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect('Select columns to keep', all_columns, default=all_columns)
    df_cleaned = df_cleaned[selected_columns]

    # Display cleaned data
    st.subheader("✅ Cleaned Data ✅")
    st.write(df_cleaned)
    st.header("📊 Visualize Data 📊")
    numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_columns) > 0:
        column1 = st.selectbox('Select X-axis column for visualization', numeric_columns)
        column2 = st.selectbox('Select Y-axis column for visualization', numeric_columns)
        if column1 != column2:
            st.subheader(f"🔵 Scatter plot of {column1} vs {column2} 🔵")
            st.write(f"Visualizing the relationship between {column1} and {column2}") 
            fig, ax = plt.subplots()
            ax.scatter(df_cleaned[column1], df_cleaned[column2])
            ax.set_xlabel(column1)
            ax.set_ylabel(column2)
            st.pyplot(fig)
        else:
            st.error("X and Y axes cannot be the same!")
        st.subheader(f"📊 Histogram of {column1} 📊")
        fig, ax = plt.subplots()
        ax.hist(df_cleaned[column1], bins=20, color='skyblue', edgecolor='black')
        ax.set_xlabel(column1)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
        st.subheader(f"📦 Boxplot of {column1} 📦")
        fig, ax = plt.subplots()
        sns.boxplot(data=df_cleaned[column1], ax=ax, color='lightgreen')
        st.pyplot(fig)
    else:
        st.warning("⚠️ No numeric columns available to visualize. Please clean the data and try again.")
    # File Conversion csv to excel
    st.header("🔄 Convert Data Format 🔄")
    conversion_format = st.radio("Choose format to convert the cleaned data:", ["CSV", "Excel"])
    if conversion_format == "CSV":
        # Convert the cleaned DataFrame to CSV
        csv = df_cleaned.to_csv(index=False)
        st.download_button("💾 Download CSV 💾", csv, f"{original_filename}.csv", "text/csv")
    elif conversion_format == "Excel":
        # Convert the cleaned DataFrame to Excel using openpyxl engine....
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df_cleaned.to_excel(writer, index=False)
        st.download_button("💾 Download Excel 💾", excel_buffer.getvalue(), f"{original_filename}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.write("""
    🚀 Data cleaning and visualization are important skills that help you understand and make decisions based on the data.
    Keep going, and remember: Learning from your mistakes and persistence is key to success! 
    """)
st.write("👩‍💻 Created by: Aleeza 💫")
