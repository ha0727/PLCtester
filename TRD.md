# Technical Requirements Document (TRD)

## 1. Executive Technical Summary
- **Project Overview**: 본 프로젝트는 장비업체 PLC 엔지니어가 현장 투입 전 MES와 Mitsubishi PLC 간의 통신을 검증할 수 있도록 돕는 Windows 데스크톱 애플리케이션 개발을 목표로 한다. 자동화된 테스트 시나리오 실행, 실시간 이벤트 모니터링, 결과 리포트 생성을 통해 테스트 시간을 단축하고, 사전 단계에서 사양 불일치를 발견하여 현장 디버깅 시간을 줄인다.
- **Core Technology Stack**: Python, PySide6, asyncio, pandas, openpyxl, PyInstaller, pymcprotocol을 사용하여 Windows 데스크톱 애플리케이션을 개발한다.
- **Key Technical Objectives**: 테스트 시간 50% 단축, 사전 단계에서 사양 불일치 발견률 100%, 결과 리포트 자동 생성. 이벤트 처리 지연 100ms 이하.
- **Critical Technical Assumptions**: PLC는 Mitsubishi Ethernet 프로토콜을 사용하며, 테스트 실행 PC는 인터넷 연결이 가능하고, MES 수집 서버의 테스트용 엔드포인트가 사전에 설정되어 있어야 한다.

## 2. Tech Stack

