import streamlit as st

from streamlit_option_menu import option_menu
import os


# 페이지 설정
st.set_page_config(page_title="Top Navigation Menu", layout="wide")

# 상단 네비게이션 바
selected = option_menu(
    menu_title=None, 
    options=["Home", "Services", "Products", "About"],
    icons=["house", "tools", "bag", "info"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

# 선택된 메뉴에 따라 콘텐츠를 표시합니다.
if selected == "Home":
    # company.html 파일의 내용을 읽어와서 표시
    with open('home.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    

    components.html(html_content, height=600)

elif selected == "Services":
    # 기본값 설정
    if 'service_page' not in st.session_state:
        st.session_state['service_page'] = None

    # 사이드바에 버튼 추가
    if st.sidebar.button('Statistics'):
        st.session_state['service_page'] = 'Statistics'
    if st.sidebar.button('Target Materials'):
        st.session_state['service_page'] = 'Target Materials'
    if st.sidebar.button('Recent Detection'):
        st.session_state['service_page'] = 'Recent Detection'

    # 선택된 서비스 페이지에 따라 콘텐츠 표시
    if st.session_state['service_page'] == 'Statistics':
        st.write("## Statistics Page")
        st.write("지금까지 얼마나 잘 detect 했는지, 품목별로 detect율 같은거 뽑아내서 그래프로 그려넣으면 좋을 것 같아요. 설명페이지마냥")
    elif st.session_state['service_page'] == 'Target Materials':
        st.write("## Target Materials Page")
        materials = st.sidebar.multiselect(
            "detect 할 항목들을 선택해주세요 (ps. 전체를 한번에 자동으로 선택할 수 있도록 하는 기능 넣으면 좋을 듯)",
            ["SSD", "knife", "USB", "기타등등"]
        )
        st.session_state['selected_materials'] = materials  # 선택한 항목들을 세션 상태에 저장
        st.write("선택한 규제항목이 맞는지 다시 한번 확인하고 모델 사용하기를 눌러주세요: ", materials)
    elif st.session_state['service_page'] == 'Recent Detection':
        st.write("## 모델 사용하는 거 보여주기")
        if 'selected_materials' in st.session_state:
            selected_materials = st.session_state['selected_materials']
            st.write("Selected materials for detection: ", selected_materials)
        else:
            st.write("No materials selected.")
    else:
        # 기본 Service 페이지 콘텐츠
        st.write("# Services")
        st.write("Add your services introduction content here.")

elif selected == "Products":
    st.write("# Products")
    st.write("Add your products introduction content here.")

elif selected == "About":
    st.write("# About")
    # company.html 파일의 내용을 읽어와서 표시
    with open('company.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=600)
