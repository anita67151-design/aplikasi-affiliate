import streamlit as st
import google.generativeai as genai

# Tampilan Judul
st.set_page_config(page_title="Affiliate Script AI", page_icon="🚀")
st.title("🚀 AI Affiliate Content Generator")

# Sidebar untuk API Key
api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

deskripsi = st.text_area("Paste Deskripsi Produk dari Marketplace:")

if st.button("Generate Script"):
    if not api_key:
        st.error("Silakan masukkan API Key di sidebar!")
    elif not deskripsi:
        st.warning("Masukkan deskripsi produk dulu!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Anda adalah ahli affiliate marketing. Berdasarkan deskripsi produk berikut:
            '{deskripsi}'
            
            Buatkan script video promosi untuk TikTok/Shopee Video.
            Format wajib:
            1. Hook: (pembuka yang bikin penasaran).
            2. Isi: (keunggulan produk yang relevan).
            3. Call to Action: (ajakan beli yang kuat).
            
            Gunakan gaya bahasa santai dan menjual.
            """
            
            response = model.generate_content(prompt)
            st.subheader("Hasil Script:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
