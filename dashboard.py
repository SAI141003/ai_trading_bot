# 📁 dashboard.py — Live Trading Dashboard using rich

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pandas as pd
import os
import datetime

console = Console()

console.clear()
console.rule("[bold green]AI Trading Bot Dashboard")

# 📄 Load trade log
if not os.path.exists("trade_logs.csv"):
    console.print("[red]No trade logs found.[/red]")
    exit()

trades = pd.read_csv("trade_logs.csv")
if trades.empty:
    console.print("[yellow]No trades placed yet.[/yellow]")
    exit()

# 📊 Show recent trades
table = Table(title="Today's Trades")
table.add_column("Time", style="dim")
table.add_column("Symbol")
table.add_column("Type")
table.add_column("Strike")
table.add_column("SecID")

for _, row in trades.tail(10).iterrows():
    time = row['timestamp'].split()[1][:5]
    table.add_row(time, row['symbol'], row['type'], str(row['strike']), str(row['security_id']))

# 📦 Show exits if available
exit_section = "[bold red]No exits yet.[/bold red]"
if os.path.exists("exit_trades.csv"):
    exits = pd.read_csv("exit_trades.csv")
    if not exits.empty:
        exit_table = Table(title="Today's Exits")
        exit_table.add_column("Time", style="dim")
        exit_table.add_column("Symbol")
        exit_table.add_column("Price")
        for _, row in exits.tail(5).iterrows():
            time = row['timestamp'].split()[1][:5]
            exit_table.add_row(time, row['symbol'], f"₹{row['exit_price']}")
        exit_section = exit_table

# 🧠 Show AI signal trend (mock example)
signal_graph = "[green]↑ BUY CALL[/green] → [red]↓ BUY PUT[/red] → [yellow]HOLD"

# 📦 Show Panel Summary
summary = Panel.fit(signal_graph, title="[bold blue]AI Signal Trend", border_style="blue")

console.print(table)
console.print(exit_section)
console.print(summary)
console.rule("[bold cyan]End of Dashboard")

