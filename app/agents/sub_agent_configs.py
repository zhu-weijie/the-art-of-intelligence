from .sub_agent import SubAgent

research_sub_agent = SubAgent(
    name="research-agent",
    description="Used to research more in-depth questions. Only give this researcher one topic at a time.",
    prompt="You are a dedicated researcher. Your job is to conduct research based on the user's question and provide a detailed answer.",
)

critique_sub_agent = SubAgent(
    name="critique-agent",
    description="Used to critique a report. You can find the report at `final_report.md`.",
    prompt="You are a dedicated editor. You are being tasked to critique a report.",
)

# A list to easily import all configs
all_sub_agents = [research_sub_agent, critique_sub_agent]
