# 독립 평가 1단계 — 그림만 읽은 해석

reviewer: 새 문맥 diagram_reviewer. 입력은 preview/structure.png(1280×840), preview/keys.png(1280×788), 독자 질문과 audience만 제공. 원본 증거·명세·제작자 reasoning 미제공.

다음은 reviewer가 반환한 해석이다.

그림은 서비스 범위, 프로세스 범위, worker 범위, 기록 key의 동일성을 분리해서 보여줍니다. P의 worker 추가와 Q의 기록 인자 변경은 서로 다른 변경입니다.

- 경계와 소유권: 논리 서비스 S 안에 프로세스 P와 Q. P는 Coordinator 1, 현재 worker 3과 추가 제안 1, 공유 Pool 1. Mailbox는 worker마다 하나. Q는 Coordinator 1, worker 3, worker별 Mailbox, Pool 1 유지.
- 공유: P worker는 P Pool, Q worker는 별개 Q Pool 공유. Mailbox의 데이터/구현 격리 보장까지 설명하지 않음.
- P 증가: 3→4, mailbox 추가, 기존 Pool 사용. Coordinator/Pool 수와 Q 구성/key 유지. 처리량·용량·병목은 알 수 없음.
- Helper: 같은 소스 정의이며 실행 프로세스·인스턴스·메모리·기록 하나의 공유를 뜻하지 않음. node_id로 key 선택.
- Key: 평소 P→record:P, Q→record:Q. Q가 P 전달하면 두 호출이 record:P 대상. 프로세스 정체성과 인자는 반드시 같지 않음.
- 순서: worker–pool은 공유, S→Catalog는 갱신 요약, 호출→key는 대상. 좌우는 조건 비교이며 실행 순서 아님. coordinator의 전달 방식 미표시.
- 실패: 같은 key 대상이어도 최종 값·충돌 오류·갱신 유실은 규칙 부재로 알 수 없음. 확정적 데이터 손실로 읽으면 과함.
- 남은 모호함: Catalog 배포 위치/공유 방식, Pool 종류/용량, mailbox 처리, coordinator 통신. 서비스 밖 Catalog를 별도 프로세스로 확정할 수 없음. 오른쪽 record:Q 생략도 삭제 근거가 아님.

원본 증거와 HTML/SVG는 읽지 않았으며 위 해석은 두 PNG만 기준. 실제 동시성·실패 동작은 그림만으로 검증할 수 없음.
