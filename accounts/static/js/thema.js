document.addEventListener("DOMContentLoaded", function () {
    // 초기 설정
    let currentNewsIndex = 0;

    // 함수 정의: 다음 뉴스로 이동하는 함수
    function showNextNews() {
        const newsflashElements = document.querySelectorAll('.mainNewsTicker dd.data span');
        
        // 현재 뉴스를 숨김
        newsflashElements[currentNewsIndex].style.display = 'none';

        // 다음 뉴스 인덱스 계산
        currentNewsIndex = (currentNewsIndex + 1) % newsflashElements.length;

        // 다음 뉴스를 보임
        newsflashElements[currentNewsIndex].style.display = '';
    }

    // 일정 시간 간격으로 자동으로 다음 뉴스로 전환
    const intervalId = setInterval(showNextNews, 40000); // 5000 밀리초(5초)마다 전환

    // 이벤트 핸들러: 마우스가 뉴스에 올라갈 때, 자동 전환을 일시 중지
    function viewNewsflashPause() {
        clearInterval(intervalId);
    }

    // 이벤트 핸들러: 마우스가 뉴스에서 벗어날 때, 자동 전환을 다시 시작
    function viewNewsflashStart() {
        intervalId = setInterval(showNextNews, 5000);
    }

    // 초기 설정: 이벤트 핸들러 등록
    const newsflashElements = document.querySelectorAll('.mainNewsTicker dd.data span');
    newsflashElements.forEach((element, index) => {
        element.addEventListener('mouseover', viewNewsflashPause);
        element.addEventListener('mouseout', viewNewsflashStart);
    });
});


function showTab(tabToShow, tabToHide, event) {
    event.preventDefault();
    // 선택한 탭 보이기
    document.getElementById(tabToShow).style.display = '';
    // 다른 탭 숨기기
    document.getElementById(tabToHide).style.display = 'none';
}

function hideTab(tabToHide, tabToShow, event) {
    event.preventDefault();
    document.getElementById(tabToShow).style.display = 'none';

    document.getElementById(tabToHide).style.display = '';
}

function showTab2(tabgsell, tabgbuy, event) {
    event.preventDefault();
    document.getElementById(tabgbuy).style.display = '';
    document.getElementById(tabgsell).style.display = 'none';
}

function hideTab2(tabgbuy, tabgsell, event) {
    event.preventDefault();
    document.getElementById(tabgbuy).style.display = 'none';
    document.getElementById(tabgsell).style.display = '';
}