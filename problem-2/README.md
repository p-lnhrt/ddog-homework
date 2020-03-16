##### Author: Pierre LIENHART
##### Contact: pierre.lienhart@gmail.com

# Datadog data science homework - Problem 2

## 1. General description
This application downloads baseball-statistics files to the local file system, computes for each team triple how many
players played for these three teams and returns the triples with a minimal number of player. The results are either printed
to the standard output or written to a text file. 
 
**Important notice**: Team identification
A quick data analysis show that using the team trigram (ex: "PIT") is not enough to uniquely identify a baseball team. Two
teams ("CLE" and "HOU") have indeed two sub-teams playing in two different leagues ("AL" and "NL"). This is why we chose
to use the concatenation of the team's trigram and the team's league name to uniquely identify each single team (Ex: "HOU-NL"). 
The league name is sometimes not available (for team "BL1" for example). In these cases, the team's ID coincides with the 
team's trigram. 

The projects consists in: 
* An entry-point file *main.py* used to launch the application from the command line (See Sections 4 & 5).
* A Python package named *ddog* that gathers all the objects and functions (and their associated unit tests - See 
Section 6) the application is made from. In order for the application to run in a Python environment (See Section 2), 
this package needs to be built and installed (See Section 3).
* Four helper files:
    * A *requirements.txt* file, required to setup the application's Python execution environment (See Section 2).
    * A *setup.py* file, required to build the *ddog* package (See Section 3).
    * A *config.ini* configuration file, required to be in the application working directory.
    * A *CHANGELOG.md* file which keeps track of the changes associated with each version of the application.

About the *config.ini* file: This file gather the following configurations in a single DEFAULT section:
* `MinYear`: The minimum year a user can request baseball statistics for.
* `MaxYear`: The maximum year a user can request baseball statistics for.
* `LoggingLevel`: The level of the application's root logger. The application provides a basic logging setup in which 
only the root logger is used.
* `TmpFileFormattedName`: Name template (as a Python formatted string) to be used for baseball-statistics files when 
stored on the local file system. 
* `TmpFileRegex`: Regex (Python flavor) to be used to match the above `TmpFileFormattedName`.
* `FormattedSourceURL`: HTTP source URL for baseball-statistics files (as a Python formatted string).

**All input files are expected to be CSV text files all with the same number of columns and column ordering.**

## 2. Execution environment
To ensure our projects runs using the appropriate dependencies, we first create and activate a dedicated Python (virtual)
execution environment using the project's *requirements.txt* file. Change your current directory to the problem's 
directory and run the following commands:

```bash
conda create -y -c conda-forge -n py36-problem-2 --file requirements.txt
conda activate py36-problem-2
```

Starting from this moment, **we always assume that the current Python execution environment is the project's dedicated
virtual environment**.

## 3. Build
Assuming our current working directory is the project's root directory, first begin with the following command to ensure 
we get a clean build with no lingering artifacts from previous builds: 

```bash
rm -rf build dist
```

We install and/or upgrade the required packages used to build and install our package using Python package manager `pip`:
```bash
pip install --upgrade pip setuptools wheel
```

The following command builds a distribution wheel file (*.whl*) in a *dist* directory:
```bash
python setup.py bdist_wheel
```

In order to run our program from the command line, the built package needs to be installed in our virtual environment:
```bash
pip install --no-index dist/ddog-0.1.0-py3-none-any.whl
```

Now you are ready to run the application from the command-line (See Section 5). 

## 4. Command-line interface (CLI)
Running the application using the command line interface (See example in Section 5) consists in running in entry-point
script *main.py* using the appropriate Python binary: `python main.py`

Six optional flags can be used to tune the application's behavior:
* `--from`: Year of the first baseball statistical report to include (Default: 1871).
* `--to`: Year of the last baseball statistical report to include (Default: 2014).
* `--tmp`: Path to a local directory where the downloaded data should be temporarily stored (Default: *./tmp*).
* `--players`: Minimum number of players a team triple should contain to be returned (Default: 50).
* `--sink`: Output sink for the computed list of triples. Either "console" (default) to print to the standard output or a 
local path to an output text file in an already-existing directory (Ex: */path/to/dir/results.txt*).
* `--keep`: Whether the temporary directory and its content should be kept after running (Default: Content is dropped).

Requested year range should be included within the 1871-2014 range.

**WARNING**: The temporary directory where the data is downloaded is removed by default (unless the `--keep` flag is added)
whether an exception is raised or not. In particular, do not write the results in this specific temporary directory.

CLI documentation is also available through:
```bash
python main.py --help
```

## 5. Running the application
Assuming the appropriate Python virtual environment is activated, the following command will download all the baseball-statistics 
files from 1871 to 2014 included to a temporary directory *./tmp*, compute all the team triples of at least 50 players and
print the results to the console. The `--keep` flag ensures that *./tmp* and its content is not destroyed after the 
application ends.

```bash
python main.py --from 1871 --to 2014 --tmp ./tmp --players 50 --keep --sink console
```

Aside from the application logs, output the the standard output should look like this:
```bash
Team triple: CIN-NL|PHI-NL|SLN-NL - Count: 84
Team triple: CHN-NL|CIN-NL|SLN-NL - Count: 81
Team triple: CHN-NL|PHI-NL|SLN-NL - Count: 74
Team triple: CIN-NL|PIT-NL|SLN-NL - Count: 70
Team triple: CHN-NL|CIN-NL|PIT-NL - Count: 61
Team triple: CHN-NL|CIN-NL|PHI-NL - Count: 60
Team triple: CHN-NL|PHI-NL|PIT-NL - Count: 56
Team triple: BOS-AL|CHA-AL|CLE-AL - Count: 56
Team triple: CIN-NL|PHI-NL|PIT-NL - Count: 56
Team triple: PHI-NL|PIT-NL|SLN-NL - Count: 55
Team triple: CHA-AL|CLE-AL|NYA-AL - Count: 53
Team triple: CHN-NL|PIT-NL|SLN-NL - Count: 53
```

**Important notice**: The *config.ini* file must be located in the application's working directory.

## 6. Tests
To run all the project's unit tests, ensure that the appropriate Python virtual environment is activated, that your 
current directory is the project's root directory and run the following command: 
```bash
python -m pytest
```

To run a specific test module, simply add its path to the preceding command. For example:
```bash
python -m pytest ./ddog/tests/test_cli.py
```

## 7. Complexity analysis