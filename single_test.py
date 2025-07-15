from agents.search_agent import SearchAgent
from agents.reasoning_agent import FinalAnswerAgent
from agents.intent_agent import IntentAgent
from agents.configs import Configuration
import asyncio
import json


main_config = Configuration(use_filtering_model=True)

intent_clf_agent = IntentAgent(config = main_config)
search_agent = SearchAgent(config = main_config)
final_agent = FinalAnswerAgent(config = main_config)


async def main():

    query= "Hành vi không chấp hành hiệu lệnh của đèn tín hiệu giao thông, không chấp hành hiệu lệnh, hướng dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông đối với người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô bị xử phạt vi phạm hành chính như thế nào?"
    
    result = await intent_clf_agent.run(query = query)
    if result:
        search_result = await search_agent.run(query = query)
        final_result = await final_agent.run(query = query,search_agent_outputs=search_result)
        print(final_result)

if __name__ == "__main__":
    asyncio.run(main())

