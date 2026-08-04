# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# LLM 관련 라이브러리
from langchain_openai import OpenAI, OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import Pinecone, PineconeVectorStore
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import uvicorn

load_dotenv()

app = FastAPI()

#권한설정
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], # 모든 도메인 허용
  allow_methods=["*"], # 모든 HTTPS 메소드 허용 (GET, POST, PUT, DELETE 등)
  allow_headers=["*"]  # 모든 헤더 허용
)

# 1. 모델 및 벡터 DB import
embeddings = OpenAIEmbeddings(model = 'text-embedding-3-large')

# pinecone 초기화
index_name = 'my-tax-index'
vector_store = PineconeVectorStore(index_name = index_name, embedding=embeddings)

# llm 모델 불러오기
llm = ChatOpenAI(model = 'gpt-4o', temperature = 0)

# 페르소나 설정 (System Prompt)
system_prompt = """
당신은 대한민국의 AI 세무사로 소득세에 대한 전문가입니다.
사용자 질문에 대해서는 아래 [법령 근거]를 바탕으로 정중하고 명확하게 답변합니다.

[답변 원칙]
1. 반드시 제공된 [법령 근거] 안에서만 답변하며, 추측하지 마세요.
2. 답변 시작 시 "네, 소득세 관련하여 문의주셨군요. 해당 내용을 법령에 근거하여 설명해 드리겠습니다."와 같은 정중한 어조를 사용하세요.
3. 근거가 되는 조항(예: 소득세법 제1조)을 반드시 언급하세요.
4. 법령에 내용이 없을 경우 "죄송합니다만, 현재 제가 가진 자료에서는 해당 내용을 찾을 수 없습니다."라고 안내하세요.

[법령 근거]:
{context}
"""

qa_prompt = ChatPromptTemplate.from_messages([
  SystemMessagePromptTemplate.from_template(system_prompt),
  HumanMessagePromptTemplate.from_template("{question}")
])

# 2. 메모리 설정
memory = ConversationBufferMemory(
  memory_key = "chat_history",
  return_messages = True,
  output_key = "answer"
)

# 3. 체인 설정
qa_chain = ConversationalRetrievalChain.from_llm(
  llm = llm,
  retriever = vector_store.as_retriever(search_kwargs = {'k' : 3}),
  memory = memory,
  return_source_documents = True,
  combine_docs_chain_kwargs = {"prompt" : qa_prompt}
)

class TaxRequest(BaseModel):
  message : str

### 위와 같은 Chain 방식은 Deprecated됨
### LCEL로 직접적으로 LangChain을 구성하는게 표준
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# retriever = vector_store.as_retriever(search_kwargs={'k': 3})

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# 이런 구조를 만들어서 context와 question에 값을 넣어야 함!
# 입력: "소득세율이 어떻게 되나요?"
#         ↓
# {"context": (검색 + 가공된 관련 법령 텍스트), "question": "소득세율이 어떻게 되나요?"}

# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | qa_prompt
#     | llm
#     | StrOutputParser()
# )

# answer = rag_chain.invoke("소득세율이 어떻게 되나요?")

# 4. FastAPI 엔드포인트 설정
@app.post('/chat')
async def chat(request: TaxRequest):
  try:
    result = qa_chain.invoke({"question" : request.message})

    # print(result.keys()) 로 key 값들 확인하기
    return {"answer" : result["answer"],
            "sources" : [doc.page_content for doc in result["source_documents"]]}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"에러 발생 : {str(e)}")