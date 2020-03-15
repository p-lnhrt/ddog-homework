##### Author: Pierre LIENHART
##### Contact: pierre.lienhart@gmail.com

# Datadog data science homework - Problem 2

## 1. General description

## 2. Execution environment

## 3. Build

## 4. Command-line interface (CLI)
Running the application using the command line interface (See example in Section 5) consists in running in entry-point
script `main.py` using the appropriate Python binary: `python main.py`

Six optional flags can be used to tune the application's behavior:
* `--from`: Year of the first baseball statistical report to include (Default: 1871).
* `--to`: Year of the last baseball statistical report to include (Default: 2014).
* `--tmp`: Path to a local directory where the downloaded data should be temporarily stored (Default: ./tmp).
* `--players`: Minimum number of players a team triple should contain to be returned (Default: 50).
* `--keep`: Whether the temporary directory and its content should be kept after running (Default: Content is dropped).
* `--sink`: Output sink for the computed list of triples. Either "console" (default) to print to the standard output or a 
local path to an output text file.

Requested year range should be included within the 1871-2014 range.

CLI documentation is also available through:
```bash
python main.py -h|--help
```

## 5. Running the application
Assuming the appropriate Python virtual environment is activated, the following command will download all the baseball-statistics 
files from 1871 to 2014 included to a temporary directory `./tmp`, compute all the team triples of at least 50 players and
print the results to the console. The `--keep` flag ensures that `./tmp` and its content is not destroyed after the 
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