import functools

from liccheck.command_line import (Level, check_package, get_packages_info,
                                   group_by, parse_args, read_strategy)


def process(requirement_file, strategy, level=Level.STANDARD, no_deps=False):
    print('gathering licenses...')
    pkg_info = get_packages_info(requirement_file, no_deps)
    deps_mention = '' if no_deps else ' and dependencies'
    print('{} package{}{}.'.format(len(pkg_info),
                                   '' if len(pkg_info) <= 1 else 's',
                                   deps_mention))
    groups = group_by(pkg_info,
                      functools.partial(check_package, strategy, level=level))

    packages = []
    for r, ps in groups.items():
        for p in ps:
            packages.append({
                'name': p['name'],
                'version': p['version'],
                'license': (p['licenses'] or ['UNKNOWN'])[0],
                'status': r
            })
    packages = sorted(packages, key=lambda i: i['name'])
    return packages


def main(args):
    args = parse_args(args)
    strategy = read_strategy(args.strategy_ini_file)
    return process(args.requirement_txt_file, strategy, args.level,
                   args.no_deps)
