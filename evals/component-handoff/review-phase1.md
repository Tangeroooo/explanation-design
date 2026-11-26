# 1단계: 렌더링된 그림만 보고 한 해석

확인 대상은 `component-handoff-1x.png` 한 장이며, 소스·명세·다른 자료는 읽지 않았다. 그림에 보이는 문구와 연결만으로 해석했다.

## 첫 결론

mailbox는 worker마다 하나씩 소유하고, pool은 프로세스마다 하나씩 공유한다. P에 worker를 하나 추가하면 P의 worker가 3개에서 4개가 되고 mailbox도 하나 늘어난다. P.pool은 기존 하나를 그대로 쓰며 Q의 구성은 바뀌지 않는다.

## 경계와 소유 범위

- 위쪽은 논리 관점이다. S가 Catalog의 record를 갱신하는 논리 주체다. Catalog는 외부 논리 대상이고 배포 위치는 알려져 있지 않다.
- 아래쪽은 프로세스 관점이다. S가 배포된 프로세스가 P와 Q이며, 큰 사각형은 실행 순서가 아니라 소유 범위를 나타낸다.
- P에는 coordinator 하나, 현재 worker 세 개, 공용 pool 하나가 있다. 각 worker 안에 해당 번호의 mailbox가 들어 있다.
- Q에도 coordinator 하나, worker 세 개, 공용 pool 하나가 있다. Q.worker[i]는 세 인스턴스를 요약한 표현이고, Q.mailbox[i]는 각 worker가 하나씩 소유한다. Q.pool은 P.pool과 별개다.

## 책임과 접점

- P.coordinator는 job 전달을 맡는다. 공개 입력 접점은 `submit(job)`이다.
- worker가 소유한 mailbox의 공개 접점은 `enqueue(job)`이다. mailbox를 worker 내부에 배치했지만 외부에서 호출할 수 있는 접점임을 명시한다.
- coordinator에서 mailbox로 가는 보라색 화살표는 선택된 mailbox 하나로 job을 전달한다. 그림에서는 mailbox[3]에 닿지만, 옆 문구가 대표 연결이라고 명시하므로 worker[3] 고정이나 broadcast로 읽을 이유는 없다.
- S에서 Catalog로 가는 빨간 화살표는 `record 갱신` 관계다. 그 호출을 구현하는 실제 컴포넌트는 미상이므로 coordinator 또는 worker의 책임이라고 확정할 수 없다.

## 연결과 변경 제안

- worker에서 P.pool로 이어지는 회색 선은 방향 없는 자원 공유 관계다. worker 사이의 job 전달이나 실행 순서로 읽히지 않는다.
- 점선 경계의 P.worker[4]와 그 내부 P.mailbox[4]가 추가 제안이다. 기존 worker와 같은 mailbox 접점 및 P.pool 공유 관계를 갖는다.
- 추가 worker도 기존 P.pool로 연결된다. P.pool 설명이 현재 3개, 제안 후 4개 worker의 공유를 직접 확인해 준다.
- Q는 변경 없음으로 명시된다. Q의 접점 상세는 생략되어 있다.

## 남아 있는 의미상 불명확함

- worker가 mailbox를 소비하고 실제 job을 처리하는 방법과 그 이후의 흐름은 나타나지 않는다. worker 추가가 처리량이나 병렬 실행 증가를 보장한다고 읽을 수 없다.
- mailbox 선택 규칙, 용량, 순서와 pool의 종류·용량·API·계약은 알려져 있지 않다. 공유 경쟁이나 worker 추가의 성능 영향도 판단할 수 없다.
- Catalog 배포 위치 및 내구성, record 갱신을 실행하는 컴포넌트는 의도적으로 열려 있다.
- P.worker[4]를 mailbox 선택 대상에 포함하기 위해 별도 등록이나 coordinator 변경이 필요한지는 설명하지 않는다. 그림이 확정하는 변경은 worker와 mailbox 추가 및 기존 pool 공유까지다.
- Q는 worker별 pool 연결선을 개별적으로 그리지 않는다. 다만 `Q.pool 공유`와 `Q.pool ×1`, P.pool과 별개라는 문구 덕분에 소유·공유 관계는 읽을 수 있다.

1단계에서는 렌더링 외의 근거와 일치하는지, 실제 구현이 이 구조인지 확인하지 않았다.
