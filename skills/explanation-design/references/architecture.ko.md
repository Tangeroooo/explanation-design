# 아키텍처 분석

먼저 분석 수준을 정한다: 논리 module / process / host / 외부 service. 필요하면 각각 별도 view로 보여준다. 같은 상자 모양으로 이 수준들을 섞지 않는다.

각 요소에서 확인할 것: 책임, 소유 상태, public interface, dependency 방향, 배치 위치의 근거. `A가 B를 import`하는 의존과 `B가 A에 callback`하는 control flow는 다를 수 있다.

구조도를 그리기 전에 조사 결과를 [컴포넌트 명세](../assets/component-brief.ko.md)에 옮긴다. 관련 컴포넌트나 반복 그룹별로 소유권·수량·내부 상세·근거 있는 인터페이스·관계 종류를 기록한다. 근거가 없는 것과 의도적으로 표시하지 않는 것을 구분한다. 이름만 나열한 목록으로 제작 명세를 대신하지 않는다.

그림이 도움이 되면 [visual-selection](visual-selection.ko.md)에 따라 책임 구획·인터페이스 접점·유형별 자원·소유 경계가 보이는 컴포넌트 뷰를 만든다. 공유 자원은 호출자마다 복제하지 않고 실제 소유자 안에 한 번 표시한다. 재설계는 배치를 맞춘 Before/After 구조나 고정된 구조도 위의 책임 변경으로 비교한다. sequence만으로 모듈 경계나 아키텍처 설명 요청을 충족했다고 판단하지 않는다. 상호작용 순서가 추가 질문에 답할 때만 덧붙인다. 공간 배치로 실행 순서를 만들어내지 않는다.

구체적 요청 하나의 data flow와 control flow를 따로 추적한다. 읽기·쓰기·소유권 이전, sync 호출·async 전달, 실패 감지 주체를 표시한다. store 아이콘으로 영속성·복제·일관성을 자동 부여하지 않는다.

변경 설명에서는 다음을 고정한다.

- 유지할 계약: public API, 데이터 형식, 사용자에게 보이는 성공 조건, compatibility.
- 변경 가능한 내부: module 분리, queue 위치, batching, cache 등 근거 있는 범위.
- Before와 After의 공통 식별자 및 추가·삭제·이동된 책임.
- migration 중 두 경로가 공존할 때 routing·데이터 소유자·rollback 조건.

폴더 이름만으로 runtime 경계를 추측하지 않는다. 배포 설정을 못 봤으면 배포 topology는 미확인으로 표시한다. 구조 변경 추천은 [design-derivation](design-derivation.ko.md)로 이어간다.
