#!/usr/bin/env python3
"""
Lakehouse Table Explorer CLI
A utility tool to explore Iceberg tables in your lakehouse setup with Nessie catalog and MinIO storage.
"""

import click
import os
import sys
from typing import Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint

from config import LakehouseConfig
from lakehouse_explorer import LakehouseExplorer

console = Console()

@click.group()
@click.option('--config', '-c', type=click.Path(exists=True), help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """Lakehouse Table Explorer - Explore your Iceberg tables across namespaces"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    try:
        if config:
            lakehouse_config = LakehouseConfig.from_file(config)
        else:
            # Try to load from environment variables
            try:
                lakehouse_config = LakehouseConfig.from_env()
            except ValueError as e:
                console.print(f"[red]Configuration error: {e}[/red]")
                console.print("\n[yellow]You can either:")
                console.print("1. Set environment variables (see README)")
                console.print("2. Use --config flag with a configuration file")
                console.print("3. Run 'lakehouse-explorer setup' to create a sample config[/yellow]")
                sys.exit(1)
        
        ctx.obj['config'] = lakehouse_config
        ctx.obj['explorer'] = LakehouseExplorer(lakehouse_config)
        
    except Exception as e:
        if verbose:
            import traceback
            console.print(f"[red]Error: {traceback.format_exc()}[/red]")
        else:
            console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--output', '-o', default='config.json', help='Output file for configuration')
def setup(output):
    """Create a sample configuration file"""
    config = LakehouseConfig(
        nessie_uri="", s3_endpoint="", s3_access_key="", 
        s3_secret_key="", warehouse_path=""
    )
    config.create_sample_config(output)

@cli.command()
@click.pass_context
def list_namespaces(ctx):
    """List all available namespaces"""
    explorer = ctx.obj['explorer']
    
    namespaces = explorer.list_namespaces()
    
    if not namespaces:
        console.print("[yellow]No namespaces found[/yellow]")
        return
    
    console.print(f"\n[bold green]Found {len(namespaces)} namespace(s):[/bold green]")
    for i, namespace in enumerate(namespaces, 1):
        namespace_str = ".".join(namespace) if namespace else "default"
        console.print(f"{i:2d}. {namespace_str}")

@cli.command()
@click.option('--namespace', '-n', help='Specific namespace to list tables from')
@click.pass_context
def list_tables(ctx, namespace):
    """List all tables, optionally filtered by namespace"""
    explorer = ctx.obj['explorer']
    
    if namespace:
        # Convert string namespace to tuple
        namespace_tuple = tuple(namespace.split('.')) if namespace != 'default' else ()
        tables = explorer.list_tables_in_namespace(namespace_tuple)
        
        if not tables:
            console.print(f"[yellow]No tables found in namespace '{namespace}'[/yellow]")
            return
        
        console.print(f"\n[bold green]Tables in namespace '{namespace}':[/bold green]")
        for i, table in enumerate(tables, 1):
            console.print(f"{i:2d}. {table}")
    else:
        # List all tables across all namespaces
        all_tables = explorer.get_all_tables()
        
        if not all_tables:
            console.print("[yellow]No tables found[/yellow]")
            return
        
        total_tables = sum(len(tables) for tables in all_tables.values())
        console.print(f"\n[bold green]Found {total_tables} table(s) across {len(all_tables)} namespace(s):[/bold green]")
        
        for namespace, tables in all_tables.items():
            namespace_str = ".".join(namespace) if namespace else "default"
            console.print(f"\n[bold cyan]{namespace_str}:[/bold cyan]")
            for table in tables:
                console.print(f"  • {table}")

@cli.command()
@click.pass_context
def overview(ctx):
    """Show an overview of all namespaces and tables in tree format"""
    explorer = ctx.obj['explorer']
    explorer.display_namespace_tree()

@cli.command()
@click.argument('table_path')
@click.pass_context
def info(ctx, table_path):
    """Show detailed information about a specific table
    
    TABLE_PATH should be in format: namespace.table_name or just table_name for default namespace
    """
    explorer = ctx.obj['explorer']
    
    # Parse table path
    if '.' in table_path:
        parts = table_path.split('.')
        namespace = tuple(parts[:-1])
        table_name = parts[-1]
    else:
        namespace = ()  # Default namespace
        table_name = table_path
    
    explorer.display_table_info(namespace, table_name)

@cli.command()
@click.argument('table_path')
@click.option('--limit', '-l', default=10, type=int, help='Number of rows to preview')
@click.pass_context
def preview(ctx, table_path, limit):
    """Preview data from a specific table
    
    TABLE_PATH should be in format: namespace.table_name or just table_name for default namespace
    """
    explorer = ctx.obj['explorer']
    
    # Parse table path
    if '.' in table_path:
        parts = table_path.split('.')
        namespace = tuple(parts[:-1])
        table_name = parts[-1]
    else:
        namespace = ()  # Default namespace
        table_name = table_path
    
    explorer.display_table_preview(namespace, table_name, limit)

@cli.command()
@click.argument('search_term')
@click.pass_context
def search(ctx, search_term):
    """Search for tables by name across all namespaces"""
    explorer = ctx.obj['explorer']
    
    matches = explorer.search_tables(search_term)
    
    if not matches:
        console.print(f"[yellow]No tables found matching '{search_term}'[/yellow]")
        return
    
    console.print(f"\n[bold green]Found {len(matches)} table(s) matching '{search_term}':[/bold green]")
    for namespace, table_name in matches:
        namespace_str = ".".join(namespace) if namespace else "default"
        console.print(f"  • {namespace_str}.{table_name}")

@cli.command()
@click.pass_context
def interactive(ctx):
    """Start interactive mode for exploring tables"""
    explorer = ctx.obj['explorer']
    
    console.print(Panel.fit(
        "[bold blue]🚀 Welcome to Lakehouse Explorer Interactive Mode![/bold blue]\n"
        "You can now explore your tables interactively.",
        border_style="blue"
    ))
    
    while True:
        console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
        console.print("1. 📋 List all namespaces")
        console.print("2. 📊 Show table overview")
        console.print("3. 🔍 Search tables")
        console.print("4. ℹ️  Get table info")
        console.print("5. 👁️  Preview table data")
        console.print("6. 🚪 Exit")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"], default="6")
        
        if choice == "1":
            namespaces = explorer.list_namespaces()
            if namespaces:
                console.print(f"\n[bold green]Found {len(namespaces)} namespace(s):[/bold green]")
                for i, ns in enumerate(namespaces, 1):
                    ns_str = ".".join(ns) if ns else "default"
                    console.print(f"{i:2d}. {ns_str}")
            else:
                console.print("[yellow]No namespaces found[/yellow]")
        
        elif choice == "2":
            explorer.display_namespace_tree()
        
        elif choice == "3":
            search_term = Prompt.ask("Enter search term")
            matches = explorer.search_tables(search_term)
            if matches:
                console.print(f"\n[bold green]Found {len(matches)} table(s):[/bold green]")
                for ns, table in matches:
                    ns_str = ".".join(ns) if ns else "default"
                    console.print(f"  • {ns_str}.{table}")
            else:
                console.print(f"[yellow]No tables found matching '{search_term}'[/yellow]")
        
        elif choice == "4":
            table_path = Prompt.ask("Enter table path (namespace.table or just table)")
            if '.' in table_path:
                parts = table_path.split('.')
                namespace = tuple(parts[:-1])
                table_name = parts[-1]
            else:
                namespace = ()
                table_name = table_path
            explorer.display_table_info(namespace, table_name)
        
        elif choice == "5":
            table_path = Prompt.ask("Enter table path (namespace.table or just table)")
            limit = int(Prompt.ask("Number of rows to preview", default="10"))
            
            if '.' in table_path:
                parts = table_path.split('.')
                namespace = tuple(parts[:-1])
                table_name = parts[-1]
            else:
                namespace = ()
                table_name = table_path
            
            explorer.display_table_preview(namespace, table_name, limit)
        
        elif choice == "6":
            console.print("[green]👋 Goodbye![/green]")
            break

if __name__ == '__main__':
    cli()
