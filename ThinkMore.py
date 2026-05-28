import streamlit as st
import google.generativeai as genai
import json

# إعدادات الصفحة
st.set_page_config(page_title="فكر أكثر | thinkMore - ذكاء اصطناعي", page_icon="🧠", layout="centered")

# الحقن الشامل للـ RTL (من اليمين إلى اليسار) وتنسيق القوالب
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp, html, body {
        direction: RTL !important;
        text-align: right !important;
    }
    p, span, h3, h4, h5, h6, .stMarkdown {
        direction: RTL !important;
        text-align: right !important;
    }
    input, textarea, [data-baseweb="textarea"], .stTextArea textarea {
        direction: RTL !important;
        text-align: right !important;
    }
    .centered-content {
        text-align: center !important;
        direction: RTL !important;
        display: block;
        width: 100%;
    }
    ul, ol {
        direction: RTL !important;
        text-align: right !important;
        padding-right: 30px !important;
        padding-left: 0px !important;
    }
    li {
        direction: RTL !important;
        text-align: right !important;
    }
    div.stButton > button {
        width: 100%;
        direction: RTL !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 جلب المفتاح السري بأمان من إعدادات السيرفر السحابي دون كشفه في الكود
try:
    API_KEY = st.secrets["GEMINI_KEY = "AIzaSyRB708""]
except:
    API_KEY = None

# دالة توليد الأفكار والأبحاث عبر الـ API
def generate_nebula_idea(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        أنت باحث وأكاديمي خبير ومتخصص في تفكيك "نهج البلاغة" لأمير المؤمنين علي بن أبي طالب (عليه السلام)، وتربط السنن الكونية بالاستراتيجيات المعاصرة.
        اختر حكمة، أو مقولة، أو جزءاً من خطبة أو رسالة من نهج البلاغة بشكل عشوائي تماماً (تأكد من تنوع الاختيارات في كل مرة بين السياسة، والوعي، والصبر، وبناء الذات).
        
        قم بصياغة المخرجات بدقة متناهية حصراً بصيغة JSON، واستخدم المفاتيح التالية باللغة العربية:
        - "category": تصنيف محدد وموجز للفكرة.
        - "title": عنوان بليغ وجذاب يلخص جوهر الفكرة.
        - "content": النص الشريف والدقيق المقتبس من نهج البلاغة.
        - "deep_dive_markdown": ورقة بحثية وتفكيك استراتيجي معمق جداً كبحث فعلي وحقيقي للنص بصيغة الماركداون (Markdown) النقي، مقسمة بشكل صارم إلى العناوين التالية:
          ### 📋 ورقة بحثية وتفكيك استراتيجي للنص
          **1. التحليل الفلسفي والتأصيل المعرفي:**
          **2. السنن الكونية والاجتماعية والسياسية الحاكمة:**
          **3. آليات الإسقاط والتطبيق العملي المعاصر:**

        ملاحظة حاسمة: لا تضع أي نصوص خارج قالب الـ JSON، ولا تستخدم وسوم HTML، بل ماركداون نقي داخل قيمة المفتاح.
        """
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
        return None

# --- واجهة التطبيق الرئيسية ---
st.markdown("<div class='centered-content'><h1 style='color: #2C3E50; margin-bottom: 0px;'>🧠 فكر أكثر | thinkMore AI</h1></div>", unsafe_allow_html=True)
st.markdown("<div class='centered-content'><p style='color: #16A085; font-size: 18px; margin-top: 0px;'>المحرك الديناميكي المستوحى من نهج البلاغة</p></div>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

if 'ai_idea' not in st.session_state:
    st.session_state.ai_idea = None
if 'show_deep' not in st.session_state:
    st.session_state.show_deep = False

# التحقق من وجود المفتاح السري المدمج
if not API_KEY:
    st.error("🔴 لم يتم العثور على المفتاح السري المسمى GEMINI_KEY في إعدادات Streamlit Cloud Secrets.")
else:
    if st.session_state.ai_idea is None:
        with st.spinner("جاري استخراج درة فكرية من نهج البلاغة عبر الذكاء الاصطناعي..."):
            st.session_state.ai_idea = generate_nebula_idea(API_KEY)

    idea = st.session_state.ai_idea

    if idea:
        st.markdown(f"<div class='centered-content' style='margin-bottom: 15px;'><span style='background-color: #EBF5FB; color: #2980B9; padding: 6px 16px; border-radius: 20px; font-size: 15px; font-weight: bold;'>📌 المسار المعرفي: {idea.get('category')}</span></div>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"### 📜 {idea.get('title')}")
            st.markdown(f"<p style='font-size: 19px; line-height: 1.8; color: #2C3E50; font-style: italic;'>{idea.get('content')}</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 توليد حكمة وبحث جديد"):
                st.session_state.show_deep = False
                with st.spinner("جاري الغوص في نهج البلاغة وتوليد تحليل جديد..."):
                    st.session_state.ai_idea = generate_nebula_idea(API_KEY)
                st.rerun()

        with col2:
            if st.button("🔍 تعمّق استراتيجي في النص"):
                st.session_state.show_deep = True
                st.rerun()

        if st.session_state.show_deep:
            st.write("") 
            with st.container(border=True):
                st.markdown(idea.get('deep_dive_markdown'))
            
            st.divider()
            st.markdown("### 📝 كراسة التدبر والاستسقاط الفكري:")
            user_notes = st.text_area("كيف تنعكس هذه الأوراق البحثية الصادرة عن الذكاء الاصطناعي على واقعك المعاصر؟", height=120, label_visibility="collapsed")
            if user_notes:
                st.toast("تم حفظ تأملاتك بنجاح!")
