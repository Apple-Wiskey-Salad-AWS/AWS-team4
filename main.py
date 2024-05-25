import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import boto3
import json
import settings  # settings.py 파일을 import하여 동영상 경로를 가져옴
import time

# S3 클라이언트 생성
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')
bucket_name = 'newdataa'

# 페이지 설정
st.set_page_config(page_title="Top Navigation Menu", layout="wide")

# 상단 네비게이션 바
selected = option_menu(
    menu_title=None, 
    options=["Home", "Services", "Products", "About"],
    icons=["house", "tools", "info", "people"],
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
    # home.html 파일의 내용을 읽어와서 표시
    with open('home.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=600)

elif selected == "Services":
    # 사이드바에 Radio 버튼 추가
    st.sidebar.title("Images/ Video Config")
    media_choice = st.sidebar.radio("Select Media Type", ("Image", "Video"))

    uploaded_image = None
    uploaded_video = None

    if media_choice == "Image":
        st.sidebar.header("Choose a sample Image")
        sample_image = st.sidebar.selectbox("Choose a sample image...", ["None"] + list(settings.IMAGES_DICT.keys()))
        uploaded_image = st.sidebar.file_uploader("Or upload an image...", type=["jpg", "jpeg", "png"])
    elif media_choice == "Video":
        st.sidebar.header("Choose a sample Video")
        sample_video = st.sidebar.selectbox("Choose a sample video...", ["None"] + list(settings.VIDEOS_DICT.keys()))
        uploaded_video = st.sidebar.file_uploader("Or upload a video...", type=["mp4", "avi", "mov"])

    # 탐지할 항목 선택 멀티셀렉트 추가
    st.sidebar.header("Select Items for Detection")
    materials = st.sidebar.multiselect(
        "Detect 할 항목들을 선택해주세요",
        ["SSD", "knife", "USB", "기타등등"]
    )
    st.session_state['selected_materials'] = materials  # 선택한 항목들을 세션 상태에 저장
    st.write("선택한 규제항목이 맞는지 다시 한번 확인하고 모델 사용하기를 눌러주세요: ", materials)
    
    # 동영상 및 이미지 파일 업로드 to S3
    if uploaded_image is not None:
        st.sidebar.write("### 동영상 및 이미지 업로드 및 처리")
        input_key = f"lambda-input/{uploaded_image.name}"
        s3.upload_fileobj(uploaded_image, bucket_name, input_key)
        st.sidebar.write("File uploaded successfully to S3")
    
    if uploaded_video is not None:
        st.sidebar.write("### 동영상 및 이미지 업로드 및 처리")
        input_key = f"lambda-input/{uploaded_video.name}"
        s3.upload_fileobj(uploaded_video, bucket_name, input_key)
        st.sidebar.write("File uploaded successfully to S3")

    # 검출 시작 버튼
    if st.sidebar.button("검출 시작"):
        result_container = st.sidebar.empty()
        result_container.write("Pending...")

        if media_choice == "Video":
            if sample_video != "None":
                # S3에서 선택한 동영상 처리
                input_key = settings.VIDEOS_DICT[sample_video].replace(f"s3://{bucket_name}/", "")
                result_key = f"lambda-output/{input_key}.json"
                with st.spinner('Pending...'):
                    while True:
                        try:
                            result_obj = s3.get_object(Bucket=bucket_name, Key=result_key)
                            result = json.loads(result_obj['Body'].read().decode())
                            result_container.write("Inference Result:", result)
                            break
                        except Exception as e:
                            time.sleep(5)
            elif uploaded_video is not None:
                # 사용자가 업로드한 동영상 처리
                input_key = f"lambda-input/{uploaded_video.name}"
                result_key = f"lambda-output/{uploaded_video.name}.json"
                with st.spinner('Pending...'):
                    while True:
                        try:
                            result_obj = s3.get_object(Bucket=bucket_name, Key=result_key)
                            result = json.loads(result_obj['Body'].read().decode())
                            result_container.write("Inference Result:", result)
                            break
                        except Exception as e:
                            time.sleep(5)
            else:
                st.sidebar.write("No video selected or uploaded.")
        elif media_choice == "Image":
            if sample_image != "None":
                # S3에서 선택한 이미지 처리
                input_key = settings.IMAGES_DICT[sample_image].replace(f"s3://{bucket_name}/", "")
                result_key = f"lambda-output/{input_key}.json"
                with st.spinner('Pending...'):
                    while True:
                        try:
                            result_obj = s3.get_object(Bucket=bucket_name, Key=result_key)
                            result = json.loads(result_obj['Body'].read().decode())
                            result_container.write("Inference Result:", result)
                            break
                        except Exception as e:
                            time.sleep(5)
            elif uploaded_image is not None:
                # 사용자가 업로드한 이미지 처리
                input_key = f"lambda-input/{uploaded_image.name}"
                result_key = f"lambda-output/{uploaded_image.name}.json"
                with st.spinner('Pending...'):
                    while True:
                        try:
                            result_obj = s3.get_object(Bucket=bucket_name, Key=result_key)
                            result = json.loads(result_obj['Body'].read().decode())
                            result_container.write("Inference Result:", result)
                            break
                        except Exception as e:
                            time.sleep(5)
            else:
                st.sidebar.write("No image selected or uploaded.")

        # Lambda function invocation
        lambda_payload = {
            'Records': [{
                's3': {
                    'bucket': {
                        'name': bucket_name
                    },
                    'object': {
                        'key': input_key
                    }
                }
            }]
        }
        lambda_response = lambda_client.invoke(
            FunctionName='smwu-aiml-team4',
            InvocationType='RequestResponse',
            Payload=json.dumps(lambda_payload)
        )
        
        # 응답 로깅 추가
        st.sidebar.write(f"Lambda Response: {lambda_response}")

        lambda_result = json.loads(lambda_response['Payload'].read().decode())
        result_body = json.loads(lambda_result['body'])
        
        # result_body 로깅 추가
        st.sidebar.write(f"Result Body: {result_body}")
        
        inference_id = result_body.get('inference_id')
        st.sidebar.write(f"Inference ID: {inference_id}")

elif selected == "Products":
    st.write("# Products")
    with open('product.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=5000)

elif selected == "About":
    st.write("# About")
    # company.html 파일의 내용을 읽어와서 표시
    with open('company.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=1500)
