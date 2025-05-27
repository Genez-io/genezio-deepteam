import asyncio
from deepteam import red_team
from deepteam.vulnerabilities import (
    Bias,
    Toxicity,
    GraphicContent

)
from deepteam.attacks.single_turn import PromptInjection
from deepeval.models import AnthropicModel



async def model_callback(input: str) -> str:
    await asyncio.sleep(13)
    
    model = AnthropicModel(
        model="claude-sonnet-4-20250514",
        temperature=0
    )
    response, _ = await model.a_generate(input)
    return response


bias = Bias(types=["race", "gender", "politics", "religion"])
toxicity = Toxicity(types=["insults", "profanity", "threats", "mockery"])
graphic_content = GraphicContent(types=["sexual content", "graphic content", "pornographic content"])

prompt_injection = PromptInjection()
attacks = [
    PromptInjection(weight=3),
]
t = red_team(
    model_callback=model_callback,
    vulnerabilities=[
        bias,
        toxicity,
        graphic_content
    ],
    attacks=attacks,
)

print(t.overview.to_df())