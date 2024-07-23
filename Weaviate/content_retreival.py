import weaviate
from typing import List
import const
from data_classes import ContractContent 
from data_classes import ContractSummary 

class ContractRetriever():
    def __init__(self, url: str):
        self.client = weaviate.Client(url)

    def get_batch_with_cursor(self, cursor=None):
        query = (
            self.client.query.get(const.WEAVIATE_CONTRACT_CLASS, ["filename", "text", "pagenumber"])
            # Optionally retrieve the vector embedding by adding `vector` to the _additional fields
            # .with_additional(["id vector"])
            .with_limit(10)
        )

        # print(f"cursor --- {cursor})

        # if cursor is not None:
        #     return query.with_after(cursor).do()
        # else:
        return query.do()
    

    def retrieve(self, query: str, top_k: int = 1) -> List[ContractContent]:
        query_results = (
            self.client.query
            .get(const.WEAVIATE_CONTRACT_CLASS, ["filename", "text", "pagenumber"])
            .with_near_text({"concepts": [query]})
            .with_additional(['certainty'])
            .with_limit(top_k)
            .do()
        )["data"]["Get"][const.WEAVIATE_CONTRACT_CLASS]

        evidence = list(map(
            lambda result: ContractContent(
                passage=result["text"],
                filename=result["filename"],
                confidence=result["_additional"]["certainty"],
                pagenumber=result["pagenumber"]
            ),
            query_results,
        ))

        return evidence
    
class ContractSummaryRetriever():
    def __init__(self, url: str):
        self.client = weaviate.Client(url)

    def retrieve(self, query: str, top_k: int = 1) -> List[ContractSummary]:
        query_results = (
            self.client.query
            .get(const.WEAVIATE_CONTRACT_SUMMARY_CLASS, ["filename", "text"])
            .with_near_text({"concepts": [query]})
            .with_additional(['certainty'])
            .with_limit(top_k)
            .do()
        )["data"]["Get"][const.WEAVIATE_CONTRACT_SUMMARY_CLASS]

        evidence = list(map(
            lambda result: ContractSummary(
                passage=result["text"],
                filename=result["filename"],
                confidence=result["_additional"]["certainty"]
            ),
            query_results,
        ))

        return evidence
