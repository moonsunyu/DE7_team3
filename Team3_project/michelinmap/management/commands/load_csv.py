# myapp/management/commands/load_csv.py
# 이 파일을 위의 경로에 저장하세요!

import pandas as pd
from django.core.management.base import BaseCommand
from michelinmap.models import Region, City, Restaurant, Review  # ⚠️ myapp을 여러분 앱 이름으로 변경!


class Command(BaseCommand):
    help = 'CSV 파일에서 데이터를 읽어서 DB에 저장합니다'

    def handle(self, *args, **options):
        # 이 부분이 실제로 실행되는 코드입니다
        
        print(" CSV 데이터 로딩을 시작합니다!")
        print("-" * 50)
        
        # ============================================
        # 1. Region (지역) 데이터 로드
        # ============================================
        print(" Step 1: Region 데이터 로딩중...")
        
        # CSV 파일 읽기
        df = pd.read_csv('regions.csv')
        
        # 한 줄씩 처리
        for index, row in df.iterrows():
            # DB에 저장 (이미 있으면 건너뛰고, 없으면 생성)
            region, created = Region.objects.get_or_create(
                id=row['id'],
                defaults={'r_name': row['r_name']}
            )
            
            if created:
                print(f"    새로운 지역 추가: {row['r_name']}")
        
        print(f"   완료! 전체 지역 수: {Region.objects.count()}개\n")
        
        
        # ============================================
        # 2. City (도시) 데이터 로드
        # ============================================
        print(" Step 2: City 데이터 로딩중...")
        
        df = pd.read_csv('cities.csv')
        
        for index, row in df.iterrows():
            # 먼저 해당 Region을 찾아야 함
            region = Region.objects.get(id=row['region_id'])
            
            # City 생성
            city, created = City.objects.get_or_create(
                id=row['id'],
                defaults={
                    'c_name': row['c_name'],
                    'region': region  # 위에서 찾은 region 연결
                }
            )
            
            if created:
                print(f"   새로운 도시 추가: {row['c_name']}")
        
        print(f"   완료! 전체 도시 수: {City.objects.count()}개\n")
        
        
        # ============================================
        # 3. Restaurant (식당) 데이터 로드
        # ============================================
        print(" Step 3: Restaurant 데이터 로딩중...")
        print("   (데이터가 많아서 시간이 좀 걸려요...)")
        
        df = pd.read_csv('restaurants.csv')
        count = 0
        
        for index, row in df.iterrows():
            # 해당 City 찾기
            city = City.objects.get(id=row['city_id'])
            
            # Restaurant 생성
            restaurant, created = Restaurant.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'address': row['address'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'category': row['category'],
                    'page' : row['page'],
                    'price': row['price'] if pd.notna(row['price']) else None,
                    'rating': row['rating'] if pd.notna(row['rating']) else None,
                    'review_cnt': row['review_cnt'] if pd.notna(row['review_cnt']) else None,
                    'call_number': row['call_number'] if pd.notna(row['call_number']) else None,
                    'city': city
                }
            )
            
            if created:
                count += 1
                # 50개마다 진행상황 표시
                if count % 50 == 0:
                    print(f"   ... {count}개 완료")
        
        print(f"   완료! 전체 레스토랑 수: {Restaurant.objects.count()}개\n")
        
        
        # ============================================
        # 4. Review (리뷰) 데이터 로드
        # ============================================
        # print(" Step 4: Review 데이터 로딩중...")
        # print("   (리뷰가 많아서 시간이 좀 더 걸려요...)")
        
        # df = pd.read_csv('reviews.csv')
        # count = 0
        
        # for index, row in df.iterrows():
        #     # 해당 Restaurant 찾기
        #     restaurant = Restaurant.objects.get(id=row['restaurant_id'])
            
        #     # Review 생성
        #     review, created = Review.objects.get_or_create(
        #         id=row['id'],
        #         defaults={
        #             'restaurant': restaurant,
        #             'star': row['star'] if pd.notna(row['star']) else 0.0,
        #             'comment': row['comment'] if pd.notna(row['comment']) else ''
        #         }
        #     )
            
        #     if created:
        #         count += 1
        #         # 100개마다 진행상황 표시
        #         if count % 100 == 0:
        #             print(f"   ... {count}개 완료")
        
        # print(f"   완료! 전체 리뷰 수: {Review.objects.count()}개\n")
        
        
        # ============================================
        # 완료!
        # ============================================
        print("=" * 50)
        print(" 모든 데이터 로딩이 완료되었습니다!")
        print("=" * 50)
        print(f" 최종 데이터 현황:")
        print(f"   - 지역(Region): {Region.objects.count()}개")
        print(f"   - 도시(City): {City.objects.count()}개")
        print(f"   - 레스토랑(Restaurant): {Restaurant.objects.count()}개")
        print(f"   - 리뷰(Review): {Review.objects.count()}개")
        print("=" * 50)