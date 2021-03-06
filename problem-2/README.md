##### Author: Pierre LIENHART
##### Contact: pierre.lienhart@gmail.com

# Datadog data science homework - Problem 2

## 1. Project's description
## 1.1 General description
This application downloads baseball-statistics files to the local file system, computes for each team triple how many
players played for these three teams and returns the triples with a minimal number of player. The results are either printed
to the standard output or written to a text file. 
 
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

## 1.2 Design overview
In addition to the `main.py` entry-point script. The project consists in a `ddog` Python package made of 5 Python modules:
* `cli.py`: This module gathers every function and object related to the parsing and validation of command-line arguments.
In particular, we implemented an augmented argument parser object (class `CliArgParser`). 
* `source.py`: This module gathers every function and object related to the downloading and reading of baseball-statistics
CSV files: 
     * All the logic related to the loading of CSV files into a `pandas.DataFrame` object is encapsulated in 
     the `BaseballFilesLoader` object.
     * All the logic related to the downloading of CSV files using a formatted HTTP URL is encapsulated in the 
     `BaseballFilesDownloader` object.
     * All the operations related to the management of a local temporary directory (create if it does not exists, remove
     if requested) are implemented using a context manager (`TempDir` object).
* `processing.py`: This module gather all the "business logic", i.e.: the code dedicated to the specific computation of the
triples (encapsulated in the `TripleCounter` object). The `compute` method of the `TripleCounter` object expects a 
`pandas.DataFrame` and returns its results as a list (possibly empty) of (`frozenset`, `int`) tuples.
* `output.py`: This module gather all the logic related to the formatting and writing of the processing results to the chosen
sink. The appropriate sink object (currently two implementations: `ConsoleSink` and `LocalFileSystemSink`) is returned
by the factory object `SinkFactory`. Each sink implementation must implement the sink interface described by the `Sink`
abstract base class which consists of a single `write` method which expects a list (possibly empty) of 
(`frozenset`, `int`) tuples.
* `constants.py` : This helper module gathers the package's global constants.

## 1.3 Triple count computation 
### 1.3.1 Team and players identification
A quick data analysis show that using the team trigram (ex: "PIT") is not enough to uniquely identify a baseball team. Two
teams ("CLE" and "HOU") have indeed two sub-teams playing in two different leagues ("AL" and "NL"). This is why we chose
to use the concatenation of the team's trigram and the team's league name to uniquely identify each single team (Ex: "HOU-NL"). 
The league name is sometimes not available (for team "BL1" for example). In these cases, the team's ID coincides with the 
team's trigram. 

To avoid issues raised by possible namesakes, we chose to use the player ID code field instead of the player name to 
uniquely identify players.

### 1.3.2 Triples computation strategy
The code dedicated to the triples' computation can be found in the `ddog.processing.TripleCounter.compute` method.

Section 1.3.1 showed that we actually only need 3 columns from the input files. To spare memory space, the `pandas` CSV
reader has been set up such that only the required columns are loaded into memory. 

The first stage of the computation is dedicated to get for each unique player its list of played teams. Players with a 
list of less than 3 teams are discarded since no triple can be generated with less than three teams. The second stage of
the computation consists in building a triple counter by iterating over the players returned by the first stage. For each
player, we generate all the 3-combinations (triples) from its played-team list and update the triple counter. The counter
is a dictionary the keys of which are the triples (implemented as 3-element immutable `frozenset` objects) and the values
of which are the triple counts. The counter object is finally filtered to keep only the triples with the required minimum
count.

## 1.4 Complexity analysis
Let $n$, $p$ and $k$ be the numbers of records, unique players and unique teams in the input dataset respectively.

During the first stage the computation, the loaded dataset goes through the following transformations:
* Dropping duplicates: This operation can be performed with a $O(n)$ time and space complexity. Worse case scenario, there
are no duplicates, the number of records remains unchanged after the transformation.
* Adding a new column using a simple filter: This step has a $O(n)$ time and a $O(1)$ space complexity.
* Aggregation where the two aggregation operations are not more complex than a count: This operation can be performed 
with a $O(n)$ time and space complexity (at worse, if no duplicates where found before). Space complexity in particular 
is at this stage still $O(n)$ as we collect the team IDs in lists which is equivalent to reshaping the data.
* Filter on the team counts: This step has a $O(p)$ time and a $O(1)$ space complexity.

First stage has therefore a $O(n)$ time and space complexity.

The second stage of the computation consists for each player who played in at least 3 teams (worst case: $p$ players) to 
generate all the 3-combinations from the teams the player played in (worst case: each player played in each of
the $k$ teams) and update a counter (a dictionary) with the produced combinations. The counter is finally filtered over 
the counts.

Notice: Using a dictionary as counter allows us to take advantage of a $O(1)$ time complexity on get and set operations.

$\binom(a, b) ~ O(a^{b})$ for $a$ big enough. Generating the combinations is the most expensive operation here 
($O(k^3)$). Worst case scenario for the second stage has therefore a $O(pk^3)$ time complexity and a $O(k^3)$ space 
complexity (the generated dictionary/counter has at most $O(k^3)$ key-value pairs).

## 2. Execution environment
To ensure our project runs using the appropriate dependencies, we first create and activate a dedicated Python (virtual)
execution environment using the project's *requirements.txt* file. Change your current directory to the problem's 
directory and run the following commands:

```bash
conda create -y -c conda-forge -n py36-problem-2 --file requirements.txt
```

Activate the environment using:

```bash
conda activate py36-problem-2
```

If the above command requires extra `conda` configurations, you can still use:

```bash
source activate /opt/anaconda/envs/py36-problem-2
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
pip install --no-index dist/ddog-0.0.1-py3-none-any.whl
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
Team triple         Count
-------------------------
CIN-NL|PHI-NL|SLN-NL, 80
CHN-NL|CIN-NL|SLN-NL, 74
CHN-NL|PHI-NL|SLN-NL, 68
CIN-NL|PIT-NL|SLN-NL, 63
CHN-NL|CIN-NL|PHI-NL, 54
CIN-NL|PHI-NL|PIT-NL, 54
CHN-NL|CIN-NL|PIT-NL, 53
BOS-AL|CHA-AL|CLE-AL, 52
CHA-AL|CLE-AL|NYA-AL, 50
PHI-NL|PIT-NL|SLN-NL, 50
CHN-NL|PHI-NL|PIT-NL, 50
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