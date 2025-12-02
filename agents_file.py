from langchain_core.messages import convert_to_messages
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
# from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from tools_module import search_tool, say_hello

# from IPython.display import display, Image

load_dotenv()

############# Creating the Agents #############

research_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[search_tool],
    prompt=(
        "You are a research agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with research-related tasks, DO NOT do any math.\n"
        "- After you're done with your tasks, respond to the supervisor directly.\n"
        "- You must always include links to your sources when available.\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="research_agent",
)

restaurant_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[search_tool],
    prompt=(
        "You are a restaurant agent.\n"
        "You are responsible for providing information about restaurants and dining options.\n"
        "Please look at the user's query for context.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with restaurant-related tasks, DO NOT engage with anyting that is beyond the scope of finding food in the erea specified by the user.\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Provide a link to the restaurant's homepage where possible"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="restaurant_agent",
)

supervisor = create_supervisor(
    model=init_chat_model("openai:gpt-4.1"),
    agents=[research_agent, restaurant_agent], # , math_agent
    tools=[say_hello],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a research agent. Assign research-related tasks to this agent\n"
        "- a restaurant agent. Assign restaurant-related tasks and queries to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()
############## End of Agent Definitions ###############


############## Utility Functions ##############
def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)


def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print("\n")
############## End of Utility Functions ##############


def main():
    while True:
        print("Type 'quit' to exit.")
        user_input = input("\nYou: ").strip()
        if user_input == "quit":
            break
        for chunk in supervisor.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            },
        ):
            pretty_print_messages(chunk, last_message=True)

        # final_message_history = chunk["supervisor"]["messages"]


if __name__ == "__main__":
    # Uncomment this to save/create the visual graph
    with open("graph.png", "wb") as f:
        f.write(supervisor.get_graph().draw_mermaid_png())
    # main()
