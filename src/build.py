import argparse
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description="Compile against your local game assemblies")
parser.add_argument("--game", required=True)
parser.add_argument("--dotnet", default="dotnet")
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
game = Path(args.game).expanduser().resolve()
sdk = subprocess.check_output([args.dotnet, "--list-sdks"], text=True).strip().splitlines()[-1]
version, folder = sdk.split(" [")
compiler = Path(folder.rstrip("]")) / version / "Roslyn/bincore/csc.dll"
managed = game / "Dressmaker.app/Contents/Resources/Data/Managed"
if not managed.is_dir():
    managed = game / "Dressmaker_Data/Managed"
output = root / "BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll"
output.parent.mkdir(parents=True, exist_ok=True)
references = list(managed.glob("*.dll")) + [game / "BepInEx/core/BepInEx.dll", game / "BepInEx/core/0Harmony.dll"]
lines = ["/nologo", "/target:library", "/nostdlib+", "/optimize+", '/out:"%s"' % output]
lines += ['/reference:"%s"' % file for file in references]
lines += ['"%s"' % (root / "src/DressmakerLanguages.cs")]
with tempfile.TemporaryDirectory() as temp:
    rsp = Path(temp) / "compile.rsp"
    rsp.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run([args.dotnet, str(compiler), "@" + str(rsp)], check=True)
print("Built " + str(output))
