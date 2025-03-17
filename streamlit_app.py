import pandas as pd
import numpy as np

#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px

import streamlit as st


def get_data():
    df = pd.read_csv("World-happiness-report-2024.csv")
    df = df.sort_values(by='Ladder score', ascending=False).head(10)
    #df_ts = pd.read_csv('D:/Kiran/Projects/Dashboard/data/World-happiness-report-updated_2024.csv', encoding='latin-1')
    return df

def get_all_data():
    df1 = pd.read_csv("World-happiness-report-2024.csv")
    df2 = pd.read_csv("World-happiness-report-updated_2024.csv", encoding='latin-1')
    #df_ts = pd.read_csv('D:/Kiran/Projects/Dashboard/data/World-happiness-report-updated_2024.csv', encoding='latin-1')
    df_all = pd.concat([df1,df2],ignore_index=True)
    df_all['year'].fillna(2024,inplace=True)
    return df_all

def plot_bars(df):
    numeric_cols = df.select_dtypes(include='number').columns

    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(12, 30))  # Adjust size as needed
    fig.subplots_adjust(hspace=0.4)  # Adjust spacing between subplots

    for i,col in enumerate(numeric_cols):
        row = i//2
        col_index = i%2

        sns.barplot(data=df,x=df["Country name"],y=col,ax=axes[row, col_index],hue=df["Country name"], palette="deep")
        axes[row, col_index].set_title(f'Bar Plot for {col}')

        axes[row, col_index].set_xticklabels(df['Country name'], rotation=45)

    return fig


df = get_data()
numeric_cols = df.select_dtypes(include='number').columns.to_list()

df_all = get_all_data()

st.set_page_config(layout='wide')
st.title("World Happiness Report Visualisations")

st.sidebar.header('About')
st.sidebar.info('These plots provide an overview of the characteristics of the 10 Happiest countries in the world for 2024.')
st.sidebar.info("From our analysis of the first 8 bar charts, we see that even though Generosity, Perceptions of corruption and Dystopia+residual may drastically vary from one country to the next, the key indicators to a Happy county are GDP per Capita, Social Support, Healthy Life Expectancy and Freedom to make choices."
""
""
"NB. Israel had the lowest score in the Freedom to make life choices category, but this may be due to the ongoing wars surrounding the country, leading to strict military patrols along with mandatory military service.")
st.sidebar.info("The last two plots show the changes in life ladder score and the top 10 happiest countries over the 2000-2024 timeline.")


for col in numeric_cols:
    fig = px.bar(data_frame=df,x=df['Country name'],y=df[col], color="Country name",color_discrete_sequence=px.colors.qualitative.G10, 
                 title = f"Bar chart of {col}")
    st.plotly_chart(fig,use_container_width=True)


fig = px.choropleth(df_all.sort_values('year'), 
                    locations = 'Country name',
                    color ='Life Ladder',
                    locationmode = 'country names',
                    animation_frame = 'year')
fig.update_layout(title = 'Life Ladder Comparison by Contries' )
st.plotly_chart(fig,use_container_width=True)



df_top10 = df_all.groupby("year").apply(lambda x: x.nlargest(10, "Life Ladder")).reset_index(drop=True)

fig = px.bar(
    df_top10.sort_values("year"),  
    x="Life Ladder", 
    y="Country name", 
    orientation="h",  # Horizontal bars
    animation_frame="year",  # Animate over years
    text="Life Ladder",
    color="Life Ladder",  
    color_continuous_scale="Blues",  # Color theme
    title="Life Ladder Comparison by Countries"
)

# Improve layout
fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig.update_layout(
    xaxis_title="Life Ladder Score",
    yaxis_title="Country",
    yaxis=dict(categoryorder="total ascending"),  # Sort countries by value
    plot_bgcolor="white"
)

st.plotly_chart(fig,use_container_width=True)
