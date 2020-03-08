# AGHPlanner 

is a tool to prowide easy and convenient way to to manage reservation of class rooms and solve not trivial task of assigning classes to rooms. We decided to devide the tool to two independent services: [Reservation Service](#reservation-service) and [Planner Service](#planner-service)

## Reservation Service

implements simple calendar view to show already reserved and free time gaps for each class room available in building.
(oprionaly) implements functionality to search for free class rooms at given day and/or time/time gap(like month)

- authorized users with low reservation access (LA) can request for class room (for 1 time use or for time gap) to be approved/declined by admins (declination should probably contain option to provide reason, which looks like [this](https://www.reddit.com/r/MurderedByWords/comments/ajioa3/that_time_governor_arnold_schwarzenegger_sent_a/) commonly)

- authorized users with high reservation access (HA) can reserve class rooms right away (TODO: how to deal with cases where HA user reserves requested by LA user. I propose to showing allert to HA user)

- admins have panel with requests and can upload schedule to be displayed.

## Planner Service

####TODO