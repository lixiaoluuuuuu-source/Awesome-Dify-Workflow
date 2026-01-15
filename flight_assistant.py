#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞行生活记录与决策助手智能体
支持飞行记录管理、行程卡生成、机票价格监控、飞行统计和成就解锁功能
"""

import os
import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import qrcode
from PIL import Image, ImageDraw, ImageFont
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flight_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 常量定义
FLIGHT_RECORDS_FILE = 'flight_records.json'
ACHIEVEMENTS_FILE = 'achievements.json'
PRICE_ALERTS_FILE = 'price_alerts.json'
FLIGHT_CARDS_DIR = 'flight_cards'
DOMESTIC_COUNTRIES = {'CN'}  # 国内标识

@dataclass
class FlightRecord:
    """飞行记录数据类"""
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    airline: str
    cabin_class: str  # 舱位：经济舱、商务舱、头等舱
    miles: int
    record_date: str = None
    
    def __post_init__(self):
        if self.record_date is None:
            self.record_date = datetime.now().isoformat()

    def is_international(self) -> bool:
        """判断是否为国际航班"""
        return not (self.departure_airport[0] == 'Z' and self.arrival_airport[0] == 'Z')
    
    def get_key(self) -> str:
        """生成唯一标识符"""
        return f"{self.flight_number}_{self.departure_time}_{self.departure_airport}"


class FlightAssistant:
    """飞行智能体主类"""
    
    def __init__(self):
        """初始化飞行助手"""
        self.records_file = FLIGHT_RECORDS_FILE
        self.achievements_file = ACHIEVEMENTS_FILE
        self.price_alerts_file = PRICE_ALERTS_FILE
        self.flight_cards_dir = FLIGHT_CARDS_DIR
        
        # 创建必要目录
        Path(self.flight_cards_dir).mkdir(exist_ok=True)
        
        # 初始化数据文件
        self._init_data_files()
        
        # 从环境变量读取API密钥
        self.flight_api_key = os.getenv('FLIGHT_API_KEY', '')
        self.flight_api_url = os.getenv('FLIGHT_API_URL', '')
        self.flight_cookie = os.getenv('FLIGHT_COOKIE', '')
        self.price_check_interval = int(os.getenv('PRICE_CHECK_INTERVAL_HOURS', 24))
        
        logger.info("飞行智能体初始化成功")
    
    def _init_data_files(self):
        """初始化数据文件"""
        for file_path in [self.records_file, self.achievements_file, self.price_alerts_file]:
            if not Path(file_path).exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                logger.info(f"创建数据文件: {file_path}")
    
    def _load_json(self, file_path: str) -> List:
        """加载JSON数据文件"""
        try:
            if not Path(file_path).exists():
                return []
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"读取文件 {file_path} 失败: {e}")
            return []
    
    def _save_json(self, file_path: str, data: List) -> bool:
        """保存JSON数据文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据保存到 {file_path}")
            return True
        except Exception as e:
            logger.error(f"保存文件 {file_path} 失败: {e}")
            return False

    # ===================== 功能1：飞行记录管理 =====================
    
    def add_flight_record(self, 
                         flight_number: str,
                         departure_airport: str,
                         arrival_airport: str,
                         departure_time: str,
                         arrival_time: str,
                         airline: str,
                         cabin_class: str,
                         miles: int) -> bool:
        """
        添加飞行记录
        :param flight_number: 航班号
        :param departure_airport: 起飞机场代码
        :param arrival_airport: 降落机场代码
        :param departure_time: 起飞时间 (ISO格式)
        :param arrival_time: 降落时间 (ISO格式)
        :param airline: 航空公司
        :param cabin_class: 舱位
        :param miles: 飞行里程
        :return: 是否成功添加
        """
        try:
            record = FlightRecord(
                flight_number=flight_number,
                departure_airport=departure_airport,
                arrival_airport=arrival_airport,
                departure_time=departure_time,
                arrival_time=arrival_time,
                airline=airline,
                cabin_class=cabin_class,
                miles=miles
            )
            
            records = self._load_json(self.records_file)
            records.append(asdict(record))
            
            if self._save_json(self.records_file, records):
                logger.info(f"飞行记录已添加: {flight_number}")
                
                # 触发成就检测
                self.check_and_unlock_achievements(record)
                return True
            return False
            
        except Exception as e:
            logger.error(f"添加飞行记录失败: {e}")
            return False
    
    def get_flight_records(self, 
                          airline: Optional[str] = None,
                          cabin_class: Optional[str] = None,
                          limit: int = None) -> List[Dict]:
        """
        查询飞行记录
        :param airline: 筛选航空公司（可选）
        :param cabin_class: 筛选舱位（可选）
        :param limit: 返回记录数限制
        :return: 飞行记录列表
        """
        try:
            records = self._load_json(self.records_file)
            
            # 筛选
            if airline:
                records = [r for r in records if r['airline'] == airline]
            if cabin_class:
                records = [r for r in records if r['cabin_class'] == cabin_class]
            
            # 按时间倒序排列
            records.sort(key=lambda x: x['record_date'], reverse=True)
            
            if limit:
                records = records[:limit]
            
            logger.info(f"查询飞行记录: 共{len(records)}条")
            return records
            
        except Exception as e:
            logger.error(f"查询飞行记录失败: {e}")
            return []

    # ===================== 功能2：行程卡生成 =====================
    
    def generate_itinerary_card(self, flight_record: Dict) -> Optional[str]:
        """
        生成带二维码的行程卡图片
        :param flight_record: 飞行记录字典
        :return: 生成的图片路径，失败返回None
        """
        try:
            flight_number = flight_record['flight_number']
            departure = flight_record['departure_airport']
            arrival = flight_record['arrival_airport']
            departure_time = flight_record['departure_time']
            arrival_time = flight_record['arrival_time']
            airline = flight_record['airline']
            cabin = flight_record['cabin_class']
            miles = flight_record['miles']
            
            # 生成二维码
            qr_data = f"Flight:{flight_number}|From:{departure}|To:{arrival}|Dep:{departure_time}|Airline:{airline}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # 创建行程卡背景 (1200x800)
            card_width, card_height = 1200, 800
            card = Image.new('RGB', (card_width, card_height), color='white')
            draw = ImageDraw.Draw(card)
            
            # 设置字体 (使用系统默认字体)
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            except:
                # 降级使用默认字体
                title_font = text_font = small_font = ImageFont.load_default()
            
            # 绘制标题
            draw.text((50, 30), f"Flight Itinerary - {flight_number}", fill='black', font=title_font)
            
            # 绘制航班信息
            y_offset = 100
            info_lines = [
                f"Airline: {airline}",
                f"From: {departure} → To: {arrival}",
                f"Departure: {departure_time}",
                f"Arrival: {arrival_time}",
                f"Cabin: {cabin}",
                f"Distance: {miles} miles"
            ]
            
            for line in info_lines:
                draw.text((50, y_offset), line, fill='black', font=text_font)
                y_offset += 50
            
            # 粘贴二维码
            qr_size = 200
            qr_img_resized = qr_img.resize((qr_size, qr_size))
            card.paste(qr_img_resized, (card_width - qr_size - 50, card_height - qr_size - 50))
            
            # 生成时间戳文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{flight_number}_{timestamp}.png"
            filepath = os.path.join(self.flight_cards_dir, filename)
            
            # 保存图片
            card.save(filepath)
            logger.info(f"行程卡已生成: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"生成行程卡失败: {e}")
            return None

    # ===================== 功能3：机票价格监控 =====================
    
    def check_flight_price(self,
                          departure: str,
                          arrival: str,
                          travel_date: str) -> Optional[Dict]:
        """
        查询机票价格
        :param departure: 出发地
        :param arrival: 目的地
        :param travel_date: 出行日期 (YYYY-MM-DD)
        :return: 价格信息字典，失败返回None
        """
        if not self.flight_api_key or not self.flight_api_url:
            logger.warning("未配置FLIGHT_API_KEY或FLIGHT_API_URL")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.flight_api_key}',
                'Cookie': self.flight_cookie if self.flight_cookie else '',
                'User-Agent': 'Flight-Assistant/1.0'
            }
            
            params = {
                'from': departure,
                'to': arrival,
                'date': travel_date
            }
            
            response = requests.get(
                self.flight_api_url,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"获取价格信息: {departure} -> {arrival} 日期: {travel_date}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"API调用失败 ({departure}->{arrival}): {e}")
            return None
        except json.JSONDecodeError:
            logger.error("API返回数据解析失败")
            return None
    
    def monitor_price(self,
                     departure: str,
                     arrival: str,
                     travel_date: str,
                     price_threshold: float = None) -> bool:
        """
        监控机票价格变化
        :param departure: 出发地
        :param arrival: 目的地
        :param travel_date: 出行日期
        :param price_threshold: 价格下跌阈值
        :return: 是否成功记录
        """
        try:
            price_info = self.check_flight_price(departure, arrival, travel_date)
            if not price_info:
                return False
            
            alerts = self._load_json(self.price_alerts_file)
            
            # 生成监控记录
            route_key = f"{departure}_{arrival}_{travel_date}"
            current_price = price_info.get('min_price', 0)
            
            # 检查是否存在历史记录
            previous_record = None
            for alert in alerts:
                if alert.get('route_key') == route_key:
                    previous_record = alert
                    break
            
            new_alert = {
                'route_key': route_key,
                'departure': departure,
                'arrival': arrival,
                'travel_date': travel_date,
                'current_price': current_price,
                'previous_price': previous_record.get('current_price') if previous_record else None,
                'price_drop': False,
                'timestamp': datetime.now().isoformat(),
                'raw_data': price_info
            }
            
            # 检测价格下跌
            if previous_record and new_alert['previous_price']:
                price_drop = new_alert['previous_price'] - current_price
                if price_drop > 0 and (price_threshold is None or price_drop >= price_threshold):
                    new_alert['price_drop'] = True
                    logger.warning(f"⬇️ 价格下跌提醒: {departure}->{arrival} 下跌 ¥{price_drop}")
            
            # 更新或添加记录
            if previous_record:
                for i, alert in enumerate(alerts):
                    if alert.get('route_key') == route_key:
                        alerts[i] = new_alert
                        break
            else:
                alerts.append(new_alert)
            
            self._save_json(self.price_alerts_file, alerts)
            return True
            
        except Exception as e:
            logger.error(f"价格监控失败: {e}")
            return False
    
    def start_price_monitoring(self,
                              departure: str,
                              arrival: str,
                              travel_date: str,
                              interval_hours: int = None):
        """
        启动定时价格监控（后台任务）
        注意：在实际应用中，建议使用APScheduler或Celery等任务调度库
        :param departure: 出发地
        :param arrival: 目的地
        :param travel_date: 出行日期
        :param interval_hours: 监控间隔（小时）
        """
        if interval_hours is None:
            interval_hours = self.price_check_interval
        
        logger.info(f"已启动价格监控: {departure}->{arrival}, 建议间隔{interval_hours}小时")
        logger.info("提示：可配合系统cron或任务调度器实现定时检查")

    # ===================== 功能4：飞行数据统计 =====================
    
    def get_flight_statistics(self,
                             year: Optional[int] = None,
                             month: Optional[int] = None) -> Dict:
        """
        生成飞行统计报告
        :param year: 统计年份（可选）
        :param month: 统计月份（可选）
        :return: 统计信息字典
        """
        try:
            records = self._load_json(self.records_file)
            
            # 按时间筛选
            filtered_records = []
            for record in records:
                record_date = datetime.fromisoformat(record['record_date'])
                if year and record_date.year != year:
                    continue
                if month and record_date.month != month:
                    continue
                filtered_records.append(record)
            
            # 计算统计信息
            total_flights = len(filtered_records)
            total_miles = sum(r['miles'] for r in filtered_records)
            
            # 航司偏好
            airline_count = {}
            for record in filtered_records:
                airline = record['airline']
                airline_count[airline] = airline_count.get(airline, 0) + 1
            
            # 舱位分布
            cabin_distribution = {}
            for record in filtered_records:
                cabin = record['cabin_class']
                cabin_distribution[cabin] = cabin_distribution.get(cabin, 0) + 1
            
            # 国际航班数
            international_flights = sum(
                1 for r in filtered_records
                if r['departure_airport'][0] != 'Z' or r['arrival_airport'][0] != 'Z'
            )
            
            stats = {
                'period': f"{year}-{month if month else 'ALL'}",
                'total_flights': total_flights,
                'total_miles': total_miles,
                'average_miles_per_flight': total_miles / total_flights if total_flights > 0 else 0,
                'international_flights': international_flights,
                'domestic_flights': total_flights - international_flights,
                'airline_preference': airline_count,
                'cabin_distribution': cabin_distribution,
                'top_airline': max(airline_count, key=airline_count.get) if airline_count else 'N/A'
            }
            
            logger.info(f"统计报告生成: {stats['period']}, 总飞行次数: {total_flights}")
            return stats
            
        except Exception as e:
            logger.error(f"生成统计报告失败: {e}")
            return {}
    
    def print_statistics_report(self, stats: Dict):
        """打印统计报告"""
        print("\n" + "="*60)
        print(f"飞行数据统计报告 - 时间: {stats.get('period', 'N/A')}")
        print("="*60)
        print(f"总飞行次数: {stats.get('total_flights', 0)} 次")
        print(f"总飞行里程: {stats.get('total_miles', 0)} 公里")
        print(f"平均每次里程: {stats.get('average_miles_per_flight', 0):.2f} 公里")
        print(f"国际航班: {stats.get('international_flights', 0)} 次")
        print(f"国内航班: {stats.get('domestic_flights', 0)} 次")
        print(f"最常乘坐航司: {stats.get('top_airline', 'N/A')}")
        
        if stats.get('airline_preference'):
            print("\n航司偏好:")
            for airline, count in sorted(stats['airline_preference'].items(), 
                                        key=lambda x: x[1], reverse=True):
                print(f"  - {airline}: {count} 次")
        
        if stats.get('cabin_distribution'):
            print("\n舱位分布:")
            for cabin, count in stats['cabin_distribution'].items():
                print(f"  - {cabin}: {count} 次")
        print("="*60 + "\n")

    # ===================== 功能5：飞行成就解锁 =====================
    
    def check_and_unlock_achievements(self, flight_record: FlightRecord):
        """
        检查并解锁成就
        :param flight_record: 飞行记录对象
        """
        try:
            achievements = self._load_json(self.achievements_file)
            unlocked = []
            
            # 检查首次国际飞行
            if flight_record.is_international():
                records = self._load_json(self.records_file)
                intl_count = sum(
                    1 for r in records
                    if r['departure_airport'][0] != 'Z' or r['arrival_airport'][0] != 'Z'
                )
                if intl_count == 1:
                    achievement = {
                        'id': 'first_international',
                        'name': '🌍 国际旅行家',
                        'description': '完成首次国际航班',
                        'unlocked_date': datetime.now().isoformat(),
                        'flight': flight_record.flight_number
                    }
                    achievements.append(achievement)
                    unlocked.append(achievement['name'])
            
            # 检查年度飞行达人（年度≥10次）
            year = datetime.now().year
            year_stats = self.get_flight_statistics(year=year)
            if year_stats.get('total_flights', 0) >= 10:
                # 检查是否已解锁
                if not any(a['id'] == 'frequent_flyer' for a in achievements):
                    achievement = {
                        'id': 'frequent_flyer',
                        'name': '✈️ 飞行达人',
                        'description': '年度飞行次数≥10次',
                        'unlocked_date': datetime.now().isoformat(),
                        'stats': year_stats
                    }
                    achievements.append(achievement)
                    unlocked.append(achievement['name'])
            
            # 检查长途旅人（累计里程≥10000）
            all_stats = self.get_flight_statistics()
            if all_stats.get('total_miles', 0) >= 10000:
                if not any(a['id'] == 'long_distance_traveler' for a in achievements):
                    achievement = {
                        'id': 'long_distance_traveler',
                        'name': '🚀 长途旅人',
                        'description': '累计飞行里程≥10000公里',
                        'unlocked_date': datetime.now().isoformat(),
                        'total_miles': all_stats.get('total_miles', 0)
                    }
                    achievements.append(achievement)
                    unlocked.append(achievement['name'])
            
            # 保存成就信息
            if unlocked:
                self._save_json(self.achievements_file, achievements)
                logger.info(f"🎉 解锁成就: {', '.join(unlocked)}")
            
        except Exception as e:
            logger.error(f"成就检查失败: {e}")
    
    def get_achievements(self) -> List[Dict]:
        """获取所有解锁的成就"""
        try:
            achievements = self._load_json(self.achievements_file)
            logger.info(f"已解锁成就数: {len(achievements)}")
            return achievements
        except Exception as e:
            logger.error(f"获取成就失败: {e}")
            return []
    
    def print_achievements(self):
        """打印成就列表"""
        achievements = self.get_achievements()
        if not achievements:
            print("\n还未解锁任何成就，继续飞行吧！")
            return
        
        print("\n" + "="*60)
        print("🏆 已解锁成就")
        print("="*60)
        for achievement in achievements:
            print(f"\n{achievement['name']}")
            print(f"  描述: {achievement['description']}")
            print(f"  解锁日期: {achievement['unlocked_date']}")
        print("="*60 + "\n")


def main():
    """主函数 - 演示用法"""
    assistant = FlightAssistant()
    
    print("\n🛫 飞行生活记录与决策助手启动")
    print("="*60)
    
    # 示例1：添加飞行记录
    print("\n【演示】添加飞行记录...")
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
    
    assistant.add_flight_record(
        flight_number="MU501",
        departure_airport="SHA",
        arrival_airport="LAX",
        departure_time="2024-01-10T08:00:00",
        arrival_time="2024-01-10T15:00:00",
        airline="China Eastern",
        cabin_class="Economy",
        miles=5700
    )
    
    # 示例2：查询飞行记录
    print("\n【演示】查询飞行记录...")
    records = assistant.get_flight_records(limit=5)
    print(f"查询到 {len(records)} 条飞行记录")
    
    # 示例3：生成行程卡
    if records:
        print("\n【演示】生成行程卡...")
        card_path = assistant.generate_itinerary_card(records[0])
        if card_path:
            print(f"✓ 行程卡已生成: {card_path}")
    
    # 示例4：飞行统计
    print("\n【演示】飞行数据统计...")
    stats = assistant.get_flight_statistics()
    if stats:
        assistant.print_statistics_report(stats)
    
    # 示例5：查看成就
    print("\n【演示】查看已解锁成就...")
    assistant.print_achievements()
    
    # 示例6：价格监控（需要配置API密钥）
    print("\n【演示】机票价格监控...")
    if assistant.flight_api_key:
        monitor_result = assistant.monitor_price("Beijing", "Tokyo", "2024-02-15")
        print(f"价格监控状态: {'成功' if monitor_result else '失败'}")
    else:
        print("⚠️  未配置FLIGHT_API_KEY，跳过价格监控演示")
    
    print("\n✅ 演示完成！")


if __name__ == '__main__':
    main()
