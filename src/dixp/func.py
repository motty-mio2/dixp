import os

from pathlib import Path
import subprocess as sp
from tempfile import TemporaryDirectory
from xml.etree import ElementTree
import click


@click.command()
@click.argument(
    "path",
    default="",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
)
@click.option("--exec", type=click.STRING, default="")
def exporter(path: Path, exec: str) -> None:
    if exec == "":
        if os.name == "posix":
            exec = "drawio"
        elif os.name == "nt":
            exec = "draw.io"
    with TemporaryDirectory() as temp:
        sp.run([exec, "--export", path, "--format", "xml", "--output", Path(temp) / "tmp.xml"])
        for i, n in enumerate(get_asset_names(Path(temp) / "tmp.xml")):
            sp.run(
                [
                    exec,
                    "--export",
                    Path(temp) / "tmp.xml",
                    "--format",
                    "png",
                    "--page-index",
                    f"{i}",
                    "--scale",
                    "2",
                    "--output",
                    path.parent / f"{path.stem}-{n}.png",
                ]
            )


def get_asset_names(xml_file: Path) -> list[str]:
    with open(xml_file, "r") as f:
        x: str = f.read()
        root: ElementTree.Element = ElementTree.fromstring(x)
        return [c.attrib["name"] for c in root.findall("diagram")]
