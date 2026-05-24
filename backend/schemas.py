from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="待分析的评论文本")


class DimensionResult(BaseModel):
    label_id: int
    sentiment: str


class AnalyzeResponse(BaseModel):
    content: str
    predictions: dict
    summary: dict[str, int]
    suggestions: dict | None = None


class HistoryItem(BaseModel):
    id: int
    content_preview: str
    positive_count: int
    negative_count: int
    neutral_count: int
    not_mentioned_count: int
    created_at: str


class HistoryListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[HistoryItem]


class HistoryDetailResponse(BaseModel):
    id: int
    content: str
    predictions: dict
    positive_count: int
    negative_count: int
    neutral_count: int
    not_mentioned_count: int
    created_at: str


class SystemStatusResponse(BaseModel):
    model_name: str
    device: str
    gpu_name: str
    model_loaded: bool
    num_labels: int
    num_classes: int


class BatchTaskResponse(BaseModel):
    task_id: str
    status: str
    total: int
    processed: int


class LabelInfo(BaseModel):
    key: str
    display_name: str
    category: str
