"""Example configuration should be copied to meetup2xibo/config.py and edited."""


MEETUP_API_CONFIG = {

    # URL name for Meetup group
    "group_url_name": "NOVA-Makers",

    # Meetup API key
    "api_key": "zvbxrpl"
}

LOCATION_CONFIG = {

    # Default location
    "default_location": "TBD",

    # Location phrases and corresponding locations
    # (list longer phrases first)
    "location_phrases": [
        ("Classroom A and B", "Classroom A/B"),
        ("Classroom A/B", "Classroom A/B"),
        ("Classroom A", "Classroom A"),
        ("Classroom B", "Classroom B"),
        ("Conference room 1", "Conference Room 1"),
        ("Conference rm 1", "Conference Room 1"),
        ("Metalshop", "Metal Shop"),
        ("Metal shop", "Metal Shop"),
        ("Woodshop", "Woodshop"),
        ("Wood shop", "Woodshop"),
    ]

}

XIBO_DB_CONNECTION = {

    # Connection parameters
    # (see https://mysqlclient.readthedocs.io/user_guide.html#functions-and-attributes)
    "user": "xibo",
    "passwd": "zvbxrpl",
    "db": "xibo",

    # Required to save results
    "autocommit": True
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

# API code for Meetup event schedule dataset
XIBO_DATASET_CODE = "novalabsschedule"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
