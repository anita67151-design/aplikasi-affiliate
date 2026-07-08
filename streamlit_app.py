import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Affiliate Pro", page_icon="⚡")
st.title("⚡ Affiliate Content Machine")

api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
deskripsi = st.text_area("Paste deskripsi produk:")
mode = st.radio("Mode:", ["Generate VO", "Generate Caption & Hashtag"])

# Fungsi untuk mendapatkan model yang PASTI ada di akun Anda
def get_model(api_key):
    genai.configure(api_key=api_key)
    # Mencari model yang mendukung generateContent
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if not models:
        raise Exception("Tidak ada model yang tersedia di API Key Anda.")
    # Menggunakan model pertama yang tersedia agar tidak error 404
    return genai.GenerativeModel(models[0].name)

if 'last_vo' not in st.session_state: st.session_state.last_vo = ""

if st.button("Proses"):
    if not api_key: 
        st.error("Masukkan API Key!")
    else:
        try:
            model = get_model(api_key)
            
            if mode == "Generate VO":
                prompt = f"""
                Bertindaklah sebagai affiliator Shopee/TikTok profesional.
                Produk: {deskripsi}
                
                Instruksi Ketat:
                1. Bahasa natural, santai, talking head.
                2. Hook langsung bahas produk (jangan: "Pernah gak...", "Siapa yang...").
                3. TANPA keterangan adegan, TANPA emoji, TANPA penjelasan.
                4. Durasi 25-40 detik, 70-120 kata.
                5. Struktur: Hook -> Problem -> Solusi -> Benefit -> CTA kuat.
                6. CTA harus memancing tindakan.
                7. Format: VO 1, "Teks VO", dst.
                """
                response = model.generate_content(prompt)
                st.session_state.last_vo = response.text
                st.write(response.text)
            
            else:
                prompt = f"""
                Buatkan caption & hashtag berdasarkan VO ini: {st.session_state.last_vo}
                
                Format WAJIB:
                🎥 VO 1
                TikTok: [1 kalimat natural + 5 hashtag relevan]
                Shopee: [2-4 kata + 10 hashtag SEO]
                
                Langsung hasil saja, TANPA basa-basi.
                """
                response = model.generate_content(prompt)
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
