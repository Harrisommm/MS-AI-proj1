window.onload = function(){
    const switchElement = document.getElementById('alertToggle');
    // 스위치 상태 변경 시 이벤트 처리
    
    switchElement.addEventListener('change', function () {
        if (this.checked) {
            // 스위치가 켜진 경우, Django View에서 데이터 가져오기
            fetch('sound')
            .then(response => response.json())
            .then(data => {
                // JavaScript에서 데이터 처리 및 오디오 재생
                if (data.sound === 1) {
                    playAudio();
                }
            });
        } else {
            // 스위치가 꺼진 경우, 오디오 중지
            stopAudio();
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
