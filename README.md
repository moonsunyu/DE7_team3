### GIT 브랜치 만들기
1. `git pull origin master` -> 새로 업데이트된 내용 가져오기
2. `git checkout -b [브랜치명]` -> 새로운 브랜치 생성 후 이동
3. 파일 수정 ~~~~
4. `git add .` -> 변화 저장
5. `git commit -m "feature: 로그인 기능 구현"` -> 메세지 작성
6. `git push -u origin [브랜치명]` -> 브랜치에 변화 내용 업로드(push)
7. git에서 pull request 후 충돌 없을 경우 merge

&nbsp;

### 메시지/브랜치 이름 작성 규칙
#### 기능 변경 O
- `feat`	새로운 기능 추가
- `fix`	버그 수정
- `docs`	문서 수정
- `style`	코드 스타일 변경 (코드 포매팅, 세미콜론 누락 등)

#### 기능 변경 X
- `design`	사용자 UI 디자인 변경 (CSS 등)
- `test`	테스트 코드, 리팩토링 테스트 코드 추가
- `refactor`	코드 리팩토링
- `build`	빌드 파일 수정
- `ci`	CI 설정 파일 수정
- `perf`	성능 개선
- `chore`	빌드 업무 수정, 패키지 매니저 수정 (gitignore 수정 등)
- `rename`	파일 혹은 폴더명을 수정만 한 경우
- `remove`	파일을 삭제만 한 경우
