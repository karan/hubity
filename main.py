import argparse, os, sys

if sys.version_info[0] != 3 or sys.version_info[1] < 8:
    print(
        "Version Error: Version: %s.%s.%s incompatible please use Python 3.8+"
        % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
    )
    sys.exit(0)

try:
    from plexapi import server
    import yaml
except (ModuleNotFoundError, ImportError):
    print("Requirements Error: Requirements are not installed")
    sys.exit(0)


DEBUG = False

default_dir = os.path.dirname(os.path.abspath(__file__))
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


def sort_by_title(titles, managedHubs):
    sorted_mh = []
    for title in titles:
        for mh in managedHubs:
            if mh.title == title:
                sorted_mh.append(mh)
                break
    return sorted_mh


def print_existing_mh(plex):
    gen_config = {}
    plex_libs = plex.library.sections()
    for pl in plex_libs:
        gen_config[pl.title] = {"managed_hubs": []}
        plex_library_section = plex.library.section(pl.title)
        plex_managed_hubs = plex_library_section.managedHubs()
        for mh in plex_managed_hubs:
            gen_config[pl.title]["managed_hubs"].append(
                {mh.title: {"identifier": mh.identifier}}
            )
    print(yaml.dump(gen_config))


def reconcile_mh(plex, config_libs):
    for library_name in config_libs:
        print(f"[START] {library_name=}")
        mh_config = config["libraries"][library_name]["managed_hubs"]

        plex_library_section = plex.library.section(library_name)
        plex_managed_hubs = plex_library_section.managedHubs()

        if DEBUG:
            print("Current Order of %d libraries" % len(plex_managed_hubs))
            for mh in plex_managed_hubs:
                print(f"{mh.title=} {mh.identifier=}")

        # Sort ManagedHubs first
        desired_sorted_titles = [list(mhc.keys())[0] for mhc in mh_config]
        sorted_mh = sort_by_title(desired_sorted_titles, plex_managed_hubs)

        if DEBUG:
            print("Sorted Order of %d libraries" % len(plex_managed_hubs))
            for mh in sorted_mh:
                print(f"{mh.title=} {mh.identifier=}")

        for idx, mh in enumerate(sorted_mh):
            if idx == 0:
                mh.move()
            else:
                mh.move(after=sorted_mh[idx - 1])

        print(f"[DONE] {library_name=}")


def main():
    parser = argparse.ArgumentParser(description="Run the tool in a certain mode.")
    parser.add_argument(
        "-g",
        "--generate-config",
        action="store_true",
        help="Print a libraries config that should be used as a starting point.",
    )
    parser.add_argument("-a", "--apply", action="store_true", help="Apply the config.")
    args = parser.parse_args()

    plex = server.PlexServer(config["plex"]["url"], config["plex"]["token"])
    config_libs = list(config["libraries"].keys())

    if args.generate_config:
        print_existing_mh(plex)

    if args.apply:
        reconcile_mh(plex, config_libs)


if __name__ == "__main__":
    main()
