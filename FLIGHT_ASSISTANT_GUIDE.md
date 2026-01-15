# 飞行生活记录与决策助手 - 使用指南

## 📋 项目概述

这是一个完整的Python飞行智能体系统，支持飞行记录管理、行程卡生成、机票价格监控、飞行数据统计和成就解锁功能。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
FLIGHT_API_KEY=your_api_key_here
FLIGHT_API_URL=https://api.example.com/flights
FLIGHT_COOKIE=your_cookie_here
PRICE_CHECK_INTERVAL_HOURS=24
LOG_LEVEL=INFO
```

### 3. 运行演示

```bash
python flight_assistant.py
```

## 📖 功能说明

### 1️⃣ 飞行记录管理

录入和查询飞行记录。

```python
from flight_assistant import FlightAssistant

assistant = FlightAssistant()

# 添加飞行记录
assistant.add_flight_record(
    flight_number="CA888",
    departure_airport="PEK",      # 起飞机场代码
    arrival_airport="JFK",         # 降落机场代码
    departure_time="2024-01-15T10:30:00",
    arrival_time="2024-01-15T22:30:00",
    airline="Air China",
    cabin_class="Business",
    miles=6850
)

# 查询飞行记录
records = assistant.get_flight_records(airline="Air China", limit=10)

# 查询所有记录
all_records = assistant.get_flight_records()
```

**数据存储：** 所有记录保存在 `flight_records.json`

---

### 2️⃣ 行程卡生成

根据飞行记录生成带二维码的行程卡图片。

```python
# 生成行程卡（包含二维码）
records = assistant.get_flight_records()
if records:
    card_path = assistant.generate_itinerary_card(records[0])
    print(f"行程卡已生成: {card_path}")
```

**特性：**
- 包含航班基本信息
- 二维码编码航班关键信息
- 图片保存在 `flight_cards/` 目录
- 自动异常处理，字体降级支持

---

### 3️⃣ 机票价格监控

监控指定航线的机票价格变化。

```python
# 检查单次价格
price_info = assistant.check_flight_price(
    departure="Beijing",
    arrival="Tokyo",
    travel_date="2024-02-15"
)

# 持续监控价格（记录价格变化）
assistant.monitor_price(
    departure="Beijing",
    arrival="Tokyo",
    travel_date="2024-02-15",
    price_threshold=100  # 仅记录下跌≥100元的情况
)

# 启动定时监控
assistant.start_price_monitoring(
    departure="Beijing",
    arrival="Tokyo",
    travel_date="2024-02-15",
    interval_hours=24
)
```

**说明：**
- API密钥从环境变量 `FLIGHT_API_KEY` 读取
- 价格记录保存在 `price_alerts.json`
- 可配合系统cron或APScheduler实现定时检查

---

### 4️⃣ 飞行数据统计

按年度/月度统计飞行数据并生成报告。

```python
# 统计全年数据
stats = assistant.get_flight_statistics(year=2024)

# 统计某月数据
stats = assistant.get_flight_statistics(year=2024, month=1)

# 统计全部数据
stats = assistant.get_flight_statistics()

# 打印统计报告
assistant.print_statistics_report(stats)
```

**统计指标：**
- 总飞行次数
- 总飞行里程
- 平均每次里程
- 国际/国内航班数
- 航司偏好排名
- 舱位分布

---

### 5️⃣ 飞行成就解锁

自动检测并解锁飞行成就。

```python
# 查看已解锁成就
achievements = assistant.get_achievements()

# 打印成就列表
assistant.print_achievements()
```

**预设成就规则：**

| 成就ID | 成就名称 | 解锁条件 |
|--------|--------|--------|
| `first_international` | 🌍 国际旅行家 | 首次完成国际航班 |
| `frequent_flyer` | ✈️ 飞行达人 | 年度飞行次数≥10次 |
| `long_distance_traveler` | 🚀 长途旅人 | 累计飞行里程≥10000公里 |

**成就数据：** 保存在 `achievements.json`

---

## 📁 文件结构

```
.
├── flight_assistant.py          # 主程序文件
├── requirements.txt             # 依赖库清单
├── .env.example                 # 环境变量模板
├── .env                         # 环境变量（本地，不上传）
├── flight_records.json          # 飞行记录数据
├── achievements.json            # 成就数据
├── price_alerts.json            # 价格监控记录
├── flight_cards/                # 生成的行程卡图片
│   ├── CA888_20260115_121509.png
│   └── MU501_20260115_121509.png
└── flight_assistant.log         # 程序日志
```

---

## 🔐 安全性

### 敏感信息处理

所有敏感信息从**环境变量**读取，不在代码中硬编码：

```python
# ✓ 正确做法
api_key = os.getenv('FLIGHT_API_KEY')

