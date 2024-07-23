import json
from typing import List
from content_retreival import ContractRetriever, ContractSummaryRetriever
import const

def get_batch_with_cursor(client, class_name, class_properties, batch_size, cursor=None):

    query = (
        client.query.get(class_name, class_properties)
        # Optionally retrieve the vector embedding by adding `vector` to the _additional fields
        .with_additional(["id vector"])
        .with_limit(batch_size)
    )

    if cursor is not None:
        return query.with_after(cursor).do()
    else:
        return query.do()
    

# weaviate_client = weaviate.Client(url=const.WEAVIATE_URL)
# response = weaviate_client.schema.get(const.WEAVIATE_CONTRACT_CLASS)
# print(json.dumps(response, indent=2))


# contractRetreiver  = ContractRetriever(const.WEAVIATE_URL)
# print(contractRetreiver.retrieve("What are the transfer terms?", 2))

contractSummaryRetreiver  = ContractSummaryRetriever(const.WEAVIATE_URL)
print(contractSummaryRetreiver.retrieve("What are the transfer terms?", 2))
      