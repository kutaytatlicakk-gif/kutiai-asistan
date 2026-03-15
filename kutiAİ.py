import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="KutiAİ VIP", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 KutiAİ VIP Asistan")
st.caption("Gemini Pro ile Güçlendirilmiş Akıllı Asistan")
st.divider()

# --- 2. GÜVENLİ API BAĞLANTISI ---
# Anahtarı Streamlit Secrets'tan (o gizli kasadan) alır
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
else:
    st.error("⚠️ API Anahtarı bulunamadı! Lütfen Streamlit Settings -> Secrets kısmına GOOGLE_API_KEY ekleyin.")
    st.stop()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana çiz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SOHBET MANTIĞI ---
if prompt := st.chat_input("KutiAİ'ye bir şeyler sorun..."):
    # Kullanıcı mesajını göster ve kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zekanın yanıtını oluştur
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            try:
                # Modeli çalıştır
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
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("🚀 **KutiAİ v1.0**")
    st.write("Geliştirici: Kutay")
