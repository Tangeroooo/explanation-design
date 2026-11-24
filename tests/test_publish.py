"""Exercise failure classification and no-rewrite behavior with isolated command fakes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
FAKE='''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
tool=Path(sys.argv[0]).name
args=sys.argv[1:]
with open(os.environ['COMMAND_LOG'],'a') as f:f.write(json.dumps([tool,*args])+'\\n')
mode=os.environ['CASE_MODE']
if tool=='gh':
    if args[:2]==['api','user']:
        if mode=='auth-network':print('error connecting to api.github.com',file=sys.stderr);sys.exit(1)
        print('SomeoneElse' if mode=='wrong-account' else 'Tangeroooo')
    elif args[:2]==['api','repos/Tangeroooo/explanation-design']:
        if mode=='lookup-network':print('DNS lookup failed',file=sys.stderr);sys.exit(1)
        if mode in ('absent','owned-list-fails') and not Path(os.environ['COMMAND_LOG']+'.created').exists():
            print('gh: Not Found (HTTP 404)',file=sys.stderr);sys.exit(1)
        print(json.dumps({'default_branch':'main','visibility':'public'}))
    elif args and args[0]=='api' and args[1].startswith('user/repos'):
        if mode=='owned-list-fails':print('connection reset',file=sys.stderr);sys.exit(1)
    elif args[:2]==['repo','create']:
        Path(os.environ['COMMAND_LOG']+'.created').write_text('created')
        print('created')
    else:print('{}')
elif tool=='git':
    if args[:3]==['remote','get-url','origin'] or args[:5]==['remote','get-url','--push','--all','origin']:
        print('https://github.com/Other/other.git' if mode=='wrong-origin' else 'https://github.com/Tangeroooo/explanation-design.git')
    elif args==['branch','--show-current']:print('main')
    elif args[:2]==['ls-remote','--heads']:
        if mode=='diverged':print('abc123 refs/heads/main')
    elif args[:2]==['merge-base','--is-ancestor']:
        sys.exit(1 if mode=='diverged' else 0)
    elif args[:3]==['diff','--cached','--quiet']:sys.exit(0)
'''


class PublishTests(unittest.TestCase):
    def run_case(self,mode):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'.git').mkdir()
            (root/'scripts').mkdir()
            shutil.copy2(ROOT/'scripts/publish-github.sh',root/'scripts/publish-github.sh')
            (root/'scripts/check.py').write_text('print("isolated checks stub")')
            commands=root/'bin'
            commands.mkdir()
            for name in ('gh','git'):
                p=commands/name
                p.write_text(FAKE)
                p.chmod(0o755)
            log=root/'commands.jsonl'
            env={**os.environ,'PATH':str(commands)+os.pathsep+os.environ['PATH'],'COMMAND_LOG':str(log),'CASE_MODE':mode}
            result=subprocess.run(['bash',str(root/'scripts/publish-github.sh')],env=env,text=True,capture_output=True)
            calls=[json.loads(x) for x in log.read_text().splitlines()]
            return result,calls

    def test_auth_and_lookup_errors_never_create_or_push(self):
        for mode in ('auth-network','wrong-account','lookup-network','owned-list-fails','wrong-origin','diverged'):
            with self.subTest(mode=mode):
                result,calls=self.run_case(mode)
                self.assertNotEqual(result.returncode,0,result.stdout)
                self.assertFalse(any(c[:3] in (['gh','repo','create'],['gh','repo','edit']) for c in calls))
                self.assertFalse(any('push' in c or 'commit' in c or 'add' in c for c in calls))

    def test_explicit_absence_and_existing_repo_both_use_non_force_push(self):
        for mode in ('absent','exists'):
            result,calls=self.run_case(mode)
            self.assertEqual(result.returncode,0,result.stderr)
            pushes=[c for c in calls if c[0]=='git' and 'push' in c]
            self.assertEqual(len(pushes),1)
            self.assertNotIn('--force',pushes[0])
            self.assertEqual(any(c[:3]==['gh','repo','create'] for c in calls),mode=='absent')


if __name__=='__main__':unittest.main()
