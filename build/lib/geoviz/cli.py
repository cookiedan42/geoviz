import click
import shapely
import shapely.plotting
import uuid
import matplotlib.pyplot as plt
import os
import itertools
import json

color_cycle = plt.rcParams["axes.prop_cycle"]
color_cycle = itertools.cycle(color_cycle)


def plot_wkt(arg, **kwargs):
    shape = shapely.from_wkt(arg)
    return plot_shape(shape, **kwargs)


def plot_shape(shape, **kwargs):
    match shape.geom_type:
        case "MultiPolygon":
            shapely.plotting.plot_polygon(
                shape, add_points=False, color=next(color_cycle)["color"], **kwargs
            )
        case "Polygon":
            shapely.plotting.plot_polygon(
                shape, add_points=False, color=next(color_cycle)["color"], **kwargs
            )
        # TODO Rect and Triangle from Geo

        case "Line":
            shapely.plotting.plot_line(
                shape, color=next(color_cycle)["color"], **kwargs
            )
        case "LineString":
            shapely.plotting.plot_line(
                shape, color=next(color_cycle)["color"], **kwargs
            )

        case "Point":
            shapely.plotting.plot_points(
                shape, color=next(color_cycle)["color"], **kwargs
            )
        case "MultiPoint":
            shapely.plotting.plot_points(
                shape, color=next(color_cycle)["color"], **kwargs
            )

        case _:
            print(f"invalid type: {shape.geom_type}")
    return shape

def v_log(msg:str,v:bool):
    if v:
        click.echo(msg)


@click.command()
@click.argument("text", nargs=-1)
@click.option("-t", "--target", default="", help="target file")
@click.option("-v", "--verbose", default=False, is_flag=True, help="more logs")
@click.option("-f", "--files", default=False, is_flag=True, help="treat input as files")
@click.option("--format", default="wkt", help="data format")
def main(files, text, format, target, verbose):
    if not target:
        target = f"/tmp/{uuid.uuid4()}.svg"

    stdin = click.get_text_stream("stdin")
    if not stdin.isatty():
        text = stdin.read()
        stdin.close()

    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    if files:
        drawn = False
        for f in text:
            name, ext = os.path.splitext(f)
            match ext:
                case ".wkt":
                    with open(f) as fp:
                        text = fp.readlines()
                    if len(text) > 0:
                        v_log(f"adding geometries from {f}",verbose)
                    for row in text:
                        drawn = True
                        plot_wkt(row, ax=ax)
                case ".geojson":
                    with open(f) as fp:
                        text = json.load(fp)
                    geoms = []
                    if "features" in text.keys():
                        geoms = [
                            shapely.geometry.shape(feature["geometry"])
                            for feature in text["features"]
                        ]
                    if "geometry" in text.keys():
                        geoms = [shapely.geometry.shape(text["geometry"])]
                    if len(geoms) > 0:
                        v_log(f"adding geometries from {f}",verbose)
                    for geom in geoms:
                        drawn = True
                        plot_shape(geom, ax=ax)
                case _:
                    v_log(f"unsupported file extension: {ext}",verbose)
        if drawn:
            fig.savefig(target)
            click.echo(target)
        return

    # else is a piped thing
    text = text.split("\n")
    text = [i for i in text if i != ""]
    match format:
        case "wkt":
            for row in text:
                plot_wkt(row, ax=ax)
            fig.savefig(target)
            click.echo(target)
        case _:
            v_log("unsupported input",verbose)
