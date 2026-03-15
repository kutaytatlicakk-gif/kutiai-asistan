import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="KutiAİ VIP", page_icon="🤖", layout="centered")

# Şık bir tasarım için CSS (Arka plan ve mesaj kutuları)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stChatMessage { border-radius: 20px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 KutiAİ VIP Asistan")
st.caption("Gemini 1.5 Flash ile Güçlendirilmiş En Hızlı Versiyon")
st.divider()

# --- 2. GÜVENLİ API BAĞLANTISI ---
# Streamlit Secrets üzerinden anahtarı çeker
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Hata veren 'gemini-pro' yerine en güncel modeli kullanıyoruz
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ API Anahtarı bulunamadı! Lütfen Secrets kısmını kontrol edin.")
    st.stop()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana yansıt
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SOHBET MANTIĞI ---
if prompt := st.chat_input("KutiAİ'ye bir şeyler sorun..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zekanın yanıt üretme süreci
    with st.chat_message("assistant"):
        with st.spinner("KutiAİ düşünüyor..."):
            try:
                # Yanıt üretme
                response = model.generate_content(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                # Yanıtı hafızaya kaydet
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")

# --- 5. YAN MENÜ ---
with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("🚀 **Sürüm: KutiAİ v1.1**")
    st.write("👨‍💻 **Geliştirici: Kutay**")
    st.info("Bu asistan Gemini 1.5 Flash teknolojisini kullanır.")