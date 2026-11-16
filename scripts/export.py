"""Export a GitHub Pages-ready project. Never include credentials or Site identity."""
import shutil,zipfile,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'exports';OUT.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
 stage=Path(temp)
 shutil.copytree(ROOT/'dist',stage,dirs_exist_ok=True)
 for name in ['AGENTS.md','README.md','CHANGELOG.md','SUBMISSION.md']:
  shutil.copyfile(ROOT/name,stage/name)
 for name in ['content','data','scripts','src','templates','evidence']:
  shutil.copytree(ROOT/name,stage/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 zip_path=OUT/'Basketball_Playbook_Project.zip'
 with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(stage.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(stage))
print(zip_path)
