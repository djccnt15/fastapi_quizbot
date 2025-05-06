from pydantic import BaseModel, ConfigDict, Field


class ResourceId(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class QuizCreate(BaseModel):
    question: str = Field(..., title="퀴즈 질문", examples="🇰🇷 대한민국의 수도는?")
    content: str = Field(..., title="퀴즈 내용", examples="1️1️⃣ 서울\n2️⃣ 인천\n3️⃣ 부산\n4️⃣ 대구")
    answer: int = Field(..., title="정답", examples=1)


class Quiz(QuizCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
