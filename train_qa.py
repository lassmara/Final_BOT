
import numpy as np
from keybert import KeyBERT
import fitz
import os
import openai
from langchain.embeddings import OpenAIEmbeddings
kw_model = KeyBERT()
from langchain_core.documents.base import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import io
import matplotlib.pyplot as plt

os.environ["OPENAI_API_KEY"] = "key"

docs = []
embedding_function = OpenAIEmbeddings()
keyword_images = {}
TXT = []

def extract_text_and_images(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        # Extract text from the page
        text = page.get_text()
        #print(f"Text from page {page_number + 1}:")
        #print(text)
        docs.append(Document(text))
        key_words = kw_model.extract_keywords(text)
        TXT.append(text)
        #print(f"Key words from the text are : {key_words}")
        # Extract images from the page
        images = page.get_images(full=True)

        if images:
            #keyword_images['.'.join(key_words)] = images
            lst = []
            for i in key_words:
                lst.append(i[0])
            string = '.'.join(lst)
            keyword_images[string] = []
            #print(f"Images from page {page_number + 1}:")
            for img_index, img_info in enumerate(images):
                xref = img_info[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_format = base_image["ext"]

                with open(f"page_{page_number + 1}_image_{img_index + 1}.{image_format}", "wb") as image_file:
                    image_file.write(image_bytes)
                    keyword_images[string].append(image_bytes)
                #print(f"Image saved: page_{page_number + 1}_image_{img_index + 1}.{image_format}")
        #else:
           # print(f"No images found on page {page_number + 1}")

    # Close the PDF document
    pdf_document.close()

pdf_path = r"D:/VSCODE/INTEREXT/Cat/ChatBOT/HTMLWorks/Ander Baher_Internal Guidelines.pdf"
extract_text_and_images(pdf_path)

embedding_function = OpenAIEmbeddings()

# load docs into Chroma
vector_db = Chroma.from_documents(docs, embedding_function, persist_directory='persist_directory_path')

# Helpful to force a save
vector_db.persist()

# get db connection
vector_db_connection = Chroma(persist_directory='persist_directory_path', embedding_function=embedding_function)

# create a retriever
retriever = vector_db_connection.as_retriever(search_kwargs={"k": 4})

# create embeddings
embeddings = OpenAIEmbeddings()

# create embeddings filter
embeddings_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)

# create a compression retriever filter using retriever and embeddings
compression_retriever_filter = ContextualCompressionRetriever(
    base_compressor=embeddings_filter, base_retriever=retriever
)
def Q_A(question):
    

    llm = ChatOpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=compression_retriever_filter,
                                    verbose=True)

    answer = qa(question)
    ans=answer['result']
    return ans

"""target_keywords = kw_model.extract_keywords(answer['result'])


p2 = []
for string in keyword_images.keys():
    print(string.split('.'))
p2.append(string.split('.'))

# Function to compute cosine similarity between two lists
def compute_similarity(list1, list2):
    # Convert lists to sets to remove duplicates
    set1 = set(list1)
    set2 = set(list2)

    # Create a vocabulary containing all unique tokens from both lists
    vocabulary = set1.union(set2)

    # Create vectors for both lists
    vector1 = [1 if token in set1 else 0 for token in vocabulary]
    vector2 = [1 if token in set2 else 0 for token in vocabulary]

    # Compute cosine similarity between the two vectors
    similarity = cosine_similarity([vector1], [vector2])[0][0]
    return similarity

target_keys = target_keywords
for i in range(len(target_keys)):
    target_keys[i] = target_keys[i][0]
# Compute similarity between l1 and each list in l2
similarities = []
for list2 in p2:
    similarity = compute_similarity(target_keys, list2)
    similarities.append(similarity)

# Print similarities
for i, similarity in enumerate(similarities):
    print(f"Similarity between l1 and l2[{i}]: {similarity}")

sim = np.array(similarities)

i=0
print(answer['result'])
for key, value in keyword_images.items():
    if i==sim.argmax(axis=0):
        img_bytes = value[0]
    img_stream = io.BytesIO(img_bytes)

    # Open the image using PIL
    image = Image.open(img_stream)

    # Convert image to numpy array
    image_array = np.array(image)

    # Display the image using matplotlib
    plt.imshow(image_array)
    plt.axis('off')  # Turn off axis
    plt.show()"""
