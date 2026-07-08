import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Affiliate Content Machine", page_icon="⚡")
st.title("⚡ Affiliate Content Machine")

api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

deskripsi = st.text_area("Paste deskripsi/foto produk:")
mode = st.radio("Mode:", ["Generate VO", "Generate Caption & Hashtag (dari VO sebelumnya)"])

# Menyimpan hasil VO di memori sesi agar bisa lanjut ke Caption
if 'last_vo' not in st.session_state:
    st.session_state.last_vo = ""

if st.button("Proses"):
    if not api_key:
        st.error("Masukkan API Key!")
    else:
        try:
            genai.configure(api_key=api_key)
            models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(models[0].name)
            
            if mode == "Generate VO":
                prompt = f"""
                [PROMPT VO ANDA]:
                { (isi teks prompt VO Anda di sini) }
                
                Produk: {deskripsi}
                """
                response = model.generate_content(prompt)
                st.session_state.last_vo = response.text
                st.subheader("Hasil VO:")
                st.write(response.text)
            
            else: # Mode Caption
                prompt = f"""
                [PROMPT CAPTION & HASHTAG ANDA]:
                { (isi teks prompt Caption & Hashtag Anda di sini) }
                
                Input VO: {st.session_state.last_vo}
                """
                response = model.generate_content(prompt)
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")
