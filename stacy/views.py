from sarah.models import Event
from discordmvc.actions import reply, listen, query


def list_plan(client, message, context):
    events = list(context.db.query(Event).all())
    yield reply(events=events)


def create_event(client, message, context):
    name_response = yield query(stage="name")
    name = name_response.content

    description_response = yield query(name=name, stage="description")
    description = description_response.content

    context.db.add(Event(name=name, description=description))

    yield reply(name=name, stage="end")


def delete_event(client, message, context):
    events = list(context.db.query(Event).all())

    name_response = yield query(stage="list-events", events=events)
    name = name_response.content

    event = context.db.query(Event).filter(Event.name == name).first()
    if event:
        confirm_response = yield query(stage="confirm", event=event)
        confirm = confirm_response.content
        if confirm.upper() == "YES":
            context.db.query(Event).filter(Event.name == name).delete()

            yield reply(stage="done")
        else:
            yield reply(stage="cancel")

    else:
        yield reply(stage="missing")
