@echo off
chcp 65001 >nul
echo Setting up Git Auto Deploy for new project...

REM Create .vscode folder
mkdir .vscode 2>nul

REM Create tasks.json
echo { > .vscode\tasks.json
echo     "version": "2.0.0", >> .vscode\tasks.json
echo     "tasks": [ >> .vscode\tasks.json
echo         { >> .vscode\tasks.json
echo             "label": "Git Auto Deploy", >> .vscode\tasks.json
echo             "type": "shell", >> .vscode\tasks.json
echo             "command": "git add . && git commit -m 'Auto update' && git push", >> .vscode\tasks.json
echo             "group": "build", >> .vscode\tasks.json
echo             "presentation": { >> .vscode\tasks.json
echo                 "echo": true, >> .vscode\tasks.json
echo                 "reveal": "always" >> .vscode\tasks.json
echo             } >> .vscode\tasks.json
echo         } >> .vscode\tasks.json
echo     ] >> .vscode\tasks.json
echo } >> .vscode\tasks.json

REM Create deploy.bat
echo @echo off > deploy.bat
echo chcp 65001 ^>nul >> deploy.bat
echo echo Starting Auto Deploy... >> deploy.bat
echo git add . >> deploy.bat
echo git commit -m "Auto update" >> deploy.bat
echo git push >> deploy.bat
echo echo Deploy Complete! >> deploy.bat
echo echo Check your website in a few minutes. >> deploy.bat
echo pause >> deploy.bat

echo Setup Complete! Use deploy.bat file for auto deployment.
pause