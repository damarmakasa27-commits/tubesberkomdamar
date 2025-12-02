import streamlit as st
import matplotlib.pyplot as plt

st.title("Mining Transaction Summary")

st.markdown("""
Program ini memberikan rekap hasil akhir penjualan, pajak, ongkir, keuntungan, 
dan emisi CO₂ dari berbagai jenis bahan galian.
""")

# INPUT DASAR
st.header("Input Dasar")

N = st.number_input("Masukkan jumlah jenis bahan galian:", min_value=1, step=1)

harga_ongkir = st.number_input("Masukkan harga ongkos kirim per km:", min_value=0.0)
jarak = st.number_input("Masukkan jarak pengiriman (km):", min_value=0.0)
biaya_operasional = st.number_input("Masukkan biaya operasional:", min_value=0.0)

# List data
bahan_galian = []
stok = []
harga_jual = []
jumlah_beli = []
kemurnian = []
diesel_list = []
listrik_list = []

# Emission factors
faktor_emisi_diesel = 2.68
faktor_emisi_listrik = 0.85

# INPUT DATA PER BAHAN
st.header("Input Data Tiap Bahan Galian")

for i in range(N):
    st.subheader(f"Bahan galian ke-{i+1}")

    nama = st.text_input(f"Nama bahan galian {i+1}", key=f"nama_{i}")
    stok_bahan = st.number_input(f"Jumlah stok {nama} (kg):", min_value=0.0, key=f"stok_{i}")
    harga = st.number_input(f"Harga per kg {nama}:", min_value=0.0, key=f"harga_{i}")
    jumlah = st.number_input(f"Jumlah dibeli {nama} (kg):", min_value=0.0, key=f"beli_{i}")
    kem = st.number_input(f"Kemurnian {nama} (%):", min_value=0.0, max_value=100.0, key=f"kem_{i}")

    diesel = st.number_input(f"Konsumsi diesel (liter) untuk {nama}:", min_value=0.0, key=f"diesel_{i}")
    listrik = st.number_input(f"Konsumsi listrik (kWh) untuk {nama}:", min_value=0.0, key=f"listrik_{i}")

    bahan_galian.append(nama)
    stok.append(stok_bahan)
    harga_jual.append(harga)
    jumlah_beli.append(jumlah)
    kemurnian.append(kem)
    diesel_list.append(diesel)
    listrik_list.append(listrik)

# PERHITUNGAN
if st.button("Hitung Summary"):
    stok_tidak_cukup = any(jumlah_beli[i] > stok[i] for i in range(N))

    if stok_tidak_cukup:
        st.error("Ada jumlah pembelian yang melebihi stok!")
    else:
        st.success("Perhitungan berhasil!")

        total_pajak = 0
        total_emisi = 0
        total_sebelum = 0
        total_penjualan = 0

        emisi_per_bahan = []

        st.header("Summary Penjualan per Bahan")

        for i in range(N):
            hasil = harga_jual[i] * jumlah_beli[i]
            hasil_kemurnian = hasil * (kemurnian[i] / 100)
            pajak = hasil_kemurnian * 0.1
            sisa = stok[i] - jumlah_beli[i]

            total_pajak += pajak
            total_sebelum += hasil_kemurnian
            total_penjualan += hasil_kemurnian + pajak

            # Emisi
            emisi = faktor_emisi_diesel * diesel_list[i] + faktor_emisi_listrik * listrik_list[i]
            total_emisi += emisi
            emisi_per_bahan.append(emisi)

            # Output
            st.subheader(f"{bahan_galian[i]}")
            st.write(f"Jumlah dibeli: **{jumlah_beli[i]} kg**")
            st.write(f"Harga per kg: **{harga_jual[i]}**")
            st.write(f"Kemurnian: **{kemurnian[i]}%**")
            st.write(f"Harga bersih: **{hasil_kemurnian:,.0f}**")
            st.write(f"Pajak (10%): **{pajak:,.0f}**")
            st.write(f"Sisa stok: **{sisa} kg**")
            st.write(f"Total harga setelah pajak: **{hasil_kemurnian + pajak:,.0f}**")
            st.write(f"Emisi CO₂: **{emisi:.2f} kg**")

        # Ongkir
        total_ongkir = jarak * harga_ongkir
        total_penjualan += total_ongkir

        # Keuntungan
        keuntungan = total_penjualan - biaya_operasional

        # RINGKASAN AKHIR
        st.header("Ringkasan Akhir")
        st.write(f"Total harga sebelum pajak & ongkir: **{total_sebelum:,.0f}**")
        st.write(f"Total pajak: **{total_pajak:,.0f}**")
        st.write(f"Total ongkir: **{total_ongkir:,.0f}**")
        st.write(f"Total harga setelah pajak & ongkir: **{total_penjualan:,.0f}**")
        st.write(f"Total keuntungan: **{keuntungan:,.0f}**")
        st.write(f"Total emisi CO₂ seluruh produksi: **{total_emisi:.2f} kg**")

        # GRAFIK 1 – Jumlah Pembelian
        st.header("Grafik Jumlah Pembelian Bahan Galian")

        plt.figure(figsize=(7, 4))
        plt.bar(bahan_galian, jumlah_beli)
        plt.xlabel("Jenis Bahan Galian")
        plt.ylabel("Jumlah Pembelian (kg)")
        plt.xticks(rotation=20)
        st.pyplot(plt)

        # GRAFIK 2 – Emisi Per Bahan
        st.header("Grafik Emisi CO₂ per Bahan")

        plt.figure(figsize=(7, 4))
        plt.plot(bahan_galian, emisi_per_bahan, marker='o')
        plt.xlabel("Jenis Bahan Galian")
        plt.ylabel("Emisi CO₂ (kg)")
        plt.grid(True)
        plt.xticks(rotation=20)
        st.pyplot(plt)