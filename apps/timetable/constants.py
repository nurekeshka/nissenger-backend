from enum import Enum


TIMETABLE_DATABASE_LINK = 'https://{}.edupage.org/rpr/server/maindbi.js?__func=mainDBIAccessor'
TIMETABLE_DATABASE_DATA = {
    "__args": [
        None,
        2021,
        {},
        {
            "op": "fetch",
            "needed_part": {
                "teachers": [
                    "short"
                ],
                "classes": [
                    "short"
                ],
                "classrooms": [
                    "short"
                ],
                "subjects": [
                    "name"
                ],
                "periods": [
                    "period",
                    "starttime",
                    "endtime"
                ],
                "dayparts": [
                    "starttime",
                    "endtime"
                ]
            },
            "needed_combos": {}
        }
    ],
    "__gsh": "00000000"
}

class TimetableIndexes(Enum):
    teachers = 0
    subjects = 1
    classrooms = 2
    classes = 3
    periods = 4
    dayparts = 5
