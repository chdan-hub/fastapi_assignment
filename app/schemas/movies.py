# app/schemas/movies.py
from dataclasses import Field
from typing import Annotated

from pydantic import BaseModel

# 영화 등록 API
class CreateMovieRequest(BaseModel):
	"""
	영화 등록 API 요청 모델
	- 클라이언트가 영화 title, playtime, genre(list[str])를 전달할 때 사용
	"""
	title: str
	playtime: int
	genre: list[str]

# 영화 응답 모델
class MovieResponse(BaseModel):
	"""
	영화 응답 모델
	- API 응답으로 반환되는 영화 정보
	- 필드: id, title, playtime, genre
	"""
	id: int
	title: str
	playtime: int
	genre: list[str]

# 전체 영화 검색 및 리스트 조회 API
class MovieSearchParams(BaseModel):
	"""
	영화 검색 파라미터 모델
	- Query Params:
	    - title: 영화 제목 (부분 일치 검색 가능)
	    - genre: 장르 (하나의 문자열만 선택 가능)
	- 조건:
	    - title 또는 genre 중 하나라도 존재하면 해당 조건으로 검색
	    - 둘 다 없으면 전체 영화 리스트 반환
	"""
	title: str | None = None
	genre: str | None = None

# 특정 영화 정보 수정 API
class MovieUpdateRequest(BaseModel):
	"""
	영화 수정 요청 모델
	- Request Body:
	    - title: 영화 제목 (선택적)
	    - playtime: 상영 시간 (0보다 커야 함, 선택적)
	    - genre: 장르 리스트 (선택적)
	- 조건:
	    - 모든 필드는 선택적이며, 전달된 값만 업데이트 됨
	    - playtime이 주어진 경우 반드시 0보다 커야 함
	"""
	title: str | None = None
	playtime: Annotated[int, Field(gt=0)] | None = None
	genre: list[str] | None = None