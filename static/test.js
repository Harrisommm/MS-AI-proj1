window.onload = function(){
    const switchElement = document.getElementById('alertToggle');
    let intervalId;  // setInterval을 관리하기 위한 변수

    // 스위치 상태 변경 시 이벤트 처리
    switchElement.addEventListener('change', function () {
        if (this.checked) {
            // 스위치가 켜진 경우, 주기적으로 Django View에서 데이터 가져오기
            intervalId = setInterval(fetchAndProcessData, 5000);  // 1초마다 실행 (1000ms)
        } else {
            // 스위치가 꺼진 경우, 오디오 중지 및 setInterval 해제
            stopAudio();
            clearInterval(intervalId);
        }
    });

    // 초기 로딩 시 스위치가 켜져있다면 주기적으로 데이터 가져오기 시작
    // if (switchElement.checked) {
    //     intervalId = setInterval(fetchAndProcessData, 1000);
    // }
}

// 주기적으로 Django View에서 데이터 가져와 처리하는 함수
function fetchAndProcessData() {
    fetch('sound')
    .then(response => response.json())
    .then(data => {
        // JavaScript에서 데이터 처리 및 오디오 재생
        if (data.sound == 1) {
            playAudio();
        }
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
