import streamlit as st
import pulp
import numpy as np
import matplotlib.pyplot as plt

st.title("🧮 Aplikasi Optimasi Produksi (Linear Programming)")

st.markdown("Aplikasi ini memaksimalkan keuntungan produksi dua produk dengan batasan sumber daya.")

# ------------------------------
# Input dari pengguna
# ------------------------------
with st.sidebar:
    st.header("Input Parameter Produksi")
    keuntungan_A = st.number_input("Keuntungan per unit Produk A", value=30)
    keuntungan_B = st.number_input("Keuntungan per unit Produk B", value=20)
    
    waktu_A = st.number_input("Jam kerja per unit Produk A", value=2)
    waktu_B = st.number_input("Jam kerja per unit Produk B", value=1)
    total_waktu = st.number_input("Total jam kerja tersedia", value=100)

    bahan_A = st.number_input("Bahan baku per unit Produk A", value=1)
    bahan_B = st.number_input("Bahan baku per unit Produk B", value=1)
    total_bahan = st.number_input("Total bahan baku tersedia", value=80)

# ------------------------------
# Model LP
# ------------------------------
model = pulp.LpProblem("Optimasi_Produksi", pulp.LpMaximize)
x = pulp.LpVariable("Produk_A", lowBound=0, cat="Continuous")
y = pulp.LpVariable("Produk_B", lowBound=0, cat="Continuous")

# Fungsi objektif
model += keuntungan_A * x + keuntungan_B * y

# Kendala
model += waktu_A * x + waktu_B * y <= total_waktu, "Kendala_Waktu"
model += bahan_A * x + bahan_B * y <= total_bahan, "Kendala_Bahan"

# ------------------------------
# Solusi
# ------------------------------
model.solve()

st.subheader("📌 Hasil Optimasi")
if pulp.LpStatus[model.status] == 'Optimal':
    st.success("Solusi Optimal Ditemukan ✅")
    st.write(f"Jumlah Produk A: {x.varValue}")
    st.write(f"Jumlah Produk B: {y.varValue}")
    st.write(f"Total Keuntungan: Rp {pulp.value(model.objective):,.0f}")
else:
    st.error("Tidak ditemukan solusi optimal.")

# ------------------------------
# Visualisasi Feasible Area
# ------------------------------
st.subheader("📊 Visualisasi Area Feasible")

x_vals = np.linspace(0, max(total_waktu, total_bahan), 200)
y1 = (total_waktu - waktu_A * x_vals) / waktu_B
y2 = (total_bahan - bahan_A * x_vals) / bahan_B
y_vals = np.minimum(y1, y2)

fig, ax = plt.subplots()
plt.plot(x_vals, y1, label="Kendala Waktu")
plt.plot(x_vals, y2, label="Kendala Bahan")
plt.fill_between(x_vals, 0, y_vals, where=(y_vals >= 0), color='skyblue', alpha=0.4, label='Area Feasible')

plt.plot(x.varValue, y.varValue, 'ro', label='Solusi Optimal')
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.xlabel('Jumlah Produk A')
plt.ylabel('Jumlah Produk B')
plt.title('Area Feasible dan Solusi Optimal')
plt.legend()
plt.grid(True)
st.pyplot(fig)
