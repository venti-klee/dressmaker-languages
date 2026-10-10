# Dressmaker · Mod 다국어 도우미

[简体中文](README.zh-CN.md) · [English](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Yuuma ModLoader 화면과 Mod의 영어 표시 텍스트를 번역하는 독립 macOS 도구입니다. **0.1.1은 초기 버전이며 게임 안에서의 통합 동작은 아직 검증하지 않았습니다.**

## 기능

- 게임 번역 대상과 도우미 화면 언어를 각각 설정합니다. 중국어, 영어, 일본어, 한국어, 프랑스어, 독일어, 스페인어를 지원합니다.
- 사전, 수동 수정, 캐시를 오프라인으로 사용하고 선택적으로 Argos 모델을 설치할 수 있습니다.
- 키가 없는 MyMemory, 실험적 Bing 웹 연동, 사용 가능한 LibreTranslate 인스턴스를 선택합니다.
- 새 Mod의 일반적인 JSON 표시 항목을 스캔하고 게임에 나타나는 알 수 없는 영어를 수집합니다.
- 대상 언어별 캐시, 수동 수정 우선 적용, 변수와 서식 태그 보호를 제공합니다.

## 플레이어 시작하기

1. [Yuuma ModLoader Mac 버전](https://www.nexusmods.com/dressmaker/mods/1?tab=files)을 먼저 설치하세요.
2. 저장소 Releases에서 **Dressmaker-Languages-Mac-0.1.1.zip**을 받아 전체 폴더를 압축 해제하세요. Python 3.9 이상이 필요합니다.
3. `Start.command` 또는 `针影裁梦多语言助手.app`을 여세요.
4. 도우미 언어, 게임 폴더와 대상 언어를 확인하고 설정을 저장한 뒤 패치를 설치하고 게임을 재시작하세요.
5. 새 Mod를 설치하면 스캔하세요. 번역하는 동안 도우미를 실행해 두고 결과를 검토하거나 수정하세요.

모델, 제거, 데이터 위치는 [한국어 설명서](docs/ko.md)를 참고하세요. GitHub Download ZIP은 컴파일된 플러그인과 `.app`이 없는 소스입니다. 플레이어는 Release 설치 패키지를 사용하세요.

## 범위와 검증

`name`, `displayName`, `display_name`, `description`, `tooltip`, `title` 등의 JSON 항목을 읽습니다. 게임에서는 ModLoader의 Unity Text / TextMeshPro와 스캔한 이름을 대상으로 합니다. 자체 화면, 이미지 속 글자, 특수 바이너리와 영어가 아닌 원문은 보장하지 않습니다. 원단 콘텐츠를 추가하거나 게임 전체에 새 언어를 제공하지 않습니다.

ModLoader 0.7.3 / BepInEx 5.4.23.5 / Unity 6000.3.4f1에서 빌드했으며 자동 테스트 25개를 통과했습니다. 로컬 화면의 언어 전환을 확인했고 Bing과 MyMemory에서 실제 번역을 받았습니다. 웹 연동은 네트워크, 제한, 페이지 변경으로 실패할 수 있습니다. 외부 원단 이름, 게임 내 배치와 글꼴은 검증이 필요합니다.

온라인 모드에서는 미번역 영어 표시를 선택한 서비스에 보냅니다. 요청 간격은 최소 3초이며 기본 일일 한도는 UTF-8 4,500바이트입니다. 실패하면 원문을 유지합니다. MyMemory 대체 옵션은 기본적으로 꺼져 있으며 켜면 두 시도 모두 한도에 포함합니다. 기존 사전과 캐시는 오프라인에서 사용할 수 있습니다.

## 개발과 기여

소스는 `src/`와 `assistant/`에 있습니다. 기본 도우미는 Python 표준 라이브러리만 사용합니다.

```sh
python3 -m unittest discover -s tests -v
```

플러그인을 빌드하려면 자신의 게임과 ModLoader 어셈블리, .NET SDK가 필요합니다. 도우미는0.1.1이며 변경되지 않은 게임 플러그인 내부 버전은0.1.0입니다. GitHub Actions는 설정했지만 원격 실행은 아직 하지 않았습니다.

용어, 글꼴, 호환성 Issue / Pull Request를 환영합니다. 게임, OS, 로더 버전과 공개 가능한 원문을 제공하세요. 화면 문구 수정 시 일곱 언어 사전과 설명서를 함께 갱신하고 저장 파일, 비공개 Mod와 게임 자산은 올리지 마세요.

## GitHub 공개

1. 빈 **Public** 저장소를 만드세요. README와 라이선스는 이미 있으므로 따로 생성하지 마세요.
2. **Dressmaker-Languages-GitHub-0.1.1.zip**을 풀고 내부 내용을 업로드하세요. 루트에 `README.md`가 있어야 하며 `.github/`, `.gitignore`, `.gitattributes`도 포함하세요. Finder에서 `Command + Shift + .`으로 숨김 파일을 볼 수 있습니다. Git으로 올리면 실행 스크립트 권한이 유지됩니다.
3. `v0.1.1` Release를 만들고 Mac 패키지를 첨부하세요. 소스는 저장소용이고 Mac 패키지는 플레이어용입니다.
4. 공개 전에 본인 게임에서 확인하고 검증 내용을 갱신하세요. 개인 데이터, 경로, 토큰, Git 기록은 패키지에서 제외했습니다. 

정확한 파일 목록은 `UPLOAD-MANIFEST.json`에 있습니다. 아래에 GitHub 공식 공개 방법 링크가 있습니다.

GitHub 공식 안내: [Create repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) · [Create Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

## 출처와 라이선스

[SallyHCA 도구의 공개 기능](https://www.nexusmods.com/dressmaker/mods/339)을 참고해 독립 구현했습니다. 해당 코드, 사전, 자산은 포함하지 않습니다. 독립 코드와 작성한 사전은 [MIT](LICENSE)이며 게임이나 참고 프로젝트 자산의 권리를 부여하지 않습니다. 게임, Nexus Mods, Microsoft, Argos와 공식 관계가 없습니다.

## 감사의 말

이 프로젝트의 기반이 된 제작자와 팀에 감사드립니다.

- [Cozy Lives (개발)와 Free Lives (배급)](https://store.steampowered.com/app/4019220/Dressmaker/) — 플레이어가 직접 옷을 디자인하고 재단하고 바느질할 수 있는 Dressmaker를 만들어 주셔서 감사합니다.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — 커뮤니티가 원단과 액세서리를 만들 수 있도록 로더와 커스텀 콘텐츠 지원을 제공해 주셔서 감사합니다.
- [SallyHCA — 자동 중국어 번역 도구](https://www.nexusmods.com/dressmaker/mods/339) — Mod 관리자와 콘텐츠 이름을 번역하는 방법을 공개해 주셔서 감사합니다. 도구와 공개 설명이 이 프로젝트의 번역 흐름에 영감을 주었습니다.

이 프로젝트는 독립 구현이며 감사 표기는 원작자의 보증을 뜻하지 않습니다. 해당 프로그램, 사전, 게임 자산과 모델은 이 패키지에 재배포하지 않습니다.
