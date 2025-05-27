from deepteam import red_team
from deepteam.vulnerabilities import Bias
from deepteam.vulnerabilities.custom import CustomVulnerability
from deepteam.attacks.single_turn import PromptInjection, ROT13, MathProblem
from deepeval.models import GeminiModel
from deepteam.metrics import BiasMetric
from prompt import generate_race_bias_attack_prompt, generate_gender_bias_attack_prompt, generate_politics_bias_attack_prompt, generate_religion_bias_attack_prompt

async def model_callback(input: str) -> str:

    model = GeminiModel(
        model_name="gemini-2.5-pro-preview-05-06",
        api_key="your api key",
        temperature=0.7
    )
    return model.generate(input)

# Create custom vulnerabilities for each bias type
race_bias = CustomVulnerability(
    name="Race Bias",
    types=["racial_stereotypes", "racial_discrimination"],
    custom_prompt=generate_race_bias_attack_prompt(max_goldens=5, purpose="bias testing"),
    metric_class=BiasMetric
)

gender_bias = CustomVulnerability(
    name="Gender Bias",
    types=["gender_stereotypes", "gender_discrimination"],
    custom_prompt=generate_gender_bias_attack_prompt(max_goldens=5, purpose="bias testing"),
    metric_class=BiasMetric
)

politics_bias = CustomVulnerability(
    name="Political Bias",
    types=["political_stereotypes", "political_discrimination"],
    custom_prompt=generate_politics_bias_attack_prompt(max_goldens=5, purpose="bias testing"),
    metric_class=BiasMetric
)

religion_bias = CustomVulnerability(
    name="Religious Bias",
    types=["religious_stereotypes", "religious_discrimination"],
    custom_prompt=generate_religion_bias_attack_prompt(max_goldens=5, purpose="bias testing"),
    metric_class=BiasMetric
)

prompt_injection = PromptInjection()
rot_13 = ROT13(weight=1)
math_problem = MathProblem()

red_team(
    model_callback=model_callback,
    vulnerabilities=[
        race_bias,
        gender_bias,
        politics_bias,
        religion_bias,
    ],
    attacks=[prompt_injection],
)

