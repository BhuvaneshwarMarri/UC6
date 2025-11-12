### Importing Libraries
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from langgraph.graph import StateGraph, START, END


from typing import TypedDict

from dotenv import load_dotenv
load_dotenv()

### Defining LLM
llm = ChatOpenAI(
    model="gpt-4.1"
)

### Defining Embeddings function
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

### Defining State
class State(TypedDict):
    file_name: str
    file_path: str
    file_type: str
    file_content: list[Document]
    file_splits: list[Document]

### Defining Nodes
def load_file(state: State) -> State:
    try:
        loader = UnstructuredExcelLoader(state['file_path'], mode='elements')
        print(f"File Content: {loader.load()}")
        return {'file_content': loader.load()}

    except Exception as e:
        print(f"Error in load_file node: {e}")

def split_content(state: State) -> State:
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            separators=['\n', '\n\n', ',', '.', ' ']
        )

        file_splits = text_splitter.split_documents(state['file_content'])

        print(f"File Splits: {file_splits}")
        
        return {'file_splits': file_splits}

    except Exception as e:
        print(f"Error in split_content: {e}")

def embeddings_node(state: State) -> None:
    try:
        vdb = Chroma( 
            embedding_function=embeddings,
            persist_directory='vectorstore',
            collection_name=state['file_name']
        )

        vdb.add_documents(state['file_splits'])
    except Exception as e:
        print(f"Error in embeddings_node: {e}")

### Defining StateGraph
stateGraph = StateGraph(State)

### Adding Nodes
stateGraph.add_node('loader', load_file)
stateGraph.add_node('splitter', split_content)
stateGraph.add_node('embeddings', embeddings_node)

### Adding Edges
stateGraph.add_edge(START, 'loader')
stateGraph.add_edge('loader', 'splitter')
stateGraph.add_edge('splitter', 'embeddings')
stateGraph.add_edge('embeddings', END)

### Compiling StateGraph
tickets_graph = stateGraph.compile()