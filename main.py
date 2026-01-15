#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞行智能体 - 机票价格监控测试脚本
演示如何使用环境变量读取敏感信息，并模拟机票价格查询功能
"""

import os
import random
import sys
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 读取测试密钥（从环境变量读取，安全且可配置）
API_KEY = os.getenv("FLIGHT_API_KEY", "")
COOKIE = os.getenv("FLIGHT_COOKIE", "")


def monitor_flight_price(departure: str, destination: str, date: str) -> dict:
    """
    模拟机票价格查询函数（测试用）
    
    在实际使用中，这里会调用真实的机票查询API。
    此函数模拟不同日期的价格波动规律。
    
    :param departure: 出发地
    :param destination: 目的地
    :param date: 出行日期（格式：YYYY-MM-DD）
    :return: 包含价格和趋势的字典
    :raises ValueError: 当密钥未正确读取时
    """
    # 验证密钥是否读取成功（测试用）
    if not API_KEY or not COOKIE:
        print("⚠️  警告：密钥未正确读取")
        print(f"   FLIGHT_API_KEY: {'✓ 已设置' if API_KEY else '✗ 未设置'}")
        print(f"   FLIGHT_COOKIE: {'✓ 已设置' if COOKIE else '✗ 未设置'}")
        print("\n   请配置 .env 文件或设置环境变量")
    
    # 模拟不同日期的价格波动
    base_price = random.randint(500, 1500)
    
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        # 周末价格上浮20%
        if date_obj.weekday() in [5, 6]:  # 5=Saturday, 6=Sunday
            base_price = int(base_price * 1.2)
    except ValueError:
        print(f"❌ 日期格式错误: {date} (应为 YYYY-MM-DD 格式)")
        raise
    
    # 模拟价格趋势：随机返回上涨/下跌/持平
    trend = random.choice(["上涨 📈", "下跌 📉", "持平 ➡️"])
    
    return {
        "departure": departure,
        "destination": destination,
        "date": date,
        "price": base_price,
        "trend": trend,
        "tips": f"价格{trend}，当前票价 ¥{base_price}",
        "timestamp": datetime.now().isoformat()
    }


def test_single_query():
    """测试单次价格查询"""
    print("\n" + "="*60)
    print("📝 测试1: 单次机票价格查询")
    print("="*60)
    
    try:
        result = monitor_flight_price("北京 (PEK)", "上海 (SHA)", "2026-02-10")
        
        print(f"\n✓ 查询结果:")
        print(f"  出发地: {result['departure']}")
        print(f"  目的地: {result['destination']}")
        print(f"  日期: {result['date']}")
        print(f"  票价: ¥{result['price']}")
        print(f"  趋势: {result['trend']}")
        print(f"  提示: {result['tips']}")
        
        return True
    except Exception as e:
        print(f"\n❌ 查询失败: {e}")
        return False


def test_batch_query():
    """测试批量价格查询"""
    print("\n" + "="*60)
    print("📝 测试2: 批量机票价格查询")
    print("="*60)
    
    routes = [
        ("北京 (PEK)", "上海 (SHA)", "2026-02-10"),
        ("北京 (PEK)", "深圳 (SZX)", "2026-02-15"),
        ("上海 (SHA)", "广州 (CAN)", "2026-02-12"),
    ]
    
    print(f"\n查询 {len(routes)} 条路线...\n")
    
    results = []
    for departure, destination, date in routes:
        try:
            result = monitor_flight_price(departure, destination, date)
            results.append(result)
            
            status = "✓" if "下跌" in result['trend'] else "○"
            print(f"{status} {departure} → {destination} ({date}): ¥{result['price']} {result['trend']}")
        except Exception as e:
            print(f"✗ {departure} → {destination} 查询失败: {e}")
    
    return len(results) == len(routes)


def test_price_drop_detection():
    """测试价格下跌检测"""
    print("\n" + "="*60)
    print("📝 测试3: 价格下跌检测")
    print("="*60)
    
    departure, destination, date = "北京 (PEK)", "纽约 (JFK)", "2026-03-01"
    
    print(f"\n监控 {departure} → {destination} ({date}) 价格变化...\n")
    
    previous_price = None
    
    for i in range(5):
        try:
            result = monitor_flight_price(departure, destination, date)
            current_price = result['price']
            
            if previous_price is None:
                status = "🔍"
                change = ""
            elif current_price < previous_price:
                change = f"下跌 ↓ ¥{previous_price - current_price}"
                status = "⬇️ "
            elif current_price > previous_price:
                change = f"上涨 ↑ ¥{current_price - previous_price}"
                status = "⬆️ "
            else:
                change = "持平"
                status = "➡️ "
            
            print(f"  检测 #{i+1}: ¥{current_price} {status} {change}")
            previous_price = current_price
            
        except Exception as e:
            print(f"  检测 #{i+1} 失败: {e}")
    
    return True


def test_error_handling():
    """测试异常处理"""
    print("\n" + "="*60)
    print("📝 测试4: 异常处理")
    print("="*60)
    
    test_cases = [
        ("北京", "上海", "2026-02-10", "正常日期"),
        ("北京", "上海", "invalid-date", "无效日期格式"),
        ("", "上海", "2026-02-10", "空出发地"),
    ]
    
    print()
    for departure, destination, date, description in test_cases:
        try:
            result = monitor_flight_price(departure, destination, date)
            print(f"✓ {description}: ¥{result['price']}")
        except ValueError as e:
            print(f"✓ {description}: 正确捕获异常 - {e}")
        except Exception as e:
            print(f"? {description}: {type(e).__name__} - {e}")
    
    return True


def main():
    """运行所有测试"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║  🛫 飞行智能体 - 机票价格监控测试                        ║")
    print("╚" + "="*58 + "╝")
    
    # 显示配置状态
    print("\n📊 配置状态:")
    print(f"  API密钥: {'✓ 已配置' if API_KEY else '✗ 未配置'}")
    print(f"  Cookie: {'✓ 已配置' if COOKIE else '✗ 未配置'}")
    
    # 运行测试
    tests = [
        ("单次价格查询", test_single_query),
        ("批量价格查询", test_batch_query),
        ("价格下跌检测", test_price_drop_detection),
        ("异常处理", test_error_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ 测试执行异常: {e}")
            results.append((test_name, False))
    
    # 测试总结
    print("\n" + "="*60)
    print("📋 测试总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {test_name}")
    
    print(f"\n总体: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试未通过")
        return 1


if __name__ == "__main__":
    sys.exit(main())

