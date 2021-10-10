from ..db.session import db_session
from ..models.diary import Diary
from ..models.photo import Photo
from ..utils.util import Util
from ..dto.diary import (
    DiaryCardListResponseDto,
    DiaryCountResponseDto,
    DiaryCreateResponseDto,
    DiaryCreateRequestDto,
    DiaryDeleteResponseDto,
    DiaryListRequestDto,
    DiaryListResponseDto,
    DiaryRetrieveRequestDto,
    DiaryRetrieveResponseDto,
    DiaryUpdateRequestDto,
    DiaryUpdateResponseDto,
)
from datetime import datetime
from typing import Optional, List
from fastapi import File, UploadFile
from werkzeug.utils import secure_filename
import random
import string


def save_changes(data):
    try:
        db_session.add(data)
        db_session.commit()
    except Exception as e:
        print(e)


def save_new_diary(
    user_id: int, input_dto: DiaryCreateRequestDto, photos: List[UploadFile] = File(...)
) -> DiaryCreateResponseDto:

    today_diary = (
        db_session.query(Diary).filter(Diary.created_at == datetime.now()).first()
    )

    if not today_diary:

        new_diary = Diary(
            user_id,
            input_dto.context,
            input_dto.emotion,
            input_dto.value,
            input_dto.date,
        )

        save_changes(new_diary)

    else:
        pass

    created_photos = []

    string_pool = string.ascii_letters + string.digits

    try:

        for photo in photos:
            extension = secure_filename(photo.filename).split(".")[1]
            file = photo.file

            filename = (
                str(datetime.now()).replace(" ", "").replace(".", "")
                + "".join([random.choice(string_pool) for _ in range(10)])
                + "."
                + extension
            )

            url = Util.s3upload(file, filename)

            created_photos.append(url)
    except:
        pass

    new_diary.photos = created_photos
    response = new_diary.to_dict()

    return DiaryCreateResponseDto(**response)


def get_all_diaries(input_dto: DiaryListRequestDto) -> DiaryListResponseDto:
    year = input_dto.year
    month = input_dto.month

    diary = []

    if year != None and month != None:
        start = str(year) + "-" + str(month).zfill(2) + "-01"
        end = str(year) + "-" + str(int(month) + 1).zfill(2) + "-01"
        diaries = (
            db_session.query(Diary.diary_id, Diary.date)
            .filter(Diary.date.between(start, end))
            .order_by(Diary.date)
            .all()
        )
    elif year != None and month == None:
        start = str(year) + "-01-01"
        end = str(int(year) + 1) + "-01-01"
        diaries = (
            db_session.query(Diary.diary_id, Diary.date)
            .filter(Diary.date.between(start, end))
            .order_by(Diary.date)
            .all()
        )
    else:
        diaries = (
            db_session.query(Diary.diary_id, Diary.date).order_by(Diary.date).all()
        )

    diary = [{"diary_id": diary.diary_id, "date": str(diary.date)} for diary in diaries]

    return diary


def get_a_diary(
    diary_id: int, input_dto: DiaryRetrieveRequestDto
) -> DiaryRetrieveResponseDto:
    pass


def delete_diary(diary_id: int) -> DiaryDeleteResponseDto:
    pass


def update_diary(
    diary_id: int, input_dto: DiaryUpdateRequestDto
) -> DiaryUpdateResponseDto:
    pass


def count_diary(user_id: int) -> DiaryCountResponseDto:
    pass


def diary_card_list(user_id: int) -> DiaryCardListResponseDto:
    pass
