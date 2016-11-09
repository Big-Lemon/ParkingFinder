from tornado.web import Application

from ParkingFinder.handlers import HealthHandler
from ParkingFinder.handlers import FacebookGraphLoginHandler
from ParkingFinder.handlers.user_information import UserInformationHandler
from ParkingFinder.handlers.parking_space import (
    ParkingSpaceNearbyFetchHandler,
    ParkingSpaceReserveHandler
)

app = Application([
    (r'/health', HealthHandler),
    (r'/auth/facebook', FacebookGraphLoginHandler),
    (r'/user/(.*)', UserInformationHandler),
    (r'/parkingSpace/reserve/(.*)', ParkingSpaceReserveHandler),
    (r'/parkingSpace/nearby/(.*)', ParkingSpaceNearbyFetchHandler),
    (r'/user/logout', FacebookGraphLoginHandler),
])

"""
==============================================================================
/user/{user_id}?access_token={access_token}
    GET  get user detail
        return format:
        {
            "first_name": "hong",
            "last_name": "li",
            "activated_vehicle": "235JFK4"
            # this can be saved in cache of frontend
            "profile_picture_url": "www.xxx.sss/ssss"
            "owned_vehicles": [
                {
                    "plate": "235JFK4",
                    "brand": "honda",
                    "model": "civic",
                    "color": "white",
                    "year": "2008"
                }
            ]
        }

==============================================================================
/user/{user_id}?access_token={access_token}

    POST update user info
        request format:
        {
            # all fields in the request payload are marked as request update
            "activated_vehicle": "124FJK3"
            "new vehicle":
            {
                "plate": "124FJK3",
                "brand": "toyota",
                "model": "corolla",
                "color": "black",
                "year": "2016"
            }

        }

==============================================================================
/auth/facebook?access_token

    GET
        - login through facebook oauth2
        return format:
        {
            "access_token": {
                "user_id": "123456"
                "expires_at": 1231231231,
                "issued_at": 1231231231,
                "access_token": access_token
            },
            "user": {
                "user_id": "123456"
                "first_name": "hong",
                "last_name": "li",
                "profile_picture_url": "www.xxx.sss/ssss"

                # if activated_vehicle is Null, registration required before
                # other services
                "activated_vehicle": null
                "owned_vehicles": [
                ]
            }
        }

==============================================================================
/parkingSpace/nearby/{user_id}?x={x}&y={y}&radius={r}&access_token={access_token}

    GET
        - get parking space around the coordinate(x,y) with radius r
        return format:
        {}

==============================================================================

/parkingSpace/reserve/{user_id}?access_token={access_token}

    POST
        - reserve a parking space around the coordinate(x,y) or
         destination name(UCLA parking lot 7,level 1) with radius r

        request format:
            {
                "coordinate": {
                    "x": 1002.232,
                    "y": 2104.642,
                },
                "destination" {  # optional
                    "name": "UCLA parking lot 7",
                    "level": 1,  # optional
                }
                # TODO: any addition information required
                "meta" : {}
            }

        return format:
            {
            }

==============================================================================

/parkingSpace/post/{user_id}?access_token={access_token}

    POST
        - Post owned parking space to other users

        request format:
        {}

        return format:
        {}

==============================================================================

/parkingSpace/reserve/{user_id}?access_token={access_token}

    POST
        - Reserve a parking space posted by other users

        request format:
        {}

        return format:
        {
            # car's detail
        }

==============================================================================

/parkingSpace/checkIn/{user_id}?access_token={access_token}

    POST
        - check in a parking space

        request format:
            # client should provide either parking space id or a new discovered parking space
            {
                "parkingSpaceId": "1233123123"
            }
                or
            {
                "x": "123123.21312",
                "y": "123123.21312",
                "parkingSpace": {
                    "name": "ucla parking lot 4",
                    "level": "4", # optional
                    # ..... addition information
                }
            }

        return format:
            {}

==============================================================================

/parkingSpace/checkout/{user_id}?access_token={access_token}

    POST
        - check out a parking space (leaving)
        request format:
            {
                "parkingSpaceId": "1234566213"
            }

        return format:
            {
                ""

            }

==============================================================================

/parkingSpace/status/{parkingSpaceId}?access_token={access_token}
    # have to check if parkingSpace with parking space id is belong to user with
    # access_token in query params

    GET
        Return the status of transition of a parking space

        return format:
            {
                "status": "reserved"
            }

/parkingSpace/status/extend?access_token={access_token}

    POST
        # extend the waiting time of a posted parkingSpace by the owner of the space
        request format:
            {
                "parkingSpaceId": "123123",
                "extendTime": 123123  # datetime.timedelta
            }


==============================================================================

/parkingSpace/location/user_id?access_token={access_token}
    # validate the permission to achieve other user's id
    POST
        Return the location of other user

        request format:
            {
                # current location of the user
                "x": "123123.2112",
                "y": "123523.2135",

                # query location of other user
                "user_id": "1231231"
            }

        return format:
            {
                "x": "24235.2132",
                "y": "12340945"
            }

"""
