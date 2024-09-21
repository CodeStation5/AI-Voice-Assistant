import enum
from typing import Annotated
from livekit.agents import llm
import logging

# Hold temperature logs at confirmation level
logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)


class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"

# LLM decides what to use by the context given in the function
class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        # Default temperature set for each room
        self._temperature = {
            Zone.LIVING_ROOM: 21,
            Zone.BEDROOM: 21,
            Zone.KITCHEN: 21,
            Zone.BATHROOM: 21,
            Zone.OFFICE: 21,
        }

    # Use Python generator to specify function to be called by LLM
    # Description is used to describe the function in the LLM to respond to user queries
    @llm.ai_callable(description="Get the temperature in a specific room")
    def get_temperature(
        self, zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")]
    ):
        logger.info("Get temp - zone %s", zone)
        temp = self._temperature[Zone(zone)]
        return f"The temperature in the {zone} is {temp}C"

    @llm.ai_callable(description="Set the temperature in a specific room")
    def set_temperature(
        self,
        zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")],
        temp: Annotated[int, llm.TypeInfo(description="The temperature to set")],
    ):
        logger.info("Set temo - zone %s, temp: %s", zone, temp)
        self._temperature[Zone(zone)] = temp
        return f"The temperature in the {zone} is now {temp}C"