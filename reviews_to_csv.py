import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

place_ids = ["691828370", "1363474684", "8102414"]  # 여러 가게 place_id (카카오맴 url)

# 크롬 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 결과 저장용 리스트
all_reviews = []
avg_ratings = []

for place_id in place_ids:
    try:
        url = f"https://place.map.kakao.com/{place_id}"
        print(f"\n접속할 URL: {url}")
        driver.get(url)
        time.sleep(1)

        # 리뷰 탭으로 이동
        driver.execute_script("location.hash = '#review';")
        time.sleep(2)

        # 가게 이름
        store_name = driver.find_element(By.CSS_SELECTOR, "h2.tit_head > a.link_head").text
        print("가게 이름:", store_name)

        # 스크롤로 리뷰 전체 로딩
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        review_list = driver.find_elements(By.CSS_SELECTOR, "div.group_review ul > li div.info_review.type_detail")

        review_data = []
        ratings = []

        for li in review_list:
            try:
                spans = li.find_elements(By.XPATH, ".//span[@class='starred_grade']/span[@class='screen_out']")
                rating = float(spans[1].get_attribute("innerText"))
                ratings.append(rating)

                try:
                    review_wrap = li.find_element(By.CSS_SELECTOR, "div.wrap_review")
                    try:
                        btn_more = review_wrap.find_element(By.CSS_SELECTOR, "a span.btn_more")
                        driver.execute_script("arguments[0].click();", btn_more)
                        time.sleep(0.3)
                    except:
                        pass

                    review_text = review_wrap.find_element(By.TAG_NAME, "p").text
                    review_text = review_text.replace("접기", "").strip()
                    review_text = " ".join(review_text.split())
                except:
                    review_text = None

                review_data.append({
                    "store_name": store_name,
                    "place_id": place_id,
                    "rating": rating,
                    "review": review_text
                })

            except Exception as e:
                print("리뷰 오류:", e)

        # 평균 평점 저장
        if ratings:
            avg_rating = round(sum(ratings) / len(ratings), 1)
            avg_ratings.append({
                "store_name": store_name,
                "place_id": place_id,
                "avg_rating": avg_rating,
                "review_count": len(ratings)
            })
            print(f"평균 평점: {avg_rating} ({len(ratings)}개)")
        else:
            avg_ratings.append({
                "store_name": store_name,
                "place_id": place_id,
                "avg_rating": None,
                "review_count": 0
            })
            print("리뷰 없음(리뷰 미제공)")

        # 전체 리뷰 저장
        all_reviews.extend(review_data)

    except Exception as e:
        print(f"[오류] {place_id} 크롤링 실패: {e}")

# 드라이버 종료
driver.quit()

# CSV로 저장
df_reviews = pd.DataFrame(all_reviews)
df_avg = pd.DataFrame(avg_ratings)

df_reviews.to_csv("리뷰_모음.csv", index=False, encoding='utf-8-sig')
df_avg.to_csv("평균평점_모음.csv", index=False, encoding='utf-8-sig')

print("\n모든 CSV 저장 완료")

