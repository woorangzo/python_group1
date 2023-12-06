function validateLoginForm(e) {
    function validateLoginForm(e) {
        e.preventDefault();
        var id = document.getElementById('floatingText').value;
        var password = document.getElementById('floatingPassword').value;

        // 간단한 유효성 검사 예제
        var isValid = true;

        // 오류 메시지 초기화
        document.getElementById('idError').innerHTML = '';
        document.getElementById('passwordError').innerHTML = '';

        if (!id) {
            document.getElementById('idError').innerHTML = 'ID를 입력하세요.';
            isValid = false;
        }

        if (!password) {
            document.getElementById('passwordError').innerHTML = '비밀번호를 입력하세요.';
            isValid = false;
        }

        if (isValid) {
            // 유효성 검사 통과 시 폼 제출
            e.currentTarget.submit();
        }

        return isValid;
    }
}

