
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#Get API Keys from .env file
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["ANTHROPIC_API_KEY"] = os.getenv('ANTHROPIC_API_KEY')


#Initialize Model Depending on Model Choice
def Initialize_Model(Service,ModelChoice,name,sys_prompt):
    if Service == 'Anthropic':
        if ModelChoice == "Claude 3.5 Sonnet":
            model = init_chat_model("claude-3-5-sonnet-latest", model_provider="anthropic")
        else:
            model = init_chat_model("claude-3-5-haiku-latest", model_provider="anthropic")
    else:
        if ModelChoice == 'GPT-4o':
            model = init_chat_model("gpt-4o", model_provider="openai")
        elif ModelChoice == 'GPT-4o-mini':
            model = init_chat_model("gpt-4o-mini", model_provider="openai")
        elif ModelChoice == 'o1':
            model = init_chat_model("o1", model_provider="openai")
        else:
            model = init_chat_model("o1-mini", model_provider="openai")

    if sys_prompt == '':
        prompt_template = ChatPromptTemplate.from_messages(
    [( "system",
        "The User's name is" + name,),
        MessagesPlaceholder(variable_name="messages"),])
    else:

        prompt_template = ChatPromptTemplate.from_messages(
        [( "system",
            "The User's name is" + name + ". Also please" + sys_prompt,),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
            # Define a new graph
    workflow = StateGraph(state_schema=MessagesState)


        # Define the function that calls the model
    def call_model(state: MessagesState):
        prompt = prompt_template.invoke(state)
        response = model.invoke(prompt)
        return {"messages": response}


        # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

        # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app

#Function Call to chat with the model
def Chat_Model(Chatbot,prompt):
    config = {"configurable": {"thread_id": "abc123"}}
    input_messages = [HumanMessage(prompt)]
    output = Chatbot.invoke({"messages": input_messages}, config)
    return output["messages"][-1].content





