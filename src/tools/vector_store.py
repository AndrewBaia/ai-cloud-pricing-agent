"""
Vector store tool using ChromaDB for storing and retrieving cloud pricing information.
"""
import chromadb
from chromadb.config import Settings
import json
from typing import List, Dict, Any, Optional
from loguru import logger
import uuid


class VectorStoreTool:
    """ChromaDB-based vector store for cloud pricing and documentation."""

    def __init__(self, persist_directory: str = "./data/chromadb"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection_name = "cloud_pricing_docs"
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the ChromaDB collection with pricing data."""
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except Exception:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(self.collection_name)
            self._populate_initial_data()
            logger.info(f"Created new collection: {self.collection_name}")

    def _populate_initial_data(self):
        """Populate the collection with initial cloud pricing documentation."""
        documents = [
            {
                "id": str(uuid.uuid4()),
                "content": "AWS P3 instances are optimized for machine learning and high-performance computing workloads. They feature NVIDIA Tesla V100 GPUs with 16GB or 32GB of GPU memory.",
                "metadata": {
                    "provider": "AWS",
                    "instance_family": "P3",
                    "gpu_type": "V100",
                    "use_case": "machine_learning"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Azure NC series VMs are designed for compute-intensive and graphics-intensive applications. They feature NVIDIA Tesla K80 GPUs.",
                "metadata": {
                    "provider": "Azure",
                    "instance_family": "NC",
                    "gpu_type": "K80",
                    "use_case": "graphics_compute"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Google Cloud Platform offers GPU instances with various NVIDIA GPU types. They provide flexible pricing models including on-demand and preemptible instances.",
                "metadata": {
                    "provider": "GCP",
                    "gpu_types": "K80, P100, V100, A100",
                    "pricing_models": "on-demand, preemptible",
                    "use_case": "flexible_compute"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Cost optimization strategies for GPU instances: 1) Use spot/preemptible instances for non-critical workloads, 2) Choose the right instance size based on your workload requirements, 3) Consider reserved instances for long-term usage.",
                "metadata": {
                    "topic": "cost_optimization",
                    "strategies": "spot_instances, right_sizing, reserved_instances",
                    "applicable_providers": "AWS, Azure, GCP"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "content": "AWS pricing: P3.2xlarge costs $3.06/hour, P3.8xlarge costs $12.24/hour, P3.16xlarge costs $24.48/hour in us-east-1 region.",
                "metadata": {
                    "provider": "AWS",
                    "region": "us-east-1",
                    "instances": "p3.2xlarge, p3.8xlarge, p3.16xlarge",
                    "prices": "3.06, 12.24, 24.48"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Azure pricing: NC6 costs $0.90/hour, NC12 costs $1.80/hour, NC24 costs $3.60/hour in East US region.",
                "metadata": {
                    "provider": "Azure",
                    "region": "East US",
                    "instances": "NC6, NC12, NC24",
                    "prices": "0.90, 1.80, 3.60"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "content": "GCP pricing: n1-standard-8 with K80 GPU costs $0.70/hour, n1-standard-16 costs $1.40/hour, n1-standard-32 costs $2.80/hour in us-central1.",
                "metadata": {
                    "provider": "GCP",
                    "region": "us-central1",
                    "instances": "n1-standard-8, n1-standard-16, n1-standard-32",
                    "prices": "0.70, 1.40, 2.80"
                }
            }
        ]

        # Add documents to collection
        ids = [doc["id"] for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]

        self.collection.add(
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )

        logger.info(f"Populated collection with {len(documents)} initial documents")

    def search_similar(self, query: str, n_results: int = 5,
                      where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for similar documents in the vector store.

        Args:
            query: Search query string
            n_results: Number of results to return
            where: Metadata filters

        Returns:
            Search results with documents, metadata, and distances
        """
        logger.info(f"Vector search - Query: '{query}', Results: {n_results}, Filters: {where}")

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        logger.info(f"Found {len(results['documents'][0]) if results['documents'] else 0} similar documents")

        return {
            "query": query,
            "results": results
        }

    def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Add a new document to the vector store.

        Args:
            content: Document content
            metadata: Document metadata

        Returns:
            Document ID
        """
        doc_id = str(uuid.uuid4())

        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )

        logger.info(f"Added document with ID: {doc_id}")
        return doc_id

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID.

        Args:
            doc_id: Document ID

        Returns:
            Document data or None if not found
        """
        try:
            result = self.collection.get(ids=[doc_id])
            if result["documents"]:
                return {
                    "id": doc_id,
                    "content": result["documents"][0],
                    "metadata": result["metadatas"][0]
                }
        except Exception as e:
            logger.error(f"Error retrieving document {doc_id}: {e}")

        return None

    def update_document(self, doc_id: str, content: str, metadata: Dict[str, Any]):
        """
        Update an existing document.

        Args:
            doc_id: Document ID
            content: New content
            metadata: New metadata
        """
        self.collection.update(
            ids=[doc_id],
            documents=[content],
            metadatas=[metadata]
        )
        logger.info(f"Updated document: {doc_id}")

    def delete_document(self, doc_id: str):
        """
        Delete a document from the vector store.

        Args:
            doc_id: Document ID to delete
        """
        self.collection.delete(ids=[doc_id])
        logger.info(f"Deleted document: {doc_id}")

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "persist_directory": self.persist_directory
        }
