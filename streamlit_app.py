import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Affiliate Script AI", page_icon="🚀")
st.title("🚀 AI Affiliate Content Generator")

api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
deskripsi = st.text_area("Paste Deskripsi Produk dari Marketplace:")

if st.button("Generate Script"):
    if not api_key:
        st.error("Masukkan API Key di sidebar!")
    elif not deskripsi:
        st.warning("Masukkan deskripsi produk!")
    else:
        try:
            genai.configure(api_key=api_key)
            # Kita coba gunakan model yang pasti ada di semua akun
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            prompt = f"Buatkan script video promosi untuk: {deskripsi}. Format: Hook, Isi, CTA. Gaya: Santai & Menjual."
            
            response = model.generate_content(prompt)
            st.subheader("Hasil Script:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
