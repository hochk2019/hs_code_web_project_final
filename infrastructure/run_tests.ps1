param(
    [switch]$SkipFrontend
)

Write-Host "==> Cài đặt môi trường backend" -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -e backend[dev]

Write-Host "==> Chạy Ruff" -ForegroundColor Cyan
python -m ruff check backend/app

Write-Host "==> Chạy pytest" -ForegroundColor Cyan
pytest backend/tests

if (-not $SkipFrontend) {
    Write-Host "==> Cài đặt frontend" -ForegroundColor Cyan
    pushd frontend
    npm install
    Write-Host "==> Chạy lint Next.js" -ForegroundColor Cyan
    npm run lint
    Write-Host "==> Chạy kiểm thử frontend" -ForegroundColor Cyan
    npm run test
    popd
}
