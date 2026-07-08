import streamlit as st
import google.generativeai as genai

st.title("🚀 AI Affiliate Content Generator")

api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
deskripsi = st.text_area("Paste Deskripsi Produk:")

if st.button("Generate Script"):
    if not api_key:
        st.error("Masukkan API Key!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # KITA UBAH CARA MENGAMBIL MODEL
            # Kita minta daftar model yang tersedia, lalu ambil yang pertama (pasti ada)
            models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(models[0].name) 
            
            prompt = f"Buatkan script konten affiliate untuk produk ini: {deskripsi}. Format: Hook, Isi, CTA. Bahasa santai."
            response = model.generate_content(prompt)
            
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
