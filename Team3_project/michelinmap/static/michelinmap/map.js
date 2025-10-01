let map;

document.addEventListener("DOMContentLoaded", function() {
    // 레스토랑 데이터 가져오기
    const restaurantItems = document.querySelectorAll(".restaurant-item");
    const restaurants = Array.from(restaurantItems).map(item => {
        const name = item.querySelector(".restaurant-name").textContent;
        const lat = parseFloat(item.dataset.lat);
        const lng = parseFloat(item.dataset.lng);
        return { name, lat, lng };
    });

    const mapContainer = document.getElementById("map");
    let centerLatLng, mapLevel;

    if (!restaurants || restaurants.length === 0) {
        // city_id 없거나 식당 리스트 없음 → 서울시청 중심, level 7
        centerLatLng = new kakao.maps.LatLng(37.5665, 126.9780);
        mapLevel = 7;
    } else {
        // city_id 존재 → 첫 번째 식당 좌표 중심, level 3
        centerLatLng = new kakao.maps.LatLng(restaurants[0].lat, restaurants[0].lng);
        mapLevel = 3;
    }

    map = new kakao.maps.Map(mapContainer, {
        center: centerLatLng,
        level: mapLevel
    });

     // 모든 식당에 마커 + 커스텀 오버레이 생성
    restaurants.forEach(r => {
        if (isNaN(r.lat) || isNaN(r.lng)) return;

        const position = new kakao.maps.LatLng(r.lat, r.lng);

        // 마커
        const marker = new kakao.maps.Marker({ position, map });

        // 커스텀 오버레이
        const overlay = new kakao.maps.CustomOverlay({
            position,
            content: `<div style="padding:2px 5px; background:#fff; border:1px solid #ccc; font-size:12px;">${r.name}</div>`,
            yAnchor: 2.8
        });
        overlay.setMap(map);
    });

    // hover 이벤트 → 지도 중심 이동
    restaurantItems.forEach(item => {
        const nameLink = item.querySelector(".restaurant-name");

        nameLink.addEventListener("mouseenter", function () {
            const lat = parseFloat(item.dataset.lat);
            const lng = parseFloat(item.dataset.lng);

            if (!isNaN(lat) && !isNaN(lng)) {
                map.setCenter(new kakao.maps.LatLng(lat, lng));
            }
        });
    });
});