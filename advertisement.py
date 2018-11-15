import pprint
import time
import umihico
apikey = umihico._set_env_value("github_adv", optional_value=None)
import requests
from common import content_tinydb
import json
from api import iter_repo


def send_star_all():
    for repo in content_tinydb.all():
        if repo["stargazers_count"] > 0:
            continue
        username, reponame = repo["full_name"].split('/', 1)
        sleep_time = 5
        while True:
            time.sleep(sleep_time)
            try:
                send_star(username, reponame)
            except Exception as e:
                print(e)
                sleep_time *= 2
                print(sleep_time)
            else:
                break
        print(username, reponame)


def send_star(username, reponame):
    url = f"https://api.github.com/user/starred/{username}/{reponame}"
    headers = {"Authorization": f"token {apikey}", "Content-Length": '0'}
    response = requests.put(url, headers=headers)
    response.raise_for_status()
    print(response.status_code)


def test_send_star():
    send_star("umihico", "minigun-requests")


def create_issue(username, reponame, title, text):
    url = f"https://api.github.com/repos/{username}/{reponame}/issues"
    headers = {
        "Authorization": f"token {apikey}",
        "Content-Length": '0',
        'Accept': "application/vnd.github.symmetra-preview+json", }
    data = {
        "title": title,
        "body": text,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print(response.status_code)
    print(response.text)


def test_create_issue():
    create_issue("umihico", "thumbnailed-portfolio-websites",
                 "issue test", 'issue_text')


def get_topic_diff_repos():
    other_topics = ['portfolio-site', 'portfolio-page',
                    'portfolio-template', 'personal-portfolio']
    full_names = []
    for topic in other_topics:
        for repo in iter_repo(topic=topic):
            topics = repo['topics']
            if 'portfolio-website' not in topics:
                full_name = repo['full_name']
                print(full_name, topic)
                full_names.append(full_name)
    pprint.pprint(full_names)


def ask_to_put_topic():
    full_names = [
        # 'mathesond2/davidmatheson.me',
        # 'kejriwalrahul/kejriwalrahul.github.io',
        'gummywormz/gummywormz.github.io',
        'savinamonet/Portfolio-Site-of-Savina-Fierro',
        'mbrav/mbrav.github.io',
        'xR86/xR86.github.io',
        'nawazishali/nawazishali.github.io',
        'vikrantkakad/vikrantkakad.github.io',
        'musaab-abdalla/frontend-nanodegree-build-portfolio-site',
        'trajano/trajano-portfolio',
        'davidhu2000/davidhu2000.github.io',
        'lizdizon/ld-portfolio-gulp',
        'tomanistor/tomanistor.com',
        'datyayu/new-datyayu.xyz',
        'findawayer/findawayer.github.io',
        'abadiu/abadiu',
        'lucymariej/lucymariej.github.io',
        'kubami9/Great-Portfolio-Site',
        'salvadornico/salvadornico.github.io',
        'franzos/f-a.nz',
        'ntoand/home',
        'blshv/siwple',
        'Taylor-S/portfolioSite',
        'michaelnetbiz/fortpolio',
        'chazmcgrill/hurricane-charlie-website',
        'ddavignon/portfolio-site',
        'jocoio/portfolio2.0',
        'alexxlefa/alexxlefa.github.io',
        'daviddeejjames/dfjames-gatsby',
        'fabe/site',
        'biancapower/portfolio',
        'estebansanmartin/estebansanmartin.github.io',
        'timweisinger/timweisinger.github.io',
        'finnyfound/finnyfound.github.io',
        'estebansanmartin/template-react',
        'Credwa/isledev-portfolio-PWA',
        'drurez/drurez.github.io',
        'iamjosan/portfolio-site',
        'Chloeiii/Chloeiii.github.io',
        'ceciliaconsta3/CeciliaConstantine.com',
        'vivek1996/vivek1996.github.io',
        'mishingo/mishingo.github.io',
        'dawspa/DawidsWebPortfolio',
        'ashbadger/ashbadger.xyz',
        'lexmartinez/portfolio-site',
        'Antonious-Stewart/Astewart400.github.io',
        'bigdjrp/bigdjrp.github.io',
        'chris-peters/chris-peters.github.io',
        'sandofvega/sov',
        'EOussama/eoussama.github.io',
        'Maggie199/Maggie199.github.io',
        'arif2009/arif2009.github.io',
        'thedelk/fend-project-1',
        'seabazz/css-landing-page-layout',
        'Asjas/udacity-portfolio-project',
        'Rafi993/portfolio',
        'adriantoddross/portfolio',
        'codeghoul/codeghoul.github.io',
        'juan-ONE/realjuanli.com',
        'zubayerhimel/zubayerhimel.github.io',
        'tfirdaus/personal-portfolio',
        'gummywormz/gummywormz.github.io',
        'djmsuman/djmsuman.github.io',
        'hedhyw/hedhyw.github.io',
        'nawazishali/nawazishali.github.io',
        'SrGrace/Portfolio',
        'sash-ua/sash-ua.github.io',
        'Keiranbeaton/graduate-portfolio',
        'yamanoku/vue_portfolio_templete',
        'onit4ku/onit4ku.github.io',
        'velibr12/velibr12.github.io',
        'Spazcool/Spazcool.github.io',
        'Cree8002/Cree8002.github.io',
        'tjinauyeung/v2',
        'petergns/petergns.github.io',
        'imraghava/imraghava.github.io',
        'patronaxxx/portfolio',
        'sourcerer-io/sourcerer-app',
        'michalgrochowski/dobrywebdev-v2',
        'beppujah/angolare',
        'castrodd/creative',
        'ashokkoduru/know-me',
        'vchrombie/vchrombie.github.io',
        'dbanbahji/dbanbahji.github.io',
        'timweisinger/timweisinger.github.io',
        'maniarasu/maniarasu.github.io',
        'ayushin78/ayushin78.github.io',
        'fractalfox01/Portfolio',
        'cykins4good/cykins4good.github.io',
        'MRummanHasan/Portfolio',
        'sylhare/Type-on-Strap',
        'itsTeknas/itsTeknas.github.io',
        'srabalogh/srabalogh.github.io',
        'adescode/AiA-Portfolio',
        'Cain96/Cain96.github.io',
        'jessicapspeers/clean-portfolio',
        'ThePhD/ThePhD.github.io',
        'niltonslf/niltonslf.github.io',
        'victorialung/victorialung',
        'Grupphaus/Grupphaus.github.io',
        'acherry125/Event-Horizon',
        'jessicalam/JessicaLamCV',
        'EOussama/eoussama.github.io',
        'skyvova/android-course-landing',
        'teinen/teinen.github.io',
        'kubekbreha/OpalCamp',
        'adriantoddross/portfolio',
        'arif2009/arif2009.github.io',
        'aranab/skarafat-looks',
        'carlawarde/carlawarde.github.io',
        'dsplayname/portfolio',
        'bill-c-martin/bill-c-martin.github.io',
        'FR0ST1N/TooMinimal',
        'banastas/portfolio',
        'GaziTaufiqIslam/Portfolio-template',
        'thundergolfer/junior-theme',
        'templateflip/material-portfolio',
        'Bronzeowl/basic-portfolio',
        'blunt/tachy.designs',
        'blunt/tachy.apparel',
        'shankariyerr/swift-portfolio',
        'blunt/tachy.pots',
        'BarkhaShukla/BarkhaShukla.github.io',
        'website-templates/portfolio_one-page-template',
        'amitgunjal/amitgunjal.github.io',
        'fractalfox01/Portfolio',
        'rushout09/rushout09.github.io',
        'diiegopereira/freemo',
        'AbhishikthAleti97/AbhishikthAleti97.github.io',
        'beautimour/portfolify',
        'Chingaipe/Portfolio-template',
        'ldrahnik/ldrahnik',
        'techmarcs/techmarcs.github.io',
        'Mugurinho/portfolio',
        'Tyby84/project-alpha',
        'nissim-panchpor/nissim-panchpor.github.io',
        'Belzee10/personal-portfolio',
        'NickM101/project_portfolio',
        'ErickMurage/Personal-Portfolio',
        'mseymour/markseymour.ca',
        'joequich/personal-portfolio',
        'Samuelachema/samuelachema.github.io',
        'Dostonbek1/Dostonbek1.github.io',
        'LiskB/Personal-Portfolio']
    import tqdm
    for full_name in tqdm.tqdm(full_names):
        username, reponame = full_name.split('/', 1)
        print(username, reponame)
        create_issue("umihico", "thumbnailed-portfolio-websites", "adding topic #portfolio-websites",
                     "Hello! I'm collecting screenshots of everybody's portfolio here.\nhttps://umihico.github.io/thumbnailed-portfolio-websites/\nIf you don't mind, I'd like you to add topic #portfolio-website. Then I can crawl later. Thank you!")
        raise


if __name__ == '__main__':
    # send_star_all()
    # test_create_issue()
    ask_to_put_topic()
    # get_topic_diff_repos()
