# 极简版 Flight Agent 本地测试脚本
class FlightAssistant:
    def answer(self, question):
        # 这里可以替换成你的智能体核心逻辑
        basic_responses = {
            "CA1501状态": "CA1501 今日准点起飞，北京首都机场 T3 → 上海虹桥机场 T2",
            "天津飞广州航班": "下周五天津→广州有国航CA3302、南航CZ3121，经济舱最低650元",
            "行李丢失怎么办": "联系机场行李服务中心，提供行李牌、身份证和航班信息登记挂失"
        }
        # 匹配问题关键词返回结果，无匹配则默认回复
        for key in basic_responses:
            if key in question:
                return basic_responses[key]
        return "你可以问我航班状态、行程规划或机场相关问题~"

# 对话入口
if __name__ == "__main__":
    agent = FlightAssistant()
    print("✈️  航班助手已启动（输入 exit 退出）")
    while True:
        user_q = input("你：")
        if user_q.lower() == "exit":
            print("助手：再见啦~")
            break
        print("助手：", agent.answer(user_q))
