function updateKPI() {
        fetch('/get_kpi_data/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('kpi-value').textContent = data.value;
                document.getElementById('kpi-change').textContent = data.change;
                document.getElementById('kpi-percent').textContent = data.percent;

                // 코스피 데이터를 가져왔으면 코스피를 보이게 하고, 코스닥은 숨기기
                document.getElementById('kpi-info').style.display = 'block';
                document.getElementById('kosdaq-info').style.display = 'none';
            })
            .catch(error => {
                console.error('Error fetching KPI data:', error);
                document.getElementById('kpi-value').textContent = 'Error';
                document.getElementById('kpi-change').textContent = '';
                document.getElementById('kpi-percent').textContent = '';
            });
    }

    function updateKosdaq() {
        fetch('/get_kosdaq_data/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('kosdaq-value').textContent = data.value;
                document.getElementById('kosdaq-change').textContent = data.change;
                document.getElementById('kosdaq-percent').textContent = data.percent;

                // 코스닥 데이터를 가져왔으면 코스피를 숨기고, 코스닥은 보이게 하기
                document.getElementById('kpi-info').style.display = 'none';
                document.getElementById('kosdaq-info').style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching KOSDAQ data:', error);
                document.getElementById('kosdaq-value').textContent = 'Error';
                document.getElementById('kosdaq-change').textContent = '';
                document.getElementById('kosdaq-percent').textContent = '';
            });
    }

    // 초기 로딩
    updateKPI();

    // 일정 간격으로 KPI 업데이트
    setInterval(function() {
        updateKPI();
        // 코스피를 업데이트한 후에 코스닥을 업데이트
        updateKosdaq();
    }, 3000);