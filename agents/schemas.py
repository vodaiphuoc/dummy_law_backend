from pydantic import BaseModel, Field, HttpUrl

class LawDocModel(BaseModel):
    doc_number: str
    url: str
    content: str = Field(
        default=None,
        description="Content of the law doc"
    )

class PAGE_MAIN_CONTENT(BaseModel):
    r"""
    Schema for main content of the web page
    """
    web_page_number: int = Field(
        description="the order of web page input"
    )

    main_content: str = Field(
        description="main content output after filtering"
    )

    url: str = Field(
        description="the url of the web page"
    )

    law_docs: None | list[LawDocModel] = Field(
        default=None,
        frozen=False,
        description="per page can contains some original law documents"
    )

class ClassificationResult(BaseModel):
    """
    Represents the result of classifying a user's question.
    """

    is_legal_question: bool = Field(
        description="Whether the question is related to law, notarization, or authentication."
    )
    reason: str = Field(description="A brief explanation for the classification.")
