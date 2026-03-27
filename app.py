import streamlit as st
import google.generativeai as genai

# ١. ڕێکخستنا لاپەڕەی (Page Config)
st.set_page_config(page_title="کورد جیمینی", page_icon="🤖", layout="centered")

# ٢. دیزاینا CSS بۆ ڕەنگێن تاری و براندێ ipbits
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
        st.image("ip.jpeg", width=150)
    except:
        st.warning("⚠️ فایلێ لوگۆیی (ip.jpeg) ناهێتە دیتن ل سەر گیتھابێ")

st.markdown("<h1>🤖 کورد جیمینی - بادینی</h1>", unsafe_allow_html=True)

# ٤. ڕێکخستنا کلیلێ API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ کلیلێ (API Key) د ناڤ Secrets دا ناهێتە دیتن!")

# ڕێکخستنێن پاراستنێ (Safety Settings) بۆ چارەسەرکرنا ئاریشا Invalid Argument
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# پێناسەکرنا مۆدێلێ Gemini 1.5 ب زمانێ بادینی
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    system_instruction="تۆ 'کورد جیمینی' یی، یاریدەدەرەکی زیرەکی دەستکردی زۆر شارەزا و ڕێزدار. تۆ تەنێ و تەنێ ب زارۆکێ بادینی (دهۆک، سەرسنک، ئامێدی) بەرسڤێ ددەی. ب هیچ ڕەنگەکێ پەیڤێن سۆرانی بکار نەئینە."
)

# ٥. هەلگرتنا نامەیێن چاتی (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشادانا نامەیێن کەڤن
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# ٦. وەرگرتنا پرسیارێ و بەرسڤدان
if prompt := st.chat_input("تشتەکی ب بادینی پرسیار بکە..."):
    # زێدەکرنا پەیاما تە بۆ لیستی
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# ئەگەر پەیاما دووماهیێ یا بکارهێنەری بیت، بەرسڤێ وەرگرە
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    
    with st.spinner("دێ نوکە بەرسڤێ دەم..."):
        try:
            # پەیوەندی دگەل گوگل بۆ وەرگرتنا بەرسڤێ
            response = model.generate_content(last_prompt)
            if response and response.text:
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            else:
                st.warning("ببوورە، من نەشیا بەرسڤەکێ بۆ ڤێ پرسیارێ درست کەم.")
        except Exception as e:
            st.error(f"ئاریشەیەک چێبوو: {str(e)}")
