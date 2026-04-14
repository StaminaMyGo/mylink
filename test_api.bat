@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set BASE_URL=http://127.0.0.1:8000

echo.
echo ==============================
echo   FastAPI 接口测试
echo ==============================
echo.

echo [测试 1] 根路径
curl -s %BASE_URL%/
echo.
echo.

echo [测试 2] 路径参数
curl -s "%BASE_URL%/items/1?q=test"
echo.
echo.

echo [测试 3] 搜索功能
curl -s "%BASE_URL%/search?q=keyword^&page=2"
echo.
echo.

echo [测试 4] 创建商品 (POST JSON)
curl -s -X POST "%BASE_URL%/items" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"测试商品\",\"price\":99.9,\"tax\":10.0}"
echo.
echo.

echo [测试 5] 用户登录 (表单提交)
curl -s -X POST "%BASE_URL%/login" ^
  -F "username=admin" ^
  -F "password=123456"
echo.
echo.

echo ==============================
echo   所有测试完成！
echo ==============================
pause
