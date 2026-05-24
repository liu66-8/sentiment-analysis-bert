# 🍜 细粒度餐饮评论情感分析系统 - 一键启动脚本
# PowerShell 版本

$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

$env:HF_ENDPOINT = "https://hf-mirror.com"

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║     🍜  细粒度餐饮评论情感分析系统       ║" -ForegroundColor Cyan
Write-Host "  ║     Sentiment Analysis System           ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 第一步：检查模型文件
Write-Host "  [1/3] 检查模型文件..." -ForegroundColor Yellow
$modelPath = Join-Path $ProjectDir "models\BEST_checkpoint.tar"
if (-not (Test-Path $modelPath)) {
    Write-Host "  [错误] models\BEST_checkpoint.tar 不存在！" -ForegroundColor Red
    Write-Host "  请确保已训练模型或将模型文件放在 models 目录" -ForegroundColor Red
    Read-Host "按回车退出"
    exit 1
}
Write-Host "  [✓] 模型文件已就绪" -ForegroundColor Green

# 第二步：启动后端
Write-Host ""
Write-Host "  [2/3] 启动后端服务..." -ForegroundColor Yellow

$backendProcess = Start-Process -FilePath "python" `
    -ArgumentList "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000" `
    -PassThru `
    -WindowStyle Minimized

Write-Host "  [✓] 后端进程已启动 (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "  [*] 等待后端就绪..." -ForegroundColor Gray

for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    try {
        $null = Invoke-WebRequest -Uri "http://localhost:8000/api/status" -UseBasicParsing -TimeoutSec 2
        Write-Host "  [✓] 后端服务就绪" -ForegroundColor Green
        break
    } catch {
        if ($i -eq 29) {
            Write-Host "  [警告] 后端启动超时，尝试继续..." -ForegroundColor DarkYellow
        }
    }
}

# 第三步：打开浏览器
Write-Host ""
Write-Host "  [3/3] 打开浏览器..." -ForegroundColor Yellow
Start-Process "http://localhost:8000"
Write-Host "  [✓] 浏览器已打开" -ForegroundColor Green

Write-Host ""
Write-Host "  ══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    前端页面: http://localhost:8000" -ForegroundColor White
Write-Host "    API 文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host "    默认账号: admin / admin" -ForegroundColor White
Write-Host "  ══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  按 Ctrl+C 或关闭此窗口停止服务" -ForegroundColor Gray
Write-Host ""

try {
    $backendProcess.WaitForExit()
} finally {
    if (-not $backendProcess.HasExited) {
        Stop-Process -Id $backendProcess.Id -Force
        Write-Host "  后端服务已停止" -ForegroundColor Gray
    }
}
