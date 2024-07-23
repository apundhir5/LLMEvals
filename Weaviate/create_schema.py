import weaviate
import const

def create_shema(schemaClass, schemaDesc, schemaProperties):
    client = weaviate.Client(const.WEAVIATE_URL)

    current_collection_names = {collection["class"] for collection in client.schema.get()["classes"]}
    if schemaClass in current_collection_names:
        client.schema.delete_class(schemaClass)
        print(f"Existing {schemaClass} data deleted!")

    nltkchunk_class_schema = {
        "class": schemaClass,
        "vectorizer": "text2vec-transformers",
        "description": schemaDesc,
        "properties": schemaProperties
    }
    
    client.schema.create_class(nltkchunk_class_schema)
    print(f"{schemaClass} schema created!")

def create_contract_schema():
    properties = [
                    {
                        "name": "filename",
                        "dataType": ["string"],
                        "description": "File Name",
                    },
                    {
                        "name": "text",
                        "dataType": ["text"],
                        "description": "Page Text",
                    },
                    {
                        "name": "pagenumber",
                        "dataType": ["int"],
                        "description": "Page Number",
                    }
                ]
    create_shema(const.WEAVIATE_CONTRACT_CLASS, "Data Entered as pages", properties)

def create_contract_summary_schema():
    properties = [
                {
                    "name": "filename",
                    "dataType": ["string"],
                    "description": "File Name",
                },
                {
                    "name": "text",
                    "dataType": ["text"],
                    "description": "Summary",
                }
            ]
    create_shema(const.WEAVIATE_CONTRACT_SUMMARY_CLASS, "Document Summary", properties)

if __name__ == "__main__":
    create_contract_schema()
    create_contract_summary_schema()