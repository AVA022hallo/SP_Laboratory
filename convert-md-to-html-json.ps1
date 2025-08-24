[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 设置 Markdown 文件夹路径和输出文件夹路径
$mdDir = "D:\WorkProject\NodejsProject\markdown\john\md"
$outputDir = "D:\WorkProject\NodejsProject\markdown\john\html_output"

# 如果输出文件夹不存在，则创建
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# 获取所有的 Markdown 文件
$mdFiles = Get-ChildItem -Path $mdDir -Filter *.md

# 初始化一个空的数组，用于存储结果
$jsonArray = @()

foreach ($file in $mdFiles) {
    $mdPath = $file.FullName
    # 去除文件名中的 '#' 符号并生成对应的 HTML 文件路径
    $htmlPath = Join-Path $outputDir (($file.BaseName -replace '#', '') + ".html")

    # 使用 npx markdown-it 命令将 Markdown 文件转换为 HTML 文件
    npx markdown-it $mdPath -o $htmlPath

    # 确保 HTML 文件已经生成
    if (Test-Path $htmlPath) {
        # 读取 Markdown 内容和 HTML 内容
        $mdContent = Get-Content $mdPath -Raw
        $htmlContent = Get-Content $htmlPath -Raw

        # 将文件名、Markdown 内容和 HTML 内容存储到 JSON 数组中
        $jsonArray += [PSCustomObject]@{
            filename = $file.Name
            content  = $mdContent
            html     = $htmlContent
        }
    } else {
        Write-Host "警告: 生成 HTML 文件失败 '$htmlPath'"
    }
}

# 将 JSON 数组转换为 JSON 格式并保存到 output.json 文件
$jsonArray | ConvertTo-Json -Depth 3 | Set-Content "output.json" -Encoding UTF8

Write-Host "完成！HTML 文件已生成在 '$outputDir'，JSON 文件为 'output.json'"
