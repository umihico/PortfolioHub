
class RepositoryScore():
    def __init__(self, name, language, size):
        self.name = name
        self.language = language
        self.size = size
        self.date_point = None
        self.size_point = None
        self.total_point = None


def calc_skillset(raw_repositories):
    self_repositories = [r for r in raw_repositories if not r['fork']]
    has_lang_repositories = [r for r in self_repositories if r['language'] is not None]
    repositories = [RepositoryScore(r['name'], r['language'], r['size'])
                    for r in has_lang_repositories]
    for date_point, repo in enumerate(reversed(repositories), start=1):
        repo.date_point = date_point
    sizes = [r.size for r in repositories]
    size_to_points_dict = {size: p for p, size in enumerate(sorted(sizes))}
    for repo in repositories:
        repo.size_point = size_to_points_dict[repo.size]
    for repo in repositories:
        repo.total_point = repo.size_point*repo.date_point
    lang_point_sum_dict = {}
    for repo in repositories:
        lang = repo.language
        lang_point_sum_dict[lang] = lang_point_sum_dict.get(lang, 0)+repo.total_point
    total = sum(lang_point_sum_dict.values())
    if total == 0:
        return []
    for key in lang_point_sum_dict:
        lang_point_sum_dict[key] = int((lang_point_sum_dict[key]*100)/total)
    lang_point_sum_dict = {lang: size for lang, size in lang_point_sum_dict.items() if size > 0}
    lang_list = list(sorted(lang_point_sum_dict.items(), key=lambda x: x[1], reverse=True))
    return lang_list
