import streamlit as st
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optimasi Produksi Coklat & Biskuit", layout="wide")

st.title("🍫🍪 Optimasi Produksi Coklat & Biskuit")
st.markdown("Aplikasi ini digunakan untuk memaksimalkan keuntungan produksi dari dua produk: **Coklat** dan **Biskuit**, dengan mempertimbangkan batasan bahan baku dan waktu kerja.")

# Input Parameter
st.header("📥 Input Parameter Produksi")
col1, col2 = st.columns(2)

with col1:
    profit_coklat = st.number_input("Keuntungan per unit Coklat (Rp)", value=5000)
    profit_biskuit = st.number_input("Keuntungan per unit Biskuit (Rp)", value=3000)
    total_bahan = st.number_input("Total Bahan Baku Tersedia (kg)", value=100)
    total_waktu = st.number_input("Total Waktu Produksi (jam)", value=80)

with col2:
    bahan_coklat = st.number_input("Bahan Baku per unit Coklat (kg)", value=2)
    bahan_biskuit = st.number_input("Bahan Baku per unit Biskuit (kg)", value=1)
    waktu_coklat = st.number_input("Waktu Produksi per unit Coklat (jam)", value=1.5)
    waktu_biskuit = st.number_input("Waktu Produksi per unit Biskuit (jam)", value=1)

# Model LP
c = [-profit_coklat, -profit_biskuit]
A = [
    [bahan_coklat, bahan_biskuit],
    [waktu_coklat, waktu_biskuit]
]
b = [total_bahan, total_waktu]
x_bounds = (0, None)

# Solve LP
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds], method='highs')

st.header("📤 Hasil Optimasi")
if res.success:
    coklat, biskuit = res.x
    total_keuntungan = -res.fun
    st.success("✅ Solusi Optimal Ditemukan")
    st.write(f"Produksi Coklat: **{coklat:.2f} unit**")
    st.write(f"Produksi Biskuit: **{biskuit:.2f} unit**")
    st.write(f"💰 Total Keuntungan Maksimum: **Rp {total_keuntungan:,.2f}**")
else:
    st.error("❌ Gagal menemukan solusi. Cek kembali input parameter.")

# Visualisasi Feasible Area
st.header("📊 Visualisasi Area Feasible")
fig, ax = plt.subplots()

x_vals = np.linspace(0, total_bahan, 400)
y1 = (total_bahan - bahan_coklat * x_vals) / bahan_biskuit
y2 = (total_waktu - waktu_coklat * x_vals) / waktu_biskuit
y1 = np.maximum(0, y1)
y2 = np.maximum(0, y2)

plt.plot(x_vals, y1, label="Kendala Bahan Baku")
plt.plot(x_vals, y2, label="Kendala Waktu")
plt.fill_between(x_vals, np.minimum(y1, y2), color='lightgreen', alpha=0.5)

if res.success:
    plt.plot(coklat, biskuit, 'ro', label="Solusi Optimal")
    plt.text(coklat, biskuit, f"({coklat:.1f}, {biskuit:.1f})", fontsize=9, color='red')

plt.xlabel("Unit Coklat")
plt.ylabel("Unit Biskuit")
plt.title("Area Feasible dan Solusi Optimal")
plt.legend()
st.pyplot(fig)
