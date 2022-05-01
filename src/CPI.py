from exceptions.CPI_Exceptions import InvalidFile, InvalidParameters
import requests
import time


class CPI:

    def __init__(self, file: str = None, facebook_page_id: str = None, access_token: str = None):
        if file is None and (facebook_page_id is None or access_token is None):
            raise InvalidParameters('Either a file or a combination of Facebook Page ID AND Access Token '
                                    'must be supplied.')
        if file is not None and not file.endswith('.txt'):
            raise InvalidFile('File must be a .txt file containing the Facebook Page ID on the first line and the '
                              'Access Token on the second line.')
        if file is None:
            self.facebook_page_id = facebook_page_id
            self.access_token = access_token
        else:
            try:
                user_file = open(file)
                self.facebook_page_id = user_file.readline().strip()
                self.access_token = user_file.readline().strip()
                user_file.close()
            except FileNotFoundError:
                raise FileNotFoundError
        self.graph_api_url = 'https://graph.facebook.com/v10.0/'
        self.TIMEOUT_SECONDS = 15
        self.insta_id = self.__validate()

    def publish_image(self, image_url: str, caption: str = None) -> bool:
        pre_upload_url = self.graph_api_url + '{}/media'.format(self.insta_id)
        pre_upload = {'image_url': image_url,
                      'caption': caption if caption is not None else '',
                      'access_token': self.access_token}
        pre_upload_request = requests.post(pre_upload_url, data=pre_upload, timeout=self.TIMEOUT_SECONDS)
        if pre_upload_request.status_code != 200:
            return False
        pre_upload_result = pre_upload_request.json()
        if 'id' in pre_upload_result:
            creation_id = pre_upload_result['id']
            publish_url = self.graph_api_url + '{}/media_publish'.format(self.insta_id)
            publish = {
                'creation_id': creation_id,
                'access_token': self.access_token
            }
            if requests.post(publish_url, data=publish, timeout=self.TIMEOUT_SECONDS).status_code != 200:
                return False
        else:
            return False
        print(f'Successfully posted image to Instagram at {"".join(map(str, time.strftime("%H:%M:%S").split()))}.')
        return True

    def publish_video(self, video_url: str, caption: str = None) -> bool:
        pre_upload_url = self.graph_api_url + '{}/media'.format(self.insta_id)
        pre_upload = {'media_type': 'VIDEO',
                      'video_url': video_url,
                      'caption': caption if caption is not None else '',
                      'access_token': self.access_token}
        pre_upload_request = requests.post(pre_upload_url, data=pre_upload, timeout=self.TIMEOUT_SECONDS)
        pre_upload_result = pre_upload_request.json()

        if 'id' in pre_upload_result:
            creation_id = pre_upload_result['id']
            progress_req = self.graph_api_url + f'/{creation_id}?access_token={self.access_token}&fields=status_code'
            video_progress = requests.get(progress_req)
            if video_progress.status_code != 200:
                return False
            video_progress = video_progress.json()
            while video_progress['status_code'] == 'IN_PROGRESS':
                time.sleep(10)
                video_progress = requests.get(progress_req).json()
                if video_progress['status_code'] == 'ERROR':
                    return False
            publish_url = self.graph_api_url + '{}/media_publish'.format(self.insta_id)
            publish_data = {
                'creation_id': creation_id,
                'access_token': self.access_token
            }
            if requests.post(publish_url, data=publish_data, timeout=self.TIMEOUT_SECONDS).status_code != 200:
                return False
        else:
            return False
        print(f'Successfully posted video to Instagram at {"".join(map(str, time.strftime("%H:%M:%S").split()))}.')
        return True

    def __validate(self) -> str:
        insta_id_url = self.graph_api_url + '{}?fields=instagram_business_account'.format(self.facebook_page_id)
        querystring = {'access_token': self.access_token}
        headers = {'Accept': 'application/json'}
        response = requests.get(insta_id_url, headers=headers, params=querystring, timeout=self.TIMEOUT_SECONDS)
        if response.status_code != 200:
            raise InvalidFile(response.json()['error']['message'])
        insta_id = response.json()['instagram_business_account']['id']
        return insta_id
