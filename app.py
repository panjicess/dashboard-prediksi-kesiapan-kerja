# ============================================================
# app.py - DASHBOARD PREDIKSI KESIAPAN KERJA MAHASISWA
# DENGAN FITUR EVALUASI FAKTOR DOMINAN
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# ============================================================
# SETUP HALAMAN
# ============================================================
st.set_page_config(
    page_title="Prediksi Kesiapan Kerja Mahasiswa",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# FUNGSI REKOMENDASI
# ============================================================
def tampilkan_rekomendasi(soft_input, life_input, tech_input):
    st.markdown("---")
    st.subheader("Rekomendasi Pembinaan")
    
    soft_avg = np.mean(soft_input)
    life_avg = np.mean(life_input)
    tech_avg = np.mean(tech_input)
    
    if soft_avg < 3.0:
        st.warning("Soft Skill rendah. Perlu pelatihan komunikasi, manajemen stres, dan kerja sama tim.")
    elif soft_avg < 4.0:
        st.info("Soft Skill sedang. Tingkatkan komunikasi dan pengambilan keputusan.")
    else:
        st.success("Soft Skill baik. Pertahankan.")
    
    if life_avg < 3.0:
        st.warning("Life Skill rendah. Perlu pengembangan kepemimpinan dan kemampuan presentasi.")
    elif life_avg < 4.0:
        st.info("Life Skill sedang. Tingkatkan kepemimpinan dan relasi.")
    else:
        st.success("Life Skill baik. Pertahankan.")
    
    if tech_avg < 3.0:
        st.warning("Technical Skill rendah. Perlu pelatihan manajemen waktu dan proyek.")
    elif tech_avg < 4.0:
        st.info("Technical Skill sedang. Tingkatkan manajemen kualitas dan proyek.")
    else:
        st.success("Technical Skill baik. Pertahankan.")
    
    st.markdown("---")
    st.subheader("Rangkuman Rekomendasi")
    
    rekomendasi = []
    if soft_avg < 3.5:
        rekomendasi.append("Ikuti pelatihan komunikasi dan kepemimpinan")
    if life_avg < 3.5:
        rekomendasi.append("Aktif dalam organisasi untuk mengembangkan life skill")
    if tech_avg < 3.5:
        rekomendasi.append("Ikuti workshop dan sertifikasi teknis")
    
    if rekomendasi:
        for r in rekomendasi:
            st.write("- " + r)
    else:
        st.success("Semua aspek sudah baik. Pertahankan dan terus tingkatkan.")

# ============================================================
# FUNGSI EVALUASI FAKTOR DOMINAN
# ============================================================
def evaluasi_faktor_dominan(model, feature_names):
    st.markdown("---")
    st.subheader("Evaluasi Faktor Dominan")
    
    # Hitung feature importance per kelompok
    soft_cols = feature_names[:18]
    life_cols = feature_names[18:27]
    tech_cols = feature_names[27:36]
    
    feature_importance = pd.DataFrame({
        'Fitur': feature_names,
        'Importance': model.feature_importances_
    })
    
    soft_imp = feature_importance[feature_importance['Fitur'].isin(soft_cols)]['Importance'].sum()
    life_imp = feature_importance[feature_importance['Fitur'].isin(life_cols)]['Importance'].sum()
    tech_imp = feature_importance[feature_importance['Fitur'].isin(tech_cols)]['Importance'].sum()
    total_imp = soft_imp + life_imp + tech_imp
    
    soft_pct = soft_imp / total_imp * 100
    life_pct = life_imp / total_imp * 100
    tech_pct = tech_imp / total_imp * 100
    
    # Tampilkan dalam bentuk bar dengan warna
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if soft_pct >= 40:
            st.success(f"Soft Skill: {soft_pct:.1f}%")
            st.caption("Dominan - Pertahankan")
        elif soft_pct >= 25:
            st.info(f"Soft Skill: {soft_pct:.1f}%")
            st.caption("Sedang - Perhatikan")
        else:
            st.error(f"Soft Skill: {soft_pct:.1f}%")
            st.caption("Rendah - Perlu Evaluasi!")
    
    with col2:
        if life_pct >= 40:
            st.success(f"Life Skill: {life_pct:.1f}%")
            st.caption("Dominan - Pertahankan")
        elif life_pct >= 25:
            st.info(f"Life Skill: {life_pct:.1f}%")
            st.caption("Sedang - Perhatikan")
        else:
            st.error(f"Life Skill: {life_pct:.1f}%")
            st.caption("Rendah - Perlu Evaluasi!")
    
    with col3:
        if tech_pct >= 40:
            st.success(f"Technical: {tech_pct:.1f}%")
            st.caption("Dominan - Pertahankan")
        elif tech_pct >= 25:
            st.info(f"Technical: {tech_pct:.1f}%")
            st.caption("Sedang - Perhatikan")
        else:
            st.error(f"Technical: {tech_pct:.1f}%")
            st.caption("Rendah - Perlu Evaluasi!")
    
    # Visualisasi bar chart
    st.markdown("---")
    fig, ax = plt.subplots(figsize=(8, 4))
    categories = ['Soft Skill', 'Life Skill', 'Technical']
    percentages = [soft_pct, life_pct, tech_pct]
    colors = ['#27ae60' if x >= 40 else '#f39c12' if x >= 25 else '#e74c3c' for x in percentages]
    
    bars = ax.bar(categories, percentages, color=colors)
    ax.set_ylabel('Kontribusi (%)')
    ax.set_title('Kontribusi Faktor Dominan terhadap Kesiapan Kerja')
    ax.set_ylim(0, 100)
    
    for bar, pct in zip(bars, percentages):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{pct:.1f}%', ha='center', fontsize=12)
    
    st.pyplot(fig)
    
    # Rekomendasi evaluasi
    st.markdown("---")
    st.subheader("Rekomendasi Evaluasi untuk Dosen")
    
    data = [
        ("Soft Skill", soft_pct, "Tingkatkan komunikasi, kerja tim, dan manajemen stres."),
        ("Life Skill", life_pct, "Tingkatkan kepemimpinan, relasi, dan kemampuan presentasi."),
        ("Technical Skill", tech_pct, "Tingkatkan manajemen waktu, kualitas, dan proyek.")
    ]
    data.sort(key=lambda x: x[1])
    
    terendah = data[0]
    kedua = data[1]
    
    st.write(f"""
    **Fokus Pembinaan:**
    
    1. **{terendah[0]}** ({terendah[1]:.1f}%) - Kontribusi terendah → **Perlu dievaluasi dan ditingkatkan**
    2. **{kedua[0]}** ({kedua[1]:.1f}%) - Kontribusi sedang → Perlu diperhatikan
    """)
    
    st.info(f"💡 Rekomendasi untuk {terendah[0]}: {terendah[2]}")
    
    # Tabel ringkasan
    st.markdown("---")
    st.subheader("Ringkasan Evaluasi")
    summary_df = pd.DataFrame({
        'Kelompok': ['Soft Skill', 'Life Skill', 'Technical'],
        'Kontribusi': [f'{soft_pct:.1f}%', f'{life_pct:.1f}%', f'{tech_pct:.1f}%'],
        'Status': [
            'Dominan' if soft_pct >= 40 else 'Sedang' if soft_pct >= 25 else 'Perlu Evaluasi',
            'Dominan' if life_pct >= 40 else 'Sedang' if life_pct >= 25 else 'Perlu Evaluasi',
            'Dominan' if tech_pct >= 40 else 'Sedang' if tech_pct >= 25 else 'Perlu Evaluasi'
        ]
    })
    st.dataframe(summary_df, hide_index=True)

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    model = joblib.load('model_random_forest_final.pkl')
    feature_names = joblib.load('feature_names.pkl')
    return model, feature_names

st.title("Prediksi Kesiapan Kerja Mahasiswa")
st.markdown("---")

try:
    model, feature_names = load_model()
    st.success("Model berhasil dimuat")
except:
    st.error("File model tidak ditemukan.")
    st.stop()

# ============================================================
# SIDEBAR INFORMASI
# ============================================================
st.sidebar.title("Informasi")
st.sidebar.markdown("""
**Model Prediksi Kesiapan Kerja**
- Algoritma: Random Forest
- Fitur: 36 item (Soft, Life, Technical Skill)
- Skala: 0-5

**Panduan Penggunaan:**
1. Pilih metode input
2. Klik tombol Prediksi
3. Lihat hasil dan rekomendasi
""")

# ============================================================
# TAB: INPUT MANUAL VS UPLOAD EXCEL
# ============================================================
tab1, tab2 = st.tabs(["Input Manual", "Upload Excel"])

# ============================================================
# TAB 1: INPUT MANUAL
# ============================================================
with tab1:
    st.subheader("Input Data Mahasiswa Manual")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Soft Skill**")
        soft_input = []
        soft_cols = feature_names[:18]
        for col in soft_cols:
            val = st.slider(col, 0, 5, 2, key=f"manual_{col}")
            soft_input.append(val)
    
    with col2:
        st.markdown("**Life Skill**")
        life_input = []
        life_cols = feature_names[18:27]
        for col in life_cols:
            val = st.slider(col, 0, 5, 2, key=f"manual_life_{col}")
            life_input.append(val)
    
    with col3:
        st.markdown("**Technical Skill**")
        tech_input = []
        tech_cols = feature_names[27:36]
        for col in tech_cols:
            val = st.slider(col, 0, 5, 2, key=f"manual_tech_{col}")
            tech_input.append(val)
    
    input_data = soft_input + life_input + tech_input
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Soft Skill", f"{np.mean(soft_input):.2f}", "Skala 0-5")
    with col2:
        st.metric("Life Skill", f"{np.mean(life_input):.2f}", "Skala 0-5")
    with col3:
        st.metric("Technical Skill", f"{np.mean(tech_input):.2f}", "Skala 0-5")
    
    st.markdown("---")
    
    if st.button("Prediksi Manual", type="primary", use_container_width=True):
        input_df = pd.DataFrame([input_data], columns=feature_names)
        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Hasil Prediksi")
            if pred == 1:
                st.success("SIAP KERJA")
                st.metric("Probabilitas", f"{proba[1]*100:.2f}%")
            else:
                st.error("BELUM SIAP KERJA")
                st.metric("Probabilitas", f"{proba[0]*100:.2f}%")
        
        with col2:
            st.subheader("Distribusi Probabilitas")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(['Belum Siap', 'Siap'], proba, color=['#e74c3c', '#27ae60'])
            ax.set_ylim(0, 1)
            ax.set_ylabel('Probabilitas')
            for i, v in enumerate(proba):
                ax.text(i, v + 0.05, f'{v*100:.1f}%', ha='center')
            st.pyplot(fig)
        
        tampilkan_rekomendasi(soft_input, life_input, tech_input)
        
        # ========== FITUR EVALUASI FAKTOR DOMINAN ==========
        evaluasi_faktor_dominan(model, feature_names)

# ============================================================
# TAB 2: UPLOAD EXCEL (SAMA, TAMBAHKAN evaluasi_faktor_dominan)
# ============================================================
with tab2:
    st.subheader("Upload File Excel untuk Prediksi Batch")
    st.markdown("""
    **Format File Excel:**
    - File harus memiliki 36 kolom fitur (skala 0-5)
    - Kolom pertama dapat berisi NIM atau Nama Mahasiswa
    - Nilai setiap fitur: skala 0-5
    """)
    
    template_df = pd.DataFrame({
        'NIM': ['123456', '234567'],
        'Nama': ['Mahasiswa A', 'Mahasiswa B'],
        **{col: [3, 4] for col in feature_names[:5]},
        **{col: [3, 4] for col in feature_names[5:10]},
        **{col: [3, 4] for col in feature_names[10:15]},
        **{col: [3, 4] for col in feature_names[15:20]},
        **{col: [3, 4] for col in feature_names[20:25]},
        **{col: [3, 4] for col in feature_names[25:30]},
        **{col: [3, 4] for col in feature_names[30:36]}
    })
    
    buffer = BytesIO()
    template_df.to_excel(buffer, index=False)
    buffer.seek(0)
    
    st.download_button(
        label="Download Template Excel",
        data=buffer,
        file_name="template_prediksi_mahasiswa.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Upload file Excel (format .xlsx atau .xls)",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        try:
            df_upload = pd.read_excel(uploaded_file)
            st.success(f"File berhasil diupload ({len(df_upload)} baris data)")
            
            st.subheader("Preview Data")
            st.dataframe(df_upload.head(10))
            
            fitur_ditemukan = []
            for col in feature_names:
                if col in df_upload.columns:
                    fitur_ditemukan.append(col)
                elif col.lower() in [c.lower() for c in df_upload.columns]:
                    match = [c for c in df_upload.columns if c.lower() == col.lower()]
                    if match:
                        fitur_ditemukan.append(match[0])
            
            if len(fitur_ditemukan) != len(feature_names):
                st.warning(f"Hanya {len(fitur_ditemukan)} dari {len(feature_names)} fitur yang ditemukan")
                missing = set(feature_names) - set(fitur_ditemukan)
                st.write("Fitur yang hilang:", list(missing))
            else:
                X_upload = df_upload[fitur_ditemukan].values
                st.info(f"{len(fitur_ditemukan)} fitur ditemukan, siap diprediksi")
                
                if st.button("Prediksi Semua Data", type="primary", use_container_width=True):
                    y_pred_batch = model.predict(X_upload)
                    y_proba_batch = model.predict_proba(X_upload)[:, 1]
                    
                    df_upload['Prediksi'] = y_pred_batch
                    df_upload['Probabilitas'] = y_proba_batch
                    df_upload['Status'] = df_upload['Prediksi'].map({1: 'Siap Kerja', 0: 'Belum Siap'})
                    
                    st.subheader("Hasil Prediksi")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Mahasiswa", len(df_upload))
                    with col2:
                        siap = df_upload['Status'].value_counts().get('Siap Kerja', 0)
                        st.metric("Siap Kerja", siap, f"{siap/len(df_upload)*100:.1f}%")
                    with col3:
                        belum = df_upload['Status'].value_counts().get('Belum Siap', 0)
                        st.metric("Belum Siap", belum, f"{belum/len(df_upload)*100:.1f}%")
                    
                    st.subheader("Detail Hasil Prediksi")
                    cols_to_show = []
                    if 'NIM' in df_upload.columns:
                        cols_to_show.append('NIM')
                    if 'Nama' in df_upload.columns:
                        cols_to_show.append('Nama')
                    if 'Nama Lengkap' in df_upload.columns:
                        cols_to_show.append('Nama Lengkap')
                    if not cols_to_show:
                        cols_to_show = [df_upload.columns[0]]
                    
                    cols_to_show.extend(['Status', 'Probabilitas'])
                    st.dataframe(df_upload[cols_to_show])
                    
                    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
                    
                    status_counts = df_upload['Status'].value_counts()
                    axes[0].pie(status_counts.values, labels=status_counts.index, 
                                autopct='%1.1f%%', colors=['#27ae60', '#e74c3c'], explode=[0.05, 0])
                    axes[0].set_title(f'Hasil Prediksi (n={len(df_upload)})')
                    
                    axes[1].hist(y_proba_batch, bins=20, edgecolor='black', alpha=0.7, color='purple')
                    axes[1].axvline(0.5, color='red', linestyle='--', linewidth=2, label='Threshold 0.5')
                    axes[1].axvline(y_proba_batch.mean(), color='blue', linestyle='--', 
                                   linewidth=2, label=f'Mean={y_proba_batch.mean():.3f}')
                    axes[1].set_title('Distribusi Probabilitas')
                    axes[1].set_xlabel('Probabilitas Siap Kerja')
                    axes[1].set_ylabel('Jumlah Mahasiswa')
                    axes[1].legend()
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # ========== FITUR EVALUASI FAKTOR DOMINAN ==========
                    evaluasi_faktor_dominan(model, feature_names)
                    
                    output = BytesIO()
                    df_upload.to_excel(output, index=False)
                    output.seek(0)
                    
                    st.download_button(
                        label="Download Hasil Prediksi (Excel)",
                        data=output,
                        file_name="hasil_prediksi_mahasiswa.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
        except Exception as e:
            st.error(f"Error membaca file: {str(e)}")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Model Prediksi Kesiapan Kerja Mahasiswa - Random Forest")