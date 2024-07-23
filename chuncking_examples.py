
from langchain.text_splitter import CharacterTextSplitter

def load_doc():
    from langchain.document_loaders import Docx2txtLoader
    loader = Docx2txtLoader("Data/sample.docx")
    return loader.load()

def chunk_document():
    documents = load_doc()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    documents = text_splitter.split_documents(documents)

    print(len(documents))
    # for doc in documents:
    #     print(doc)
    #     print('-----------------------------------')

# chunk_document()


def unstructureddoc():
    from langchain.document_loaders import UnstructuredWordDocumentLoader
    from langchain.text_splitter import TokenTextSplitter

    loader = UnstructuredWordDocumentLoader("Data/sample.docx", mode="elements", strategy="fast",) 
    docs = loader.load()

    text_splitter = TokenTextSplitter(chunk_size=256, chunk_overlap=20)
    my_doc = text_splitter.split_documents(docs)

    print(len(my_doc))                        
    # print(my_doc)
# unstructureddoc()

def nltk():
    from langchain.text_splitter import NLTKTextSplitter
    text_splitter = NLTKTextSplitter(chunk_size=256, chunk_overlap=10)

    docs = text_splitter.split_documents(load_doc())
    print(len(docs))
    # for doc in docs:
    #     print(doc)
# nltk()


def load_doc_split():
    from langchain.document_loaders import Docx2txtLoader
    loader = Docx2txtLoader("Data/sample.docx")
    return loader.load_and_split()

def spacy():
    docs =  load_doc_split()

    texts = []
    for doc in docs:
        texts.append(doc.page_content)

    from langchain.text_splitter import SpacyTextSplitter
    text_splitter = SpacyTextSplitter(chunk_size=1000)
    chunks = text_splitter.split_text(''.join(texts))

    print(f"docs : {len(docs)}, Texts: {len(texts)}, chunks:{len(chunks)}")
    # print(chunks[0])
# spacy()

def reverse_char_text_split():
    docs =  load_doc_split()

    texts = []
    for doc in docs:
        texts.append(doc.page_content)

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 256,
        chunk_overlap  = 20
    )

    chunks = text_splitter.split_text(''.join(texts))
    print(f"docs : {len(docs)}, Texts: {len(texts)}, chunks:{len(chunks)}")
    print(chunks[0])
    
# reverse_char_text_split()

def mark_down():
    docs =  load_doc_split()

    texts = []
    for doc in docs:
        texts.append(doc.page_content)

    from langchain.text_splitter import MarkdownTextSplitter
    text_splitter = MarkdownTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 256,
        chunk_overlap  = 20
    )

    chunks = text_splitter.split_text(''.join(texts))
    print(f"docs : {len(docs)}, Texts: {len(texts)}, chunks:{len(chunks)}")
    print(chunks[0])
# mark_down()

def latex():
    docs =  load_doc_split()

    texts = []
    for doc in docs:
        texts.append(doc.page_content)

    from langchain.text_splitter import LatexTextSplitter
    text_splitter = LatexTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 256,
        chunk_overlap  = 20
    )

    chunks = text_splitter.split_text(''.join(texts))
    print(f"docs : {len(docs)}, Texts: {len(texts)}, chunks:{len(chunks)}")
    print(chunks[0])
latex()