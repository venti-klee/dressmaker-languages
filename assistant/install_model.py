import os
from pathlib import Path
import sys

target = {"zh-CN": "zh", "ja": "ja", "ko": "ko", "fr": "fr", "de": "de", "es": "es"}[sys.argv[1]]
models = Path(sys.argv[2]).resolve()
models.mkdir(parents=True, exist_ok=True)
os.environ["ARGOS_PACKAGES_DIR"] = str(models)
import argostranslate.package

argostranslate.package.update_package_index()
packages = argostranslate.package.get_available_packages()
package = next((p for p in packages if p.from_code == "en" and p.to_code == target), None)
if package is None:
    raise RuntimeError("当前 Argos 模型索引中没有英语到此语言的直译模型")
argostranslate.package.install_from_path(package.download())
print("已安装英语到 %s 的离线模型" % target)
