import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="KutiAİ VIP", page_icon="🤖", layout="centered")

st.title("🤖 KutiAİ VIP Asistan")
st.caption("v1.1 - En Hızlı Yapay Zeka Sürümü")
st.divider()

# --- 2. API VE MODEL BAĞLANTISI ---
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # HATA ÇÖZÜMÜ: Buradaki model ismini 'gemini-1.5-flash-latest' yapıyoruz
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
else:
    st.error("⚠️ API Anahtarı bulunamadı!")
    st.stop()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. MESAJLAŞMA ---
if prompt := st.chat_input("KutiAİ'ye bir şeyler sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Yanıt üretme
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Hata kodunu çok kısa gösterelim
            st.error("Bir bağlantı sorunu oluştu, lütfen sayfayı yenileyin.")
            print(f"Hata detayı: {e}")

# --- 5. YAN MENÜ ---
with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("🚀 **Sürüm: KutiAİ v1.1**")
    st.write("👨‍💻 **Geliştirici: Kutay**")