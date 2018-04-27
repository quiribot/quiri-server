from adapt.intent import IntentBuilder
from quiri.skills import Answer, QuiriSkill, intent_handler


class WeatherSkill(QuiriSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add()

    def add(self):
        weather_keyword = ["weather"]

        for wk in weather_keyword:
            self.engine.register_entity(wk, "WeatherKeyword")

        weather_types = ["snow", "rain", "wind", "sleet", "sun"]

        for wt in weather_types:
            self.engine.register_entity(wt, "WeatherType")

        locations = ["Seattle", "San Francisco", "Tokyo"]

        for loc in locations:
            self.engine.register_entity(loc, "Location")

    weather_intent = IntentBuilder("WeatherIntent")\
        .require("WeatherKeyword")\
        .optionally("WeatherType")\
        .require("Location")\
        .build()

    @intent_handler(weather_intent)
    async def run(self, q):
        print(q)
        answer = Answer()
        answer.set_answer("this is weather intent", f"loc: {q.Location}")
        return answer


def register(add_skill):
    add_skill(WeatherSkill)
