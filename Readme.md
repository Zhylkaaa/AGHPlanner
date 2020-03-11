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

simple service that allows to:

- upload data containing information about classes, time slots and classrooms. Example:

```python
{
	'classes': [class(name="ASD", type=W, is_AB = False, lecturer="Faliszewski"), 
		class(name="Algebra", type=C, is_AB=False, lecturer="Przybyło"), 
		class(name="Python", type=L, is_AB=True, lecturer="Kaleta")]
	'classrooms': [room(name='1.38', type=W), room(name='3.22', type=C), room(name='3.27d', type=L&C)]
	'timeslots': [slot(8:00, 9:30), slot(9:35, 11:05), slot(11:15, 12:45), slot(12:50, 14:20)]
}
```

- than assign each class to classroom using blackbox function inside the service (probably some kind of SAT solver?) and show results using some kind of calendar view or indicate that it's impossible to do so

- download results as csv

