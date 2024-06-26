from crewai import Agent, Task, Crew, Process

from langchain_community.llms import Ollama
ollama_llm = Ollama(model="llama3:instruct")

from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

researcher = Agent(
    role='researcher',
    goal='Search the internet for the information requested',
    backstory="""
    You are a researcher. Using the information in the task, you find out some of the most popular facts about the topic along with some of the trending aspects.
    You provide a lot of information thereby allowing a choice in the content selected for the final blog.
    """,
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=ollama_llm
)
writer = Agent(
    role='writer',
    goal='Craft compelling content on a set of information provided by the researcher.',
    backstory="""You are a writer known for your humorous but informative way of explaining. 
    You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True,
    llm=ollama_llm
)
task1 = Task(
    description="""Research about open source LLMs vs closed source LLMs. 
    Your final answer MUST be a full analysis report""",
    agent=researcher,
    expected_output='A refined finalized version of the blog post in markdown format'
)
task2 = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant facts and differences between open-source LLMs and closed-source LLMs.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, and avoid complex words so it doesn't sound like AI.
    Your final answer MUST be the full blog post of at least 4 paragraphs.
    The target word count for the blog post should be between 1,500 and 2,500 words, with a sweet spot at around 2,450 words.""",
    agent=writer,
    expected_output='A refined finalized version of the blog post in markdown format'
)
crew = Crew(
agents=[researcher, writer],
tasks=[task1, task2],
verbose=2,
)
result = crew.kickoff()
print(result)
