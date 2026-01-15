# 机票价格监控测试脚本使用指南

## 📝 脚本概述

`main.py` 是一个完整的机票价格监控测试脚本，演示如何：
- 从环境变量安全读取API密钥
- 模拟机票价格查询功能
- 检测价格波动和下跌提醒
- 处理异常情况

## 🚀 快速开始

### 1. 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的配置
# FLIGHT_API_KEY=your_api_key_here
# FLIGHT_COOKIE=your_cookie_here
```

### 2. 运行测试

```bash
# 直接运行测试脚本
python main.py

# 或者指定Python版本
python3 main.py
```

## 📊 测试内容

脚本包含4个完整的测试用例：

### 测试1: 单次机票价格查询 ✓

```
输入：出发地、目的地、出行日期
输出：票价、价格趋势、提示信息
```

**示例代码：**
```python
result = monitor_flight_price("北京 (PEK)", "上海 (SHA)", "2026-02-10")
print(f"票价: ¥{result['price']}")
print(f"趋势: {result['trend']}")
```

### 测试2: 批量机票价格查询 ✓

```
同时查询多条路线的价格
批量处理和错误处理
```

**示例代码：**
```python
routes = [
    ("北京 (PEK)", "上海 (SHA)", "2026-02-10"),
    ("北京 (PEK)", "深圳 (SZX)", "2026-02-15"),
]

for departure, destination, date in routes:
    result = monitor_flight_price(departure, destination, date)
    print(f"{departure} → {destination}: ¥{result['price']}")
```

### 测试3: 价格下跌检测 ✓

```
持续监控同一路线的价格变化
检测并记录价格下跌情况
```

**示例代码：**
```python
for i in range(5):  # 模拟5次检查
    result = monitor_flight_price(departure, destination, date)
    if result['price'] < previous_price:
        print(f"⬇️ 价格下跌: ¥{previous_price - result['price']}")
```

### 测试4: 异常处理 ✓

```
正常日期处理
无效日期格式捕获
空值处理
```

## 🔑 环境变量配置

在 `.env` 文件中配置以下变量：

```ini
# 机票查询API密钥
FLIGHT_API_KEY=your_flight_api_key

# 航班查询Cookie
FLIGHT_COOKIE=your_cookie_value

# 其他配置
PRICE_CHECK_INTERVAL_HOURS=24
LOG_LEVEL=INFO
```

### 获取API密钥

1. **GitHub Secrets方式**（推荐用于CI/CD）
   - 在GitHub仓库设置中添加Secrets
   - 在GitHub Actions中使用: `${{ secrets.FLIGHT_API_KEY }}`

2. **本地环境变量**（开发时使用）
   - 创建 `.env` 文件
   - 填入密钥信息
   - python-dotenv会自动加载

## 💻 使用示例

### 示例1: 查询单个航班价格

```python
from main import monitor_flight_price

# 查询北京到上海的机票价格
result = monitor_flight_price(
    departure="北京 (PEK)",
    destination="上海 (SHA)",
    date="2026-02-10"
)

print(f"出发地: {result['departure']}")
print(f"目的地: {result['destination']}")
print(f"日期: {result['date']}")
print(f"票价: ¥{result['price']}")
print(f"趋势: {result['trend']}")
```

**输出：**
```
出发地: 北京 (PEK)
目的地: 上海 (SHA)
日期: 2026-02-10
票价: ¥1250
趋势: 下跌 📉
```

### 示例2: 批量监控多条路线

```python
from main import monitor_flight_price

routes = [
    ("北京", "上海", "2026-02-10"),
    ("北京", "广州", "2026-02-15"),
    ("上海", "深圳", "2026-02-12"),
]

for departure, destination, date in routes:
    try:
        result = monitor_flight_price(departure, destination, date)
        print(f"{departure} → {destination}: ¥{result['price']} {result['trend']}")
    except Exception as e:
        print(f"查询失败: {e}")
```

### 示例3: 价格监控和告警

```python
from main import monitor_flight_price

departure = "北京"
destination = "上海"
date = "2026-02-10"
alert_threshold = 100  # 下跌超过100元时告警

previous_price = None

