const fs = require("fs");
const path = require("path");
const cheerio = require("cheerio");

const folderPath = "D:/WorkProject/NodejsProject/Pesonal_blog_V1.3/pages/jhnotes";  // HTML 文件所在目录
const jsonOutputPath = "D:/WorkProject/NodejsProject/Pesonal_blog_V1.3/pages/jhnotes/output.json";  // 输出的 JSON 文件路径

let articles = [];

// 递归遍历文件夹，读取所有 HTML 文件
function walkDir(dir) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      walkDir(fullPath);  // 递归子目录
    } else if (file.endsWith(".html")) {
      parseHtml(fullPath, stat.mtime);  // 传递文件的修改时间
    }
  });
}

// 解析 HTML 文件
function parseHtml(filePath, lastModified) {
  const content = fs.readFileSync(filePath, "utf-8");
  const $ = cheerio.load(content);

  const title = $("h1").text().trim();  // 获取 <h1> 标签中的标题

  // 格式化文件的修改时间为 YYYY-MM-DD
  const date = formatDate(lastModified);

  let description = "";
  $("p").each((i, elem) => {
    description += $(elem).text().trim() + " ";
  });

  description = description.replace(/\s+/g, " ").trim();
  if (description.length > 200) description = description.slice(0, 200);  // 限制描述长度

  // 如果没有描述，保留为空字符串，而不是跳过
  description = description || "";

  const relativePath = path.relative(path.dirname(jsonOutputPath), filePath).replace(/\\/g, "/");
  const url = `../jhnotes/${relativePath}`;

  articles.push({
    date,
    title,
    url,
    description
  });
}

// 格式化日期为 YYYY-MM-DD
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// 生成 JSON 文件
function generateJson() {
  if (articles.length > 0) {
    const outputData = JSON.stringify(articles, null, 2);
    fs.writeFileSync(jsonOutputPath, outputData, "utf-8");
    console.log(`已生成 ${articles.length} 条文章信息到 ${jsonOutputPath}`);
  } else {
    console.log("没有找到任何文章信息，JSON 文件未生成。");
  }
}

// 启动文件解析
walkDir(folderPath);
generateJson();
