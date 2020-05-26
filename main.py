import requirements
from find_repositories import find_repositories
from screenshot_portfolios import screenshot_portfolios
from fill_skillset import fill_skillset
from fill_location import fill_location


def main(event, context):
    result = {}
    result['find_repositories'] = find_repositories()
    result['screenshot_portfolios'] = screenshot_portfolios()
    result['fill_skillset'] = fill_skillset()
    result['fill_location'] = fill_location()
    return result


def test_main():
    main(None, None)
