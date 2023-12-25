# hubity

Re-order Plex hubs using a config file.

**Why would you use it?**

If you manage a lot of collections (using something like [Plex Meta Manager](https://metamanager.wiki/en/latest/)) and want to make sure your collections show up in Recommendations in the correct order. While you can do it manually, it can take a long time for particularly large number of collections.

## Installation

1. Clone the repo

1. Install dependencies: `pip3 install -r requirements.txt`

## Usage

```python
$ python3 main.py --help
usage: main.py [-h] [-g] [-a]

Run the tool in a certain mode.

options:
  -h, --help            show this help message and exit
  -g, --generate-config
                        Print a libraries config that should be used as a starting point.
  -a, --apply           Apply the config.
```

1. Start with a simple configuration (copy the provided template).

1. Add your Plex URL and token.

1. Run `python3 main.py -g`. This will print existing hubs for your libraries. You can copy-paste than in the config file.

1. Re-order the hubs as needed in the config file.

1. Apply changes with `python3 main.py -a`

