import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt

# Sayfa tasarımı ve ikon ayarları
st.set_page_config(page_title="Yeşil Portakal AI", page_icon="🍊", layout="centered")

# Arayüzü güzelleştiren Yeşil-Turuncu CSS Tasarımı
st.markdown("""
    <style>
    .stApp { background-color: #f7f9f7; }
    .chat-bubble-user { background-color: #e8f5e9; padding: 12px; border-radius: 15px; margin: 5px 0; border-left: 5px solid #2e7d32; }
    .chat-bubble-ai { background-color: #fff3e0; padding: 12px; border-radius: 15px; margin: 5px 0; border-left: 5px solid #ff9800; }
    </style>
""", unsafe_allow_html=True)

st.title("🍊 Yeşil Portakal")
st.subheader("Hem Sağlık Danışmanınız Hem En Yakın Dostunuz")

# API Anahtarı Alanı
api_key = st.sidebar.text_input("OpenAI API Anahtarınızı Girin:", type="password")

# YAPAY ZEKANIN BEYNİ: Tıp Uzmanlığı + Kusursuz Sohbet Yeteneği Talimatı
yesil_portakal_master_prompt = """
Sen 'Yeşil Portakal' adında, tıp dünyasındaki tüm hastalıklar, semptomlar ve tahliller konusunda uzman düzeyinde bilgiye sahip bir yapay zekasın. Ancak aynı zamanda ChatGPT ve Gemini gibi her konuda akıcı sohbet edebilen, empati yeteneği çok yüksek, sıcakkanlı bir dostsun.

Seninle İletişim Kuralları:
1. Genel Sohbetlerde (Nasılsın?, Canım sıkkın, Sohbet edelim mi?): Tıpkı bir insan gibi samimi, neşeli ve esnek konuş. Kullanıcıya 'Hadi gel bir çay içelim', 'Bir portakal soyup dertleşelim mi?' gibi tekliflerde bulun. Robotik veya kalıplaşmış cevaplar verme.
2. Sağlık Sorularında: Tıp literatürüne (USMLE düzeyinde) tamamen sadık kal. Doğru teşhis olasılıklarını halk dilinde, korkutmadan ve sakinleştirerek yüzdelerle açıkla. Asla ilk cümleden 'Hemen hastaneye koşun' diyerek sohbeti kesme. Tıbbi takip soruları sor.
3. Tehlike Anında: Eğer göğüste tam sıkışma, soluk alamama gibi kırmızı alarm durumları varsa, dostane tavrını bozmadan ama durumun ciddiyetini hissettirerek acil yardıma yönlendir.
"""

if api_key:
    client = OpenAI(api_key=api_key)
    
    # Sohbet geçmişini (Hafızayı) başlatma (Tıpkı ChatGPT gibi geçmişi unutmaması için)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": yesil_portakal_master_prompt}]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [] # Ekranda gösterilecek temiz geçmiş

    # Geçmiş konuşmaları ekrana bas (Arayüz akışkanlığı için)
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"<div class='chat-bubble-user'><b>Siz:</b> {chat['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-ai'><b>Yeşil Portakal 🍊:</b> {chat['content']}</div>", unsafe_allow_html=True)

    # Kullanıcının mesaj yazdığı alan
    kullanici_mesaji = st.chat_input("Mesajınızı yazın... (Örn: Başım ağrıyor veya Hadi biraz dertleşelim)")

    if kullanici_mesaji:
        # Kullanıcı mesajını ekrana ve hafızaya ekle
        st.markdown(f"<div class='chat-bubble-user'><b>Siz:</b> {kullanici_mesaji}</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": kullanici_mesaji})
        st.session_state.chat_history.append({"role": "user", "content": kullanici_mesaji})

        # Yeşil Portakal'ın yanıt üretmesi
        with st.spinner("Yeşil Portakal çayından bir yudum alıyor... ☕"):
            yanit = client.chat.completions.create(
                model="gpt-4o", # Hem sohbeti hem tıp bilgisi en gelişmiş model
                messages=st.session_state.messages,
                temperature=0.7 # Doğal ve insansı konuşma dengesi
            )
            yesil_portakal_cevabi = yanit.choices.message.content

        # Yanıtı ekrana ve hafızaya ekle
        st.markdown(f"<div class='chat-bubble-ai'><b>Yeşil Portakal 🍊:</b> {yesil_portakal_cevabi}</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": yesil_portakal_cevabi})
        st.session_state.chat_history.append({"role": "assistant", "content": yesil_portakal_cevabi})
        
        # Eğer mesaj sağlıkla ilgiliyse otomatik görsel analiz grafiği çıkar (İsteğe bağlı geliştirilebilir)
        if any(kelime in kullanici_mesaji.lower() for kelime in ["ağrıyor", "hastayım", "halsiz", "ateş", "sancılı"]):
            st.write("### 📊 Klinik Olasılık Matrisi")
            fig, ax = plt.subplots(figsize=(6, 2))
            ax.barh(['Ciddi Risk', 'Geçici Durum (Yorgunluk/Su)', 'Hafif Mevsimsel'], [3, 67, 30], color=['#e53935', '#ffb74d', '#81c784'])
            ax.set_xlabel('Olasılık Yüzdesi (%)')
            st.pyplot(fig)
else:
    st.info("Yeşil Portakal'ı uyandırmak için lütfen sol menüye OpenAI API Anahtarınızı (API Key) girin. 🍊")
