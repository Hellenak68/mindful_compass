@echo off
echo 새 프로젝트 Git 자동화 설정 중...

REM .vscode 폴더 생성
mkdir .vscode 2>nul

REM tasks.json 생성
echo { > .vscode\tasks.json
echo     "version": "2.0.0", >> .vscode\tasks.json
echo     "tasks": [ >> .vscode\tasks.json
echo         { >> .vscode\tasks.json
echo             "label": "Git 자동 배포", >> .vscode\tasks.json
echo             "type": "shell", >> .vscode\tasks.json
echo             "command": "git add . && git commit -m \"자동 업데이트\" && git push", >> .vscode\tasks.json
echo             "group": "build", >> .vscode\tasks.json
echo             "presentation": { >> .vscode\tasks.json
echo                 "echo": true, >> .vscode\tasks.json
echo                 "reveal": "always" >> .vscode\tasks.json
echo             } >> .vscode\tasks.json
echo         } >> .vscode\tasks.json
echo     ] >> .vscode\tasks.json
echo } >> .vscode\tasks.json

REM auto-deploy.bat 생성
echo @echo off > auto-deploy.bat
echo echo 자동 Git 배포 시작... >> auto-deploy.bat
echo git add . >> auto-deploy.bat
echo git commit -m "자동 업데이트 %%date%% %%time%%" >> auto-deploy.bat
echo git push >> auto-deploy.bat
echo echo 배포 완료! 웹사이트가 곧 업데이트됩니다. >> auto-deploy.bat
echo pause >> auto-deploy.bat

echo 설정 완료! auto-deploy.bat 파일을 더블클릭하여 사용하세요.
pause
