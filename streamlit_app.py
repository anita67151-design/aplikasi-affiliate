import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Affiliate Content Machine", page_icon="⚡")
st.title("⚡ Affiliate Content Machine")

api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
deskripsi = st.text_area("Paste deskripsi/foto produk:")
mode = st.radio("Mode:", ["Generate VO", "Generate Caption & Hashtag"])

if 'last_vo' not in st.session_state: st.session_state.last_vo = ""

if st.button("Proses"):
    if not api_key: st.error("Masukkan API Key!")
    else:
        try:
            genai.configure(api_key=api_key)
            # Menggunakan model yang paling stabil untuk teks panjang
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if mode == "Generate VO":
                # PROMPT LENGKAP ANDA DIMASUKKAN DI SINI
                prompt = f"""
                Anda adalah affiliator Shopee dan TikTok Shop berpengalaman. 
                Produk: {deskripsi}
                
                Instruksi WAJIB:
                1. Gunakan bahasa Indonesia natural, santai, untuk talking head.
                2. Durasi tiap VO 25-40 detik (70-120 kata).
                3. Struktur: Hook -> Problem -> Solusi -> Benefit -> CTA kuat.
                4. Hook HARUS langsung bahas produk di kalimat pertama (jangan basa-basi).
                5. HINDARI: keterangan adegan/B-roll, emoji, pengulangan, dan bahasa iklan formal.
                6. JANGAN meringkas VO menjadi poin-poin. Buat naskah utuh.
                7. Format output:
                   VO 1
                   "Teks VO lengkap"
                   
                   VO 2
                   "Teks VO lengkap"
                   (dan seterusnya)
                """
                response = model.generate_content(prompt)
                st.session_state.last_vo = response.text
                st.write(response.text)
            
            else:
                prompt = f"""
                Buatkan caption dan hashtag berdasarkan VO berikut: {st.session_state.last_vo}
                
                Format WAJIB:
                🎥 VO 1
                TikTok
                [Caption 1 kalimat, natural, keyword utama]
                #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
                
                Shopee
                [Caption 2-4 kata]
                #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5 #hashtag6 #hashtag7 #hashtag8
                
                (Buatkan untuk semua VO yang ada. Langsung hasil, tanpa penjelasan tambahan).
                """
                response = model.generate_content(prompt)
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
