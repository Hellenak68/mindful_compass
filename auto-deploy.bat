@echo off
echo 자동 Git 배포 시작...
git add .
git commit -m "자동 업데이트 %date% %time%"
git push
echo 배포 완료! 웹사이트가 곧 업데이트됩니다.
pause
