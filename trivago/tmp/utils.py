import json

def read_json_file(file_path):
    """JSON 파일을 읽어와서 데이터를 반환합니다."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    """데이터를 JSON 파일에 저장합니다."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4, separators=(',', ': '))


def add_data_to_json(file_path, new_data):
    """JSON 파일에 데이터를 추가하고 저장합니다."""
    # JSON 파일을 읽어옵니다.
    data = read_json_file(file_path)
    

    data['datas'].append(new_data)
    
    # 변경된 데이터를 파일에 저장합니다.
    write_json_file(file_path, data)