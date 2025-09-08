@echo off
chcp 65001 >nul
echo Starting Auto Deploy...
git add .
git commit -m "Auto update"
git push
echo Deploy Complete!
echo Check your website in a few minutes.
pause
