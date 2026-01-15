# ✈️ 飞行生活记录与决策助手智能体

一个功能完整的Python飞行管理系统，支持飞行记录管理、行程卡生成、机票价格监控、飞行数据统计和成就解锁。

## 🌟 核心功能

### 1. 📝 飞行记录管理
- 录入航班信息（航班号、机场、时间、航司、舱位、里程）
- 支持多条件查询和过滤
- 数据持久化到 `flight_records.json`

### 2. 🎫 行程卡生成
- 根据飞行记录生成带二维码的行程卡图片
- 二维码包含航班关键信息
- 自动保存到 `flight_cards/` 目录
- 异常处理和字体降级支持

### 3. 💰 机票价格监控
- 查询指定航线的机票价格
- 持续监控价格变化并记录下跌提醒
- API密钥从环境变量读取（安全性优先）
- 支持定时监控设置

### 4. 📊 飞行数据统计
- 按年度/月度统计飞行数据
- 计算总飞行次数、总里程、平均航程
- 统计航司偏好、舱位分布
- 生成可视化统计报告

### 5. 🏆 飞行成就解锁
- 自动检测并解锁成就
- 预设成就规则：
  - 🌍 **国际旅行家** - 首次国际航班
  - ✈️ **飞行达人** - 年度飞行≥10次
  - 🚀 **长途旅人** - 累计里程≥10000km
- 成就信息保存到 `achievements.json`

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入API密钥
```

### 运行演示
```bash
# 基础演示
python flight_assistant.py

# 高级用法示例
python examples.py
```

## 📂 项目结构

```
.
├── flight_assistant.py          # 主程序（1000+行，完整功能实现）
├── examples.py                  # 高级用法示例
├── requirements.txt             # 依赖库清单
├── .env.example                 # 环境变量模板
├── FLIGHT_ASSISTANT_GUIDE.md    # 完整使用指南
├── flight_records.json          # 飞行记录数据（自动生成）
├── achievements.json            # 成就数据（自动生成）
├── price_alerts.json            # 价格监控记录（自动生成）
├── flight_cards/                # 生成的行程卡图片目录
└── flight_assistant.log         # 程序执行日志
```

## 💻 使用示例

### 基础使用

```python
from flight_assistant import FlightAssistant

assistant = FlightAssistant()

# 添加飞行记录
assistant.add_flight_record(
    flight_number="CA888",
    departure_airport="PEK",
    arrival_airport="JFK",
    departure_time="2024-01-15T10:30:00",
    arrival_time="2024-01-15T22:30:00",
    airline="Air China",
    cabin_class="Business",
    miles=6850
)

# 查询记录
records = assistant.get_flight_records(airline="Air China")

# 生成行程卡
card_path = assistant.generate_itinerary_card(records[0])

# 获取统计信息
stats = assistant.get_flight_statistics(year=2024)
assistant.print_statistics_report(stats)

# 查看成就
assistant.print_achievements()
```

### 价格监控

```python
# 检查价格
price_info = assistant.check_flight_price(
    departure="Beijing",
    arrival="Tokyo",
    travel_date="2024-02-15"
)

# 监控价格变化
assistant.monitor_price(
    departure="Beijing",
    arrival="Tokyo",
    travel_date="2024-02-15",
    price_threshold=100  # 仅记录下跌≥100元
)
```

## 🔐 安全特性

✅ **敏感信息管理**
- API密钥从环境变量读取
- 支持 GitHub Secrets 集成
- 不在代码中硬编码任何密钥

✅ **异常处理**
- 文件操作异常处理
- API调用失败处理
- JSON解析异常处理
- 图像生成失败降级处理

✅ **日志记录**
- 详细的操作日志
- 保存到 `flight_assistant.log`
- 支持控制台和文件同时输出

## 📋 技术栈

| 功能 | 库 | 版本 |
|------|----|----|
| HTTP请求 | requests | 2.31.0 |
| 图像处理 | pillow | 10.1.0 |
| 二维码生成 | qrcode | 7.4.2 |
| 环境变量 | python-dotenv | 1.0.0 |

## 📊 数据格式

### flight_records.json
```json
{
  "flight_number": "CA888",
  "departure_airport": "PEK",
  "arrival_airport": "JFK",
  "departure_time": "2024-01-15T10:30:00",
  "arrival_time": "2024-01-15T22:30:00",
  "airline": "Air China",
  "cabin_class": "Business",
  "miles": 6850,
  "record_date": "2026-01-15T12:15:09"
}
```

### achievements.json
```json
{
  "id": "long_distance_traveler",
  "name": "🚀 长途旅人",
  "description": "累计飞行里程≥10000公里",
  "unlocked_date": "2026-01-15T12:15:09",
  "total_miles": 12550
}
```

## 🔧 扩展功能

系统设计支持以下扩展：

- [ ] **数据库支持** - SQLite/PostgreSQL存储
- [ ] **Web界面** - Flask/FastAPI仪表盘
- [ ] **推送通知** - 邮件/微信/企业微信集成
- [ ] **多用户支持** - 用户认证和隔离
- [ ] **导入/导出** - CSV/Excel支持
- [ ] **机票预订** - 第三方接口集成
- [ ] **实时信息** - 机场和航班状态查询

## 📚 文档

- **[完整使用指南](FLIGHT_ASSISTANT_GUIDE.md)** - 详细功能说明和高级用法
- **[示例代码](examples.py)** - 8个实用示例

## ⚙️ 环境变量配置

```ini
# API密钥（必需）
FLIGHT_API_KEY=your_api_key

# API端点
FLIGHT_API_URL=https://api.example.com/flights

# Cookie（可选）
FLIGHT_COOKIE=your_cookie

# 监控间隔（小时）
PRICE_CHECK_INTERVAL_HOURS=24

# 日志级别
LOG_LEVEL=INFO
```

## 🐛 常见问题

**Q: 如何处理文件不存在的情况？**
A: 程序会自动创建缺失的JSON文件和目录

**Q: 行程卡图片生成失败？**
A: 检查系统是否安装了字体文件，程序会自动降级处理

**Q: 如何实现定时价格监控？**
A: 参考 FLIGHT_ASSISTANT_GUIDE.md 中的APScheduler集成示例

## 📝 日志示例

```
2026-01-15 12:15:09 - INFO - 飞行智能体初始化成功
2026-01-15 12:15:09 - INFO - 创建数据文件: flight_records.json
2026-01-15 12:15:09 - INFO - 飞行记录已添加: CA888
2026-01-15 12:15:09 - INFO - 🎉 解锁成就: 🌍 国际旅行家
2026-01-15 12:15:09 - INFO - 行程卡已生成: flight_cards/CA888_20260115_121509.png
```

## 🎯 设计特点

✨ **代码质量**
- 完整的类型注解
- 详细的代码注释
- 异常处理覆盖完整
- 日志记录全面

✨ **可维护性**
- 模块化设计
- 清晰的职责划分
- 易于扩展的架构
- 完善的文档

✨ **安全性**
- 敏感信息外部化
- 环境变量管理
- API调用超时控制
- 数据验证和清理

## 📞 反馈与支持

如发现问题或有改进建议，欢迎：
- 提交 Issue
- 提交 Pull Request
- 联系项目维护者

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**版本**: 1.0.0 | **最后更新**: 2026年1月15日
