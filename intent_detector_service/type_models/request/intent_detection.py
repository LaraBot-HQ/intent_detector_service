from typing import Optional

from pydantic import BaseModel, Field


class PatternMatcherObject(BaseModel):
    id: str = Field(description="Identifier for the match value you want to match, example: TIMES, MUSIC, SONGS, etc")
    patterns: list[dict] = Field(
        description=(
            "Based on your action, give a general match pattern in order to extract entities "
            "more accurately, example of a match pattern for music by an artist:"
            "\n<some optional proper noun> <some proper noun> <by> <some proper noun>"
            "\nby_pattern = [ "
            "{'POS': 'PROPN', 'OP': '?'}, {'POS': 'PROPN', 'OP': '?'}, {'POS': 'PROPN'}, "
            "{'ORTH': '''''', 'OP': ''?''},{'LOWER': 'song','OP': ''?''}, {'LOWER': 'by'}, "
            "{'POS': 'PROPN'},{'POS': 'PROPN', 'OP': ''?''} ]"
            "\n This parameter is optional in case it is not passed the engine will try to extract"
            "entities as best as it can"
        )
    )


class ActionObject(BaseModel):
    action: str = Field(
        description="Plain text with the action key, example:\n"
                    "Larabot, I would like to hear some adele music"
    )
    matchers: Optional[list[PatternMatcherObject]] = Field(
        description="List of patterns for extracting entities",
        default_factory=list
    )


class IntentPayload(BaseModel):
    message: str = Field(description="original user message")
    actions: list[ActionObject] = Field(description="list of actions to validate")
