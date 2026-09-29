"""Tela inicial (welcome / splash) do avaliacao-tui.

Mostra um ASCII art "SENAI" com gradiente arco-íris + subtítulo.
Qualquer tecla (exceto q) avança para o painel principal.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static


# === ASCII art "SENAI" com ondas em degradê acima e abaixo ===
SENAI_ASCII = """\
███             ███             ███             ███             ███             █
███░            ███░            ███░            ███░            ███░            ███
███░            ███░            ███░            ███░            ███░            ███░
███░            ███░            ███░            ███░            ███░            ███░
███░            ███░            ███░            ███░            ███░            ███░
██░            ███░            ███░            ███░            ███░            ███░
░            ███░            ███░            ███░            ███░            ███░
            ░░░             ░░░             ░░░             ░░░             ░░░
███████╗ ██████╗████████╗ ███████╗█   ██╗     ██╗██ ██╗ ██████╗ █████╗ ███████╗ ███
╔══██╗██╔══██╗██╔═══██╗██╔════╝    ██║     ██║░  ██║██╔════╝██╔══██╗██╔════╝██░
██████╔╝██████╔╝██║   ██║█████╗      ██║   ████║   ██║██║     ███████║███████╗░
██╔═══╝ ██╔══██╗██║   ██║██╔══╝      ██║ ███░██║   ██║██║     ██╔══██║╚════██║
██║    ███║  ██║╚██████╔╝██║██╗      ███████╗╚██████╔╝╚██████╗██║  ██║███████║
╚═╝  ███╚═╝  ╚═╝ ╚═════╝░╚═╝╚═╝      ╚══════╝ ╚═════╝██╚═════╝╚═╝  ╚═╝╚══════╝
███░            ███░            ███░            ███░            ███░            █
░░░             ░░░             ░░░             ░░░             ░░░             ░░
███             ███             ███             ███             ███             ███
███░            ███░            ███░            ███░            ███░            ███░
░            ███░            ███░            ███░            ███░            ███░
            ███░            ███░            ███░            ███░            ███░
            ███░            ███░            ███░            ███░            ███░
            ███░            ███░            ███░            ███░            ███░"""


# Paleta do arco-íris (6 cores — Rich aceita nomes padrão)
RAINBOW = ("red", "yellow", "green", "cyan", "blue", "magenta")


def rainbow(text: str) -> str:
    """Devolve `text` com cada caractere não-branco envolto em markup colorido,
    percorrendo ciclicamente a paleta do arco-íris.

    Espaços não recebem markup (para não poluir a saída). A posição reseta
    a cada quebra de linha, então cada linha começa sempre do vermelho.
    """
    out: list[str] = []
    pos = 0
    for ch in text:
        if ch == "\n":
            out.append(ch)
            pos = 0
        elif ch == " ":
            out.append(ch)
        else:
            color = RAINBOW[pos % len(RAINBOW)]
            out.append(f"[{color}]{ch}[/{color}]")
            pos += 1
    return "".join(out)


class HomeScreen(Screen):
    """Tela de boas-vindas. Qualquer tecla → vai para o MainScreen."""

    DEFAULT_CSS = """
    HomeScreen {
        align: center middle;
        background: $surface;
    }

    #home-stack {
        align: center middle;
        width: auto;
        height: auto;
    }

    #ascii-art {
        content-align: center middle;
        width: auto;
        height: auto;
        text-style: bold;
    }

    #subtitle {
        margin-top: 2;
        content-align: center middle;
        width: 100%;
        color: $accent;
        text-style: bold;
    }

    #prompt {
        margin-top: 3;
        content-align: center middle;
        width: 100%;
        color: $secondary;
    }

    #hint {
        margin-top: 1;
        content-align: center middle;
        width: 100%;
        color: $text-muted;
    }
    """

    BINDINGS = [
        Binding("q", "app.quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="home-stack"):
            yield Static(rainbow(SENAI_ASCII), id="ascii-art", markup=True)
            yield Static(
                "Avaliação  —  Parte 2  (Implantação de Sistemas)",
                id="subtitle",
            )
            yield Static(
                "[bold]Pressione qualquer tecla para continuar[/bold]",
                id="prompt",
                markup=True,
            )
            yield Static(
                "[dim]q  sair  ·  Enter / Space / Esc  começar[/dim]",
                id="hint",
                markup=True,
            )

    def on_key(self, event) -> None:
        # Qualquer tecla que não seja 'q' (que está em BINDINGS) avança.
        # q já é tratada pela binding acima → sai do app.
        if event.key == "q":
            return
        self.app.switch_screen("main")
