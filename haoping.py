import streamlit as st
from openai import OpenAI
import pyperclip

st.title("🌟 好评生成器")

# 设置API密钥
openai_api_key = "api-key"

# 可选项使用按钮组
st.write("评论风格")
review_styles = ["幽默", "激情", "感激", "冲动"]
selected_style = st.radio("选择评论风格", review_styles, key="review_style", horizontal=True)

st.write("使用人群")
user_groups = ["学生", "工作党", "失业人群", "转行人群"]
selected_group = st.radio("选择使用人群", user_groups, key="user_group", horizontal=True)

st.write("满意的功能点")
features = ["上手简单", "语音识别准确", "生成的答案专业", "不容易被面试官发现"]
selected_features = st.multiselect("选择满意的功能点", features, key="features")

st.write("服务体验")
service_levels = ["靠谱，啥都能解决", "随叫随到，解决问题快", "能扛事", "态度好，还能给我一些建议"]
selected_service = st.radio("客服服务态度", service_levels, key="service_level", horizontal=True)

# 初始化会话状态
if 'generated_review' not in st.session_state:
    st.session_state.generated_review = ""
if 'review_history' not in st.session_state:
    st.session_state.review_history = []

# 生成按钮
if st.button("生成好评"):
    prompt = f"""
    请为"AI面试助手"生成一个真实、详细的好评。产品简介：在面试的时候使用AI面试助手生成答案，对着答案读就完事了。

    请考虑以下因素：
    1. 评论风格：{selected_style}
    2. 使用人群：{selected_group}
    3. 最满意的功能点：{', '.join(selected_features)}
    4. 服务体验：{selected_service}

    评价应该包括以下几个方面：
    1. 产品的具体优点，特别是{', '.join(selected_features)}这些功能
    2. 作为{selected_group}的使用体验
    3. 对产品价值的看法
    4. 对客户服务的评价（{selected_service}）
    5. 是否会推荐给其他{selected_group}

    注意：
    1.生成的好评应该只有50-70字左右
    2.好评中应该不要有"AI面试助手"字眼
    3.好评尽量像是真人写的

    请以{selected_style}的风格撰写评价，确保评价听起来自然、真实，不要过于夸张或明显是机器生成的。
    """
    
    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        review = response.choices[0].message.content
        st.success("好评生成成功！")
        
        # 更新会话状态
        st.session_state.generated_review = review
        st.session_state.review_history.append(review)
        
        # 显示生成的好评
        st.text_area("生成的好评", value=review, height=150, key="generated_review_display")
    except Exception as e:
        st.error(f"生成失败：{str(e)}")

# 显示生成历史
if st.session_state.review_history:
    st.write("生成历史：")
    for i, review in enumerate(st.session_state.review_history[::-1], 1):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.text_area(f"评论 {i}", value=review, height=100, key=f"history_review_{i}")
        with col2:
            if st.button(f"📋", key=f"copy_button_{i}"):
                try:
                    pyperclip.copy(review)
                    st.toast(f"评论 {i} 复制成功")
                except Exception as e:
                    st.error(f"复制失败：{str(e)}")



