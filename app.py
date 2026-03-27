import streamlit as st
import google.generativeai as genai
import os

# ١. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="کورد جیمینی", page_icon="🤖", layout="centered")

# پشکا خویندنا پەرتووکێ (Knowledge Base)
def get_sarsing_data():
    if os.path.exists("knowledge.txt"):
        with open("knowledge.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "چو زانیاری نەهاتینە دیتن."

sarsing_context = get_sarsing_data()

# ٢. دیزاینا CSS (ڕێک وەکی یا تە دڤێت)
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .chat-bubble { padding: 15px; border-radius: 20px; margin: 10px 0; max-width: 85%; direction: rtl; }
    .user { background: #1e293b; border-right: 5px solid #3b82f6; float: right; clear: both; text-align: right; }
    .bot { background: #334155; border-right: 5px solid #10b981; float: right; clear: both; text-align: right; }
    h1 { text-align: center; color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# ٣. لوگۆ
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try: st.image("ip.jpeg", width=150)
    except: st.write("Logo Not Found")

st.markdown("<h1>🤖 کورد جیمینی - بادینی</h1>", unsafe_allow_html=True)

# ٤. کلیلێ API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("کلیلێ API نەهاتیە دیتن!")

# ٥. پێناسا مۆدێلێ Gemini (ب وەشانا ٢.٥ و مێشکێ سەرسنکێ)
system_instruction = f"""
تۆ 'کورد جیمینی' یی، شارەزایەکێ فەرمی یی ل سەر سەرسنگێ.
تۆ تەنێ ب زارۆکێ بادینی بەرسڤێ ددەی.
تۆ ل سەر بنەمایێ ڤان زانیاریێن پەرتووکێ بەرسڤێ ددەی:
---
{sarsing_context}
---
ڕێسا: ب چو ڕەنگان نەکەی بێژی 'بادەرەشکێ' تاخ نینە، چونکی ئەو تاخەکێ مێژوویی یە ل سەرسنگێ.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # وەشانا نوی یا تە د dashboard دا دیتی
    system_instruction=system_instruction,
    generation_config={"temperature": 0.3} # دا کو تەنێ ڕاستیان بێژیت و خەیالان نە کەت
)

# ٦. چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("تشتەکی ب بادینی پرسیار بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("دێ نوکە بەرسڤێ دەم..."):
        try:
            response = model.generate_content(st.session_state.messages[-1]["content"])
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"ئاریشەیەک چێبوو: {str(e)}")
