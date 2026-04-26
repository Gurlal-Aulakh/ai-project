from agents import Agent, Runner


def build_concept_agent() -> Agent:
    return Agent(
        name="ConceptExplainerAgent",
        instructions="""
You explain AI and software concepts in very simple beginner-friendly language.
Use examples and avoid jargon. and at the end always say "Doodle do!!!!"
""",
        model="gpt-4.1",
    )


def build_project_agent() -> Agent:
    return Agent(
        name="ProjectGuideAgent",
        instructions="""
You explain this AI Phase 1/Phase 2 project to a beginner.
Focus on architecture, files, purpose, and next steps.
""",
        model="gpt-4.1",
    )


async def run_concept_agent(question: str) -> str:
    agent = build_concept_agent()
    result = await Runner.run(agent, question)
    return result.final_output


async def run_project_agent(question: str) -> str:
    agent = build_project_agent()
    result = await Runner.run(agent, question)
    return result.final_output