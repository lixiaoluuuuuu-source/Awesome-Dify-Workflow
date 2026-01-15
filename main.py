# 需求：Python 编写「飞行生活记录与决策助手」智能体
# 核心功能清单：
1. 飞行记录管理：支持录入航班号、起降机场、起降时间、航空公司、舱位、里程，数据保存到仓库的 flight_records.json 文件；支持查询历史记录
2. 行程卡生成：根据单条飞行记录，生成带二维码的行程卡图片（二维码包含航班关键信息），保存到 flight_cards 文件夹
3. 机票价格监控：输入出发地、目的地、出行日期，调用机票价格查询接口（用 requests 库），从 GitHub Secrets 获取 FLIGHT_API_KEY，每天定时查询并对比价格，价格下跌时记录降价提醒
4. 飞行数据统计：按年度/月度统计飞行次数、总里程、航司偏好、舱位分布，生成统计报告
5. 飞行成就解锁：预设成就规则（如首次国际飞行、年度飞行≥10次解锁「飞行达人」、累计里程≥10000公里解锁「长途旅人」），录入记录时自动判断并解锁，成就信息保存到 achievements.json
# 技术要求：
- 敏感信息（FLIGHT_API_KEY、COOKIE）从环境变量读取，不硬编码
- 依赖库写入 requirements.txt（需包含 requests、pillow、qrcode、python-dotenv）
- 代码加注释，方便调试
- 处理异常（如文件不存在、API 调用失败、二维码生成失败）
# 第一步：替换为你的 GitHub 用户名和新仓库名
GITHUB_USERNAME="lixiaoluuuuu-sourc"
REPO_NAME=".github/workflows/flight-agent.yml"

# 第二步：初始化仓库（若已初始化则跳过此步，不会影响）
git init

# 第三步：添加所有代码文件（包括main.py、requirements.txt等）
git add .

# 第四步：提交代码（备注可自定义）
git commit -m "Initial commit: 飞行生活记录与决策助手智能体代码"

# 第五步：关联新仓库并推送（强制关联避免远程仓库冲突）
git remote rm origin 2>/dev/null
git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git
git push -u origin main -f

