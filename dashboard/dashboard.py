import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')

def create_average_total_rental_df(df):
    average_total_rental_df = df.groupby(by="hr").cnt.mean().sort_values(ascending=False)
    return average_total_rental_df

def create_average_working_day_df(df):
    average_working_day_df = df.groupby(by="workingday").cnt.mean().sort_values(ascending=False)
    return average_working_day_df

def create_average_season_rental_df(df):
    average_season_rental_df = df.groupby(by="season").cnt.mean().sort_values(ascending=False)
    return average_season_rental_df

all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

season_dict = {
    'Musim Semi': 1,
    'Musim Panas': 2,
    'Musim Gugur': 3,
    'Musim Dingin': 4
}
    
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://i.pinimg.com/736x/8f/05/79/8f0579f1289a1638cec828f43b291587.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )    
    
    selected_hours = st.slider(
        label='Pilih Jam (0-23)',
        min_value=0,
        max_value=23,
        value=(0, 23)
    )
    
    selected_working_days = st.multiselect(
        label='Pilih Hari',
        options=['Hari Kerja', 'Hari Libur'],
        default=['Hari Kerja', 'Hari Libur']
    )
    
    selected_seasons = st.multiselect(
        label='Pilih Musim',
        options={
            'Musim Semi': 'Musim Semi',
            'Musim Panas': 'Musim Panas',
            'Musim Gugur': 'Musim Gugur',
            'Musim Dingin': 'Musim Dingin'
        },
        default=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
    )
    
    

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))&
                (all_df["hr"].between(selected_hours[0], selected_hours[1])) &
                (all_df["season"].isin([season_dict[season] for season in selected_seasons])) &
                (all_df["workingday"].isin([1 if day == 'Hari Kerja' else 0 for day in selected_working_days]))]


average_total_rental_df = create_average_total_rental_df(main_df)
average_working_day_df = create_average_working_day_df(main_df)
average_season_rental_df = create_average_season_rental_df(main_df)

st.image("https://images.ctfassets.net/p6ae3zqfb1e3/7EvTCz4yh5EjYm5PBF2F7b/2af90f1c0cf365a12d088f5021cb0b6d/CaBi_CaBiforEveryone_Hero_2x.png")

st.markdown("<h1 style='text-align: center;'>Capital Bikeshare</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)
 
with col1:
    total_rental = all_df.cnt.sum()
    formatted_total_rental = '{:,.0f}'.format(total_rental).replace(",",".")
    st.metric("Total Rental", value=formatted_total_rental)
 
with col2:
    registered_user = all_df.registered.sum()
    formatted_registered_user = '{:,.0f}'.format(registered_user).replace(",",".")
    st.metric("Registered Users", value=formatted_registered_user)
    
with col3:
    casual_user = all_df.casual.sum()
    formatted_casual_user = '{:,.0f}'.format(casual_user).replace(",",".")
    st.metric("Casual Users", value=formatted_casual_user)
    
    
st.subheader('Tren Rental Tiap Jam')

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=main_df, x='hr', y='cnt', marker='o', errorbar=None)
plt.xlabel('Jam')
plt.ylabel('Jumlah Rental')
st.pyplot(fig)

st.subheader('Jumlah Rental antara Hari Kerja dan Libur')

df_counts = main_df.groupby(by="workingday").cnt.mean().sort_values(ascending=False).reset_index()
df_counts["workingday"] = df_counts["workingday"].apply(lambda x : 'Hari Libur' if x == 1 else 'Hari Kerja' )
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=df_counts, x=df_counts['workingday'], y=df_counts['cnt'], hue="workingday", errorbar=None)
plt.xlabel('Hari')
plt.ylabel('Rental per jam')
st.pyplot(fig)

st.subheader('Rata-rata rental tiap Musim')

season_df = main_df.groupby(by="season").cnt.mean().sort_values(ascending=False).reset_index()
season_df["season"] = season_df["season"].apply(lambda x : 'Musim Semi' if x == 1 else ('Musim Panas'if x == 2 else ('Musim Gugur'if x == 3 else 'Musim Dingin' )))
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=season_df, x=season_df['season'], y=season_df['cnt'], hue="season", errorbar=None)
plt.xlabel('Musim')
plt.ylabel('Jumlah per Jam')
st.pyplot(fig)


