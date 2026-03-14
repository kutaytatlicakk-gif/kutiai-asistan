import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- AYARLAR (YENİ ANAHTAR ENTEGRE EDİLDİ) ---
API_KEY = "AIzaSyCXNrFbjQA9P1I4_RvUt8g1f0egfSuzQY4"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="kutiAİ v11.0", page_icon="🤖", layout="wide")

# --- ASİSTAN KİMLİĞİ ---
@st.cache_resource
def model_hazirla():
    try:
        izinli_modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        secilen = next((m for m in izinli_modeller if "1.5-flash" in m), izinli_modeller[0])
        
        instruction = (
            "Senin adın kutiAİ. Karşındaki kişiye 'Siz' diye hitap et. "
            "Asla özel isim kullanma. Nazik, profesyonel ve yardımcı bir asistan ol. "
            "Aşırı kölece tavırlardan kaçın ama saygıda kusur etme."
        )
        return genai.GenerativeModel(model_name=secilen, system_instruction=instruction)
    except:
        return None

kuti_engine = model_hazirla()

# --- SAYFA YÖNETİMİ ---
if "page" not in st.session_state:
    st.session_state.page = "chat"

# --- OYUN EKRANI ---
if st.session_state.page == "game":
    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button("❌ Çıkış", help="Sohbete dönmek için tıkla"):
            st.session_state.page = "chat"
            st.rerun()
    
    st.subheader("🕹️ Flappy Bird - Tam Ekran Modu (Zıplamak için SPACE basın)")
    
    flappy_code = """
    <div style="display: flex; justify-content: center; align-items: center; background: #222; height: 80vh;">
        <canvas id="fb" width="400" height="600" style="border:5px solid #fff; border-radius: 10px;"></canvas>
    </div>
    <script>
    var canvas = document.getElementById("fb");
    var ctx = canvas.getContext("2d");
    var bX = 50; var bY = 200; var gravity = 0.25; var velocity = 0; var score = 0;
    var pipes = []; pipes[0] = { x: canvas.width, y: 0 };
    
    window.addEventListener("keydown", function(e) {
        if(e.code == "Space") { velocity = -5; e.preventDefault(); }
    });

    function draw() {
        ctx.fillStyle = "#70c5ce"; ctx.fillRect(0,0,canvas.width,canvas.height);
        for(var i=0; i<pipes.length; i++) {
            ctx.fillStyle = "#2e7d32";
            ctx.fillRect(pipes[i].x, 0, 50, pipes[i].y);
            ctx.fillRect(pipes[i].x, pipes[i].y + 150, 50, canvas.height);
            pipes[i].x -= 2;
            if(pipes[i].x == 150) pipes.push({ x: canvas.width, y: Math.floor(Math.random()*300)+50 });
            if(bX+30 > pipes[i].x && bX < pipes[i].x+50 && (bY < pipes[i].y || bY+30 > pipes[i].y+150)) location.reload();
            if(pipes[i].x == 0) score++;
        }
        velocity += gravity; bY += velocity;
        ctx.fillStyle = "yellow"; ctx.fillRect(bX, bY, 30, 30);
        if(bY+30 > canvas.height || bY < 0) location.reload();
        ctx.fillStyle = "#fff"; ctx.font = "30px Arial"; ctx.fillText("Skor: "+score, 20, 50);
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(flappy_code, height=700)

# --- SOHBET EKRANI ---
else:
    st.title("🤖 kutiAİ v11.0")
    
    if "chat" not in st.session_state:
        st.session_state.chat = kuti_engine.start_chat(history=[])

    for msg in st.session_state.chat.history:
        role = "user" if msg.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg.parts[0].text)

    if prompt := st.chat_input("Mesajınızı yazın..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            with st.chat_message("assistant"):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
        except:
            st.error("Bir bağlantı hatası oluştu. Lütfen API anahtarınızı kontrol edin.")

    with st.sidebar:
        st.header("🎮 Eğlence")
        if st.button("🕹️ Flappy Bird Başlat"):
            st.session_state.page = "game"
            st.rerun()
        st.write("---")
        if st.button("🗑️ Hafızayı Temizle"):
            st.session_state.chat = kuti_engine.start_chat(history=[])
            st.rerun()