| Category          | Technology / Library        | Reasoning (Why it's chosen for this project) |
| ----------------- | --------------------------- | -------------------------------------------- |
| 언어               | Python                      | 생산성, 풍부한 라이브러리, 데스크톱 앱 개발에 적합. |
| UI 프레임워크       | PySide6                     | Qt 기반의 크로스 플랫폼 UI 프레임워크, Windows 데스크톱 앱 개발에 용이. |
| 비동기 프로그래밍  | asyncio                     | PLC 통신 및 UI 업데이트를 효율적으로 처리하기 위한 비동기 프로그래밍 지원. |
| 데이터 처리        | pandas                      | 테스트 결과 데이터 처리 및 리포트 생성에 유용. |
| 엑셀 처리          | openpyxl                    | Excel 리포트 생성을 위한 라이브러리. |
| 실행 파일 생성      | PyInstaller                 | Python 코드를 Windows 실행 파일(.exe)로 패키징. |
| PLC 통신           | pymcprotocol                | Mitsubishi PLC 통신을 위한 라이브러리. |

## 3. System Architecture Design

### Top-Level building blocks
- **UI (PySide6)**:
  - 사용자 인터페이스 제공 (메인 화면, 시나리오 선택, 결과 표시).
  - 사용자 입력 처리 및 결과 시각화.
- **PLC 통신 모듈 (pymcprotocol, asyncio)**:
  - Mitsubishi PLC와 통신을 설정하고 데이터를 송수신.
  - 비동기 방식으로 PLC와 통신하여 UI 응답성을 유지.
- **테스트 시나리오 실행 엔진 (Python, asyncio)**:
  - 정의된 시나리오에 따라 PLC 통신을 제어하고 테스트를 실행.
  - 각 이벤트의 Pass/Fail 여부를 판정.
- **데이터 처리 및 리포트 생성 모듈 (pandas, openpyxl)**:
  - 테스트 결과를 수집하고 분석하여 리포트 생성.
  - PDF 및 Excel 형식으로 리포트 내보내기.
- **로그 관리 모듈 (Python)**:
  - 테스트 로그를 기록하고 압축하여 업로드.
  - 로컬 저장 및 자동 삭제 기능 제공.
- **설정 관리 모듈 (Python)**:
  - PLC 통신 파라미터 (IP, Port) 설정 및 연결 테스트 기능 제공.
- **업데이트 모듈**:
  - 프로그램 자동 업데이트 확인 및 설치.

### Top-Level Component Interaction Diagram

```mermaid
graph TD
    A[UI (PySide6)] --> B[PLC 통신 모듈 (pymcprotocol, asyncio)]
    A --> C[테스트 시나리오 실행 엔진 (Python, asyncio)]
    C --> B
    C --> D[데이터 처리 및 리포트 생성 모듈 (pandas, openpyxl)]
    C --> E[로그 관리 모듈 (Python)]
    A --> F[설정 관리 모듈 (Python)]
    A --> G[업데이트 모듈]
```

- UI (PySide6)는 사용자 입력을 받아 PLC 통신 모듈, 테스트 시나리오 실행 엔진, 설정 관리 모듈과 상호 작용합니다.
- 테스트 시나리오 실행 엔진은 PLC 통신 모듈을 통해 PLC와 통신하며, 결과를 데이터 처리 및 리포트 생성 모듈과 로그 관리 모듈로 전달합니다.
- 설정 관리 모듈은 PLC 통신 파라미터를 설정하고 연결 테스트를 수행합니다.
- 업데이트 모듈은 프로그램 업데이트를 확인하고 설치합니다.

### Code Organization & Convention

**Domain-Driven Organization Strategy**
- **Domain Separation**: PLC 통신, 테스트 시나리오, 리포트 생성, 로그 관리, UI 등의 도메인으로 분리.
- **Layer-Based Architecture**: Presentation Layer (UI), Business Logic Layer (테스트 시나리오 실행), Data Access Layer (PLC 통신, 리포트 생성)로 분리.
- **Feature-Based Modules**: 각 기능별로 모듈을 구성 (예: 시나리오 선택, 리포트 다운로드).
- **Shared Components**: 공통 유틸리티, 타입 정의 등을 shared 모듈에 저장.

**Universal File & Folder Structure**
```
/
├── src/
│   ├── ui/                      # PySide6 UI 관련 코드
│   │   ├── main_window.py       # 메인 윈도우
│   │   ├── scenario_view.py     # 시나리오 상세 화면
│   │   ├── widgets/             # 재사용 가능한 위젯
│   │   │   ├── ...
│   │   ├── resources/           # UI 리소스 (이미지, 스타일시트)
│   ├── plc/                     # PLC 통신 관련 코드
│   │   ├── plc_client.py        # PLC 클라이언트
│   │   ├── protocol.py          # 통신 프로토콜 정의
│   ├── scenario/                # 테스트 시나리오 관련 코드
│   │   ├── scenario_runner.py   # 시나리오 실행 엔진
│   │   ├── scenarios/          # 시나리오 정의 파일
│   │   │   ├── common/
│   │   │   ├── normal/
│   │   │   ├── abnormal/
│   ├── report/                  # 리포트 생성 관련 코드
│   │   ├── report_generator.py  # 리포트 생성기
│   │   ├── templates/           # 리포트 템플릿
│   ├── log/                     # 로그 관리 관련 코드
│   │   ├── logger.py            # 로깅 모듈
│   │   ├── log_uploader.py      # 로그 업로더
│   ├── config/                  # 설정 관리 관련 코드
│   │   ├── config_manager.py    # 설정 관리자
│   ├── utils/                   # 유틸리티 함수
│   │   ├── ...
├── tests/                     # 유닛 테스트
├── requirements.txt           # 의존성 패키지 목록
├── setup.py                   # 설치 스크립트
├── main.py                    # 프로그램 시작점
```

### Data Flow & Communication Patterns
- **Client-Server Communication**: UI와 PLC 통신 모듈 간의 API 요청/응답 패턴.
- **Database Interaction**: 데이터베이스 사용하지 않음. 설정 파일 및 로그 파일에 데이터 저장.
- **External Service Integration**: SFTP/HTTP를 통한 로그 업로드.
- **Real-time Communication**: asyncio를 사용하여 PLC로부터 실시간 이벤트 스트림 처리.
- **Data Synchronization**: 테스트 결과 데이터는 메모리에 저장되며, 리포트 생성 시 파일로 저장.

## 4. Performance & Optimization Strategy

- PLC 통신은 asyncio를 사용하여 비동기적으로 처리하여 UI 응답성을 유지한다.
- 데이터 처리 및 리포트 생성 시 pandas를 사용하여 효율적인 데이터 처리 및 분석을 수행한다.
- UI 업데이트는 필요한 부분만 갱신하여 성능 저하를 최소화한다.
- 로그 파일은 일정 기간 후 자동 삭제하여 디스크 공간을 관리한다.

## 5. Implementation Roadmap & Milestones

### Phase 1: Foundation (MVP Implementation)
- **Core Infrastructure**: 프로젝트 설정, 기본 UI 레이아웃, PLC 통신 모듈 구현.
- **Essential Features**: 시나리오 타입 선택, 시나리오 목록 표시, PLC IP/Port 입력 및 연결 테스트 기능 구현.
- **Basic Security**: PLC 통신 암호화 (필요 시).
- **Development Setup**: 개발 환경 설정, CI/CD 파이프라인 구축.
- **Timeline**: 2주

### Phase 2: Feature Enhancement
- **Advanced Features**: 시나리오 상세 화면, 실시간 이벤트 대시보드, 리포트 생성, 로그 압축 및 업로드 기능 구현.
- **Performance Optimization**: 이벤트 처리 지연 최소화, 리포트 생성 속도 향상.
- **Enhanced Security**: SFTP/HTTPS를 통한 안전한 로그 업로드.
- **Monitoring Implementation**: 시스템 모니터링 및 로깅 설정.
- **Timeline**: 4주

## 6. Risk Assessment & Mitigation Strategies

### Technical Risk Analysis
- **Technology Risks**: asyncio 및 pymcprotocol 사용의 복잡성, PySide6 UI 개발의 어려움.
- **Performance Risks**: PLC 통신 지연, UI 렌더링 성능 저하.
- **Security Risks**: PLC 통신 데이터 보안, 로그 업로드 시 보안 취약점.
- **Integration Risks**: MES 시스템과의 연동 문제, PLC 프로토콜 호환성 문제.
- **Mitigation Strategies**: asyncio 및 pymcprotocol 사용법 학습, PySide6 전문가 자문, 성능 테스트 및 최적화, 보안 프로토콜 적용, MES 시스템 연동 테스트 수행, PLC 프로토콜 호환성 확인.

### Project Delivery Risks
- **Timeline Risks**: 개발 일정 지연, 예상치 못한 기술적 문제 발생.
- **Resource Risks**: 개발 인력 부족, 기술 전문가 확보 어려움.
- **Quality Risks**: 코드 품질 저하, 테스트 부족으로 인한 버그 발생.
- **Deployment Risks**: 배포 환경 문제, 설치 문제.
- **Contingency Plans**: 개발 일정 조정, 추가 인력 투입, 코드 리뷰 및 테스트 강화, 배포 환경 사전 점검, 설치 매뉴얼 제공.
