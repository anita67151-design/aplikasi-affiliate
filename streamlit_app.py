import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Affiliate Content Machine", page_icon="⚡")
st.title("⚡ Affiliate Content Machine")

api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

deskripsi = st.text_area("Paste deskripsi/foto produk:")
mode = st.radio("Mode:", ["Generate VO", "Generate Caption & Hashtag"])

# Menyimpan hasil VO agar bisa digunakan untuk Caption
if 'last_vo' not in st.session_state:
    st.session_state.last_vo = ""

if st.button("Proses"):
    if not api_key:
        st.error("Masukkan API Key di sidebar!")
    elif not deskripsi and mode == "Generate VO":
        st.warning("Masukkan deskripsi produk!")
    else:
        try:
            genai.configure(api_key=api_key)
            models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(models[0].name)
            
            if mode == "Generate VO":
                prompt = f"""
                Bertindaklah sebagai affiliator Shopee/TikTok berpengalaman.
                Aturan VO: 
                - Gunakan bahasa natural, santai, talking head, durasi 25-40 detik.
                - Hook harus langsung menunjukkan produk (no basa-basi).
                - Hindari keterangan adegan/B-roll.
                - CTA kuat & memancing tindakan.
                - Tidak ada emoji.
                - Fokus pada manfaat, bukan spesifikasi.
                - Format: VO 1, "Teks VO", dst.
                
                Produk: {deskripsi}
                """
                response = model.generate_content(prompt)
                st.session_state.last_vo = response.text
                st.subheader("Hasil VO:")
                st.write(response.text)
            
            else:
                prompt = f"""
                Buatkan Caption dan Hashtag berdasarkan VO ini:
                {st.session_state.last_vo}
                
                Format WAJIB:
                🎥 VO X
                TikTok: [1 kalimat natural, keyword produk] + #hashtags
                Shopee: [2-4 kata] + #hashtags (SEO Shopee)
                
                Tanpa penjelasan tambahan, langsung hasil.
                """
                response = model.generate_content(prompt)
                st.subheader("Hasil Caption:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")
