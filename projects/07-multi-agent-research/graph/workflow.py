import time

from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState
from agents.research import research_agent
from agents.technical import technical_agent
from agents.industry import industry_agent
from agents.critic import critic_agent
from agents.writer import writer_agent

def research_node(state: ResearchState):
    start = time.perf_counter()

    result = research_agent(state["query"])

    print(f"Research: {time.perf_counter() - start:.2f}s")

    return {
        "research_results": result
    }


def technical_node(state: ResearchState):
    try:
        result = technical_agent(state["query"])

        return {
            "technical_results": result
        }

    except Exception as e:
        return {
            "technical_results": f"Technical agent failed: {e}"
        }


def industry_node(state: ResearchState):
    start = time.perf_counter()

    result = industry_agent(state["query"])

    print(f"Industry: {time.perf_counter() - start:.2f}s")

    return {
        "industry_results": result
    }

def critic_node(state: ResearchState):
    return {
        'critic_feedback': critic_agent(
            state['research_results'],
            state['technical_results'],
            state['industry_results']
        )
    }

def writer_node(state: ResearchState):
    return {
        "final_answer": writer_agent(
            state["query"],
            state["research_results"],
            state["technical_results"],
            state["industry_results"],
            state["critic_feedback"],
        )
    }


builder = StateGraph(ResearchState)

builder.add_node('research',research_node)
builder.add_node('technical',technical_node)
builder.add_node('industry',industry_node)

builder.add_node('critic',critic_node)
builder.add_node("writer", writer_node)

builder.add_edge(START, 'research')
builder.add_edge(START, 'technical')
builder.add_edge(START, 'industry')

builder.add_edge('research', 'critic' )
builder.add_edge('technical', 'critic' )
builder.add_edge('industry', 'critic' )

builder.add_edge( 'critic' , 'writer')
builder.add_edge('writer', END)


graph = builder.compile()