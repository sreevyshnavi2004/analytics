import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(
    page_title="Universal Data Analytics Dashboard",
    layout="wide"
)

st.title("📊 Universal Data Analytics & Visualization Dashboard")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    # Read File
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Dataset Loaded Successfully!")

        # Dataset Overview
        st.header("📌 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        st.dataframe(df.head())

        # Data Information
        st.header("📋 Data Information")

        info_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(info_df)

        # Missing Values
        st.header("⚠ Missing Value Analysis")

        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if len(missing) > 0:
            fig = px.bar(
                x=missing.index,
                y=missing.values,
                labels={"x": "Columns", "y": "Missing Count"},
                title="Missing Values by Column"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No Missing Values Found")

        # Numerical Analysis
        numerical_cols = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        if numerical_cols:

            st.header("📈 Numerical Statistics")

            st.dataframe(df[numerical_cols].describe())

            # Correlation Matrix
            st.subheader("Correlation Heatmap")

            corr = df[numerical_cols].corr()

            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale="RdBu_r"
            )

            st.plotly_chart(fig, use_container_width=True)

            # Distribution Plot
            st.subheader("Distribution Analysis")

            selected_num = st.selectbox(
                "Select Numerical Column",
                numerical_cols
            )

            fig = px.histogram(
                df,
                x=selected_num,
                nbins=30,
                marginal="box",
                title=f"Distribution of {selected_num}"
            )

            st.plotly_chart(fig, use_container_width=True)

            # Box Plot
            fig = px.box(
                df,
                y=selected_num,
                title=f"Box Plot - {selected_num}"
            )

            st.plotly_chart(fig, use_container_width=True)

        # Categorical Analysis
        categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if categorical_cols:

            st.header("🏷 Categorical Analysis")

            selected_cat = st.selectbox(
                "Select Categorical Column",
                categorical_cols
            )

            value_counts = (
                df[selected_cat]
                .value_counts()
                .head(20)
                .reset_index()
            )

            value_counts.columns = [selected_cat, "Count"]

            fig = px.bar(
                value_counts,
                x=selected_cat,
                y="Count",
                title=f"Top Categories in {selected_cat}"
            )

            st.plotly_chart(fig, use_container_width=True)

        # Interactive Visualization Builder
        st.header("🎨 Visualization Builder")

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Scatter Plot",
                "Line Chart",
                "Bar Chart",
                "Box Plot",
                "Histogram",
                "Pie Chart"
            ]
        )

        all_cols = df.columns.tolist()

        if chart_type == "Scatter Plot":

            x = st.selectbox("X Axis", all_cols)
            y = st.selectbox("Y Axis", all_cols)

            color = st.selectbox(
                "Color By",
                ["None"] + all_cols
            )

            fig = px.scatter(
                df,
                x=x,
                y=y,
                color=None if color == "None" else color
            )

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Line Chart":

            x = st.selectbox("X Axis", all_cols)
            y = st.selectbox("Y Axis", all_cols)

            fig = px.line(df, x=x, y=y)

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Bar Chart":

            x = st.selectbox("X Axis", all_cols)
            y = st.selectbox("Y Axis", all_cols)

            fig = px.bar(df, x=x, y=y)

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Box Plot":

            x = st.selectbox("Category", all_cols)
            y = st.selectbox("Value", all_cols)

            fig = px.box(df, x=x, y=y)

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Histogram":

            x = st.selectbox("Column", all_cols)

            fig = px.histogram(df, x=x)

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Pie Chart":

            names = st.selectbox("Category", all_cols)

            value_col = st.selectbox(
                "Values",
                numerical_cols if numerical_cols else all_cols
            )

            fig = px.pie(
                df,
                names=names,
                values=value_col
            )

            st.plotly_chart(fig, use_container_width=True)

        # Data Filtering
        st.header("🔍 Data Filtering")

        filter_column = st.selectbox(
            "Select Column to Filter",
            all_cols
        )

        unique_values = df[filter_column].dropna().unique()

        selected_values = st.multiselect(
            "Choose Values",
            unique_values
        )

        if selected_values:
            filtered_df = df[
                df[filter_column].isin(selected_values)
            ]

            st.write(
                f"Filtered Records: {len(filtered_df)}"
            )

            st.dataframe(filtered_df)

            csv = filtered_df.to_csv(index=False)

            st.download_button(
                "⬇ Download Filtered Data",
                csv,
                "filtered_data.csv",
                "text/csv"
            )

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Upload a CSV or Excel file to begin analysis.")