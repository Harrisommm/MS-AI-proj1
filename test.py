
def read_detect_status_file():
    file_path = './temp/detect_status.txt'
    with open(file_path, 'r') as file:
        content = file.readlines()

    read_dict = {}
    for line in content:
        key, value = line.strip().split(' : ')
        read_dict[key] = value

    return read_dict


def send_status():
    status_dict = read_detect_status_file()
    # manhole_hole과 person이 모두 1인 경우에 대한 조건 확인
    if status_dict['manhole_hole'] == 'True' and status_dict['person'] == 'True':
        # 원하는 처리 수행
        status_dict['sound']= 1
        print(status_dict)

send_status()