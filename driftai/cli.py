import sys
from functools import partial
from pathlib import Path

import click

from driftai import Approach, Project
from driftai.data import Dataset, SubDataset
from driftai.result_report import ResultReport
from driftai.result_report.metrics import *

from driftai.run import RunGenerator
from driftai.utils import import_from, to_camel_case

@click.group()
def main():
    """
    Simple CLI for DriftAI
    """    
    sys.path.append(str(Path('.').absolute()))

    
def _is_running_in_project():
    return Path("driftai.db").exists()


@main.command()
@click.argument('project_name')
def new(project_name):
    """
    Creates the directory tree for a new driftai project
    """
    if Path(project_name).is_dir():
        print("Project already exists")
        click.Abort()
        return

    Project(name=project_name)


@main.command()
@click.argument('item', type=click.Choice(["dataset"]))
@click.option('--path', '-p', help="Path of dataset's datasource")
@click.option('--heading/--no-heading',
                default=True,
                help="If the first line of CSV is the header or not")
@click.option('--label', '-l',
                help="The column name of the label. By default, the label is the last column")

@click.option('--parsing-pattern', 
               help='Pattern to read the files inside the directory')
@click.option('--datatype', '-d',
                default="img",
                help="Data type of files inside the directory")
def add(item, path, heading, label, parsing_pattern, datatype):

    if not _is_running_in_project():
        print("You must use driftai CLI inside an driftai project directory")
        return

    if item == "dataset":
        if path is None:
            print("You must provide a path with -p or --path option")
            click.Abort()
            return
        
        datasource_params = dict()
        if parsing_pattern:
            datasource_params['path_pattern'] = parsing_pattern

        path_to_dataset = Path(path).absolute().resolve()
        factory_fn = (partial(Dataset.from_dir, datatype=datatype, **datasource_params) 
                        if path_to_dataset.is_dir() 
                        else partial(Dataset.read_file, label=label, first_line_heading=heading))

        ds = factory_fn(path=str(path_to_dataset))
        ds.save()
        print("Dataset with id {} created".format(ds.id))


def generate_subdataset(dataset, method, by):
    def parse_by(method, by):
        if method == "k_fold":
            return int(by)
        return float(by)

    by = parse_by(method, by)
    sbds = SubDataset(dataset=Dataset.load(dataset), method=method, by=by)
    sbds.save()
    print("Subdataset with id {} created".format(sbds.id))


def generate_approach(identifier, subdataset_id, inside_project):
    if inside_project and not subdataset_id:
        print('Error: To create an approach you must specify a subdataset using the option --subdataset')
        return

    if inside_project:
        a = Approach(project=Project.load(),
                     name=identifier,
                     subdataset=SubDataset.load(subdataset_id))
        a.save()
    else:
        with Path(identifier + '.py').open("w") as f:
            f.write(Approach._EMPTY_APPROACH
                            .format(id=to_camel_case(identifier),
                                    runner_decorator=''))



@main.command()
@click.argument("item", type=click.Choice(["subdataset", "approach"]))
@click.argument("identifier")
@click.option(
    "--subdataset",
    "-s",
    default='',
    help="In case item=approach. ID of the subdataset where approach will retrieve the data")
@click.option("--method", "-m", type=click.Choice(['k_fold', 'train_test']))
@click.option(
    "--by",
    help=
    "In case method=k_fold, by is the number of folds. If method=train_test, by is the percentage of training instance")
@click.option(
    "--dataset",
    "-d",
    help="ID of the dataset which new subdataset will be generated from")
@click.option(
    '--project/--no-project',
    default=True,
    help='Create approach script inside a project or not?')
def generate(item, 
             identifier, 
             subdataset, 
             method, 
             by, 
             dataset,
             project):
    if project and not _is_running_in_project():
        print("You must use driftai CLI inside an driftai project directory")
        return

    generators = {
        "subdataset": partial(generate_subdataset, identifier, method, by),
        "approach": partial(generate_approach, 
                            identifier, 
                            subdataset, 
                            project)
    }
    generators[item]()

    
@main.command()
@click.argument("approach_id")
def status(approach_id):
    if not _is_running_in_project():
        print("You must use driftai CLI inside an driftai project directory")
        return
    print("Loading approach data...")
    stat = Approach.load(approach_id).status
    if not stat["done"]:
        print("Approach {} is still running".format(approach_id))
        print(stat["progress_bar"] + " Done runs: " + str(stat["done_runs"]) + " Total runs: " + str(stat["total_runs"]))
    else:
        print("There are no left runs for Approach {approach_id}!".format(approach_id))


@main.command()
@click.argument('approach-id')
@click.option('--resume/--no-resume', default="False", help="Resume the last execution?")
def run(approach_id, resume):
    if not _is_running_in_project():
        print("You must use driftai CLI inside an driftai project directory")
        return
    if not Approach.collection().exists(approach_id):
        print("Approach with id {} does not exist.".format(approach_id))
        return

    sys.path.append(Project.load().path)

    namespace = 'approaches.' + approach_id
    cls_name = to_camel_case(approach_id) + "Approach"

    approach_cls = import_from(namespace, cls_name)
    approach_cls().run(resume=resume)

@main.command()
@click.argument('approach-id')
@click.option('--metric', '-m', 
              multiple=True, 
              type=click.Choice(list(str_to_metric_fn.keys())))
def evaluate(approach_id, metric):
    if not _is_running_in_project():
        print("You must use driftai CLI inside an driftai project directory")
        return
    if not Approach.collection().exists(approach_id):
        print("Approach with id {} does not exist.".format(approach_id))
        return

    approach = Approach.load(approach_id)
    r = ResultReport(approach=approach, metrics=[str_to_metric_fn[m] for m in metric])
    r.as_dataframe()\
        .to_csv(approach_id + "_evaluation.csv", index=False)       


if __name__ == "__main__":
    main()
