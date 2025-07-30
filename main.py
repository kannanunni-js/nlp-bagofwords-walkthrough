import os
import click
import uvicorn
from core.config import settings

@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "production"], case_sensitive=False),
    default="local",
    help="The environment to run the application in. Can be either 'local' or 'production'.",
)
@click.option(
    "--log-level",
    type=click.Choice(["critical", "error", "warning", "info", "debug", "trace"], case_sensitive=False),
    default="info",
    help="The log level to set. Can be one of 'critical', 'error', 'warning', 'info', 'debug', or 'trace'.",
)
@click.option(
    "--host",
    type=click.STRING,
    default="127.0.0.1",
    help="The host to run the application on. Defaults to '127.0.0.1'.",
)
@click.option(
    "--port",
    type=click.INT,
    default="8000",
    help="The port to run the application on. Defaults to '8000'.",
)
@click.option(
    "--reload",
    type=click.BOOL,
    is_flag=True,
    default=False,
    help="Whether to reload the application on changes. Defaults to 'off'.",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
    help="Whether to enable debug mode. Defaults to 'off'.",
)
@click.option(
    "--proxy",
    type=click.BOOL,
    is_flag=True,
    default=False,
    help="Whether to enable proxy mode. Defaults to 'off'.",
)
def main(
    env: str,
    log_level: str,
    host: str,
    port: int,
    reload: bool,
    debug: bool,
    proxy: bool,
):
    os.environ.setdefault("ENVIRONMENT", env)
    os.environ.setdefault("LOG_LEVEL", log_level)
    os.environ.setdefault("DEBUG", ("off", "on")[debug])

    from tools.service_logger import init_logger
    from tools.proj_banner import print_project_banner

    init_logger(settings.LOG_LEVEL)
    print_project_banner(
        project_title="Bag of Words (BoW) NLP",
        description="""
            Bag of Words (BoW) is a foundational NLP technique for text representation, 
            used to convert text into numerical feature vectors. This repo includes:
            
            - A from-scratch implementation using basic Python
            - An optimized implementation using scikit-learn
            - Jupyter notebooks with step-by-step explanations and results
            """,
        features=[
            "From-scratch BoW implementation in pure Python",
            "BoW with scikit-learn's CountVectorizer",
            "Text preprocessing: lowercasing, stopwords removal, punctuation cleaning",
            "Cosine similarity for comparing documents",
            "Jupyter notebook visualizations and tests",
            "Clean and commented codebase for learning purposes",
        ],
        repo_name="Bag of Words Git Repo",
        repo_link="https://github.com/kannanunni-js/nlp-bagofwords-walkthrough",
    )

    uvicorn.run(
        app="server:app",
        host=host,
        port=port,
        reload=reload,
        proxy_headers=proxy,

        loop="uvloop" if os.name == "posix" else "asyncio",

        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL,
        forwarded_allow_ips=settings.FORWARDED_ALLOW_IPS,
        ws_max_queue=settings.WS_MAX_QUEUE,

        use_colors=True,
        server_header=False,
    )

if __name__ == '__main__':
    main()