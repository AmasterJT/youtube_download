#!/usr/bin/env python3
import os
import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import print as rprint
from yt_dlp import YoutubeDL

app = typer.Typer()
console = Console()

def obtener_info_video(url: str) -> dict:
    """Obtiene información del vídeo antes de descargar"""
    opciones_info = {"quiet": True, "no_warnings": True}
    with YoutubeDL(opciones_info) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def descargar_con_progreso(url: str, carpeta: Path, calidad: str, solo_audio: bool):
    """Descarga con barra de progreso rica"""
    formatos = {
        "mejor": "bestvideo+bestaudio/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "audio": "bestaudio/best"
    }
    
    # ✅ CORREGIDO: opciones DENTRO de la función y con formato dinámico
    opciones = {
        "format": formatos[calidad] if not solo_audio else formatos["audio"],
        "merge_output_format": "mp4" if not solo_audio else "mp3",
        "outtmpl": str(carpeta / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
    }
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Descargando...", total=None)
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                progress.update(task, description=f"📥 {d.get('filename', 'Desconocido')} ({d.get('_percent_str', '0%')})")
            elif d['status'] == 'finished':
                progress.update(task, description=f"✅ {d['filename']}")
        
        opciones['progress_hooks'] = [progress_hook]
        with YoutubeDL(opciones) as ydl:
            ydl.download([url])
        progress.update(task, description="🎉 ¡Completado!")

@app.command()
def descargar(
    url: str = typer.Argument(..., help="URL del vídeo"),
    carpeta: Path = typer.Option(Path("videos"), "--carpeta", "-o", help="Carpeta de salida"),
    calidad: str = typer.Option("mejor", "--calidad", "-q", help="Calidad (mejor, 1080p, 720p, audio)"),
    solo_audio: bool = typer.Option(False, "--audio", "-a", help="Solo descargar audio (MP3)")
):
    """🔥 Descarga vídeos de YouTube en HD con sonido"""
    try:
        if not ("youtube.com" in url or "youtu.be" in url):
            rprint("[red]❌ URL no válida. Usa enlaces de YouTube.[/red]")
            raise typer.Exit(code=1)
        
        carpeta.mkdir(parents=True, exist_ok=True)
        
        rprint(Panel.fit("📺 Obteniendo información...", border_style="blue"))
        info = obtener_info_video(url)
        
        duracion = f"{int(info.get('duration', 0)//60):02d}:{int(info.get('duration', 0)%60):02d}"
        rprint(Panel.fit(
            f"[bold cyan]🎥 {info.get('title', 'Sin título')}\n"
            f"👤 {info.get('uploader', 'Desconocido')} | ⏱️ {duracion} | 👀 {info.get('view_count', 0):,}",
            border_style="green"
        ))
        
        if console.input("\n[bold green]¿Descargar? [Enter=yes / n=no][/bold green]: ").lower().startswith('n'):
            rprint("[yellow]👋 Cancelado por el usuario[/yellow]")
            return
        
        descargar_con_progreso(url, carpeta, calidad, solo_audio)
        rprint(f"[bold green]🎉 Descargado en: {carpeta.absolute()}[/bold green]")
        
    except KeyboardInterrupt:
        rprint("\n[yellow]⚠️  Cancelado por el usuario[/yellow]")
    except Exception as e:
        rprint(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(code=1)

@app.command()
def lista(url: str):
    """📋 Muestra información del vídeo sin descargar"""
    try:
        info = obtener_info_video(url)
        formatos = info.get('formats', [])
        
        rprint(Panel.fit(
            f"[bold cyan]🎥 {info.get('title')}\n"
            f"📊 Formatos disponibles: {len(formats)}",
            border_style="blue"
        ))
        
        hd_formatos = [f for f in formatos if f.get('height') and f['height'] >= 720][:5]
        if hd_formatos:
            rprint("[bold]Formatos HD disponibles:[/bold]")
            for fmt in hd_formatos:
                res = fmt.get('height', 'N/A')
                ext = fmt.get('ext', 'N/A')
                rprint(f"  📺 {res}p ({ext})")
                
    except Exception as e:
        rprint(f"[red]❌ Error: {e}[/red]")

@app.command()
def batch(archivo: Path = typer.Argument(..., help="Archivo con URLs (una por línea)")):
    """📚 Descarga múltiples vídeos desde archivo"""
    if not archivo.exists():
        rprint(f"[red]❌ Archivo no encontrado: {archivo}[/red]")
        raise typer.Exit(code=1)
    
    with open(archivo) as f:
        urls = [line.strip() for line in f if line.strip()]
    
    rprint(f"[bold cyan]📚 Iniciando descarga de {len(urls)} vídeos...[/bold cyan]")
    for i, url in enumerate(urls, 1):
        rprint(f"\n[bold blue]#{i}/{len(urls)}[/bold blue]")
        descargar(url, carpeta=Path("videos"), calidad="mejor")

if __name__ == "__main__":
    rprint(Panel("🎬 YouTube HD Downloader Pro", style="bold magenta"))
    app()
