import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as py

# Streamlit title and description
st.title("Food Nutrition Analysis")
st.write("Upload a CSV file to display visualizations based on the nutrition data.")

# File upload functionality
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    nutrients = pd.read_csv(uploaded_file)

    # Data cleaning and preprocessing
    nutrients = nutrients.replace("t", 0)
    nutrients = nutrients.replace("t'", 0)
    nutrients = nutrients.replace(",", "", regex=True)
    nutrients['Fiber'] = nutrients['Fiber'].replace("a", "", regex=True)

    # Handling non-numeric data
    nutrients['Grams'] = pd.to_numeric(nutrients['Grams'], errors='coerce')
    nutrients['Calories'] = pd.to_numeric(nutrients['Calories'], errors='coerce')
    nutrients['Protein'] = pd.to_numeric(nutrients['Protein'], errors='coerce')
    nutrients['Fat'] = pd.to_numeric(nutrients['Fat'], errors='coerce')
    nutrients['Sat.Fat'] = pd.to_numeric(nutrients['Sat.Fat'], errors='coerce')
    nutrients['Fiber'] = pd.to_numeric(nutrients['Fiber'], errors='coerce')
    nutrients['Carbs'] = pd.to_numeric(nutrients['Carbs'], errors='coerce')

    # Drop rows with missing values
    nutrients = nutrients.dropna()

    # Display dataset and summary statistics
    st.write("Dataset Overview", nutrients.head())
    st.write("Data Summary", nutrients.describe())

    # Plotting Protein Rich Foods
    alls = ['Vegetables A-E', 'Vegetables F-P', 'Vegetables R-Z', 'Breads cereals fastfoodgrains', 'Seeds and Nuts']
    prot = nutrients[nutrients['Category'].isin(alls)]
    protein_rich = prot.sort_values(by='Protein', ascending=False)
    top_20 = protein_rich.head(20)
    fig = px.bar(top_20, x='Food', y='Protein', color='Protein', title='Top 20 Protein Rich Foods')
    st.plotly_chart(fig)

    # Plotting Calorie Rich Foods
    cals = nutrients.sort_values(by='Calories', ascending=False)
    top_20_cals = cals.head(20)
    fig = px.bar(top_20_cals, x='Food', y='Calories', color='Calories', title='Top 20 Calorie Rich Foods')
    st.plotly_chart(fig)

    # Plotting Fat and Calorie Content
    fats = nutrients.sort_values(by='Fat', ascending=False)
    top_20_fat = fats.head(20)
    fig = px.bar(top_20_fat, x='Food', y='Fat', color='Fat', title='Top 20 Fat Content Foods')
    st.plotly_chart(fig)

    # Category-wise Distribution using Pie Charts
    category_dist = nutrients.groupby(['Category']).sum()
    fig = make_subplots(rows=2, cols=3, specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}],
                                               [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])

    fig.add_trace(go.Pie(values=category_dist['Calories'].values, title='CALORIES', labels=category_dist.index),
                  row=1, col=1)
    fig.add_trace(go.Pie(values=category_dist['Fat'].values, title='FAT', labels=category_dist.index),
                  row=1, col=2)
    fig.add_trace(go.Pie(values=category_dist['Protein'].values, title='PROTEIN', labels=category_dist.index),
                  row=1, col=3)
    fig.add_trace(go.Pie(values=category_dist['Fiber'].values, title='FIBER', labels=category_dist.index),
                  row=2, col=1)
    fig.add_trace(go.Pie(values=category_dist['Sat.Fat'].values, title='SAT.FAT', labels=category_dist.index),
                  row=2, col=2)
    fig.add_trace(go.Pie(values=category_dist['Carbs'].values, title='CARBS', labels=category_dist.index),
                  row=2, col=3)
    fig.update_layout(title_text="Category-wise Distribution of Nutrients", height=700, width=1000)
    st.plotly_chart(fig)

    # Display high-calorie desserts using Funnel Plot
    drinks = nutrients[nutrients['Category'].isin(['Fish Seafood', 'Desserts sweets'])]
    drinks_top = drinks.sort_values(by='Calories', ascending=False).head(10)
    fig = go.Figure(go.Funnelarea(values=drinks_top['Calories'].values, text=drinks_top['Food'],
                                  title="Desserts with High Calorie Percentages"))
    st.plotly_chart(fig)

    # Display high-fat desserts using Funnel Plot
    drinks_fatty = drinks.sort_values(by='Fat', ascending=False).head(10)
    fig = go.Figure(go.Funnelarea(values=drinks_fatty['Fat'].values, text=drinks_fatty['Food'],
                                  title="Desserts with High Fat Percentages"))
    st.plotly_chart(fig)

    # 3D Scatter Plot for Fat and Carbs
    trace1 = go.Scatter3d(x=nutrients['Category'], y=nutrients['Food'], z=nutrients['Fat'], mode='markers',
                          marker=dict(sizemode='diameter', sizeref=750, color=nutrients['Fat'], colorscale='Portland'))
    layout = dict(height=800, width=800, title='3D Scatter Plot of Fatty Foods')
    fig = dict(data=[trace1], layout=layout)
    st.plotly_chart(fig)

    trace1 = go.Scatter3d(x=nutrients['Category'], y=nutrients['Food'], z=nutrients['Carbs'], mode='markers',
                          marker=dict(sizemode='diameter', sizeref=750, color=nutrients['Carbs'],
                                      colorscale='Portland'))
    layout = dict(height=800, width=800, title='3D Scatter Plot of Carbohydrate Rich Foods')
    fig = dict(data=[trace1], layout=layout)
    st.plotly_chart(fig)

    # Boxplot of Calories by Category
    sns.set_style("whitegrid")
    plt.figure(figsize=(22, 10))
    ax = sns.boxenplot(x="Category", y='Calories', data=nutrients, color='#eeeeee', palette="tab10")
    plt.title("Total Calorie Content by Category", loc="center", size=32, color='#be0c0c', alpha=0.6)
    plt.xlabel('Category', color='#34495E', fontsize=20)
    plt.ylabel('Total Calories', color='#34495E', fontsize=20)
    st.pyplot(plt)
