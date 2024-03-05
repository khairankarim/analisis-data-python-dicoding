import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

# How to run the streamlit locally
# conda activate main-ds
# streamlit run ./dashboard/dashboard.py
# python -m streamlit run ./dashboard/dashboard.py

# Hour Visualization for 'casual', 'registered', and 'cnt' 
def visualize_hour(df):
    visualize = df.groupby(by="hr").agg({
    "casual_y": "sum",
    "registered_y": "sum",
    "cnt_y": "sum"})

    return visualize

# Ratio Visualization for 'casual', 'registered', and 'cnt'
def visualize_ratio(df):
    visualize = df.agg({
    "casual_y": "sum",
    "registered_y": "sum",
    "cnt_y": "sum"})

    visualize.rename({
        "casual_y": "casual",
        "registered_y": "registered",
        "cnt_y": "cnt"
    }, inplace=True)

    return visualize

def into_ratio_per_total(data_of, total_data):
    return "{:.2f}%".format(data_of/total_data*100)


# Read the Main Data
all_data_df = pd.read_csv("./dashboard/main_data.csv")

# run the streamlit

datetime_columns = ["dteday"]
for column in datetime_columns:
    all_data_df[column] = pd.to_datetime(all_data_df[column])

min_date = all_data_df["dteday"].min()
max_date = all_data_df["dteday"].max()

# all_data_df.reset_index(inplace=True)

# Create a sidebar
with st.sidebar:

    st.write("Step to use the Ranged Time")    
    st.write("1. Choose the First Date")
    st.write("2. Choose the Last Date")
    # limit start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Ranged Time',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# limitation the date
main_df = all_data_df[(all_data_df["dteday"] >= str(start_date)) & 
                     (all_data_df["dteday"] <= str(end_date))]

# call all the function
hour_visualization = visualize_hour(main_df)
ratio_visualization = visualize_ratio(main_df)

# main data frame
hours_in_a_day = [str(x) for x in range(24)]
hours_df = pd.DataFrame(hours_in_a_day)

# start the streamlit code
st.title("Visualize Data with Pyhton")
st.write("Start Date: {}".format(min_date))
st.write("End Date: {}".format(max_date))
st.write("To edit the date, you may change it on the sidebar")

st.subheader('Visualization the Transactions each Hour')
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 15))
 
    sns.barplot(
        y="casual_y", 
        x=hours_in_a_day,
        data=hour_visualization,
        #palette=colors,
        ax=ax
    )
    ax.set_title("Total Casual Transaction each Hour", loc="center", fontsize=50)
    ax.set_ylabel("Hour in a day", fontsize= 45)
    ax.set_xlabel("Hour in a day", fontsize= 40)
    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 15))
    
    # colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="registered_y", 
        x=hours_in_a_day,
        data=hour_visualization,
        # palette=colors,
        ax=ax
    )
    ax.set_title("Total Registered Transaction each Hour", loc="center", fontsize=50)
    ax.set_ylabel("Hour in a day", fontsize= 45)
    ax.set_xlabel("Registered Transaction", fontsize= 40)
    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(7, 5))
sns.despine(fig)

sns.barplot(x=hours_in_a_day, 
            y='cnt_y', 
            data=hour_visualization,
            #colors=
            #palette=
            ax=ax
            )

ax.set_ylabel("Hour in a day")
ax.set_xlabel("Casual Transaction")
ax.set_title("Total Casual Transaction each Hour")
st.pyplot(fig)



# Ratio of Total Transaction Visualization
st.subheader("Rasio of the Transactions")
total_casual = ratio_visualization["casual"]
total_registered = ratio_visualization["registered"]
total_counted = ratio_visualization["cnt"]

# ratio_xaxis_data = ratio_visualization["casual_y", 'registered_y']

col1, col2, col3 = st.columns(3)
 
with col1:
    casual_ratio = into_ratio_per_total(total_casual, total_counted)
    st.metric("Casual Ratio ({} Transactions)".format(total_casual), 
              value=casual_ratio)
 
with col2:
    registered_ratio = into_ratio_per_total(total_registered, total_counted)
    st.metric("Registered Ratio ({} Transactions)".format(total_registered), 
              value=registered_ratio)
    
with col3:
    st.metric("Total Counted Transactions", 
              value=total_counted)

fig, ax = plt.subplots(figsize=(7, 5))
sns.despine(fig)
sns.barplot(data=ratio_visualization[['casual','registered']],
            x=None,
            # x=['Casual', 'registered'],
            # y=[total_casual, total_registered], 
            y=None,
            #colors=
            #palette=
            # native_scale=True,
            # n_boot=1,
            ax=ax)

ax.set_ylabel("Hour in a day")
ax.set_xlabel("Casual Transaction")
ax.set_title("Total Casual Transaction each Hour")
ax.ticklabel_format(axis='y', style='plain')
# ax.bar_label(ax.containers[0], fontsize=15)

# ax.yaxis.set_major_formatter(FuncFormatter())

st.pyplot(fig)
