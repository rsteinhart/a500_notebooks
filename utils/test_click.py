"""
demonstrate some click options
"""

import click
import json

@click.group()
def main():
    """
    demonstration of a click group
    """


@main.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def calc_product(a, b):
    """
    usage: multiply a (float) x b (float)
    """
    # a = float(a)
    # b = float(b)
    result = a * b
    print(f"my result is {result}")
    return result


@main.command()
@click.argument("outfile", type=click.File("w"), nargs=1)
def write_json(outfile):
    """\b
    write an json file
    where OUTFILE is the full path to the output file
    note that click opens OUTFILE for us
    """
    my_params = dict(case="rico", mo_length=5.2, date=(2019, 10, 11), flux=60)
    json.dump(my_params, outfile, indent=4)


@main.command()
@click.argument("infile", type=click.File("r"), nargs=1)
def read_json(infile):
    """\b
    read a json file where INFILE is the full path to the json file
    INFILE will be opened by click
    """
    params_dict = json.load(infile)
    print(f"loaded {params_dict}")


if __name__ =="__main__":
    main()
    
