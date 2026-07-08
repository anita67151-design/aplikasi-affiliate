import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Affiliate Content Machine", page_icon="⚡")
st.title("⚡ Affiliate Content Machine")

api_key = st.secrets["GEMINI_API_KEY"]

# Input tambahan untuk jumlah VO
jumlah_vo = st.sidebar.slider("Jumlah VO yang ingin dibuat:", 1, 10, 3)

deskripsi = st.text_area("Paste deskripsi/foto produk:")
mode = st.radio("Mode:", ["Generate VO", "Generate Caption & Hashtag"])

@st.cache_resource
def get_stable_model(key):
    genai.configure(api_key=key)
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if not models:
        raise Exception("Tidak ada model yang ditemukan.")
    return genai.GenerativeModel(models[0].name)

if 'last_vo' not in st.session_state: st.session_state.last_vo = ""

if st.button("Proses"):
    if not api_key: st.error("Masukkan API Key!")
    else:
        try:
            model = get_stable_model(api_key)
            
            if mode == "Generate VO":
                # Prompt diperbarui agar mengikuti jumlah_vo
                prompt = f"""
                Anda adalah affiliator Shopee dan TikTok Shop profesional. 
                Buatkan {jumlah_vo} variasi VO (talking head) yang berbeda untuk produk: {deskripsi}.
                
                Aturan WAJIB:
                - Bahasa Indonesia natural, santai, 25-40 detik per VO.
                - Hook HARUS langsung bahas produk (no basa-basi).
                - HINDARI: keterangan adegan, emoji, ringkasan, atau struktur formal iklan.
                - Buat naskah utuh siap baca untuk setiap VO.
                - Struktur: Hook -> Problem -> Solusi -> Benefit -> CTA kuat.
                - Format output wajib:
                  VO 1
                  "Teks VO..."
                  
                  VO 2
                  "Teks VO..."
                  (dan seterusnya sampai VO {jumlah_vo})
                """
                response = model.generate_content(prompt)
                st.session_state.last_vo = response.text
                st.write(response.text)
            
            else:
                prompt = f"""
                Buatkan Caption dan Hashtag untuk setiap VO di bawah ini: {st.session_state.last_vo}
                
                Format WAJIB untuk setiap VO:
                🎥 VO [nomor]
                TikTok
                [Caption 1 kalimat, natural, keyword produk]
                #tag1 #tag2 #tag3 #tag4 #tag5
                
                Shopee
                [Caption 2-4 kata, keyword produk]
                #tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7 #tag8
                
                (Langsung hasil, tanpa penjelasan tambahan).
                """
                response = model.generate_content(prompt)
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")
