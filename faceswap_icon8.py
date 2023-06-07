import requests
import json
import pprint


def icon8_faceswap(api_url, target_url, source_url):

    try:
        # POST 요청에 보낼 데이터
        data = {
            "target_url": target_url,
            "face_tasks": [
                {
                    "source_url": source_url,
                    "source_landmarks": [0],
                    "target_landmarks": [0],
                    "boundary_adjustments": {
                        "emotion_fear": 0,
                        "emotion_anger": 0,
                        "emotion_disgust": 0,
                        "emotion_surprise": 0,
                        "emotion_contempt": 0,
                        "emotion_happiness": 0,
                        "age": 0,
                        "gender": 0
                    }
                }
            ]
        }

        # 데이터를 JSON 형식으로 직렬화
        json_data = json.dumps(data)

        # POST 요청 보내기
        response = requests.post(api_url, data=json_data)

        # 응답 확인
        if response.status_code == 200:  # 성공적인 응답 상태 코드 (예: 200)
            # JSON 형식의 응답 데이터 가져오기
            response_data = response.json()
            print("응답 데이터:", response_data)
        else:
            print("에러 발생. 응답 상태 코드:", response.status_code)

    except Exception as e:
        print("에러 발생:", e)  
        

def upload_image(api_url, image_url):
    try:
        # POST 요청에 보낼 데이터
        data = {
            "image_url": image_url
        }

        # 데이터를 JSON 형식으로 직렬화
        json_data = json.dumps(data)

        # POST 요청 보내기
        response = requests.post(api_url, data=json_data)

        # 응답 확인
        if response.status_code == 200:  # 성공적인 응답 상태 코드 (예: 200)
            # JSON 형식의 응답 데이터 가져오기
            response_data = response.json()
            print("응답 데이터:", response_data)
        else:
            print("에러 발생. 응답 상태 코드:", response.status_code)

    except Exception as e:
        print("에러 발생:", e)
        
        
if __name__ == "__main__":
    
    # API 엔드포인트 URL
    api_url = "https://api-faceswapper.icons8.com/api/v1/process_image"
    target_url= "https://storage.googleapis.com/face-swap-test/target1.jpg"
    source_url= "https://storage.googleapis.com/face-swap-test/source1.jpg",
    icon8_faceswap(api_url, target_url, source_url)
    