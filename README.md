# General

대한민국 국가 Plug and Charge(PnC) 인프라 구축을 위한 REST API 표준 명세 프로젝트입니다. 본 프로젝트는 ISO 15118 및 VDE-AR-E 2802-100-1 표준을 기반으로 설계되었으며, 국내 PnC 생태계의 상호운용성을 보장하기 위한 기술 표준을 정의합니다.

## 📁 프로젝트 구조

```
.
├── README.md           # 프로젝트 개요 및 가이드
├── api/                # API 명세 모듈
│   ├── openapi.yaml    # REST API 명세
│   ├── redocly.yaml    # Redocly 설정
│   ├── .spectral.mjs   # API 품질 관리 린팅 규칙
│   └── .redocly.lint-ignore.yaml # 린팅 예외 설정
└── opnc/                # 글로벌 레퍼런스 규격 (참조용 - 별도 배포)
```

## 주요 도구 및 사용법

본 명세서를 시각화하거나 문서화하기 위해 다음 명령어를 사용합니다 (Node.js 및 npx 환경 필요).

### 1. API 명세 린팅
정의된 규칙에 따라 API 설계 정합성을 검사합니다.
```bash
npx @redocly/cli lint api/openapi.yaml --config api/redocly.yaml
```

**[참고] 엄격한 표준 규격 및 보안 스코프 검증**
실제 배포(Production) 전, 타사 도구 체인과의 상호운용성 및 보안 정책(OAuth2 Scope 등)의 엄격한 검증이 필요한 경우 아래 단계를 수행할 수 있음

- **1단계**: 명세 파일 병합 (4번 명령어 참고)
- **2단계**: 엄격한 Spectral 린팅 실행
  ```bash
  npx @stoplight/spectral-cli lint api/openapi.bundled.yaml --ruleset spectral-strict.yaml
  ```


### 2. 실시간 문서 미리보기
명세 수정 사항을 브라우저에서 실시간으로 확인합니다.
```bash
npx @redocly/cli preview -d api
```

### 3. 정적 HTML 문서 빌드
배포용 HTML 문서를 생성합니다.
```bash
npx @redocly/cli build-docs api/openapi.yaml --output api/index.html && python3 inject_mermaid.py
```

### 4. 명세 파일 병합
분산된 파일들을 하나의 단일 명세 파일로 병합합니다.
```bash
npx @redocly/cli bundle api/openapi.yaml --output api/openapi.bundled.yaml
```

### 5. Markdown 문서 생성
명세서를 문서 보고서(PDF) 형식으로 변환합니다.
npm install -g widdershins 필요.

```bash
widdershins api/openapi.bundled.yaml -o api/openapi.md --language_tabs
```

DOCX로 추가 변환(pandoc 필요):
```
pandoc api/openapi.md -o api/openapi.docx
```
