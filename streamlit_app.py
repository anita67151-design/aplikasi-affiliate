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
            # Hardcoded model untuk mempercepat respon
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if mode == "Generate VO":
                prompt = f"""
                Bertindaklah sebagai affiliator Shopee dan TikTok Shop.
                Produk: {deskripsi}
                
                Ikuti aturan ketat:
                1. Bahasa natural, santai, talking head, 25-40 detik (70-120 kata).
                2. Hook langsung bahas produk (jangan: "Pernah nggak...", "Siapa yang...").
                3. TANPA keterangan adegan/B-roll. TANPA emoji.
                4. Struktur: Hook -> Problem -> Solusi -> Benefit -> CTA kuat.
                5. CTA harus memancing tindakan (bukan cuma "klik keranjang").
                6. Hasil harus siap baca, langsung tulis VO 1, "Teks VO", dst.
                """
                response = model.generate_content(prompt)
                st.session_state.last_vo = response.text
                st.write(response.text)
            
            else:
                prompt = f"""
                Buatkan caption dan hashtag berdasarkan VO ini: {st.session_state.last_vo}
                Ikuti format: 
                🎥 VO X
                TikTok: [Caption 1 kalimat natural + 5 hashtag relevan]
                Shopee: [Caption 2-4 kata + 8-10 hashtag SEO]
                
                Langsung hasil saja, tanpa basa-basi atau penjelasan.
                """
                response = model.generate_content(prompt)
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
