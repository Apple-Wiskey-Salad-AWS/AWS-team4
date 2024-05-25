{"filter":false,"title":"sample-endpoint_util.py","tooltip":"/sample-endpoint_util.py","ace":{"folds":[],"scrolltop":420,"scrollleft":0,"selection":{"start":{"row":37,"column":33},"end":{"row":37,"column":33},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"hash":"6803bdde43e48e56a0eb83d2ef955446639cffba","changed":true,"value":"import os\nimport numpy as np\nimport pandas as pd\nimport tensorflow as tf\nfrom sagemaker.s3 import S3Downloader\nfrom sagemaker.tensorflow import TensorFlowPredictor\nfrom PIL import Image\n\n# 로컬에서 GPU 사용 비활성화\ntf.config.set_visible_devices([], 'GPU')\n\n# EndpointUtil 클래스 정의: AWS SageMaker 엔드포인트와 통신하여 x-ray 이미지 판별을 수행합니다.\nclass EndpointUtil:\n    # 클래스 생성자: 초기 설정을 수행합니다.\n    def __init__(self, bucket_name, endpoint_name, local_folder_path):\n        self.bucket_name = bucket_name  # S3 버킷 이름\n        self.local_folder_path = local_folder_path.lstrip('/')  # 로컬 저장 경로, 시작하는 '/' 제거\n        self.predictor = TensorFlowPredictor(endpoint_name)  # SageMaker TensorFlow 예측 엔드포인트\n        self._ensure_local_folder()  # 필요한 로컬 폴더를 생성\n        self._download_test_set()  # 테스트 세트를 다운로드\n        self.image_paths = self._load_testing_data()  # 테스트 데이터를 로드\n\n    # 로컬 폴더가 없으면 생성하는 메소드\n    def _ensure_local_folder(self):\n        if not os.path.exists(self.local_folder_path):\n            os.makedirs(self.local_folder_path, exist_ok=True)\n\n    # S3에서 테스트 세트를 다운로드하는 메소드\n    def _download_test_set(self):\n        s3_path = f's3://{self.bucket_name}/{self.local_folder_path}'\n        files = S3Downloader.list(s3_path)\n        for file_path in files:\n            local_path = os.path.join(self.local_folder_path, os.path.basename(file_path))\n            if not os.path.exists(local_path):\n                S3Downloader.download(file_path, self.local_folder_path)\n\n    # 로컬에 저장된 테스트 데이터(이미지 경로)를 로드하는 메소드\n    def _load_testing_data(self):\n        folder_path = os.path.join(self.local_folder_path, 'images')\n        return [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith('.png')]\n\n    # 특정 이미지에 대한 판별을 실행하는 메소드\n    def call(self, image_path):\n        # 이미지를 로드하고 전처리합니다.\n        image = Image.open(image_path).convert('RGB')\n        image = image.resize((224, 224))\n        image_array = np.array(image) / 255.0  # 이미지 정규화\n        image_array = np.expand_dims(image_array, axis=0)  # 배치 차원 추가\n\n        # 입력 데이터를 SageMaker 엔드포인트에 전달할 입력 형식으로 준비합니다.\n        input_vals = {\n            \"instances\": image_array.tolist()\n        }\n\n        # SageMaker 엔드포인트에 예측을 요청합니다.\n        predictions = self.predictor.predict(input_vals)['predictions']\n        # 예측 결과를 데이터프레임으로 구성합니다.\n        results = pd.DataFrame(predictions, columns=['category', 'confidence'])\n\n        # 결과를 반환합니다.\n        return results\n\n","undoManager":{"mark":2,"position":2,"stack":[[{"start":{"row":0,"column":0},"end":{"row":79,"column":74},"action":"insert","lines":["import os","import numpy as np","import pandas as pd","import tensorflow as tf","from sagemaker.s3 import S3Downloader","from sagemaker.tensorflow import TensorFlowPredictor","","# 로컬에서 GPU 사용 비활성화","tf.config.set_visible_devices([], 'GPU')","","# EndpointUtil 클래스 정의: AWS SageMaker 엔드포인트와 통신하여 사용자별 영화 추천을 수행합니다.","class EndpointUtil:","    # 클래스 생성자: 초기 설정을 수행합니다.","    def __init__(self, bucket_name, endpoint_name, local_folder_path, n_user=610, n_item=9724):","        # 인자로 받은 값을 클래스 변수로 저장합니다.","        self.n_user = n_user  # 사용자 수","        self.n_item = n_item  # 아이템(영화) 수","        self.bucket_name = bucket_name  # S3 버킷 이름","        self.local_folder_path = local_folder_path.lstrip('/')  # 로컬 저장 경로, 시작하는 '/' 제거","        self.predictor = TensorFlowPredictor(endpoint_name)  # SageMaker TensorFlow 예측 엔드포인트","        # 필요한 로컬 폴더를 생성하고 테스트 세트를 다운로드합니다.","        self._ensure_local_folder()","        self._download_test_set()","        # 테스트 데이터를 로드합니다.","        self.user_test, self.item_test, self.y_test = self._load_testing_data()","","    # 로컬 폴더가 없으면 생성하는 메소드","    def _ensure_local_folder(self):","        if not os.path.exists(self.local_folder_path):","            os.makedirs(self.local_folder_path, exist_ok=True)","","    # S3에서 테스트 세트를 다운로드하는 메소드","    def _download_test_set(self):","        s3_path = f's3://{self.bucket_name}/{self.local_folder_path}'","        files = S3Downloader.list(s3_path)","        for file_path in files:","            local_path = os.path.join(self.local_folder_path, os.path.basename(file_path))","            if not os.path.exists(local_path):","                S3Downloader.download(file_path, self.local_folder_path)","","    # 로컬에 저장된 테스트 데이터를 로드하는 메소드","    def _load_testing_data(self):","        file_path = os.path.join(self.local_folder_path, 'test.npy')","        df_test = np.load(file_path)","        return np.split(np.transpose(df_test).flatten(), 3)","","    # 특정 사용자에 대한 추천을 실행하는 메소드","    def call(self, specific_user_id, threshold=0.5):","        # 특정 사용자 ID에 해당하는 데이터의 인덱스를 찾습니다.","        user_index = np.where(self.user_test == specific_user_id)[0]","        if user_index.size == 0:","            # 사용자가 테스트 데이터에 없으면 예외를 발생시킵니다.","            raise Exception(f\"User {specific_user_id} not found in the testing data.\")","","        # 특정 사용자의 데이터를 추출합니다.","        specific_user_data = self.user_test[user_index]","        specific_item_data = self.item_test[user_index]","","        # 사용자 ID와 아이템 ID를 one-hot 인코딩합니다.","        user_data_encoded = tf.one_hot(specific_user_data, depth=self.n_user).numpy().tolist()","        item_data_encoded = tf.one_hot(specific_item_data, depth=self.n_item).numpy().tolist()","","        # 인코딩된 데이터를 SageMaker 엔드포인트에 전달할 입력 형식으로 준비합니다.","        input_vals = {","            \"instances\": [","                {'input_1': user, 'input_2': item}","                for user, item in zip(user_data_encoded, item_data_encoded)","            ]","        }","","        # SageMaker 엔드포인트에 예측을 요청합니다.","        predictions = self.predictor.predict(input_vals)['predictions']","        # 예측 결과와 아이템 ID를 데이터프레임으로 구성합니다.","        recommendations = pd.DataFrame({","            'movieId': specific_item_data,","            'prediction': [pred[0] for pred in predictions]","        })","        ","        # 임계값 이상의 예측값을 가진 아이템만 필터링하여 반환합니다.","        return recommendations[recommendations['prediction'] >= threshold]"],"id":1}],[{"start":{"row":0,"column":0},"end":{"row":79,"column":74},"action":"remove","lines":["import os","import numpy as np","import pandas as pd","import tensorflow as tf","from sagemaker.s3 import S3Downloader","from sagemaker.tensorflow import TensorFlowPredictor","","# 로컬에서 GPU 사용 비활성화","tf.config.set_visible_devices([], 'GPU')","","# EndpointUtil 클래스 정의: AWS SageMaker 엔드포인트와 통신하여 사용자별 영화 추천을 수행합니다.","class EndpointUtil:","    # 클래스 생성자: 초기 설정을 수행합니다.","    def __init__(self, bucket_name, endpoint_name, local_folder_path, n_user=610, n_item=9724):","        # 인자로 받은 값을 클래스 변수로 저장합니다.","        self.n_user = n_user  # 사용자 수","        self.n_item = n_item  # 아이템(영화) 수","        self.bucket_name = bucket_name  # S3 버킷 이름","        self.local_folder_path = local_folder_path.lstrip('/')  # 로컬 저장 경로, 시작하는 '/' 제거","        self.predictor = TensorFlowPredictor(endpoint_name)  # SageMaker TensorFlow 예측 엔드포인트","        # 필요한 로컬 폴더를 생성하고 테스트 세트를 다운로드합니다.","        self._ensure_local_folder()","        self._download_test_set()","        # 테스트 데이터를 로드합니다.","        self.user_test, self.item_test, self.y_test = self._load_testing_data()","","    # 로컬 폴더가 없으면 생성하는 메소드","    def _ensure_local_folder(self):","        if not os.path.exists(self.local_folder_path):","            os.makedirs(self.local_folder_path, exist_ok=True)","","    # S3에서 테스트 세트를 다운로드하는 메소드","    def _download_test_set(self):","        s3_path = f's3://{self.bucket_name}/{self.local_folder_path}'","        files = S3Downloader.list(s3_path)","        for file_path in files:","            local_path = os.path.join(self.local_folder_path, os.path.basename(file_path))","            if not os.path.exists(local_path):","                S3Downloader.download(file_path, self.local_folder_path)","","    # 로컬에 저장된 테스트 데이터를 로드하는 메소드","    def _load_testing_data(self):","        file_path = os.path.join(self.local_folder_path, 'test.npy')","        df_test = np.load(file_path)","        return np.split(np.transpose(df_test).flatten(), 3)","","    # 특정 사용자에 대한 추천을 실행하는 메소드","    def call(self, specific_user_id, threshold=0.5):","        # 특정 사용자 ID에 해당하는 데이터의 인덱스를 찾습니다.","        user_index = np.where(self.user_test == specific_user_id)[0]","        if user_index.size == 0:","            # 사용자가 테스트 데이터에 없으면 예외를 발생시킵니다.","            raise Exception(f\"User {specific_user_id} not found in the testing data.\")","","        # 특정 사용자의 데이터를 추출합니다.","        specific_user_data = self.user_test[user_index]","        specific_item_data = self.item_test[user_index]","","        # 사용자 ID와 아이템 ID를 one-hot 인코딩합니다.","        user_data_encoded = tf.one_hot(specific_user_data, depth=self.n_user).numpy().tolist()","        item_data_encoded = tf.one_hot(specific_item_data, depth=self.n_item).numpy().tolist()","","        # 인코딩된 데이터를 SageMaker 엔드포인트에 전달할 입력 형식으로 준비합니다.","        input_vals = {","            \"instances\": [","                {'input_1': user, 'input_2': item}","                for user, item in zip(user_data_encoded, item_data_encoded)","            ]","        }","","        # SageMaker 엔드포인트에 예측을 요청합니다.","        predictions = self.predictor.predict(input_vals)['predictions']","        # 예측 결과와 아이템 ID를 데이터프레임으로 구성합니다.","        recommendations = pd.DataFrame({","            'movieId': specific_item_data,","            'prediction': [pred[0] for pred in predictions]","        })","        ","        # 임계값 이상의 예측값을 가진 아이템만 필터링하여 반환합니다.","        return recommendations[recommendations['prediction'] >= threshold]"],"id":2},{"start":{"row":0,"column":0},"end":{"row":70,"column":0},"action":"insert","lines":["import os","import numpy as np","import pandas as pd","import tensorflow as tf","from sagemaker.s3 import S3Downloader","from sagemaker.tensorflow import TensorFlowPredictor","from PIL import Image","","# 로컬에서 GPU 사용 비활성화","tf.config.set_visible_devices([], 'GPU')","","# EndpointUtil 클래스 정의: AWS SageMaker 엔드포인트와 통신하여 x-ray 이미지 판별을 수행합니다.","class EndpointUtil:","    # 클래스 생성자: 초기 설정을 수행합니다.","    def __init__(self, bucket_name, endpoint_name, local_folder_path):","        self.bucket_name = bucket_name  # S3 버킷 이름","        self.local_folder_path = local_folder_path.lstrip('/')  # 로컬 저장 경로, 시작하는 '/' 제거","        self.predictor = TensorFlowPredictor(endpoint_name)  # SageMaker TensorFlow 예측 엔드포인트","        self._ensure_local_folder()  # 필요한 로컬 폴더를 생성","        self._download_test_set()  # 테스트 세트를 다운로드","        self.image_paths = self._load_testing_data()  # 테스트 데이터를 로드","","    # 로컬 폴더가 없으면 생성하는 메소드","    def _ensure_local_folder(self):","        if not os.path.exists(self.local_folder_path):","            os.makedirs(self.local_folder_path, exist_ok=True)","","    # S3에서 테스트 세트를 다운로드하는 메소드","    def _download_test_set(self):","        s3_path = f's3://{self.bucket_name}/{self.local_folder_path}'","        files = S3Downloader.list(s3_path)","        for file_path in files:","            local_path = os.path.join(self.local_folder_path, os.path.basename(file_path))","            if not os.path.exists(local_path):","                S3Downloader.download(file_path, self.local_folder_path)","","    # 로컬에 저장된 테스트 데이터(이미지 경로)를 로드하는 메소드","    def _load_testing_data(self):","        folder_path = os.path.join(self.local_folder_path, 'images')","        return [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith('.png')]","","    # 특정 이미지에 대한 판별을 실행하는 메소드","    def call(self, image_path):","        # 이미지를 로드하고 전처리합니다.","        image = Image.open(image_path).convert('RGB')","        image = image.resize((224, 224))","        image_array = np.array(image) / 255.0  # 이미지 정규화","        image_array = np.expand_dims(image_array, axis=0)  # 배치 차원 추가","","        # 입력 데이터를 SageMaker 엔드포인트에 전달할 입력 형식으로 준비합니다.","        input_vals = {","            \"instances\": image_array.tolist()","        }","","        # SageMaker 엔드포인트에 예측을 요청합니다.","        predictions = self.predictor.predict(input_vals)['predictions']","        # 예측 결과를 데이터프레임으로 구성합니다.","        results = pd.DataFrame(predictions, columns=['category', 'confidence'])","","        # 결과를 반환합니다.","        return results","","# 예시 사용법","bucket_name = 'your-bucket-name'","endpoint_name = 'your-endpoint-name'","local_folder_path = 'your/local/folder/path'","","util = EndpointUtil(bucket_name, endpoint_name, local_folder_path)","result = util.call('path/to/your/test/image.png')","print(result)",""]}],[{"start":{"row":62,"column":0},"end":{"row":70,"column":0},"action":"remove","lines":["# 예시 사용법","bucket_name = 'your-bucket-name'","endpoint_name = 'your-endpoint-name'","local_folder_path = 'your/local/folder/path'","","util = EndpointUtil(bucket_name, endpoint_name, local_folder_path)","result = util.call('path/to/your/test/image.png')","print(result)",""],"id":5}]]},"timestamp":1716438979656}