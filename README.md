# Quest project

## How to run

```
git clone

docker compose up
```

Access http://localhost:5173/

Login with the default user and password

```
user: user
password: password
```

Check if the toast for signin check-in should appear (TODO)



## What I manage to do

- Create microservices (Auth, Quest Catalog)
- API gateway and load balancer (traefik proxy)
- Implement an event queue (RabbitMQ)
- Dockerfiles and a dockercompose file to run all containers


## What is missing

- Kubernetes config
- CQRS on the Catalog
- Finish the Quest Processing
    - Right now it is just receiving the events but not doing the necessary logic to update the progress of the user on quests


## API login/access-token

This API will be called on sign in, this will trigger to send events to the processing-service:

```
    #Not new user
    if user.status == 1:
        event_in = Event(event_type="UserSignIn", user_id=user.user_id, timestamp=datetime.now())
        publish_event(event_in)

    #New user
    if user.status == 0:
        event_in = Event(event_type="NewUserSignIn", user_id=user.user_id, timestamp=datetime.now())
        publish_event(event_in)
        user_in = UserUpdate(status=1)
        crud.update_user(session=session, db_user=user, user_in=user_in)
```

Right now the auth and catalog services are implemented, but the processing service is not complete.
The processing service is just receiving the events via message queue (RabbitMQ).

The processing service was expected to:

- On receiving a NewUserSignIn event, create a UserQuestReward entry
    - Fetch Quest data from the Catalog Service
- On receiving a UserSignIn event, update the UserQuestReward entry
    - If the quest is completed:
        - Update the user diamond/gold on the Auth Service
        - Send a update to the frontend to popup a toast to inform the quest was completed
- On receiving any event, store it at the Event table


## Note

The FastAPI microservices and frontend were based on the [official FastAPI template](https://github.com/fastapi/full-stack-fastapi-template).