for i in range(10):  # 监控10次
    result = monitor_flight_price(departure, destination, date)
    current_price = result['price']
    
    if previous_price and current_price < previous_price:
        drop = previous_price - current_price
        if drop >= alert_threshold:
            print(f"🚨 告警: 价格下跌¥{drop}!")
            print(f"   {previous_price} → {current_price}")
    
    previous_price = current_price
```

## 📋 输出解释

### 正常输出示例

```
✓ 查询结果:
  出发地: 北京 (PEK)
  目的地: 上海 (SHA)
  日期: 2026-02-10
  票价: ¥1250
  趋势: 下跌 📉
  提示: 价格下跌 📉，当前票价 ¥1250
```

### 配置警告

```
⚠️  警告：密钥未正确读取
   FLIGHT_API_KEY: ✗ 未设置
   FLIGHT_COOKIE: ✗ 未设置
   请配置 .env 文件或设置环境变量
```

### 异常处理

```
❌ 日期格式错误: invalid-date (应为 YYYY-MM-DD 格式)
✓ 正确捕获异常 - time data 'invalid-date' does not match format '%Y-%m-%d'
```

## 🔄 与flight_assistant.py集成

将 `main.py` 中的函数集成到 `flight_assistant.py`：

```python
from main import monitor_flight_price
from flight_assistant import FlightAssistant

assistant = FlightAssistant()

# 使用测试函数查询价格
result = monitor_flight_price("北京", "上海", "2026-02-10")

# 监控价格变化
assistant.monitor_price(
    departure="北京",
    arrival="上海",
    travel_date="2026-02-10"
)
```

## 🧪 测试验证

运行脚本时所有测试应该通过：

```
✓ 通过: 单次价格查询
✓ 通过: 批量价格查询
✓ 通过: 价格下跌检测
✓ 通过: 异常处理

总体: 4/4 个测试通过

🎉 所有测试通过！
```

## 📊 价格模拟规则

脚本使用以下规则模拟价格波动：

1. **基础价格**: 随机 ¥500-¥1500
2. **周末上浮**: 周六日价格 × 1.2
3. **价格趋势**: 随机上涨/下跌/持平
4. **日期检查**: 验证日期格式（YYYY-MM-DD）

## ⚙️ 配置GitHub Actions

在 `.github/workflows/flight-monitor.yml` 中使用：

```yaml
- name: 运行机票价格监控测试
  env:
    FLIGHT_API_KEY: ${{ secrets.FLIGHT_API_KEY }}
    FLIGHT_COOKIE: ${{ secrets.FLIGHT_COOKIE }}
  run: python main.py
```

## 🐛 常见问题

### Q: 提示"密钥未正确读取"怎么办？

**A:** 这是正常的。如果没有配置环境变量，脚本会继续运行（模拟模式）。

配置密钥方法：
```bash
# 方法1: 创建.env文件
echo "FLIGHT_API_KEY=your_key" > .env

# 方法2: 导出环境变量
export FLIGHT_API_KEY=your_key

# 方法3: 在命令行传入
FLIGHT_API_KEY=your_key python main.py
```

### Q: 如何集成到CI/CD流程？

**A:** 在GitHub Actions中设置Secrets：

1. 进入仓库 → Settings → Secrets and variables → Actions
2. 创建 `FLIGHT_API_KEY` 和 `FLIGHT_COOKIE` Secrets
3. 在工作流中使用：

```yaml
env:
  FLIGHT_API_KEY: ${{ secrets.FLIGHT_API_KEY }}
  FLIGHT_COOKIE: ${{ secrets.FLIGHT_COOKIE }}
```

### Q: 价格为什么每次都不一样？

**A:** 这是正常的！脚本模拟真实的价格波动。

- 基础价格随机生成 (¥500-¥1500)
- 周末价格上浮20%
- 趋势随机变化 (上涨/下跌/持平)

## 📞 支持

有问题？查看以下文件获取帮助：

- [FLIGHT_ASSISTANT_GUIDE.md](FLIGHT_ASSISTANT_GUIDE.md) - 完整功能指南
- [FLIGHT_ASSISTANT_README.md](FLIGHT_ASSISTANT_README.md) - 项目总体介绍
- [flight_assistant.py](flight_assistant.py) - 完整源代码

---

✅ 测试脚本已就绪，可直接运行或集成到CI/CD流程！
