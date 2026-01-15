#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞行智能体 - 高级用法示例
展示更复杂的场景和集成方式
"""

from flight_assistant import FlightAssistant
from datetime import datetime, timedelta
import json


def example_1_batch_import():
    """示例1: 批量导入飞行记录"""
    print("\n" + "="*60)
    print("示例1: 批量导入飞行记录")
    print("="*60)
    
    assistant = FlightAssistant()
    
    # 准备批量数据
    flights = [
        {
            "flight_number": "CZ3001",
            "departure_airport": "CTU",
            "arrival_airport": "SHA",
            "departure_time": "2024-01-20T08:00:00",
            "arrival_time": "2024-01-20T11:30:00",
            "airline": "China Southern",
            "cabin_class": "Economy",
            "miles": 1650
        },
        {
            "flight_number": "MU8512",
            "departure_airport": "SHA",
            "arrival_airport": "ICN",
            "departure_time": "2024-02-01T14:00:00",
            "arrival_time": "2024-02-01T17:30:00",
            "airline": "China Eastern",
            "cabin_class": "Business",
            "miles": 1250
        },
        {
            "flight_number": "BA112",
            "departure_airport": "LHR",
            "arrival_airport": "JFK",
            "departure_time": "2024-02-10T10:00:00",
            "arrival_time": "2024-02-10T13:30:00",
            "airline": "British Airways",
            "cabin_class": "Economy",
            "miles": 3450
        }
    ]
    
    for flight in flights:
        result = assistant.add_flight_record(**flight)
        status = "✓" if result else "✗"
        print(f"{status} 导入 {flight['flight_number']}")
    
    print(f"\n✓ 共导入 {len(flights)} 条记录")


def example_2_advanced_statistics():
    """示例2: 高级统计分析"""
    print("\n" + "="*60)
    print("示例2: 高级统计分析")
    print("="*60)
    
    assistant = FlightAssistant()
    
    # 获取全年统计
    year_stats = assistant.get_flight_statistics(year=2024)
    
    if year_stats.get('total_flights', 0) > 0:
        print(f"\n📊 2024年飞行统计:")
        print(f"  总飞行次数: {year_stats['total_flights']} 次")
        print(f"  总飞行里程: {year_stats['total_miles']} km")
        print(f"  平均每次: {year_stats['average_miles_per_flight']:.0f} km")
        
        # 计算等级
        total_miles = year_stats['total_miles']
        if total_miles >= 100000:
            level = "🏆 铂金会员"
        elif total_miles >= 50000:
            level = "💎 金牌会员"
        elif total_miles >= 10000:
            level = "🥇 银牌会员"
        else:
            level = "🎫 普通会员"
        
        print(f"  会员等级: {level}")
        
        # 计算常飞航司
        if year_stats.get('airline_preference'):
            top_airlines = sorted(
                year_stats['airline_preference'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            print(f"\n  常飞航司 TOP 3:")
            for i, (airline, count) in enumerate(top_airlines, 1):
                print(f"    {i}. {airline}: {count} 次")
    else:
        print("暂无飞行记录")


def example_3_itinerary_generation():
    """示例3: 批量生成行程卡"""
    print("\n" + "="*60)
    print("示例3: 批量生成行程卡")
    print("="*60)
    
    assistant = FlightAssistant()
    
    # 获取最近的飞行记录
    records = assistant.get_flight_records(limit=10)
    
    if not records:
        print("没有飞行记录")
        return
    
    generated_count = 0
    for record in records:
        card_path = assistant.generate_itinerary_card(record)
        if card_path:
            print(f"✓ 生成行程卡: {record['flight_number']}")
            print(f"  路径: {card_path}")
            generated_count += 1
    
    print(f"\n✓ 共生成 {generated_count} 张行程卡")


def example_4_price_monitoring_setup():
    """示例4: 设置价格监控"""
    print("\n" + "="*60)
    print("示例4: 价格监控设置")
    print("="*60)
    
    assistant = FlightAssistant()
    
    # 定义要监控的路线
    routes = [
        ("Beijing", "Tokyo", "2024-03-01"),
        ("Shanghai", "Bangkok", "2024-03-15"),
        ("Guangzhou", "Singapore", "2024-04-01"),
    ]
    
    print("\n监控路线配置:")
    for departure, arrival, travel_date in routes:
        print(f"  • {departure} → {arrival} ({travel_date})")
    
    print("\n提示: 在生产环境中，建议使用APScheduler或Celery实现定时监控")
    print("     参考代码见 FLIGHT_ASSISTANT_GUIDE.md 中的高级用法部分")


def example_5_achievements_milestones():
    """示例5: 成就和里程碑"""
    print("\n" + "="*60)
    print("示例5: 成就和里程碑")
    print("="*60)
    
    assistant = FlightAssistant()
    
    # 获取所有成就
    achievements = assistant.get_achievements()
    
    print(f"\n🏆 已解锁成就 ({len(achievements)} 个):")
    
    if achievements:
        for i, achievement in enumerate(achievements, 1):
            print(f"\n  {i}. {achievement['name']}")
            print(f"     描述: {achievement['description']}")
            print(f"     日期: {achievement['unlocked_date']}")
    else:
        print("  暂未解锁任何成就")
    
    # 显示可能的成就
    print("\n🎯 未来可解锁的成就:")
    print("  • 首次国内飞行")
    print("  • 访问超过10个国家")
    print("  • 乘坐超过5个航司")
    print("  • 连续7天内飞行")


def example_6_data_export():
    """示例6: 数据导出"""
    print("\n" + "="*60)
    print("示例6: 数据导出")
    print("="*60)
    
    assistant = FlightAssistant()
    
    # 获取所有数据
    records = assistant.get_flight_records()
    achievements = assistant.get_achievements()
    
    # 生成导出报告
    export_data = {
        "export_date": datetime.now().isoformat(),
        "summary": {
            "total_records": len(records),
            "total_achievements": len(achievements),
        },
        "records": records,
        "achievements": achievements
    }
    
    export_file = f"flight_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 数据已导出: {export_file}")
        print(f"  总记录数: {export_data['summary']['total_records']}")
        print(f"  成就数: {export_data['summary']['total_achievements']}")
    except Exception as e:
        print(f"✗ 导出失败: {e}")


def example_7_query_filters():
    """示例7: 高级查询过滤"""
    print("\n" + "="*60)
    print("示例7: 高级查询过滤")
    print("="*60)
    
    assistant = FlightAssistant()
    
    print("\n按航空公司筛选:")
    records = assistant.get_flight_records(airline="Air China")
    print(f"  Air China: {len(records)} 条记录")
    
    print("\n按舱位筛选:")
    records = assistant.get_flight_records(cabin_class="Business")
    print(f"  商务舱: {len(records)} 条记录")
    
    records = assistant.get_flight_records(cabin_class="Economy")
    print(f"  经济舱: {len(records)} 条记录")
    
    print("\n综合查询示例:")
    records = assistant.get_flight_records(
        airline="China Eastern",
        cabin_class="Economy",
        limit=5
    )
    print(f"  China Eastern 经济舱（最多5条）: {len(records)} 条记录")


def example_8_performance_stats():
    """示例8: 飞行性能统计"""
    print("\n" + "="*60)
    print("示例8: 飞行性能统计")
    print("="*60)
    
    assistant = FlightAssistant()
    
    records = assistant.get_flight_records()
    
    if not records:
        print("没有飞行记录")
        return
    
    print("\n✈️ 飞行性能分析:")
    
    # 最长航班
    longest_flight = max(records, key=lambda x: x['miles'])
    print(f"  最长航班: {longest_flight['flight_number']} ({longest_flight['miles']} km)")
    
    # 最短航班
    shortest_flight = min(records, key=lambda x: x['miles'])
    print(f"  最短航班: {shortest_flight['flight_number']} ({shortest_flight['miles']} km)")
    
    # 平均航程
    avg_miles = sum(r['miles'] for r in records) / len(records)
    print(f"  平均航程: {avg_miles:.0f} km")
    
    # 航司多样性
    airlines = set(r['airline'] for r in records)
    print(f"  乘坐航司: {len(airlines)} 个 {list(airlines)}")
    
    # 舱位多样性
    cabins = set(r['cabin_class'] for r in records)
    print(f"  体验舱位: {len(cabins)} 种 {list(cabins)}")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("🛫 飞行智能体 - 高级用法示例")
    print("="*60)
    
    try:
        example_1_batch_import()
        example_2_advanced_statistics()
        example_3_itinerary_generation()
        example_4_price_monitoring_setup()
        example_5_achievements_milestones()
        example_6_data_export()
        example_7_query_filters()
        example_8_performance_stats()
        
        print("\n" + "="*60)
        print("✅ 所有示例执行完成！")
        print("="*60)
        print("\n💡 提示:")
        print("  • 查看 FLIGHT_ASSISTANT_GUIDE.md 了解完整功能")
        print("  • 查看 flight_assistant.log 了解执行日志")
        print("  • 查看 flight_records.json 查看存储的数据")
        
    except Exception as e:
        print(f"\n❌ 执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
