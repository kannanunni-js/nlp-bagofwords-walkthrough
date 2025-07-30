from contextlib import asynccontextmanager, suppress

import anyio.to_thread
from sklearn.feature_extraction.text import CountVectorizer
from fastapi import FastAPI
from loguru import logger

from rich.console import Console
from rich.table import Table

from core.config import settings
from tools.starch_approach import load_corpus_from_file,get_bow_representation

@asynccontextmanager
async def event_manager(application: FastAPI):
    """
    Async context manager for managing the lifetime of the FastAPI application.

    This context manager is responsible for setting up the database, initializing the
    language model, and setting up the rate limiter for the application.

    :param application: The FastAPI application instance.
    """
    console = Console()
    table = Table(title=application.title)
    table.add_column("Status", justify="center", style="cyan")
    table.add_column("Method", justify="center", style="green")
    table.add_column("Path", justify="left", style="magenta", no_wrap=True)
    for route in application.routes:
        with suppress(AttributeError):
            if "/v1" in route.path or "/auth" in route.path:
                table.add_row("[✓]", list(route.methods)[0], route.path)

    console.print(table, justify="center")

    try:
        corpus = load_corpus_from_file(settings.CORPUS_FILE_PATH)

        scratch_vectors, vocab = get_bow_representation(corpus)

        vectorizer = CountVectorizer(lowercase=True)
        vectorizer_vectors = vectorizer.fit_transform(corpus).toarray()

        application.state.corpus = corpus
        application.state.vocab = vocab
        application.state.corpus_vectors = scratch_vectors
        application.state.vectorizer = vectorizer
        application.state.vectorizer_vectors = vectorizer_vectors

        logger.success("Corpus loaded and vectorized successfully using both methods")

    except Exception as e:
        logger.error(f"Error loading corpus: {e}")
        application.state.corpus = []
        application.state.corpus_vectors = []
        application.state.vocab = []

    # set up the thread limiter for the application
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = settings.CONCURRENT_THREAD_COUNT
    yield
    # close the database client
    logger.success("Instance Shutdown")
