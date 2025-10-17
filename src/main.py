#!/usr/bin/env python3
"""
Main entry point for the AI Cloud Pricing Agent.
"""
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .utils import setup_logging, Config
from .agents import CloudPricingAgent
from .tools import MockExternalAPIServer
from loguru import logger


console = Console()


def validate_config():
    """Validate configuration before starting."""
    if not Config.validate_config():
        console.print("[red]Configuration validation failed. Please check your settings.[/red]")
        sys.exit(1)


def start_external_api_server():
    """Start the mock external API server."""
    import uvicorn
    from .tools import MockExternalAPIServer

    console.print("[blue]Starting mock external API server...[/blue]")

    server = MockExternalAPIServer()
    uvicorn.run(
        server.app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )


@click.group()
def cli():
    """AI Cloud Pricing Agent - Analyze cloud GPU pricing across providers."""
    pass


@cli.command()
@click.option("--model", default=None, help="Model to use (gpt-4, claude-3-5-sonnet, etc.)")
@click.option("--api-server/--no-api-server", default=False, help="Start mock API server")
def interactive(model, api_server):
    """Start interactive mode for querying the agent."""
    validate_config()
    setup_logging()

    if api_server:
        console.print("[yellow]Note: API server will run in a separate process. Start it with 'python -m src.main api-server'[/yellow]")

    # Use specified model or default
    model_name = model or Config.DEFAULT_MODEL
    console.print(f"[green]Starting AI Cloud Pricing Agent with model: {model_name}[/green]")

    try:
        agent = CloudPricingAgent(
            model_name=model_name,
            chroma_db_path=Config.CHROMA_DB_PATH,
            external_api_url=Config.EXTERNAL_API_BASE_URL,
            external_api_key=Config.EXTERNAL_API_KEY
        )

        console.print("[green]Agent initialized successfully![/green]")
        console.print("[dim]Type 'quit' or 'exit' to end the session.[/dim]")
        console.print()

        while True:
            try:
                user_input = console.input("[bold blue]You:[/bold blue] ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break

                if not user_input:
                    continue

                console.print("[bold green]Agent:[/bold green] Thinking...")

                with console.status("[bold green]Processing your query..."):
                    response = agent.analyze_query(user_input)

                # Display response in a nice panel
                response_panel = Panel(
                    response,
                    title="[bold blue]Agent Response[/bold blue]",
                    border_style="blue"
                )
                console.print(response_panel)
                console.print()

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user. Goodbye![/yellow]")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                console.print(f"[red]An error occurred: {e}[/red]")
                console.print("[dim]Please try again or check the logs.[/dim]")

    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        console.print(f"[red]Failed to initialize agent: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.option("--model", default=None, help="Model to use")
@click.option("--output", "-o", type=click.Path(), help="Save output to file")
def query(query, model, output):
    """Process a single query and exit."""
    validate_config()
    setup_logging()

    model_name = model or Config.DEFAULT_MODEL

    try:
        agent = CloudPricingAgent(
            model_name=model_name,
            chroma_db_path=Config.CHROMA_DB_PATH,
            external_api_url=Config.EXTERNAL_API_BASE_URL,
            external_api_key=Config.EXTERNAL_API_KEY
        )

        console.print(f"[green]Processing query with model: {model_name}[/green]")

        with console.status("[bold green]Analyzing query..."):
            response = agent.analyze_query(query)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(f"Query: {query}\n\nResponse:\n{response}")
            console.print(f"[green]Response saved to: {output}[/green]")
        else:
            response_panel = Panel(
                response,
                title="[bold blue]Agent Response[/bold blue]",
                border_style="blue"
            )
            console.print(response_panel)

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def api_server():
    """Start the mock external API server."""
    console.print("[green]Starting Mock External API Server[/green]")
    console.print("[dim]This provides simulated cloud pricing comparison data.[/dim]")
    console.print("[dim]Server will be available at http://localhost:8001[/dim]")
    console.print()

    try:
        start_external_api_server()
    except KeyboardInterrupt:
        console.print("\n[yellow]API server stopped.[/yellow]")


@cli.command()
def config():
    """Show current configuration."""
    Config.print_config()


@cli.command()
def stats():
    """Show agent statistics."""
    validate_config()
    setup_logging()

    try:
        agent = CloudPricingAgent(
            model_name=Config.DEFAULT_MODEL,
            chroma_db_path=Config.CHROMA_DB_PATH,
            external_api_url=Config.EXTERNAL_API_BASE_URL,
            external_api_key=Config.EXTERNAL_API_KEY
        )

        stats = agent.get_agent_stats()

        console.print("[bold blue]Agent Statistics[/bold blue]")
        console.print(f"Model: {stats['model']}")
        console.print(f"Vector Store: {stats['vector_store_stats']['collection_name']}")
        console.print(f"Documents: {stats['vector_store_stats']['document_count']}")
        console.print(f"Tools Available: {len(stats['tools_available'])}")
        console.print("Tools:", ", ".join(stats['tools_available']))

    except Exception as e:
        console.print(f"[red]Error getting stats: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
