import requests
import pandas as pd
import streamlit as st
import re
from datetime import datetime, date
import altair as alt

st.set_page_config(page_title="Canlı Sıcaklık ve Nem Takibi", layout="wide")
st.title("🌡️ Canlı Sıcaklık ve Nem Takibi")

# -----------------------------
# Veriyi çekme fonksiyonu
# -----------------------------
@st.cache_data(ttl=60)
def veri_yukle():
    url = "https://nazmiaras.com/kevser.txt"
    response = requests.get(url)
    metin = response.text

    # Regex ile veriyi ayıkla (Sicaklik ve Â°C uyumlu)
    veriler = re.findall(r"\[(.*?)\] Sicaklik: ([0-9.]+) Â°C \| Nem: ([0-9.]+) %", metin)
    df = pd.DataFrame(veriler, columns=["Zaman", "Sıcaklık", "Nem"])

    # Tür dönüşümleri ve hatalı verileri NaT/NaN yap
    df["Zaman"] = pd.to_datetime(df["Zaman"], errors="coerce")
    df["Sıcaklık"] = pd.to_numeric(df["Sıcaklık"], errors="coerce")
    df["Nem"] = pd.to_numeric(df["Nem"], errors="coerce")

    # NaT veya NaN olan satırları temizle
    df = df.dropna(subset=["Zaman", "Sıcaklık", "Nem"])

    return df

# -----------------------------
# Veri Çek
# -----------------------------
df = veri_yukle()

# -----------------------------
# Eğer veri varsa devam et
# -----------------------------
if not df.empty:
    min_zaman = df["Zaman"].min()
    max_zaman = df["Zaman"].max()

    baslangic_default = min_zaman.date() if pd.notna(min_zaman) else date.today()
    bitis_default = max_zaman.date() if pd.notna(max_zaman) else date.today()

    # Tarih aralığı seçimi
    st.subheader("📅 Tarih Aralığı Seç")
    baslangic = st.date_input("Başlangıç", baslangic_default)
    bitis = st.date_input("Bitiş", bitis_default)

    # Filtreleme
    filtreli_df = df[
        (df["Zaman"].dt.date >= baslangic) & (df["Zaman"].dt.date <= bitis)
    ]

    # Genel Bilgiler
    st.markdown(f"🕒 **Toplam Veri Sayısı:** `{len(filtreli_df)}`  |  📅 **Son Güncelleme:** `{filtreli_df['Zaman'].max()}`")

    # Sıcaklık uyarısı
    max_sicaklik = filtreli_df["Sıcaklık"].max()
    if max_sicaklik >= 30:
        st.warning(f"⚠️ Sıcaklık yüksek! En yüksek sıcaklık: {max_sicaklik:.1f} °C")

    # CSV indirme
    csv = filtreli_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Filtrelenmiş Veriyi İndir (CSV)", data=csv, file_name="veriler.csv", mime="text/csv")

    # Sekmeli görünüm
    tab1, tab2 = st.tabs(["📊 Tablo", "📈 Grafikler"])

    with tab1:
        st.subheader("📋 Filtrelenmiş Veriler")
        st.dataframe(filtreli_df, use_container_width=True)

    with tab2:
        st.subheader("🌡️ Sıcaklık Grafiği")
        grafik_sicaklik = alt.Chart(filtreli_df).mark_line(color="orange").encode(
            x="Zaman:T", y="Sıcaklık:Q", tooltip=["Zaman", "Sıcaklık"]
        ).properties(title="Sıcaklık Zaman Grafiği")
        st.altair_chart(grafik_sicaklik, use_container_width=True)

        st.subheader("💧 Nem Grafiği")
        grafik_nem = alt.Chart(filtreli_df).mark_line(color="blue").encode(
            x="Zaman:T", y="Nem:Q", tooltip=["Zaman", "Nem"]
        ).properties(title="Nem Zaman Grafiği")
        st.altair_chart(grafik_nem, use_container_width=True)

else:
    st.error("⚠️ Uygun veri bulunamadı.")