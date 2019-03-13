"""Nova Labs Configuration"""


MEETUP_API_CONFIG = {

    # URL name for Meetup group
    "group_url_name": "NOVA-Makers",

    # Meetup API key
    "api_key": "7c43778407249123e7a7c396a2d1578"
}

LOCATION_CONFIG = {

    # Default location
    "default_location": "Nova Labs",

    # Location phrases and corresponding locations
    # (list longer phrases first)
    "location_phrases": [
        ("Classrooms A and B", "Classroom A/B"),
        ("Classroom A and B", "Classroom A/B"),
        ("Classroom A/B", "Classroom A/B"),
        ("Classroom A", "Classroom A"),
        ("Classroom B", "Classroom B"),
        ("CAD Lab", "CAD Lab"),
        ("Computer Lab", "Computer Lab"),
        ("Conference room 1", "Conference Room 1"),
        ("Conference room 2", "Conference Room 2"),
        ("Conference room 3", "Conference Room 3"),
        ("Conference rm 1", "Conference Room 1"),
        ("Conference rm 2", "Conference Room 2"),
        ("Conference rm 3", "Conference Room 3"),
        ("Orange Bay", "Orange Bay"),
        ("Orange room", "Orange Bay"),
        ("Blacksmithing", "Blacksmithing Alley outside behind Nova Labs"),
        ("out back", "Blacksmithing Alley outside behind Nova Labs"),
        ("outback", "Blacksmithing Alley outside behind Nova Labs"),
        ("Metalshop", "Metal Shop"),
        ("Metal shop", "Metal Shop"),
        ("Woodshop", "Woodshop"),
        ("Wood shop", "Woodshop"),
    ]

}

XIBO_DB_CONNECTION = {

    # Connection parameters
    # (see https://mysqlclient.readthedocs.io/user_guide.html#functions-and-attributes)
    "user": "cms",
    "passwd": "69F5A6Rf6YyUNHTu",
    "host": "localhost",
    "port": 3606,
    "db": "cms",

    # Required to save results
    "autocommit": True
}

XIBO_DB_CONFIG = {

    # API code for Meetup event schedule dataset
    "xibo_dataset_code": "novalabsschedule",

    # Delete events this number of minutes after ending
    "delete_minutes_after_event": 120
}

XIBO_DB_COLUMN_NAMES = {

    # Event column names defined via the Xibo web interface
    "meetup_id": "Meetup ID",
    "name": "Name",
    "location": "Location",
    "start_time": "ISO Start Time",
    "end_time": "ISO End Time",

    # Internal ID number used by Xibo
    "xibo_id": "id"
}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
