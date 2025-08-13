from agents.search_agent import SearchAgent
from agents.reasoning_agent import FinalAnswerAgent
from agents.intent_agent import IntentAgent
from agents.configs import Configuration
from pydantic.dataclasses import dataclass
from pydantic import computed_field
from typing import Literal, Union

@dataclass
class ReponseStatus:
    status_msg: Literal["success","backend failed"]
    status_code: int
    answer_response: Union[None, str]

    @computed_field
    @property
    def toStrFailed(self)->str:
        return f"status code: {self.status_code}, msg: {self.status_msg}"


class WorkFlow(object):
    def __init__(self, config: Configuration):
        self.intent_clf_agent = IntentAgent(config= config)
        self.search_agent = SearchAgent(config= config)
        self.final_agent = FinalAnswerAgent(config= config)

    async def __call__(self, query:str):
        try:
            intent, msg = await self.intent_clf_agent.run(query = query)
            if intent:
                search_result = await self.search_agent.run(query = query)
                answer = await self.final_agent.run(
                    query = query,
                    search_agent_outputs=search_result
                )
                status_code = 200
                
            else:
                answer = msg
                status_code = 200
            
            return ReponseStatus(
                status_msg= 'success', 
                status_code= status_code, 
                answer_response= answer
            )
         
        except Exception as e:
            print(f"Error in workflow: {str(e)}")
            answer = f"I apologize, but I encountered an error: {str(e)}"
            return ReponseStatus(
                status_msg= 'backend failed', 
                status_code= 500, 
                answer_response= answer
            )