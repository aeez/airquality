import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv('https://raw.githubusercontent.com/aeez/airquality/main/dashboard/data_wanshouxigong.csv')

# Title
st.title('Analisis Air Quality di Kota Wanshouxigong')

# About me
st.markdown("""
- **Nama**: Muhammad Akram Fais
- **Email**: makramfais@gmail.com
- **Dicoding ID**: [4eezzzz](https://www.dicoding.com/users/4eezzzz/)

## Proyek Akhir Overview
Dashboard ini memperlihatkan analisis dari dataset *air quality* di Kota Wanshouxigong. Proyek akhir ini bertujuan untuk menganalisis pola tren dan melihat korelasi antar indikator *air quality* dengan suhu di Kota Wanshouxigong.
""")

# Sidebar
with st.sidebar:
    st.image("logo.jpg")

    df.sort_values(by="date", inplace=True)
    df.reset_index(inplace=True)

    df["date"] = pd.to_datetime(df["date"])

    min_date = df["date"].min()
    max_date = df["date"].max()

    # Membuat filter rentang tanggal
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu', min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

    # Mengolah data sesuai rentang tanggal yang diinput
    df_filtered = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]


# Data Overview
st.subheader('Data Overview')
st.write(df_filtered.head(10))

# Parameter Statistik Deskriptif
st.subheader('Parameter Statistik Deskriptif')
st.write(df_filtered.describe())

# Pola Tren Indikator Air Quality
st.subheader('Pola Tren Indikator Air Quality')
pm25, pm10 = st.tabs(["PM 2.5", "PM 10"])

with pm25:
    st.header("Level PM 2.5 (Bulanan)")

    # Line chart for PM2.5 levels over selected month
    df_filtered['month_year'] = df_filtered['date'].dt.to_period('M')
    monthly_avg_pm25 = df_filtered.groupby('month_year')['PM2.5'].mean().reset_index()
    monthly_avg_pm25['month_year'] = monthly_avg_pm25['month_year'].astype(str)

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_avg_pm25['month_year'], monthly_avg_pm25['PM2.5'], marker='o')
    plt.title('Rata-rata Bulanan Kualitas Udara (PM2.5) di Wanshouxigong (2013-2017)')
    plt.xlabel('Bulan-Tahun')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(rotation=45)  # Putar label x agar tidak bertabrakan
    plt.grid(True)

    st.pyplot(plt)


with pm10:
    st.header("Level PM 10 (Bulanan)")

    # Line chart for PM2.5 levels over selected month
    monthly_avg_pm10 = df_filtered.groupby('month_year')['PM10'].mean().reset_index()
    monthly_avg_pm10['month_year'] = monthly_avg_pm10['month_year'].astype(str)

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_avg_pm10['month_year'], monthly_avg_pm10['PM10'], marker='o')
    plt.title('Rata-rata Bulanan Kualitas Udara (PM2.5) di Wanshouxigong (2013-2017)')
    plt.xlabel('Bulan-Tahun')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(rotation=45)  # Putar label x agar tidak bertabrakan
    plt.grid(True)

    st.pyplot(plt)

st.subheader("Heatmap Korelasi antar Indikator Air Quality dengan Suhu")

selected_columns = st.multiselect('Select Columns for Correlation', df.columns, default=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP'])
corr = df[selected_columns].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig)


# Kesimpulan
st.subheader('Kesimpulan')
st.write("""
- Dilihat dari rerata nilai per bulan, pola indikator polusi udara (PM2.5) di Kota Wanshouxigong mengalami kenaikan dan penurunan yang signifikan (Tidak Stabil). Pada akhir tahun sampai dengan awal tahun indikator polusi udara (PM2.5) di Kota Wanshouxigong mengalami penurunan. Pola tersebut dapat dilihat pada grafik, yaitu pada akhir tahun 2013 sampai awal tahun 2014, akhir tahun 2014 sampai awal tahun 2015, dan akhir tahun 2015 sampai awal tahun 2016. Yang dimana pola ini kerap terjadi pada musim dingin (Winter).
- Secara keseluruhan, indikator *air quality* tidak berhubungan dengan suhu yang ada di Kota Wanshouxigong. Dapat dilihat dari korelasi antar indikator *air quality* dengan suhu, hampir seluruh indikator *air quality* menunjukkan nilai yang rendah sehingga dapat disimpulkan bahwa tidak ada korelasi antara indikator *air quality* dengan suhu di Kota Wanshouxigong.
""")
