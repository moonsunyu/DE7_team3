document.addEventListener("DOMContentLoaded", function() {
    // 1. 데이터 및 요소 가져오기
    var allCities = JSON.parse(document.getElementById('cities-data').textContent);
    var regionSelect = document.getElementById('region-select');
    var citySelect = document.getElementById('city-select');

    // URL에서 현재 선택된 ID를 가져와 상태 복원에 사용합니다.
    var urlParams = new URLSearchParams(window.location.search);
    var initialRegionId = urlParams.get('region_id'); 
    var initialCityId = urlParams.get('city_id');

    // 🌟 시/군/구 select 박스를 갱신하는 핵심 함수 🌟
    function updateCitySelect(selectedRegionId, cityToSelect) {
        // 1. 초기화
        // 시/군/구 선택 옵션을 항상 맨 위에 위치시키고, cityToSelect가 없으면 selected 상태로 만듭니다.
        citySelect.innerHTML = `<option value="" disabled style="color:#999;" ${!cityToSelect ? 'selected' : ''}>시/군/구 선택</option>`;
        
        // 시/도가 선택되지 않았다면 City Select를 비활성화합니다.
        if (!selectedRegionId) {
            citySelect.disabled = true;
            return;
        }
        
        citySelect.disabled = false;

        // 2. '전체' 옵션 추가
        var allOption = document.createElement('option');
        allOption.value = 'all'; // 👈 'all' 문자열이 정확해야 합니다.
        allOption.textContent = '전체';
        
        // 새로고침 후 'all' 복원
        if (cityToSelect === 'all') {
            allOption.selected = true;
        }
        citySelect.appendChild(allOption);

        // 3. 필터링된 City 옵션 추가
        allCities.forEach(function(city) {
            // region_id가 일치하는 경우만 추가 (타입 일치 비교)
            if (city.region_id == selectedRegionId) { 
                var option = document.createElement('option');
                option.value = city.id;
                option.textContent = city.c_name;
                
                // 새로고침 후 특정 City ID 복원 (타입 일치 비교)
                if (city.id == cityToSelect) {
                    option.selected = true;
                }
                citySelect.appendChild(option);
            }
        });
    }

    // --- 1. 페이지 로드 시 초기 상태 복원 ---
    // 새로고침 시 initialRegionId가 있으면, 시/군/구 목록을 채우고 선택 상태를 복원합니다.
    if (initialRegionId) {
        updateCitySelect(initialRegionId, initialCityId);
    } else {
        // 초기 로드 시 시/도 선택 전이므로, 시/군/구는 비활성화된 상태로 시작합니다.
        updateCitySelect(null, null);
    }

    // --- 2. 이벤트 리스너: 시/도 선택 변경 시 실행 (갱신) ---
    // 시/도 선택이 바뀌면 이 함수가 실행되며, 시/군/구 목록을 업데이트합니다.
    regionSelect.addEventListener('change', function() {
        var selectedRegionId = this.value;

        // 시/도 변경 시 시/군/구 목록을 갱신하고, 선택된 시/군/구 값은 초기화합니다.
        // (null을 넘겨서 '시/군/구 선택'이 다시 selected 상태가 되도록 합니다.)
        updateCitySelect(selectedRegionId, null);
        
        // 폼 제출은 '검색' 버튼이 담당하므로, 여기서 submit()은 호출하지 않습니다.
    });

    var form = document.getElementById('location-form'); // 폼 ID 확인
    form.addEventListener('submit', function(e) {
        if (!regionSelect.value || !citySelect.value) {
            e.preventDefault(); // 제출 막기
            alert('시/도와 시/군/구를 모두 선택해주세요!');
        }
    });
});