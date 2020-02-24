import requirements
from find_repositories import find_repositories
from screenshot_portfolios import screenshot_portfolios
from fill_skillset import fill_skillset
from fill_location import fill_location


def main(event, context):
    result = {}
    result['find_repositories'] = find_repositories()
    if result['find_repositories']:
        return result
    result['screenshot_portfolios'] = screenshot_portfolios()
    result['fill_skillset'] = fill_skillset()
    result['fill_location'] = fill_location()
    return result


if __name__ == '__main__':
    main(None, None)