# ✗ 错误做法（不要这样做）
api_key = "your_secret_key"  # 永远不要硬编码！
```

### 环境变量来源

- **本地开发：** 从 `.env` 文件读取（由 `python-dotenv` 提供）
- **CI/CD：** 从GitHub Secrets或系统环境变量读取
- **生产环境：** 从密钥管理服务读取

---

## 📊 数据示例

### flight_records.json

```json
[
  {
    "flight_number": "CA888",
    "departure_airport": "PEK",
    "arrival_airport": "JFK",
    "departure_time": "2024-01-15T10:30:00",
    "arrival_time": "2024-01-15T22:30:00",
    "airline": "Air China",
    "cabin_class": "Business",
    "miles": 6850,
    "record_date": "2026-01-15T12:15:09.840684"
  }
]
```

### achievements.json

```json
[
  {
    "id": "first_international",
    "name": "🌍 国际旅行家",
    "description": "完成首次国际航班",
    "unlocked_date": "2026-01-15T12:15:09.841463",
    "flight": "CA888"
  }
]
```

---

## 🛠 高级用法

### 与Flask/FastAPI集成

```python
from flask import Flask, request, jsonify
from flight_assistant import FlightAssistant

app = Flask(__name__)
assistant = FlightAssistant()

@app.route('/api/flights', methods=['POST'])
def add_flight():
    data = request.json
    result = assistant.add_flight_record(**data)
    return jsonify({'success': result})

@app.route('/api/flights', methods=['GET'])
def get_flights():
    records = assistant.get_flight_records()
    return jsonify(records)

@app.route('/api/statistics', methods=['GET'])
def get_stats():
    year = request.args.get('year', type=int)
    stats = assistant.get_flight_statistics(year=year)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
```

### 定时价格监控（使用APScheduler）

```python
from apscheduler.schedulers.background import BackgroundScheduler
from flight_assistant import FlightAssistant

assistant = FlightAssistant()
scheduler = BackgroundScheduler()

def monitor_route():
    assistant.monitor_price("Beijing", "Tokyo", "2024-02-15")

# 每天早上8点检查价格
scheduler.add_job(monitor_route, 'cron', hour=8, minute=0)
scheduler.start()
```

---

## ❌ 常见问题 & 排查

### Q: 提示 "未配置FLIGHT_API_KEY"

**解决：** 检查 `.env` 文件中是否配置了 `FLIGHT_API_KEY`

```bash
# 查看当前配置
cat .env | grep FLIGHT_API_KEY
```

### Q: 行程卡图片生成失败

**原因：** 缺少字体文件或图像库不完整

**解决：**
```bash
# Linux
sudo apt-get install fonts-dejavu libpng-dev

# macOS
brew install freetype libpng
```

### Q: JSON文件读取错误

**原因：** 文件被损坏或编码问题

**解决：** 删除损坏的JSON文件，程序会自动重建
```bash
rm flight_records.json achievements.json price_alerts.json
```

---

## 📋 待优化功能

- [ ] 支持数据库存储（SQLite/PostgreSQL）
- [ ] Web界面仪表盘
- [ ] 推送通知（邮件/微信/企业微信）
- [ ] 多用户支持
- [ ] 导入/导出功能（CSV/Excel）
- [ ] 机票预订集成
- [ ] 机场实时信息查询

---

## 📝 许可证

MIT License

---

## 👨‍💻 贡献

欢迎提交Issue和Pull Request！

---

## 📞 联系方式

如有问题，请提交Issue或联系项目维护者。
