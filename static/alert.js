window.onload = function(){
    const switchElement1 = document.getElementById('alertToggle');
    const switchElement2 = document.getElementById('workToggle');
    
    // 작업 버튼
    let intervalId;  // setInterval을 관리하기 위한 변수

    // 스위치 상태 변경 시 이벤트 처리
    switchElement1.playsound('change', function () {
        if (this.checked) {
            // 스위치가 켜진 경우, 주기적으로 Django View에서 데이터 가져오기
            playsound();
            intervalId = setInterval(fetchAndProcessData, 5000);  // 1초마다 실행 (1000ms)
        } else {
            // 스위치가 꺼진 경우, 오디오 중지 및 setInterval 해제
            stopAudio();
            clearInterval(intervalId);
        }
    });
    switchElement2.readstatus('change', function () {
        if (this.checked) {
            document.getElementById("text_notification").innerHTML = notification_str;
        } else {
            console.log("off")
        }
    });
}

// 주기적으로 Django View에서 데이터 가져와 처리하는 함수
function playsound() {
    fetch('send_status', {
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // JavaScript에서 데이터 처리 및 오디오 재생
        if (data.sound == 'True') {
            playAudio();
        }

    });
}

function readstatus() {
    fetch('send_status', {
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // JavaScript에서 데이터 처리 및 오디오 재생
        checkManholeStatus(data)

    });
}


// 오디오 재생 함수
function playAudio() {
    // 실제로 사용할 오디오 파일 경로를 설정
    const audioPath = '/static/audio/alert.mp3';  // 예시 경로, 실제 경로에 맞게 수정

    // 오디오 엘리먼트 생성 및 재생
    const audio = new Audio(audioPath);
    audio.play();
}

// 오디오 중지 함수
function stopAudio() {
    // 모든 오디오 엘리먼트 중지
    const allAudioElements = document.querySelectorAll('audio');
    allAudioElements.forEach(audio => audio.pause());
}


//스테터스 바 출력 함수
function checkManholeStatus(status_dict) {
    // Read key values from status_dict(), defaulting to 'False' if not present
    let manhole_open = status_dict['manhole_open'] === 'True';
    let pedestrian = status_dict['person'] === 'True';

    while (manhole_open) {
        if (workin && pedestrian) {
            console.log("멘홀 작업 중 보행자가 감지되었습니다. + 음성 메세지 출력");
        } else if (workin) {
            console.log("멘홀이 열려 있고 작업 중입니다.");
        } else if (pedestrian) {
            console.log("작업시간외 맨홀 열림이 감지되었습니다. 보행자가 감지되었습니다. + 음성 메세지 출력");
        } else {
            console.log("작업시간외 맨홀 열림이 감지되었습니다.");
        }

        manhole_open = status_dict['manhole_open'];  // Placeholder condition, replace with actual logic
    }

    console.log("멘홀이 닫혀 있습니다.");
}