import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="KutiAİ VIP", page_icon="🤖", layout="centered")

st.title("🤖 KutiAİ VIP Asistan")
st.caption("Gemini 1.5 Flash - En Güncel Sürüm")
st.divider()

# --- 2. API BAĞLANTISI ---
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # HATA ÇÖZÜMÜ: Başına 'models/' ekleyerek en garanti yolu seçiyoruz
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
    except:
        # Eğer yukarıdaki olmazsa alternatif isimle deniyoruz
        model = genai.GenerativeModel("gemini-1.5-flash")
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
            # Yanıt üretirken versiyon hatası almamak için v1beta yerine standart yöntemi kullanıyoruz
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Detaylı hata mesajı gösterelim ki sorun olursa hemen çözelim
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