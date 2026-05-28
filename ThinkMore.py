import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="فكر أكثر | thinkMore", layout="centered")

# دمج الأسرار (المفتاح)
try:
    API_KEY = st.secrets["GEMINI_KEY = "AIzaSyRB708...""]
except:
    st.error("خطأ: لم يتم العثور على المفتاح السري GEMINI_KEY في إعدادات التطبيق.")
    st.stop()

def generate_idea(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "أنت خبير في نهج البلاغة. أخرج حكمة واحدة عشوائية بصيغة JSON فقط: {'category': '...', 'title': '...', 'content': '...', 'deep_dive_markdown': '...'}"
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        st.error(f"خطأ في الاتصال بالذكاء الاصطناعي: {e}")
        return None

# الواجهة
st.markdown("<h1 style='text-align: center;'>🧠 فكر أكثر | thinkMore</h1>", unsafe_allow_html=True)

# زر التوليد
if st.button("اضغط هنا لتوليد حكمة جديدة"):
    with st.spinner("جاري جلب الفكرة..."):
        data = generate_idea(API_KEY)
        if data:
            st.session_state.data = data
            st.rerun()
        else:
            st.warning("لم يتم جلب أي بيانات، حاول مرة أخرى.")

# عرض البيانات إذا كانت موجودة
if 'data' in st.session_state:
    d = st.session_state.data
    st.subheader(d.get('title', ''))
    st.info(d.get('content', ''))
    with st.expander("قراءة التحليل المعمق"):
        st.markdown(d.get('deep_dive_markdown', ''))
