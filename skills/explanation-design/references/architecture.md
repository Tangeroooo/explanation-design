# 아키텍처 분석

먼저 분석 수준을 정한다: 논리 module / process / host / 외부 service. 필요하면 각각 별도 view로 보여준다. 같은 상자 모양으로 이 수준들을 섞지 않는다.

각 요소에서 확인할 것: 책임, 소유 상태, public interface, dependency 방향, 배치 위치의 근거. `A가 B를 import`하는 의존과 `B가 A에 callback`하는 control flow는 다를 수 있다.

구체적 요청 하나의 data flow와 control flow를 따로 추적한다. 읽기·쓰기·소유권 이전, sync 호출·async 전달, 실패 감지 주체를 표시한다. store 아이콘으로 영속성·복제·일관성을 자동 부여하지 않는다.

변경 설명에서는 다음을 고정한다.

- 유지할 계약: public API, 데이터 형식, 사용자에게 보이는 성공 조건, compatibility.
- 변경 가능한 내부: module 분리, queue 위치, batching, cache 등 근거 있는 범위.
- Before와 After의 공통 식별자 및 추가·삭제·이동된 책임.
- migration 중 두 경로가 공존할 때 routing·데이터 소유자·rollback 조건.

폴더 이름만으로 runtime 경계를 추측하지 않는다. 배포 설정을 못 봤으면 배포 topology는 미확인으로 표시한다. 구조 변경 추천은 [design-derivation](design-derivation.md)로 이어간다.
