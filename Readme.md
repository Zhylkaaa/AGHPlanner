# AGHPlanner 

AGHPlanner is a tool that provides an easy and convenient way to manage the reservation of classrooms at AGH University. It also solves the nontrivial task of assigning rooms for lecture and lab groups without causing conflict for students and teachers.

We decided to divide the tool into two independent services: the [Reservation Service](#reservation-service) and the [Planner Service](#planner-service)

## Reservation Service

The reservation service is a web app that displays reserved and free time slots for each classroom in the building on a simple calendar.
(optional) It implements functionality for searching for classrooms that are free within certain times of day within a given date range.

- authorized users with low reservation access (LA) can request reservations for a classroom (for one use or periodically, e.g. every two weeks) that are approved/denied by admins. (Denying a pending reservation should optionally provide a reason, which is displayed to the user and probably looks something like [this](https://www.reddit.com/r/MurderedByWords/comments/ajioa3/that_time_governor_arnold_schwarzenegger_sent_a/))

- authorized users with high reservation access (HA) can make reservations without entering the verification queue. (TODO: how to deal with cases where a HA user's reservation conflicts with an LA user's request. I propose showing an alert to the HA user. {I propose sending a notification to the LA user as well. -- Mateusz})

- admins have access to an administrative panel with pending requests and can upload the base schedule to be displayed.

## Planner Service

####TODO
