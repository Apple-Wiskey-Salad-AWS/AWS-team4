import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sagemaker.s3 import S3Downloader
from sagemaker.tensorflow import TensorFlowPredictor
from PIL import Image

# 로컬에서 GPU 사용 비활성화
tf.config.set_visible_devices([], 'GPU')

# EndpointUtil 클래스 정의: AWS SageMaker 엔드포인트와 통신하여 x-ray 이미지 판별을 수행합니다.
class EndpointUtil:
    # 클래스 생성자: 초기 설정을 수행합니다.
    def __init__(self, bucket_name, endpoint_name, local_folder_path):
        self.bucket_name = bucket_name  # S3 버킷 이름
        self.local_folder_path = local_folder_path.lstrip('/')  # 로컬 저장 경로, 시작하는 '/' 제거
        self.predictor = TensorFlowPredictor(endpoint_name)  # SageMaker TensorFlow 예측 엔드포인트
        self._ensure_local_folder()  # 필요한 로컬 폴더를 생성
        self._download_test_set()  # 테스트 세트를 다운로드
        self.image_paths = self._load_testing_data()  # 테스트 데이터를 로드

    # 로컬 폴더가 없으면 생성하는 메소드
    def _ensure_local_folder(self):
        if not os.path.exists(self.local_folder_path):
            os.makedirs(self.local_folder_path, exist_ok=True)

    # S3에서 테스트 세트를 다운로드하는 메소드
    def _download_test_set(self):
        s3_path = f's3://{self.bucket_name}/{self.local_folder_path}'
        files = S3Downloader.list(s3_path)
        for file_path in files:
            local_path = os.path.join(self.local_folder_path, os.path.basename(file_path))
            if not os.path.exists(local_path):
                S3Downloader.download(file_path, self.local_folder_path)

    # 로컬에 저장된 테스트 데이터(이미지 경로)를 로드하는 메소드
    def _load_testing_data(self):
        folder_path = os.path.join(self.local_folder_path, 'images')
        return [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith('.png')]

    # 특정 이미지에 대한 판별을 실행하는 메소드
    def call(self, image_path):
        # 이미지를 로드하고 전처리합니다.
        image = Image.open(image_path).convert('RGB')
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0  # 이미지 정규화
        image_array = np.expand_dims(image_array, axis=0)  # 배치 차원 추가

        # 입력 데이터를 SageMaker 엔드포인트에 전달할 입력 형식으로 준비합니다.
        input_vals = {
            "instances": image_array.tolist()
        }

        # SageMaker 엔드포인트에 예측을 요청합니다.
        predictions = self.predictor.predict(input_vals)['predictions']
        # 예측 결과를 데이터프레임으로 구성합니다.
        results = pd.DataFrame(predictions, columns=['category', 'confidence'])

        # 결과를 반환합니다.
        return results

