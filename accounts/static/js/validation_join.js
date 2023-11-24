function validateForm() {
        var username = document.getElementById('floatingText').value;
        var phone = document.getElementById('floatingInput').value;
        var password1 = document.getElementById('password1').value;
        var password2 = document.getElementById('password2').value;

        // 간단한 유효성 검사 예제
        var isValid = true;

        if (!username) {
            document.getElementById('usernameError').innerHTML = '이름을 입력하세요.';
            isValid = false;
        } else {
            document.getElementById('usernameError').innerHTML = '';
        }

        if (!phone) {
            document.getElementById('phoneError').innerHTML = '전화번호를 입력하세요.';
            isValid = false;
        } else {
            document.getElementById('phoneError').innerHTML = '';
        }

        if (!password1) {
            document.getElementById('passwordError').innerHTML = '비밀번호를 입력하세요.';
            isValid = false;
        } else {
            document.getElementById('passwordError').innerHTML = '';
        }

        if (password1 !== password2) {
            document.getElementById('passwordMatchError').innerHTML = '비밀번호가 일치하지 않습니다.';
            isValid = false;
        } else {
            document.getElementById('passwordMatchError').innerHTML = '';
        }

        if (isValid) {
            // 여기에서 서버로 양식을 제출하거나 추가 동작을 수행할 수 있습니다.
        }

        return isValid;
    }