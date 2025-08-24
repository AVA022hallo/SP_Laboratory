import os
from bs4 import BeautifulSoup

# 设置目标文件夹路径
html_output_dir = r'D:\WorkProject\NodejsProject\markdown\john\html_output'
output_copy_dir = r'D:\WorkProject\NodejsProject\markdown\john\html_output_copy'

# 如果目标文件夹不存在，则创建
if not os.path.exists(output_copy_dir):
    os.makedirs(output_copy_dir)

# 定义HTML模板
html_template = '''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个人博客 - 关于我</title>

    <!-- 引入主样式 -->
    <link rel="stylesheet" href="../../css/main.css">

    <!-- 引入布局样式 -->
    <link rel="stylesheet" href="../../css/layout.css">

    <!-- 引入主题样式 -->
    <link rel="stylesheet" href="../../css/theme.css">

    <!-- 引入about样式 -->
    <link rel="stylesheet" href="jhnotes.css"> 
</head>
<body>
    <!-- 动态加载头部 -->
    <div id="header"></div>

    <div class="container">
        <!-- 动态加载侧边栏 -->
        <div id="sidebar"></div>
        <!-- 主页内容 -->
        <main>
            <h1>{filename}</h1>
            {content}
        </main>
    </div>

    <!-- 动态加载尾部 -->
    <div id="footer"></div>

    <script>
        // 加载头部
        fetch('../partials/header.html')
            .then(response => response.text())
            .then(data => document.getElementById('header').innerHTML = data);

        // 加载侧边栏
        fetch('../partials/sidebar.html')
            .then(response => response.text())
            .then(data => document.getElementById('sidebar').innerHTML = data);

        // 加载尾部
        fetch('../partials/footer.html')
            .then(response => response.text())
            .then(data => document.getElementById('footer').innerHTML = data);
    </script>
</body>
</html>
'''

# 遍历指定目录中的所有HTML文件
for filename in os.listdir(html_output_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(html_output_dir, filename)

        # 去掉文件名中的 .html 后缀
        base_filename = filename.replace('.html', '')

        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取HTML文件内容
            file_content = file.read()

            # 查找最后一个 <p>&gt; 标签的位置
            last_p_gt_index = file_content.rfind('<p>&gt;')

            # 查找最后一个 # 符号的位置
            last_hash_index = file_content.rfind('#')

            # 找到从哪个位置开始复制内容
            start_index = max(last_p_gt_index, last_hash_index)

            # 查找 <p><em> 标签的位置
            end_index = file_content.find('<p><em>')

            # 如果找到了 <p><em> 标签，则设置结束位置为该标签的开始位置
            if end_index != -1:
                file_content = file_content[start_index:end_index]
            else:
                # 如果没有找到 <p><em>，则复制到文件末尾
                file_content = file_content[start_index:]

            # 去除所有的 * 符号
            file_content = file_content.replace('*', '')

            # 将文件名作为 <h1> 标题，插入到模板中的 {filename}
            final_html = html_template.format(filename=base_filename, content=file_content)

        # 将修改后的文件保存到新的目录
        new_file_path = os.path.join(output_copy_dir, filename)
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(final_html)

        print(f"处理文件: {filename} 完成")
