# 그림 제작 명세

독자: 구조를 이해하려는 엔지니어. 입력은 system.md에 명시된 가상 시스템의 사실이며 실제 코드 검증이 아니다.

## 출처와 주장

- S1: system.md, 2026-11-25 수신, 5개 사실 항목. 그림은 모든 항목을 사용한다.
- C1 (사실): 서비스 S→Catalog 연결은 기록 갱신 요약이며 프로세스 수를 말하지 않는다. S1 첫째 항목.
- C2 (사실): P/Q 각각 coordinator 1, worker 3과 각 mailbox, worker들이 공유하는 pool 1. pool은 프로세스별로 별개다. S1 둘째 항목.
- C3 (사실): 동일 소스 함수 update_record(node_id, value)는 인자만으로 record:<node_id>를 선택한다. P는 평소 P, Q는 평소 Q를 전달한다. S1 셋째·넷째 항목.
- C4 (제안): P worker를 4개로 바꾸고 Q는 유지한다. S1 다섯째 항목. 새 worker의 mailbox와 같은 pool 사용은 C2 모델을 유지한 국소 변경으로 해석했다.
- C5 (제안과 추론): Q도 P를 전달하면 record:P가 동일 대상이 된다. S1 셋째~다섯째 항목.
- U1 (미상): 동시 갱신 순서·충돌 해결, pool 종류·용량, 처리량, coordinator-worker 통신 경로, catalog 배포 단위. 주어지지 않은 계약을 그림에 추가하지 않는다.

## 그림 1 — structure

질문: 어떤 범위에 자원이 속하고 P worker 증가가 어디에 영향을 주는가?
메시지: 서비스는 하나지만 pool은 P/Q별로 나뉘며, P에 추가되는 worker는 기존 P pool을 공유한다.
유형: architecture component view; 순서도가 범위와 공유를 지우므로 사용하지 않는다.
요소: S 논리 경계, P 프로세스 상세, Q 프로세스 요약, coordinator, worker별 mailbox, P pool, Catalog 기록 grid.
관계: 감싼 경계=소속; worker–pool 선=공유 관계(C2); S→Catalog 화살표=논리 갱신 요약(C1). coordinator 연결선은 근거가 없어 생략.
추상화: Q의 동일 worker 3개를 수량과 mailbox 귀속으로 요약한다. worker 식별 번호는 그림에서만 쓰는 구별 표지다. Catalog는 논리 서비스와 구분하지만 배포 위치를 뜻하지 않는다.
비교: 현재 P worker 3개에 네 번째만 점선 경계·추가 제안 표식으로 강조. Q, coordinator, pool 수를 유지한다.
표시/viewBox: 1280×840 CSS px, PNG 2560×1680, 2배. fit 크기, engineer 대상. 기본 복잡도 9개 이내(하위 mailbox는 worker의 상태 구획).

## 그림 2 — keys

질문: 같은 helper가 같은 기록을 갱신한다는 뜻인가?
메시지: 소스 정의의 동일성과 인자로 결정되는 기록 대상의 동일성은 다르다.
유형: architecture mapping의 조건별 비교. 좌우는 실행 순서가 아니며 같은 시스템의 조건 비교다.
요소: 공통 소스 정의 문맥, 각 프로세스 호출, Catalog의 명명된 기록.
관계: 호출→기록 화살표는 C3의 인자→key 매핑이다. 오른쪽 Q→record:P 점선은 C5 제안이다.
추상화: 호출이 coordinator/worker 어느 쪽에서 발생하는지 불명이라 연결하지 않는다. 오른쪽 record:Q 생략은 삭제를 뜻하지 않는다.
정확한 표기: update_record(node_id, value), record:P, record:Q, node_id = "P", node_id = "Q". write 표현은 원문 계약을 설명하는 의사코드다.
표시/viewBox: 1280×788 CSS px, PNG 2560×1576, 2배. fit 크기.

## 공통 제작과 검증 조건

- 설치된 diagram-design 2.6의 assets/template.html과 export_svg.py/export_png.py 사용. 별도 렌더러 없음. 편집 원본 make_sources.py, 생성된 HTML. 그림 변경 시 HTML→SVG/PNG→문서 전부 갱신.
- 테마: explanation-design의 고정 밝은 팔레트. 배경 #fbfcfe, 글자 #1f2a3c. coordination 보라 #6a4cc0/#f2eefc, worker·write 주황 #c46a17/#fff4e8, catalog 빨강 #b83a30/#fdeeee, mailbox 운송 slate #3c4a62/#eef1f6, pool 중립 #66748a/#f1f4f8, 제안 amber #b07d0a/#fff7df. pool 종류를 몰라 memory 녹색을 쓰지 않는다.
- Noto Sans KR: 설명·일반 구성요소 이름. DejaVu Sans Mono: 함수·변수·값·literal ID. 제목 30px/700, 요소 heading 18px/700, 본문 16px, 보조 14px. 중요 경계 1.5–2px, 화살표 2.5px, 제안 3px. 모두 표시 기준 값.
- 글꼴은 기존 설치 자산을 복사하고 사용 글리프로 subset하여 data URL로 포함. 라이선스 fonts/에 동봉. subset 도구는 기존 fontTools 사용; 설치 없음.
- HTML은 1280px 폭 유지, 좁은 화면은 local horizontal scroll. 원본 근거가 없는 runtime guarantee는 추가하지 않는다.
- 의미 확인: P의 worker만 늘리면 pool 수·기록 key·Q 구성은 유지. Q 인자를 P로 바꾸면 record:P 동일 대상. 동시 갱신 최종 값은 미상.
- 독립 검토: 새 문맥 reviewer 한 명. 먼저 두 1× PNG와 독자 질문만 전달, 해석 보존 후 원문·명세·실측 전달. 최대 수정/재검토 2회.
- 합격 기준: 경계·공유·인자→key가 가려지지 않고 1280px에서 읽히며, label 겹침/잘림/고립 선 없음. 정확한 글꼴은 CDP actual platform fonts로 확인. checker 제한과 미검증은 구분한다.
