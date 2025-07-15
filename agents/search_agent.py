from tavily import TavilyClient
from google import genai
from google.genai import types
import re
import json
from dotenv import load_dotenv
import os
import asyncio
from typing import Union


from .schemas import PAGE_MAIN_CONTENT, LawDocModel
from .prompts import FILTERING_SYSTEM_PROMPT, PER_PAGE_DOCUMENT_PROMPT
from .configs import Configuration, TavilySearchConfig, TavilyExtractConfig
from .utils import make_logger, measure_time


logger = make_logger(__name__)


class FindDocLaw(object):
    def __init__(self):
        self._general_pattern = "\[(?:Luật|Nghị định).*?\]\(.*?\)"
        self._law_code_pattern = "\[(?:Luật|Nghị định).*?\]"
        self._law_url_pattern = "\]\(.*?\)"

    def find(self, page_content: str)->Union[None, list[LawDocModel]]:
        res: list[str] = re.findall(self._general_pattern , page_content)
        if len(res) == 0:
            logger.info('early return in find')
            return None
        else:
            found_docs = {}
            for single_res in res:
                lawcode_seach = re.search(self._law_code_pattern, single_res)
                lawurl_seach = re.search(self._law_url_pattern, single_res)

                if lawcode_seach is not None and lawurl_seach is not None:
                    found_docs[lawcode_seach.group(0)[1:-1]] = lawurl_seach.group(0)[2:-1]
                else:
                    continue
            
            if len(found_docs) == 0:
                # incase the link is broken
                logger.info('link may broken')
                return None
            else:
                return [
                    LawDocModel(doc_number=k, url= v)
                    for k, v in found_docs.items()
                ]
                

class SearchAgent(object):

    _filter_config = types.GenerateContentConfig(
        system_instruction=FILTERING_SYSTEM_PROMPT,
        response_schema=PAGE_MAIN_CONTENT,
        response_mime_type='application/json',
        temperature = 0.1
    )

    def __init__(self, config: Configuration):
        load_dotenv()
        if os.getenv("GEMINI_API_KEY") is None:
            raise ValueError("GEMINI_API_KEY is not set")
        if os.getenv("TAVILY_API_KEY") is None:
            raise ValueError("TAVILY_API_KEY is not set")

        self.config = config
        self.tavily_client = TavilyClient(api_key= os.getenv("TAVILY_API_KEY"))
        self._search_kwargs = TavilySearchConfig().model_dump()
        self._extract_kwargs = TavilyExtractConfig().model_dump()

        if self.config.use_filtering_model:
            self.filtering_model = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        self.lawdoc_finding = FindDocLaw()

    @measure_time(logger= logger)
    async def _filtering(self, input_prompt:str)->PAGE_MAIN_CONTENT:
        r""""
        Filter out the main content of the webpage
        discard header or any other parts in body of the page
        """
        
        response = await self.filtering_model.aio.models.generate_content(
            model = self.config.filtering_model,
            contents = input_prompt,
            config = self._filter_config,
        )
        
        page_content = None
        if response.parsed is None:
            logger.info("response.parsed is None")
            page_content =  PAGE_MAIN_CONTENT(**json.loads(response.text))
        else:
            page_content:PAGE_MAIN_CONTENT = response.parsed
        
        # found_law_docs = self.lawdoc_finding.find(page_content= page_content.main_content)

        # if found_law_docs is not None:
        #     urls = [
        #             found_law_docs[_ith].url 
        #             for _ith in range(len(found_law_docs))
        #         ]
        #     lawdoc_contents = self.tavily_client.extract(
        #         urls=urls,
        #         **self._extract_kwargs
        #     )

        #     for each_result in lawdoc_contents['results']:
        #         _index = urls.index(each_result['url'])
        #         print(each_result['url'], _index)
        #         print(each_result['raw_content'])
        #         found_law_docs[_index].content = each_result['raw_content']

        # page_content.law_docs = found_law_docs
        return page_content

    @measure_time(logger = logger)
    async def run(self, query:str):
        # fast search
        search_results = self.tavily_client.search(
            query = query,
            **self._search_kwargs
        )

        # extract list of urls
        extract_results = self.tavily_client.extract(
            urls=[
                res['url'] 
                for res in search_results['results']
            ],
            **self._extract_kwargs
        )

        if self.config.use_filtering_model:
            # cleaning with llm
            response: list[PAGE_MAIN_CONTENT] = await asyncio.gather(*[
                self._filtering(
                    input_prompt=PER_PAGE_DOCUMENT_PROMPT.format(
                        query = query,
                        ith = ith,
                        **ele
                    )
                )
                for ith, ele in 
                enumerate(extract_results['results'])
            ])
            return response
        
        else:
            return [
                PAGE_MAIN_CONTENT(
                    web_page_number= ith,
                    main_content= ele['raw_content'],
                    url= ele['url']
                )
                for ith, ele in 
                enumerate(extract_results['results'])
            ]
        