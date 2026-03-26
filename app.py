import streamlit as st
import google.generativeai as genai

# ١. ڕێکخستنا سەرەتایی یا لاپەڕەی (Page Config)
st.set_page_config(page_title="کورد جیمینی", page_icon="🤖", layout="centered")

# ٢. دیزاینا CSS ب ستایلێ تاری و ڕەنگێن براندێ تە (ipbits)
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }
    /* ستایلێ چاتێ و نڤیسینا بادینی */
    .chat-bubble {
        padding: 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 85%;
        line-height: 1.6;
        font-family: 'Tahoma', sans-serif;
        direction: rtl; /* بۆ نڤیسینا ژ ڕاست بۆ چەپ */
    }
    .user {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-right: 5px solid #3b82f6;
        float: right;
        clear: both;
        text-align: right;
    }
    .bot {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-right: 5px solid #10b981;
        float: right;
        clear: both;
        text-align: right;
    }
    h1 {
        text-align: center;
        color: #3b82f6;
        font-size: 2.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ٣. نیشادانا لوگۆیێ تە (پێدڤیە فایلێ logo.png دگەل کۆدی بیت)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try:
        st.image("ip.jpeg", width=150)
    except:
        st.write("⚠️ فایلێ لوگۆیی (ip.jpeg) نەهاتیە دیتن")

st.markdown("<h1>🤖 کورد جیمینی - بادینی</h1>", unsafe_allow_html=True)

# ٤. ڕێکخستنا مێشکێ AI (ئەڤە گرنگترین پشکە بۆ زمانێ بادینی)
# تێبینی: کلیلێ (API Key) د ناڤ Secrets یێن هۆستێ خۆ دا دانیە
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ڕێنمایێن توند بۆ مۆدێلی دا کو تەنێ ب بادینی باخڤیت
system_instruction = """
تۆ 'کورد جیمینی' یی، یاریدەدەرەکی ژیریا دەستکردی یێ زۆر شارەزا و ڕێزدار.
تۆ تەنێ ب زارۆکێ (بادینی) دئاخڤی و بەرسڤێ ددەی.
ڕێساێن توند:
١. ب چو ڕەنگان زمانێ سۆرانی بکار نەئینە. (نەکەی بێژی: دەبێت، دەکات، دەکەم، دەچم).
٢. ل شوینا وان پەیڤێن بادینی یێن درست بکار بینە: (دێ بیت، دکەت، دکەم، دچم).
٣. ئەگەر بکارهێنەری ب ئینگلیزی یان عەرەبی پرسیار کر، تۆ ب بادینی بەرسڤێ بدە.
٤. تۆ خەلکێ دەڤەرا بەهدینانی (سەرسنک، دهۆک، ئامێدی) و کلتۆرێ وان زۆر باش دناسی.
٥. پەیڤێن وەکی (سەرچاڤا، برا، گەلی دەلال، ب خێر بێی) بکار بینە دا کو ئاخڤفتنا تە یا سروشتی بیت.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ٥. پاراستنا پەیامێن چاتی د ناڤ سێشنێ دا
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشادانا پەیامێن کەڤن
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# ٦. وەرگرتنا پرسیارێ ژ بکارهێنەری
if prompt := st.chat_input("تشتەکی ب بادینی پرسیار بکە..."):
    # زێدەکرنا پەیاما تە
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # وەرگرتنا بەرسڤێ ژ مۆدێلێ Gemini
    response = model.generate_content(prompt)
    
    # زێدەکرنا بەرسڤا بوتێ AI
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # نووکرنا لاپەڕەی
    st.rerun()