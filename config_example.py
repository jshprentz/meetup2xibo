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


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
