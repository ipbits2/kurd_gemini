import streamlit as st
import google.generativeai as genai

# ١. ڕێکخستنا سەرەتایی یا لاپەڕەی
st.set_page_config(page_title="کورد جیمینی", page_icon="🤖", layout="centered")

# ٢. دیزاینا CSS ب ستایلێ تاری و ڕەنگێن براندێ تە (ipbits)
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }
    .chat-bubble {
        padding: 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 85%;
        line-height: 1.6;
        font-family: 'Tahoma', sans-serif;
        direction: rtl;
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

# ٣. نیشادانا لوگۆیێ تە (ip.jpeg)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try:
        st.image("ip.jpeg", width=100)
    except:
        st.warning("⚠️ فایلێ لوگۆیی (ip.jpeg) ناهێتە دیتن ل سەر گیتھابێ")

st.markdown("<h1>🤖 کورد جیمینی - بادینی</h1>", unsafe_allow_html=True)

# ٤. ڕێکخستنا مێشکێ AI و کلیلێ (API Key)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("❌ کلیلێ (API Key) نەهاتیە دیتن د ناڤ Secrets دا!")

# ڕێنمایێن توند ب بادینی دا کو AI شاشیان نەکەت
system_instruction = """
تۆ 'کورد جیمینی' یی، یاریدەدەرەکی زیرەکی دەستکردی زۆر شارەزا.
تۆ تەنێ ب زارۆکێ (بادینی) دئاخڤی و بەرسڤێ ددەی.
ڕێساێن توند:
١. ب چو ڕەنگان زمانێ سۆرانی بکار نەئینە (نەکەی بێژی: دەبێت، دەکات، دەکەم).
٢. ل شوینا وان پەیڤێن بادینی بکار بینە: (دێ بیت، دکەت، دکەم).
٣. تۆ خەلکێ دەڤەرا بەهدینانی (سەرسنک، دهۆک، ئامێدی) و کلتۆرێ وان زۆر باش دناسی.
٤. ب ڕێز و حورمەت بەرسڤێ بدە.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ٥. هەلگرتنا نامەیێن چاتی
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشادانا نامەیێن کەڤن
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# ٦. وەرگرتنا پرسیارێ و بەرسڤدان ب شێوەیەکێ پاراستی (Try/Except)
if prompt := st.chat_input("تشتەکی ب بادینی پرسیار بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # نیشادانا نامەیا بکارهێنەری هەر نوکە
    st.rerun()

# ل ڤێرە بەرسڤا AI دهێتە وەرگرتن
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    
    with st.spinner("دێ نوکە بەرسڤێ دەم..."):
        try:
            response = model.generate_content(last_prompt)
            if response and response.text:
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            else:
                st.warning("ببوورە، من نەشیا بەرسڤەکێ بۆ ڤێ پرسیارێ چێکەم.")
        except Exception as e:
            st.error(f"ئاریشەیەک چێبوو: {str(e)}")
