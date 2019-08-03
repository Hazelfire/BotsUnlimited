class EventController:
    async def describe(message):
        await client.send_message(
            channel,
            content="Certainly, the {} will be run from {} to {} \n Location: {}\n{}".format(
                event["summary"],
                parse_datetime(event["start"]["dateTime"]),
                parse_time(event["end"]["dateTime"]),
                event["location"],
                cleanhtml(event["description"]),
            ),
        )

    async def list(message):
        upcoming = "\n".join(
            [
                event["summary"] + ", " + parse_datetime(event["start"]["dateTime"])
                for event in events
            ]
        )
