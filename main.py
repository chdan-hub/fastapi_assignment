# main.py
from http.client import HTTPException
from idlelib.query import Query
from typing import Annotated

from fastapi import FastAPI, HTTPException, status, Path

from app.models.movies import MovieModel
from app.models.users import UserModel
from app.schemas.movies import MovieResponse, CreateMovieRequest, MovieSearchParams, MovieUpdateRequest

app = FastAPI()
UserModel.create_dummy()
UserModel.create_dummy()  # API 테스트를 위한 더미를 생성하는 메서드 입니다.

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)

# 영화 등록 API
@app.post('/movies', response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest):
    movie = MovieModel.create(**data.model_dump())
    return movie

# 전체 영화 검색 및 리스트 조회 API
@app.get('/movies', response_model=list[MovieResponse], status_code=200)
async def get_movies(query_params: Annotated[MovieSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}

    if valid_query:
        return MovieModel.filter(**valid_query)

    return MovieModel.all()

# 특정 영화 상세 조회 API
@app.get('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	return movie

#특정 영화 정보 수정 API
@app.patch('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def edit_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	movie.update(**data.model_dump())
	return movie

# 특정 영화 정보 삭제 API
@app.delete('/movies/{movie_id}', status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	movie.delete()
	return