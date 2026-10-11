# Dressmaker Languages 수동 설치

먼저 [Mac용 Yuuma ModLoader](https://www.nexusmods.com/dressmaker/mods/1?tab=files)를 설치하세요. 이 ZIP에는 독립 번역 패치만 있으며 로더, 게임, 원단 Mod는 없습니다.

1. 게임을 완전히 종료합니다.
2. ZIP을 풉니다. 도우미에서 내보낸 ZIP에는 **저장된 게임 언어**, 현재 사전, 캐시와 수동 수정이 포함됩니다. 언어 변경을 먼저 저장하세요. GitHub 기본 수동 패키지는 간체 중국어이며 프로젝트에서 직접 작성한 기본 사전만 포함합니다.
3. Steam에서 게임을 오른쪽 클릭하고 관리 → 로컬 파일 보기를 선택합니다. 기존 `BepInEx`가 있는 게임 루트를 사용하며 `Dressmaker.app/Contents`에는 넣지 않습니다.
4. ZIP의 `BepInEx/plugins/DressmakerLanguages`를 게임의 `BepInEx/plugins`로 복사합니다.
5. ZIP의 `BepInEx/config/DressmakerLanguages`를 게임의 `BepInEx/config`로 복사합니다. `config`가 없으면 만드세요. **두 하위 폴더를 각각 복사하고 BepInEx 전체를 교체하지 마세요.**
6. 같은 이름의 기존 폴더가 있으면 다른 곳에 백업한 뒤 두 `DressmakerLanguages`만 교체합니다. 다른 플러그인이나 Mod는 유지합니다.
7. 게임을 다시 시작합니다.

필요한 경로 (`LANG`은 `zh-CN`, `ja`, `fr` 등의 내보낸 언어):

```text
BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll
BepInEx/config/DressmakerLanguages/runtime.json
BepInEx/config/DressmakerLanguages/known-sources.json
BepInEx/config/DressmakerLanguages/translations.LANG.json
```

Finder가 권한을 요청하면 macOS 안내를 따르세요. 복사가 안 되면 게임 폴더의 정보 가져오기 → 공유 및 사용 권한에서 본인 계정의 읽기 및 쓰기 권한을 확인하세요. 모든 사용자에게 권한을 주지 마세요. 관리 장치라면 권한이 있는 계정이 필요할 수 있습니다.

수동 복사는 도우미 쓰기 권한을 해결하지 않습니다. 스캔, 번역과 로컬 캐시 저장은 계속 가능합니다. 권한을 해결할 때까지 새 번역이나 게임 언어 변경 후 다시 내보내고, 게임 종료 후 복사하세요. 게임도 설정 폴더에 쓸 수 없다면 실행 중 새 단어 수집이 실패할 수 있지만 Mod의 일반 JSON 표시 필드는 도우미로 스캔할 수 있습니다. 도우미 재시작 시 플러그인과 설정을 모두 확인합니다.

제거하려면 게임 종료 후 두 `DressmakerLanguages` 폴더만 옮기세요. 번역을 보관하려면 도우미의 `data`를 남겨 두세요.

로컬 ZIP에는 개인 Mod 이름, 수정과 게임의 기존 번역이 포함될 수 있습니다. 공개 배포는 프로젝트 패키징 도구가 만든 기본 수동 패키지를 사용하세요.

0.1.2은 초기 버전이며 게임 내 표시와 글꼴은 미검증입니다. [전체 안내와 감사의 말](https://github.com/venti-klee/dressmaker-languages).
