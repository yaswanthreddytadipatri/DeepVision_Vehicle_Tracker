import os
import time
import requests
import base64

API_KEY = 'wxqwdrdr8ndrfc6z4'
IMAGE_FILE_PATH = '/opt/homebrew/runs/detect/predict47/crops/License_Plate/AP1.jpg'
OUTPUT_IMAGE_PATH = 'output_image.jpg'

def create_task():
    assert os.path.exists(IMAGE_FILE_PATH), f'Error: File({IMAGE_FILE_PATH}) does not exist.'
    headers = {'X-API-KEY': API_KEY}
    data = {'sync': '0'}
    files = {'image_file': open(IMAGE_FILE_PATH, 'rb')}
    url = 'https://techhk.aoscdn.com/api/tasks/visual/scale'

    # Create a task
    response = requests.post(url, headers=headers, data=data, files=files)
    task_id = None
    response_json = response.json()
    if 'status' in response_json and response_json['status'] == 200:
        result_tag = 'failed'
        if 'data' in response_json:
            response_json_data = response_json['data']
            if 'task_id' in response_json_data:
                result_tag = 'successful'
                task_id = response_json_data['task_id']
        print(f'Result of created task({result_tag}): {response_json}')
    else:
        # request failed, log the details
        print(f'Error: Failed to create task,{response.text}')
    return task_id

# def polling_task_result(task_id, time_out=30):

def polling_task_result(task_id, time_out=30):
    headers = {'X-API-KEY': API_KEY}
    url = f'https://techhk.aoscdn.com/api/tasks/visual/scale/{task_id}'
    for i in range(time_out):
        if i != 0:
            time.sleep(1)
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if 'status' in response_json and response_json['status'] == 200:
            if 'data' in response_json:
                response_json_data = response_json['data']
                if 'state' in response_json_data:
                    task_state = response_json_data['state']
                    if task_state == 1:
                        # task success
                        print(f'Result(successful): {response_json}')
                        if 'image' in response_json_data:
                            # Download the output image
                            output_image_url = response_json_data['image']
                            output_image_data = requests.get(output_image_url).content
                            with open(OUTPUT_IMAGE_PATH, 'wb') as f:
                                f.write(output_image_data)
                            print(f'Output image saved to {OUTPUT_IMAGE_PATH}')
                        break
                    elif task_state < 0:
                        # Task exception, logging the error.
                        print(f'Result(failed): {response_json}')
                        break
                    print(f'Result(polling): {response_json}')
        if i == time_out - 1:
            # Timeout, log the details, and search for support from the picwish service.
            print('Error: Timeout while polling.')
        else:
            # Task exception, logging the error.
            print(f'Error: Failed to get the task\'s result,{response.text}')
            break
    headers = {'X-API-KEY': API_KEY}
    url = f'https://techhk.aoscdn.com/api/tasks/visual/scale/{task_id}'
    for i in range(time_out):
        if i != 0:
            time.sleep(1)
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if 'status' in response_json and response_json['status'] == 200:
            if 'data' in response_json:
                response_json_data = response_json['data']
                if 'state' in response_json_data:
                    task_state = response_json_data['state']
                    if task_state == 1:
                        # task success
                        print(f'Result(successful): {response_json}')
                        if 'result' in response_json_data:
                            # Save the output image
                            image_data = base64.b64decode(response_json_data['result'])
                            with open(OUTPUT_IMAGE_PATH, 'wb') as f:
                                f.write(image_data)
                            print(f'Output image saved to {OUTPUT_IMAGE_PATH}')
                        break
                    elif task_state < 0:
                        # Task exception, logging the error.
                        print(f'Result(failed): {response_json}')
                        break
                print(f'Result(polling): {response_json}')
        if i == time_out - 1:
            # Timeout, log the details, and search for support from the picwish service.
            print('Error: Timeout while polling.')
        else:
            # Task exception, logging the error.
            print(f'Error: Failed to get the task\'s result,{response.text}')
            break

def main():
    task_id = create_task()
    if task_id is None:
        print('Error: Failed to create task, task id is None.')
        return
    polling_task_result(task_id)

if __name__ == "__main__":
    main()