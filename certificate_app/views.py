from django.shortcuts import render, redirect
from django.conf import settings
import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
from .forms import CertificateForm
from .models import Certificate, Organization
from django.http import HttpResponseForbidden
from .forms import UploadFileForm
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text,extract_text_to_fp
from io import StringIO, BytesIO
import io
import time
import random
import string
import json
import datetime
from datetime import timedelta
import requests
from textblob import TextBlob
import json
import re
import spacy
from spacy.matcher import Matcher
from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / 'orgtrust.env'
load_dotenv(dotenv_path=dotenv_path)

PATH_TRUFFLE_WK = 'C:/Documents/Naman/Final Sem Project/code/BlockchainIdentityVerficiation'
truffleFile = json.load(open(PATH_TRUFFLE_WK + '/build/contracts/CertificateStore.json'))

C_ABI = truffleFile['abi']
C_ADDRESS = os.getenv('C_Address')

company_data = {
   "id":"1d396c21-e421-4dd9-988e-55a8200c6e10",
   "name":"Google",
   "legalName":"None",
   "domain":"google.com",
   "domainAliases":[
      "google.com.cm",
      "google.sucks",
      "google.lv",
      "google.gm",
      "google.com.af",
      "google.uk",
      "google.tl",
      "google.express",
      "blogspot.co.ke",
      "google.cc",
      "google.com.tr",
      "google.shiksha",
      "google.nom.pl",
      "chromecast.co.nz",
      "feedburner.com",
      "google.dm",
      "google.as",
      "google.com.gt",
      "google.lol",
      "admob.fr",
      "gmail.ng",
      "google.rent",
      "adwords.cz",
      "adwords.nl",
      "quickofficeanywhere.com",
      "photosphere.com",
      "google.lc",
      "google.pm",
      "google.tf",
      "google.co.uk",
      "doubleclick.com",
      "google.com.de",
      "google.be",
      "blogspot.lt",
      "google.gift",
      "google.ws",
      "gmail.bj",
      "gogle.com",
      "google.uk.com",
      "songza.tv",
      "adwords.pt",
      "google.gd",
      "google.net.do",
      "google.miami",
      "appliedsemantics.com",
      "withgoogle.com",
      "keyhole.com",
      "googlesciencefair.com",
      "google.cf",
      "google.fans",
      "socialdeck.com",
      "google.tattoo",
      "google.net.ua",
      "jogamaisum.com.br",
      "google.one",
      "google.paris",
      "adwords.ro",
      "google.ba",
      "google.homes",
      "blogspot.cz",
      "gmail.ie",
      "google.com.dz",
      "google.vote",
      "quickofficeconnect.com",
      "google.com.jo",
      "google.br.com",
      "chromecast.it",
      "google.ac",
      "google.pn",
      "sparkbuy.com",
      "googlefinland.com",
      "mfg-inspector.com",
      "google.waw.pl",
      "googlefiber.org",
      "area120.com",
      "helpout.com",
      "google.ga",
      "greenparrotpictures.net",
      "adwords.co.il",
      "galaxynexus.com",
      "google.co.com",
      "adwords.com",
      "hotpot.com",
      "google.co.tz",
      "glass-community.com",
      "appspot.com",
      "adwords.it",
      "blogspot.sk",
      "songza.fm",
      "google.cd",
      "google.com.lb",
      "google.su",
      "google.eu",
      "google.porn",
      "gmail.de",
      "google.nr",
      "google.ar",
      "google.co.jp",
      "google.com.sa",
      "privacychoices.org"
   ],
   "site":{
      "phoneNumbers":[
         
      ],
      "emailAddresses":[
         
      ]
   },
   "category":{
      "sector":"Information Technology",
      "industryGroup":"Software & Services",
      "industry":"Internet Software & Services",
      "subIndustry":"Internet Software & Services",
      "gicsCode":"45103010",
      "sicCode":"73",
      "sic4Codes":[
         "7372",
         "7371"
      ],
      "naicsCode":"51",
      "naics6Codes":[
         "511210",
         "541511"
      ],
      "naics6Codes2022":[
         "513210",
         "541511"
      ]
   },
   "tags":[
      "Software",
      "Publishers",
      "Information",
      "Publishing",
      "Computer Programming",
      "Professional Services",
      "Computers",
      "E-commerce",
      "Technology",
      "Web Services & Apps",
      "Internet",
      "Information Technology & Services",
      "SAAS",
      "B2C",
      "B2B"
   ],
   "description":"Google is a multinational corporation that specializes in internet-related services and products. Its mission is to organize the world's information and make it universally accessible and useful.",
   "foundedYear":1998,
   "location":"1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
   "timeZone":"America/Los_Angeles",
   "utcOffset":-8,
   "geo":{
      "streetNumber":"1600",
      "streetName":"Amphitheatre Parkway",
      "subPremise":"None",
      "streetAddress":"1600 Amphitheatre Parkway",
      "city":"Mountain View",
      "postalCode":"94043",
      "state":"California",
      "stateCode":"CA",
      "country":"United States",
      "countryCode":"US",
      "lat":37.4213397,
      "lng":-122.0836193
   },
   "logo":"https://logo.clearbit.com/google.com",
   "facebook":{
      "handle":"google",
      "likes":23742068
   },
   "linkedin":{
      "handle":"company/google"
   },
   "twitter":{
      "handle":"Google",
      "id":"20536157",
      "bio":"#HeyGoogle",
      "followers":28946065,
      "following":294,
      "location":"Mountain View, CA",
      "site":"https://t.co/RS3iU873QG",
      "avatar":"https://pbs.twimg.com/profile_images/1605297940242669568/q8-vPggS_normal.jpg"
   },
   "crunchbase":{
      "handle":"organization/google"
   },
   "emailProvider":False,
   "type":"public",
   "ticker":"GOOG",
   "identifiers":{
      "usEIN":"None",
      "usCIK":"None"
   },
   "phone":"None",
   "metrics":{
      "alexaUsRank":1,
      "alexaGlobalRank":1,
      "trafficRank":"very_high",
      "employees":178234,
      "employeesRange":"100K+",
      "marketCap":722740000000,
      "raised":"None",
      "annualRevenue":257637000000,
      "estimatedAnnualRevenue":"$10B+",
      "fiscalYearEnd":"None"
   },
   "indexedAt":"2023-10-29T21:34:46.996Z",
   "tech":[
      "google_apps",
      "db2",
      "media.net",
      "grafana",
      "marchex",
      "oracle_crm",
      "smartsheet",
      "sybase",
      "apache_kafka",
      "sage_50cloud",
      "splunk",
      "oracle_endeca",
      "informatica",
      "appnexus",
      "apache_http_server",
      "apache_spark",
      "ibm_infosphere",
      "wrike",
      "sap_hybris_marketing",
      "couchbase",
      "atlassian_fisheye",
      "gitlab",
      "dropbox",
      "woo_commerce",
      "workamajig",
      "workday",
      "atlassian_jira",
      "sas_enterprise",
      "oracle_cash_and_treasury_management",
      "qliktech",
      "thomson_reuters_eikon",
      "flexera_software",
      "entrust",
      "tibco_spotfire",
      "oracle_data_integrator",
      "trello",
      "baidu_analytics",
      "ibm_websphere",
      "sap_concur",
      "rabbitmq",
      "cision",
      "cloudera",
      "apache_hadoop",
      "couchdb",
      "oracle_business_intelligence",
      "aws_dynamodb",
      "oracle_weblogic",
      "aws_cloudwatch",
      "openx",
      "netsuite",
      "atlassian_confluence",
      "oracle_hyperion",
      "kentico",
      "microsoft_dynamics",
      "hootsuite",
      "quickbooks",
      "successfactors",
      "sap_crystal_reports",
      "tibco_ems",
      "apache_tomcat",
      "microsoft_sql_server",
      "hp_servers",
      "hbase",
      "basecamp",
      "podio",
      "oracle_peoplesoft",
      "snaplogic",
      "okta",
      "the_trade_desk",
      "interspire",
      "fortinet",
      "mongodb",
      "microsoft_project",
      "ibm_cognos",
      "pubmatic",
      "ibm_infosphere_datastage",
      "pagerduty",
      "alteryx",
      "dell_boomi_atomsphere",
      "sas_data_integration",
      "episerver",
      "peoplesoft_crm",
      "pentaho",
      "saleslogix",
      "goldengate",
      "sap_sales_order_management",
      "jaspersoft",
      "nimsoft",
      "microsoft_teams",
      "sap_business_objects",
      "tibco_rendezvous",
      "sprinklr",
      "qlikview",
      "meltwater",
      "salesforce",
      "atlassian_crucible",
      "sugarcrm",
      "adp",
      "aws_redshift",
      "sailpoint",
      "statcounter",
      "teradata",
      "sage_crm",
      "yext",
      "google_search_appliance",
      "sage_intacct",
      "webmethods",
      "bluekai",
      "apache_storm",
      "palo_alto_networks",
      "pivotal_tracker",
      "github",
      "rsa_securid",
      "zoho_crm",
      "goldmine",
      "microstrategy",
      "oracle_fusion",
      "sap_hana",
      "matomo",
      "netsuite_crm",
      "oracle_essbase",
      "unbounce",
      "liferay",
      "five9",
      "information_builders",
      "ring_central",
      "apache_maven",
      "klarna",
      "talend",
      "clearslide",
      "twilio",
      "kronos",
      "peoplesoft_sales",
      "postgresql",
      "gigya",
      "gotomeeting",
      "mysql",
      "windows_server",
      "soasta",
      "sitefinity",
      "oracle_application_server",
      "servicenow",
      "applepay",
      "oxid",
      "adobe_marketing_cloud",
      "paychex",
      "gainsight",
      "admeld",
      "microsoft_power_bi",
      "sitecore",
      "sap_crm",
      "cyberark",
      "pipedrive",
      "factset",
      "qradar",
      "netsuite_suitecommerce",
      "salesforce_dmp",
      "magnolia_cms",
      "facebook_workplace",
      "wix",
      "neo4j",
      "openid",
      "hive",
      "filemaker_pro",
      "apache_cassandra",
      "weebly_ecommerce",
      "vmware_server",
      "sap_human_capital_management",
      "zedo"
   ],
   "techCategories":[
      "productivity",
      "database",
      "advertising",
      "monitoring",
      "marketing_automation",
      "crm",
      "data_processing",
      "accounting_and_finance",
      "data_management",
      "web_servers",
      "project_management_software",
      "ecommerce",
      "human_capital_management",
      "analytics",
      "security",
      "business_management",
      "content_management_system",
      "adverstising",
      "data_visualization",
      "customer_support",
      "social_sharing",
      "payment",
      "sales_productivity",
      "cloud_computing_services",
      "website_optimization",
      "coversion_optimization",
      "web_hosting"
   ],
   "parent":{
      "domain":"about.google"
   },
   "ultimateParent":{
      "domain":"about.google"
   }
}

new_data = {
    "status": "ok",
    "totalResults": 70032,
    "articles": [
        {
            "source": {
                "id": False,
                "name": "Biztoc.com"
            },
            "author": "wsj.com",
            "title": "US v. Google exposes Google's deepening rift with Microsoft, despite Satya Nadella's early attempts to make nice; four Microsoft witnesses have testified",
            "description": "Satya Nadella wanted to make nice with longtime rival Google when he became chief executive of Microsoft almost a decade ago. Those days now feel like a distant memory. Google’s antitrust trial in Washington, D.C., has provided a stage for Microsoft to air lo…",
            "url": "https://biztoc.com/x/896ffb6f3d30d7f6",
            "urlToImage": "https://c.biztoc.com/p/896ffb6f3d30d7f6/s.webp",
            "publishedAt": "2023-11-09T12:22:06Z",
            "content": "Satya Nadella wanted to make nice with longtime rival Google when he became chief executive of Microsoft almost a decade ago. Those days now feel like a distant memory.Googles antitrust trial in Wash… [+230 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Donanimhaber.com"
            },
            "author": "Emre Kaan Özcan",
            "title": "Google, kullanılmayan hesapları sileceğini açıkladı",
            "description": "Dünyanın en büyük arama motoru olan Amerika Birleşik Devletleri merkezli Google, önümüzdeki aydan itibaren kendi sitesindeki kullanılmayan hesapları sileceğini resmen açıkladı.",
            "url": "https://www.donanimhaber.com/google-kullanilmayan-hesaplari-silecegini-acikladi--170738",
            "urlToImage": "https://www.donanimhaber.com/images/images/haber/170738/src_340x1912xgoogle-kullanilmayan-hesaplari-silecegini-acikladi.jpg",
            "publishedAt": "2023-11-09T12:22:00Z",
            "content": "a').click(); event.preventDefault();\"&gt;Tam Boyutta Gör\r\nDünyann en büyük arama motoru olan Amerika Birleik Devletleri merkezli Google, önümüzdeki aydan itibaren kendi sitesindeki kullanlmayan hesap… [+1021 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Aftonbladet.se"
            },
            "author": False,
            "title": "Regeringen återinför gränskontroller vid Sveriges inre gräns",
            "description": "▸ I dag har regeringen fattat beslut om att återinföra gränskontroll vid Sveriges inre gräns.",
            "url": "https://www.aftonbladet.se/nyheter/a/Rr77qd/aftonbladet-direkt?pinnedEntry=1184584",
            "urlToImage": "https://images.aftonbladet-cdn.se/v2/images/156fc268-adec-4fec-ac17-baa7f1dbdb35?fit=crop&format=auto&h=56&q=50&w=100&s=8d717b112fa508073dcc3292ac8f7acfdc612d33",
            "publishedAt": "2023-11-09T12:21:26Z",
            "content": "TRE NYHETER DU INTE FÅR MISSA\r\n<ul><li>Regeringen återinför gränskontroller vid Sveriges inre gräns\r\nI dag har regeringen fattat beslut om att återinföra gränskontroll vid Sveriges inre gräns. \r\nDet … [+11846 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "ΠΙΣ: Σημαντικός ο έγκαιρος αντιγριπικός εμβολιασμός-Τι ισχύει για τον εμβολιασμό έναντι του covid",
            "description": "Σημαντικός ο έγκαιρος αντιγριπικός εμβολιασμός-Τι ισχύει για τον εμβολιασμό έναντι του SARS-CoV-2- Ποιοι πρέπει να εμβολιαστούν",
            "url": "https://www.skai.gr/news/health/pis-simantikos-o-egkairos-antigripikos-emvoliasmos",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2022-06/emvolio-covid-it.jpg?itok=qtM3ge9c",
            "publishedAt": "2023-11-09T12:21:13Z",
            "content": "- SARS-CoV-2-  \r\n, , , .\r\n 60 , , , , , , , .\r\n , , ( , ..) .\r\n 13.000 SARS-CoV-2 .\r\nO 6 , .\r\n SARS- CoV-2 60 , , .\r\n SARS- CoV-2 .\r\n .Skai.gr Google News .\r\n© 2023 skai.gr - All Rights Reserved"
        },
        {
            "source": {
                "id": False,
                "name": "Forbes"
            },
            "author": "Josipa Majic Predin, Contributor, \n Josipa Majic Predin, Contributor\n https://www.forbes.com/sites/josipamajic/",
            "title": "Venture Capital Giants In The Billion-Dollar Quest For Longevity Breakthroughs",
            "description": "These globally distributed VC funds and grant programs are reshaping the future of healthcare, and by investing in them, they're increasing our chances of paving the w...",
            "url": "https://www.forbes.com/sites/josipamajic/2023/11/09/venture-capital-giants-in-the-billion-dollar-quest-for-longevity-breakthroughs/",
            "urlToImage": "https://imageio.forbes.com/specials-images/imageserve/654cce80365b3d0e8d8a8a57/0x0.jpg?format=jpg&height=900&width=1600&fit=bounds",
            "publishedAt": "2023-11-09T12:20:37Z",
            "content": "A laboratory employee works at TreeFrog Therapeutics, a cell therapy biotech company working on ... [+] treatment research for Parkinson's disease in Pessac, on the outskirts of Bordeaux, south-weste… [+13456 chars]"
        },
        {
            "source": {
                "id": "t3n",
                "name": "T3n"
            },
            "author": "Dieter Petereit",
            "title": "Googles KI-Experten sehen kaum Intelligenz in KI-Modellen",
            "description": "Ein neues Forschungspapier dreier Deepmind-Forscher dürfte den Chefs von KI-Unternehmen, allen voran OpenAI, nicht gefallen. Darin erklären die Experten, dass Transformer-Modelle im Grunde unintelligent sind.weiterlesen auf t3n.de",
            "url": "https://t3n.de/news/googles-ki-experten-sehen-kaum-intelligenz-in-ki-modellen-1588135/",
            "urlToImage": "https://t3n.de/news/wp-content/uploads/2023/11/ai-jobinterview-1.jpg",
            "publishedAt": "2023-11-09T12:20:17Z",
            "content": "Google Deepmind ist das KI-Unternehmen im Alphabet-Konzern. Dessen Forscher:innen gelten als absolute Koryphäen auf dem Gebiet der künstlichen Intelligenz. Ihr Wort hat Gewicht.\r\nWenn nun also Google… [+3464 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Giga"
            },
            "author": "Martin Maciej",
            "title": "Android Auto deaktivieren: So geht es",
            "description": "Mit Android Auto kann man viele Funktionen vom Smartphone direkt über das Infotainment-System im Auto bedienen. Manchmal will man darauf aber nicht zugreifen und fühlt sich davon gestört. Wie kann man Android Auto deaktivieren?",
            "url": "https://www.giga.de/tipp/android-auto-deaktivieren-so-geht-es/",
            "urlToImage": "https://crops.giga.de/39/8e/1a/59c7ca94a2d20dfb26985cb99d_YyAxOTkzeDEwNDIrNjQrMTg2AnJlIDEyMDAgNjI3AzNlNTc5MjBiOWM5.jpg",
            "publishedAt": "2023-11-09T12:20:08Z",
            "content": "Mit Android Auto kann man viele Funktionen vom Smartphone direkt über das Infotainment-System im Auto bedienen. Manchmal will man darauf aber nicht zugreifen und fühlt sich davon gestört. Wie kann ma… [+2416 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Habr.com"
            },
            "author": "Frontend по-флотски",
            "title": "[Перевод] Встречаем Angular 17",
            "description": "В прошлом месяце исполнилось 13 лет с момента появления \"красного щита\" Angular. AngularJS стал отправной точкой для новой волны JavaScript-фреймворков, появившихся для поддержки растущей потребности в богатом веб-опыте. Сегодня с новым внешним видом и наборо…",
            "url": "https://habr.com/ru/articles/772894/#post-content-body",
            "urlToImage": "https://habrastorage.org/getpro/habr/upload_files/e4b/1b8/489/e4b1b8489591d2bebc8da220a5aa036a.png",
            "publishedAt": "2023-11-09T12:20:03Z",
            "content": "\"Introducing Angular v17\".\r\nFrontend -\r\n, .\r\n13 \" \" Angular. AngularJS JavaScript-, -. 17, .\r\nv17 :\r\n<ul><li>Deferrable views \r\n</li><li> 90%.\r\n</li><li> 87% 67% \r\n</li><li> , Angular\r\n</li><li></li>… [+6268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Feber.se"
            },
            "author": "Bobby Green",
            "title": "Nu kan du beställa en Cadillac Lyriq i Sverige",
            "description": "Kostar från 906.700 kronor\n\n\n\n\n\n\n\n\n\n\n\n\nNu lanserar Cadillac sin eldrivna SUV Lyriq här i Sverige. Den erbjuds i versionerna Luxury AWD och Sport AWD och båda dessa har fyrhjulsdrift, dubbla motorer på sammanlagt på 373 kW / 507 hästar, batteripack på 102 kWh …",
            "url": "https://feber.se/bil/nu-kan-du-bestalla-en-cadillac-lyriq-i-sverige/458077/",
            "urlToImage": "https://static.feber.se/article_images/57/55/52/575552.jpg",
            "publishedAt": "2023-11-09T12:20:00Z",
            "content": "+\r\nLäs artiklar före alla andra\r\nKommentera före alla andra\r\nVälj periodJu längre period, desto bättre pris. Du bestämmer! \r\nMånad\r\n39 kr/mån\r\nKvartal\r\n33 kr/mån\r\nÅr\r\n25 kr/mån\r\nVälj hur du vill beta… [+31809 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "COMPUTER BILD"
            },
            "author": "Sandra Bültermann",
            "title": "HD+ startet TV-Streaming via App",
            "description": "HD+ hat seine App erweitert: Dank neu integriertem HD+ Stream streamen Sie Ihre Lieblingssender sowie die Inhalte von Mediatheken nun auch unterwegs per Smartphone oder Tablet.",
            "url": "https://www.computerbild.de/artikel/cb-News-Internet-HD-startet-TV-Streaming-via-App-37071005.html",
            "urlToImage": "https://i.computer-bild.de/imgs/1/5/0/9/6/0/6/1/large-hd-plus-togo-194c4ed2b181019b.jpg",
            "publishedAt": "2023-11-09T12:20:00Z",
            "content": "HD+ hat seine App erweitert: Dank neu integriertem HD+ Stream streamen Sie Ihre Lieblingssender sowie die Inhalte von Mediatheken nun auch unterwegs per Smartphone oder Tablet.\r\nMit HD+ Stream hat HD… [+1456 chars]"
        },
        {
            "source": {
                "id": "der-tagesspiegel",
                "name": "Der Tagesspiegel"
            },
            "author": "Kay Grimmer",
            "title": "Thalia-Kiezbar: „Konsum“ öffnet verkürzt",
            "description": "Sie firmiert als Wohlfühlbar und ist ein Babelsberger Traditionstreff: Doch seit einer guten Woche ist das „Konsum“ zu. Am 14. November öffnet es nach Betriebsferien wieder - jedoch vorerst nur verkürzt.",
            "url": "https://www.tagesspiegel.de/potsdam/landeshauptstadt/thalia-kiezbar-konsum-offnet-verkurzt-10749130.html",
            "urlToImage": "https://www.tagesspiegel.de/images/kinocafe-konsum2/alternates/BASE_16_9_W1400/kinocafe-konsum.jpeg",
            "publishedAt": "2023-11-09T12:19:59Z",
            "content": "Das zum Kino Thalia gehörende Babelsberger Kultlokal Konsum öffnet nach einer zweiwöchigen Betriebsruhe am 14. November vorerst nur noch verkürzt. Daniela Zuklic, die gemeinsam mit Christiane Niewald… [+1377 chars]"
        },
        {
            "source": {
                "id": "der-tagesspiegel",
                "name": "Der Tagesspiegel"
            },
            "author": "Kay Grimmer",
            "title": "Thalia-Kiezbar: Potsdamer Kultlokal „Konsum“ öffnet verkürzt",
            "description": "Sie firmiert als Wohlfühlbar und ist ein Babelsberger Traditionstreff: Doch seit einer guten Woche ist das „Konsum“ zu. Am 14. November öffnet es nach Betriebsferien wieder.",
            "url": "https://www.tagesspiegel.de/potsdam/landeshauptstadt/thalia-kiezbar-potsdamer-kultlokal-konsum-offnet-verkurzt-10749130.html",
            "urlToImage": "https://www.tagesspiegel.de/images/kinocafe-konsum2/alternates/BASE_16_9_W1400/kinocafe-konsum.jpeg",
            "publishedAt": "2023-11-09T12:19:59Z",
            "content": "Das zum Kino Thalia gehörende Babelsberger Kultlokal Konsum öffnet nach einer zweiwöchigen Betriebsruhe am 14. November vorerst nur noch verkürzt. Daniela Zuklic, die gemeinsam mit Christiane Niewald… [+1377 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "CNET"
            },
            "author": "Antuan Goodwin",
            "title": "2024 Volvo EX30 First Drive: An EV Value That's Worth the Wait - CNET",
            "description": "I take an early drive in Volvo's upcoming EX30, the automaker's smallest, quickest SUV yet and one of next year's most anticipated new electric vehicles.",
            "url": "https://www.cnet.com/roadshow/news/2024-volvo-ex30-first-drive-an-ev-value-thats-worth-the-wait/",
            "urlToImage": "https://www.cnet.com/a/img/resize/aa88b5000852c2457eb53ce5e6de21217ec5748e/hub/2023/11/08/61b33918-25f7-40b5-8cc2-1db4996dae90/ogi-volvo-ex30-2024.jpg?auto=webp&fit=crop&height=675&width=1200",
            "publishedAt": "2023-11-09T12:19:47Z",
            "content": "From the moment it debuted earlier this year, Volvo's new EX30 has been my most anticipated electric vehicle of 2024. The compact SUV promised ample range, Scandinavian style and exciting performance… [+10758 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "CHIP Online Deutschland"
            },
            "author": "Michael Humpa",
            "title": "Smartspacer - Android App 1.2.2 Deutsch",
            "description": "Smartspacer - Android App 1.2.2 Deutsch: Die Gratis-App Smartspacer für Android erweitert Googles Live-Anzeige mit vielen nützlichen Funktionen.",
            "url": "https://www.chip.de/downloads/Smartspacer-Android-App_185019660.html",
            "urlToImage": "https://www.chip.de/ii/1/2/6/8/4/1/8/3/0/Design_ohne_Titel__36_-fb4c2aec385e94de.png",
            "publishedAt": "2023-11-09T12:19:00Z",
            "content": "Beschreibung\r\nLetzte Änderungen:\r\nSmartspacer - Android App\r\n wurde zuletzt am\r\n 09.11.2023\r\n aktualisiert und steht Ihnen hier\r\n in der Version\r\n 1.2.2\r\n zum Download zur Verfügung.\r\nDie CHIP Redakt… [+1287 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Smartworld.it"
            },
            "author": "Nicola Ligas",
            "title": "Ma perché le app Android non si aggiornano da sole?",
            "description": "Gli aggiornamenti automatici del Play Store, e anche del Galaxy Store, sembrano del tutto inefficaci. È un problema o è voluto?\r\nL'articolo Ma perché le app Android non si aggiornano da sole? sembra essere il primo su Smartworld.",
            "url": "https://www.smartworld.it/android/app-android-non-aggiornano.html",
            "urlToImage": "https://www.smartworld.it/images/2023/11/09/app-non-si-aggiornano-2_1200x675.jpg",
            "publishedAt": "2023-11-09T12:18:00Z",
            "content": "Le app Android si aggiornano con una frequenza elevatissima. Chi abbia tante applicazioni installate, aprendo il Play Store ogni giorno, ne troverà facilmente una decina da aggiornare, a volte anche … [+6506 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Tuttoandroid.net"
            },
            "author": "Gerardo Orlandin",
            "title": "A breve Google inizierà a eliminare gli account inutilizzati",
            "description": "Google inizierà a eliminare gli account inattivi dal mese di dicembre. Ecco cosa c'è da sapere.\nL'articolo A breve Google inizierà a eliminare gli account inutilizzati proviene da TuttoAndroid.",
            "url": "https://www.tuttoandroid.net/news/2023/11/09/google-elimina-account-inutilizzati-dicembre-2023-1019772/",
            "urlToImage": "https://img.tuttoandroid.net/wp-content/uploads/2020/08/logo_google_2019_tta_05.jpg",
            "publishedAt": "2023-11-09T12:17:12Z",
            "content": "A maggio Google aveva anticipato che avrebbe iniziato a eliminare gli account rimasti inutilizzati per tanto tempo. Ora il colosso di Mountain View ha annunciato che la pulizia inizierà il mese pross… [+1046 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Bleeding Cool News"
            },
            "author": "Aedan Juvet",
            "title": "'Fall' Movie is Confirmed to Be a Part of a Full Trilogy",
            "description": "We're very eager to witness the next chapter of the Lionsgate release Fall, a dark horse, edge-of-your-seat thriller that became a fun summer hit in 2022. But now, we're learning that the next film isn't merely a sequel; it's actually a connecting story as a …",
            "url": "https://bleedingcool.com/movies/fall-movie-is-confirmed-to-be-a-part-of-a-full-trilogy/",
            "urlToImage": "https://bleedingcool.com/wp-content/uploads/2023/04/wp11525175-1200x628.jpg",
            "publishedAt": "2023-11-09T12:17:07Z",
            "content": "Posted in: Lionsgate, Movies | Tagged: capstone studios, fall, film, lionsgate\r\nFall co-writer and director Scott Mann revealed that the upcoming sequel Fall 2 is actually a part of a planned trilogy… [+2378 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Biztoc.com"
            },
            "author": "washingtonpost.com",
            "title": "Big Tech wants AI regulation. The rest of Silicon Valley is skeptical",
            "description": "After months of high-level meetings and discussions, government officials and Big Tech leaders have agreed on one thing about artificial intelligence: The potentially world-changing technology needs some ground rules. Tech is not your friend. We are. Sign up …",
            "url": "https://biztoc.com/x/5fd16ddedf2917b5",
            "urlToImage": "https://c.biztoc.com/p/5fd16ddedf2917b5/s.webp",
            "publishedAt": "2023-11-09T12:16:34Z",
            "content": "After months of high-level meetings and discussions, government officials and Big Tech leaders have agreed on one thing about artificial intelligence: The potentially world-changing technology needs … [+294 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "MakeUseOf"
            },
            "author": "Digvijay Kumar",
            "title": "How to Save a Route on Google Maps on Any Platform",
            "description": "Whether you're using Android, iOS, or the good old web, you can save your Google Maps route for when you need it next.",
            "url": "https://www.makeuseof.com/how-save-route-on-google-maps/",
            "urlToImage": "https://static1.makeuseofimages.com/wordpress/wp-content/uploads/2023/05/google-maps-icon-on-map.jpg",
            "publishedAt": "2023-11-09T12:16:19Z",
            "content": "Key Takeaways\r\n<ul><li> Save routes on Google Maps for quick and easy access without re-entering information, avoiding congested roads and reducing traffic congestion and fuel consumption. </li><li> … [+5971 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Tuttoandroid.net"
            },
            "author": "Paolo Giorgetti",
            "title": "Unieuro lancia un “Black Friday bello bello” ricchissimo di offerte Android",
            "description": "Unieuro lancia il \"Black Friday bello bello\": scopriamo insieme le migliori offerte del volantino su smartphone, tablet Android e non solo!\nL'articolo Unieuro lancia un “Black Friday bello bello” ricchissimo di offerte Android proviene da TuttoAndroid.",
            "url": "https://www.tuttoandroid.net/news/2023/11/09/unieuro-offerte-volantino-black-friday-android-9-15-novembre-2023-1019766/",
            "urlToImage": "https://img.tuttoandroid.net/wp-content/uploads/2023/10/google-pixel-8-fotocamera-tta.jpg",
            "publishedAt": "2023-11-09T12:16:11Z",
            "content": "Mancano ancora un paio di settimane al Black Friday vero e proprio, ma Unieuro non ha intenzione di attendere e lancia il nuovo volantino “Black Friday bello bello“, con tante offerte sulla tecnologi… [+2898 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Tuttoandroid.net"
            },
            "author": "Gerardo Orlandin",
            "title": "La Ricerca Google con l’intelligenza artificiale raggiunge più continenti",
            "description": "La ricerca di Google supportata dall'intelligenza artificiale si espande in più continenti con delle novità.\nL'articolo La Ricerca Google con l’intelligenza artificiale raggiunge più continenti proviene da TuttoAndroid.",
            "url": "https://www.tuttoandroid.net/news/2023/11/09/google-sge-si-espande-1019787/",
            "urlToImage": "https://img.tuttoandroid.net/wp-content/uploads/2018/01/App_Google_59_tta.jpg",
            "publishedAt": "2023-11-09T12:16:06Z",
            "content": "Google ha annunciato che l’intelligenza artificiale generativa nella Ricerca Google si sta espandendo in oltre 120 nuovi paesi e territori, aggiungendo il supporto per quattro nuove lingue e offrendo… [+1774 chars]"
        },
        {
            "source": {
                "id": "engadget",
                "name": "Engadget"
            },
            "author": "Mat Smith",
            "title": "The Morning After: Samsung made its own generative AI model",
            "description": "Developed by Samsung Research, Gauss (named after mathematician Carl Friedrich Gauss) powers several on-device AI technologies across Samsung products. It will have a few different facets but will do a lot of the same stuff we’ve seen from other generative AI…",
            "url": "https://www.engadget.com/the-morning-after-samsung-made-its-own-generative-ai-model-121535086.html",
            "urlToImage": "https://s.yimg.com/ny/api/res/1.2/GE2uXEZP2xV9l3aIJvgJsw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD02NzU-/https://s.yimg.com/os/creatr-uploaded-images/2023-11/28233e10-7eb6-11ee-bfdf-5b1d93d4db5b",
            "publishedAt": "2023-11-09T12:15:35Z",
            "content": "Developed by Samsung Research, Gauss (named after mathematician Carl Friedrich Gauss) powers several on-device AI technologies across Samsung products. It will have a few different facets but will do… [+3862 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "International Business Times"
            },
            "author": "Raziye Akkoc",
            "title": "EU Opens Probe Into TikTok, YouTube Over Child Protection",
            "description": "The EU announced investigations on Thursday into YouTube and TikTok to find out what action the US and Chinese-owned platforms are taking to ensure the safety of minors on their platforms.",
            "url": "https://www.ibtimes.com/eu-opens-probe-tiktok-youtube-over-child-protection-3718079",
            "urlToImage": "https://d.ibtimes.com/en/full/4498112/eus-executive-arm-said-it-wanted-know-what-measures-tiktok-youtube-have-taken-comply.jpg",
            "publishedAt": "2023-11-09T12:15:31Z",
            "content": "The EU announced investigations on Thursday into YouTube and TikTok to find out what action the US and Chinese-owned platforms are taking to ensure the safety of minors on their platforms.\r\nThe Europ… [+2216 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Tecmundo.com.br"
            },
            "author": "Igor Almenara Carneiro",
            "title": "Google pode acabar de vez com apps alternativos do YouTube",
            "description": "O Google pode dar fim às últimas versões alternativas do app YouTube no Android em breve. Uma nova API incluída no sistema operacional pode limitar o funcionamento desses aplicativos, os inutilizando no processo.A novidade em teste é uma nova API WebView Medi…",
            "url": "https://www.tecmundo.com.br/software/273618-google-acabar-vez-apps-alternativos-youtube.htm",
            "urlToImage": "https://tm.ibxk.com.br/2023/11/08/08181610125388.jpg",
            "publishedAt": "2023-11-09T12:15:00Z",
            "content": "O Google pode dar fim às últimas versões alternativas do app YouTube no Android em breve. Uma nova API incluída no sistema operacional pode limitar o funcionamento desses aplicativos, os inutilizando… [+1890 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Israeli forces continue push into Gaza City - CBS Evening News",
            "description": "Israeli forces continue push into Gaza CityCBS Evening News The IDF’s war on Hamas is going better than it expected for nowThe Times of Israel Israel-Hamas war latest: IDF troops target Gaza City underground tunnels | DW NewsDW News Israel-Hamas war live upda…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204975",
            "urlToImage": False,
            "publishedAt": "2023-11-09T12:13:47Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "«Και με το μετρό και με το πράσινο, παντού», τονίζει το περιβάλλον του Χάρη Δούκα",
            "description": "«Για εμάς δίλημμα δεν υπάρχει: Και με το μετρό και με το πράσινο», αναφέρει το περιβάλλον του νέου εκλεγμένου Δημάρχου Αθηναίων",
            "url": "https://www.skai.gr/news/politics/kykloi-xari-douka-kai-me-to-metro-kai-me-to-prasino-pantou",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2023-11/xaris-doukas-intime.jpg?itok=xs2SnfrF",
            "publishedAt": "2023-11-09T12:13:41Z",
            "content": "« : », \r\n« » .\r\n« »\r\n« , . . : . . .\r\n , 1-1-2024 , . ».\r\n .Skai.gr Google News .\r\n© 2023 skai.gr - All Rights Reserved"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Republican debate: US presidential hopefuls go toe-to-toe over footwear - Reuters",
            "description": "Republican debate: US presidential hopefuls go toe-to-toe over footwearReuters Haley to Ramaswamy during heated GOP debate exchange: ‘You’re just scum’Yahoo News Nikki Haley talks about moment she called Vivek Ramaswamy 'scum' on debate stageNBC News Nikki Ha…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204973",
            "urlToImage": False,
            "publishedAt": "2023-11-09T12:13:29Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "FRANCE 24 English"
            },
            "author": "FRANCE24",
            "title": "EU opens probe into TikTok, YouTube over child protection",
            "description": "The European Commission said it had sent formal requests for information to TikTok and YouTube respectively, the first step in procedures launched under the EU's new law on digital content.\n\nThe EU's executive arm said it wanted to know what measures the vide…",
            "url": "https://www.france24.com/en/live-news/20231109-eu-opens-probe-into-tiktok-youtube-over-child-protection",
            "urlToImage": "https://s.france24.com/media/display/573044e4-7ef9-11ee-8142-005056bf30b7/w:1280/p:16x9/931fd640d90c58b6955422c5f0bbf0aeeb73fbb2.jpg",
            "publishedAt": "2023-11-09T12:13:11Z",
            "content": "Brussels (AFP) The EU announced investigations on Thursday into YouTube and TikTok to find out what action the US and Chinese-owned platforms are taking to ensure the safety of minors on their platfo… [+2243 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Robot crushes worker to death at packing plant in South Korea - NBC News",
            "description": "Robot crushes worker to death at packing plant in South KoreaNBC News Man crushed to death by robot in South KoreaBBC.com Industrial robot crushes man to death in South Korean distribution centreThe Guardian South Korean man killed by robot that failed to dif…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204971",
            "urlToImage": False,
            "publishedAt": "2023-11-09T12:13:10Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "FDA approves potent Eli Lilly obesity drug, Zepbound - STAT - STAT",
            "description": "FDA approves potent Eli Lilly obesity drug, Zepbound - STATSTAT FDA approves new weight loss drug ZepboundNBC News China and Australia trade talks are warming upQuartz FDA approves Eli Lilly’s diabetes drug Mounjaro for obesity under new name, ZepboundCNN Dia…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204969",
            "urlToImage": False,
            "publishedAt": "2023-11-09T12:12:52Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Apple co-founder Steve Wozniak hospitalized in Mexico City, source says - CNN",
            "description": "Apple co-founder Steve Wozniak hospitalized in Mexico City, source saysCNN View Full Coverage on Google News ...",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204965",
            "urlToImage": False,
            "publishedAt": "2023-11-09T12:12:34Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Aftonbladet.se"
            },
            "author": False,
            "title": "Polisen utreder misstänkt grovt brott på skola",
            "description": "▸ En gymnsiekola i Västerås har inrymt elever och lärare på en skola i Västerås.",
            "url": "https://www.aftonbladet.se/nyheter/a/Rr77qd/aftonbladet-direkt?pinnedEntry=1184582",
            "urlToImage": "https://images.aftonbladet-cdn.se/v2/images/156fc268-adec-4fec-ac17-baa7f1dbdb35?fit=crop&format=auto&h=56&q=50&w=100&s=8d717b112fa508073dcc3292ac8f7acfdc612d33",
            "publishedAt": "2023-11-09T12:12:21Z",
            "content": "TRE NYHETER DU INTE FÅR MISSA\r\n<ul><li>Polisen utreder misstänkt grovt brott på skola\r\nEn gymnsieskola i Västerås har inrymt sina elever och lärare.\r\nPolisen är på plats och utreder eventuellt grovt … [+11846 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Victor Wembanyama, Spurs fizzle on big stage in New York - ESPN - ESPN",
            "description": "Victor Wembanyama, Spurs fizzle on big stage in New York - ESPNESPN San Antonio Spurs vs. New York Knicks: 3 Best BetsSports Illustrated Spurs 105-126 Knicks (Nov 8, 2023) Game RecapESPN Despite lackluster debut, bright lights of MSG will continue to shine fo…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204963",
            "urlToImage": False,
            "publishedAt": "2023-11-09T12:12:10Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Biztoc.com"
            },
            "author": "dcs-spotify.megaphone.fm",
            "title": "Streaming Saves Disney & Video Games Keep Crushing It",
            "description": "Episode 188: Neal and Toby discuss why WeWork's bankruptcy could majorly disrupt the commercial real estate market. Plus, the guys share the biggest takeaways from entertainment and video games earnings reports and why Disney may be leaning on streaming to br…",
            "url": "https://biztoc.com/x/0ca22bfb36f12fef",
            "urlToImage": "https://c.biztoc.com/p/0ca22bfb36f12fef/s.webp",
            "publishedAt": "2023-11-09T12:12:02Z",
            "content": "Episode 188: Neal and Toby discuss why WeWork's bankruptcy could majorly disrupt the commercial real estate market. Plus, the guys share the biggest takeaways from entertainment and video games earni… [+279 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Madmoizelle.com"
            },
            "author": "Elisa Covo",
            "title": "Cyberharcèlement : Instagram et TikTok vont faciliter l’accès au 3018",
            "description": "Jeudi 9 novembre se tient la journée nationale de lutte contre le harcèlement scolaire. Pour l’occasion, les plateformes TikTok et Instagram ont annoncé s’allier à l’association e-Enfance, pour aider leurs jeunes utilisateurs victimes ou témoins de cyberharcè…",
            "url": "https://www.madmoizelle.com/cyberharcelement-instagram-et-tik-tok-vont-faciliter-lacces-au-3018-1593645",
            "urlToImage": "https://www.madmoizelle.com/wp-content/uploads/2023/11/copie-de-image-de-une-classique-horizontale-1.jpg",
            "publishedAt": "2023-11-09T12:12:00Z",
            "content": "De nouvelles fonctionnalités vont être ajoutées aux deux réseaux, afin de lutter contre le cyberharcèlement des utilisateurs sur ces plateformes. Une initiative pilotée conjointement avec l’associati… [+2115 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Capital FM Kenya"
            },
            "author": "Phidel Kizito",
            "title": "Google beefs up search with AI-powered engine - Capital Business",
            "description": "NAIROBI, Kenya, Nov 9 - Google has introduced an artificial intelligence (AI) search engine to enhance search results. Called ‘Search Generative Kenya breaking news | Kenya news today |",
            "url": "https://www.capitalfm.co.ke/business/2023/11/google-beefs-up-search-with-ai-powered-engine/",
            "urlToImage": "https://www.capitalfm.co.ke/business/files/2023/11/WAMBUI-KINYA-copy.jpg",
            "publishedAt": "2023-11-09T12:08:48Z",
            "content": "NAIROBI, Kenya, Nov 9 – Google has introduced an artificial intelligence (AI) search engine to enhance search results.\r\nCalled Search Generative Experience (SGE), it will run in the sub-Saharan Afric… [+1445 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Hospitality Net"
            },
            "author": "HotelRunner",
            "title": "HotelRunner Invites to Explore the Tomorrow of Hospitality Technology at The Phocuswright Conference",
            "description": "HotelRunner, a leading innovator in travel and hospitality technology, will attend The Phocuswright Conference from November 13 to 16 in Florida. Sponsored by HotelRunner, the premier event will once again bring together the top industry professionals and dec…",
            "url": "https://www.hospitalitynet.org/news/4119057.html",
            "urlToImage": "https://www.hospitalitynet.org/picture/social_153162766.jpg?t=1699522663",
            "publishedAt": "2023-11-09T12:08:10Z",
            "content": "HotelRunner, a leading innovator in travel and hospitality technology, will attend The Phocuswright Conference from November 13 to 16 in Florida. Sponsored by HotelRunner, the premier event will once… [+3017 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "Αιφνίδια συνάντηση Ερντογάν με τον Ιρανό πρόεδρο Ραΐσι: «Είμαστε αντιμέτωποι με μια σφαγή που νομιμοποιεί τη σφαγή παιδιών»",
            "description": "Ο Τούρκος πρόεδρος κατά τη συνάντησή του με τον Ιρανό πρόεδρο στην Τασκένδη στο πλαίσιο της Συνόδου Οικονομικής Συνεργασίας εξαπέλυσε νέα «πυρά» κατά του Ισραήλ και των δυτικών χωρών κατηγορώντας τους ότι σιωπούν και παρακολουθούν από μακριά «τις σφαγές στο Ι…",
            "url": "https://www.skai.gr/news/world/synantisi-erntogan-me-ton-irano-proedro-raisi",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2023-11/ap_erdogan-raisi.jpg?itok=qFgDf2Gw",
            "publishedAt": "2023-11-09T12:07:48Z",
            "content": ", , , , , . \r\n , «» « , ».\r\n«, , , , , , , . . , , » .\r\n« , .   , .\r\n , , 15 . , .» .\r\n«, 25 Charlie Hebdo, . 11.000 . H . T .   , ,   ;» .\r\n .Skai.gr Google News ."
        },
        {
            "source": {
                "id": False,
                "name": "Rg.ru"
            },
            "author": False,
            "title": "Samsung представила конкурента ChatGPT, который будет работать смартфонах Galaxy",
            "description": "Компания раскрыла детали своих последних разработок в области искусственного интеллекта. На конференции Samsung AI Forum 2023 было официально объявлено о том, что южнокорейская компания создала собственную генеративную мультимодальную модель Samsung Gauss.",
            "url": "https://rg.ru/2023/11/09/samsung-predstavila-konkurenta-chatgpt-kotoryj-budet-rabotat-smartfonah-galaxy.html",
            "urlToImage": "https://cdnstatic.rg.ru/uploads/images/2023/11/09/1454_b95.jpg",
            "publishedAt": "2023-11-09T12:07:24Z",
            "content": "Samsung Gauss Language, Samsung Gauss Code Samsung Gauss Image. , : , , .\r\nGauss Language - , : , , . Gauss Language \" \" Samsung, Android- One UI .\r\nGauss Image - , , , , .\r\n Gauss Code (code. i), , … [+544 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Biztoc.com"
            },
            "author": "poynter.org",
            "title": "Google and Meta owe US news publishers about $14 billion a year, our research estimates",
            "description": "News publishers all over the world have tried to estimate what Google and Meta owe them for the news they distribute to audiences. This is a difficult task due to a lack of publicly available data about audience behavior and because a lack of competition make…",
            "url": "https://biztoc.com/x/a44997e7abe727eb",
            "urlToImage": "https://c.biztoc.com/p/a44997e7abe727eb/s.webp",
            "publishedAt": "2023-11-09T12:06:16Z",
            "content": "News publishers all over the world have tried to estimate what Google and Meta owe them for the news they distribute to audiences. This is a difficult task due to a lack of publicly available data ab… [+291 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Expansion.com"
            },
            "author": "Daniel G. Lifona",
            "title": "Sixt supera por primera vez los 1.000 millones de euros de ingresos en un solo trimestre",
            "description": "La compañía alemana de alquiler de coches registró unos ingresos de 1.130 millones de euros en el tercer trimestre, un 13,2% más que en el mismo trimestre del año anterior, aunque los beneficios cayeron hasta los 246,9 millones. Leer",
            "url": "https://www.expansion.com/empresas/motor/2023/11/09/654ccaf2e5fdea77468b4616.html",
            "urlToImage": "https://phantom-expansion.unidadeditorial.es/80ecaa15baad9ba6c37d4c15a9200d2c/crop/71x73/1229x843/f/webp/assets/multimedia/imagenes/2023/11/09/16995310796006.jpg",
            "publishedAt": "2023-11-09T12:05:28Z",
            "content": "Sixt se ha convertido en patrocinador de Chicago Bulls y Los Angeles Lakers.\r\nLa compañía alemana de alquiler de coches registró unos ingresos de 1.130 millones de euros en el tercer trimestre, un 13… [+554 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Marketscreener.com"
            },
            "author": False,
            "title": "Xometry Reports Third Quarter 2023 Results",
            "description": "(marketscreener.com) Q3 revenue increased 15% year-over-year driven by strong marketplace growth of 22% year-over-year and 10% quarter-over-quarter. Supplier services revenue decreased 16% year-over-year primarily due to the $2 million year-over-year impact f…",
            "url": "https://www.marketscreener.com/quote/stock/XOMETRY-INC-124221576/news/Xometry-Reports-Third-Quarter-2023-Results-45285338/",
            "urlToImage": "https://www.marketscreener.com/images/twitter_MS_fdnoir.png",
            "publishedAt": "2023-11-09T12:05:01Z",
            "content": "<ul><li>Q3 revenue increased 15% year-over-year driven by strong marketplace growth of 22% year-over-year and 10% quarter-over-quarter. Supplier services revenue decreased 16% year-over-year primaril… [+64734 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "Στην τελική ευθεία το Νέο Αρχαιολογικό Μουσείο Σπάρτης",
            "description": "Το νέο μουσείο θα στεγαστεί στο στο κτίριο-μνημείο του π. εργοστασίου ΧΥΜΟΦΙΞ",
            "url": "https://www.skai.gr/news/culture/sparti-stin-teliki-eytheia-to-neo-arxaiologiko-mouseio",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2023-11/sparti-mouseio.jpg?itok=HYwsDQcG",
            "publishedAt": "2023-11-09T12:04:09Z",
            "content": "-  . \r\n , , , , , , .\r\n , , « , - ».\r\n , : ) , ) , ' , , .\r\n, 20 , . , . , - - . .\r\n - , (1957) , .\r\n, , .\r\n, 1.350 .., , , , , , . , , .\r\n, . , , , , , , . , , , . , , . , Cafe, , . , , , . ' , , , … [+71 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "GlobeNewswire"
            },
            "author": "Xometry, Inc.",
            "title": "Xometry Reports Third Quarter 2023 Results",
            "description": "Xometry Reports Third Quarter 2023 Results......",
            "url": "https://www.globenewswire.com/news-release/2023/11/09/2777204/0/en/Xometry-Reports-Third-Quarter-2023-Results.html",
            "urlToImage": "https://ml.globenewswire.com/Resource/Download/75f696b5-1105-460d-be1b-58599cdd3454",
            "publishedAt": "2023-11-09T12:04:00Z",
            "content": "<ul><li>Q3 revenue increased 15% year-over-year driven by strong marketplace growth of 22% year-over-year and 10% quarter-over-quarter. Supplier services revenue decreased 16% year-over-year primaril… [+64383 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Gadgets360.com"
            },
            "author": "Sucharita Ganguly, Ketan Pratap",
            "title": "Best Deals on Top OnePlus Smartphones During Ongoing Amazon Sale",
            "description": "The Amazon Great Indian Festival will end tomorrow, November 10. The e-commerce site has been offering a wide range of items at significantly discounted prices on multiple products throughout the sale. With just one day of the sale remaining, the following ar…",
            "url": "https://www.gadgets360.com/mobiles/news/amazon-great-indian-festival-finale-days-sale-2023-oneplus-nord-ce-3-oneplus-open-and-more-4561037",
            "urlToImage": "https://i.gadgets360cdn.com/large/oneplus_Amazon_Sale_oneplus_1699530351368.jpg",
            "publishedAt": "2023-11-09T12:03:51Z",
            "content": "Amazon Great Indian Festival is finally ending. The sale, which started on October 7 for Amazon Prime users in India and was later open to everyone from October 8, will end tomorrow, November 10. The… [+3128 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Marketscreener.com"
            },
            "author": False,
            "title": "Xometry Leverages Google Cloud To Accelerate The Digitization Of Manufacturing Globally",
            "description": "(marketscreener.com) Google Cloud Vertex AI To Help Accelerate Deployment Of Auto-Quote Methods & Models Within Xometry’s AI-Powered Instant Quoting EngineWill Help Ensure Xometry’s Instant Quoting Engine® Encompasses The Broadest Set Of Manufacturing Technol…",
            "url": "https://www.marketscreener.com/quote/stock/XOMETRY-INC-124221576/news/Xometry-Leverages-Google-Cloud-To-Accelerate-The-Digitization-Of-Manufacturing-Globally-45285294/",
            "urlToImage": "https://www.marketscreener.com/images/twitter_MS_fdblanc.png",
            "publishedAt": "2023-11-09T12:03:02Z",
            "content": "<ul><li>Google Cloud Vertex AI To Help Accelerate Deployment Of Auto-Quote Methods &amp; Models Within Xometrys AI-Powered Instant Quoting Engine</li><li>Will Help Ensure Xometrys Instant Quoting Eng… [+3755 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "GlobeNewswire"
            },
            "author": "Xometry, Inc.",
            "title": "Xometry Leverages Google Cloud To Accelerate The Digitization Of Manufacturing Globally",
            "description": "Xometry Leverages Google Cloud To Accelerate The Digitization Of Manufacturing Globally......",
            "url": "https://www.globenewswire.com/news-release/2023/11/09/2777202/0/en/Xometry-Leverages-Google-Cloud-To-Accelerate-The-Digitization-Of-Manufacturing-Globally.html",
            "urlToImage": "https://ml.globenewswire.com/Resource/Download/75f696b5-1105-460d-be1b-58599cdd3454",
            "publishedAt": "2023-11-09T12:02:00Z",
            "content": "<ul><li>Google Cloud Vertex AI To Help Accelerate Deployment Of Auto-Quote Methods &amp; Models Within Xometrys AI-Powered Instant Quoting Engine</li><li>Will Help Ensure Xometrys Instant Quoting Eng… [+3748 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Xataka.com"
            },
            "author": "Javier Lacort",
            "title": "Un editor de Wikipedia se pasó años simulando ser Russian Red. En realidad era un estafador indio",
            "description": "Tan solo era una marioneta. El usuario de Wikipedia llamado \"Lourdes\", registrado en 2015, era uno de los activos usuarios de la plataforma que acostumbraba a crear y editar páginas con regularidad. Dedicaba mucho tiempo a colaborar en el proyecto, convirtién…",
            "url": "https://www.xataka.com/servicios/editor-wikipedia-se-paso-anos-simulando-ser-russian-red-realidad-era-estafador-indio",
            "urlToImage": "https://i.blogs.es/78f5dc/dest2/840_560.jpeg",
            "publishedAt": "2023-11-09T12:01:44Z",
            "content": "Tan solo era una marioneta. El usuario de Wikipedia llamado \"Lourdes\", registrado en 2015, era uno de los activos usuarios de la plataforma que acostumbraba a crear y editar páginas con regularidad. … [+4615 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Xataka Android"
            },
            "author": "Alejandro Alcolea",
            "title": "Si quieres actualizaciones de HyperOS, olvídate de desbloquear el bootloader: Xiaomi lo va a poner difícil",
            "description": "Aunque aún no ha terminado el año, ya estamos muy pendientes de los móviles que llegarán a comienzos de 2024. Uno de los contrincantes de la gama alta será Samsung con su Galaxy S24, pero Xiaomi también está muy bien posicionado con el recién presentado Xiaom…",
            "url": "https://www.xatakandroid.com/sistema-operativo/quieres-actualizaciones-hyperos-olvidate-desbloquear-bootloader-xiaomi-va-a-poner-dificil",
            "urlToImage": "https://i.blogs.es/a3876f/hyperos-2/840_560.jpeg",
            "publishedAt": "2023-11-09T12:01:44Z",
            "content": "Aunque aún no ha terminado el año, ya estamos muy pendientes de los móviles que llegarán a comienzos de 2024. Uno de los contrincantes de la gama alta será Samsung con su Galaxy S24, pero Xiaomi tamb… [+3411 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "Οι Πανθέοι: Η Νίνα προειδοποιεί τη Μάρμω - Δείτε το sneak preview",
            "description": "Απόψε στις 21.00, στον ΣΚΑΪ",
            "url": "https://www.skai.gr/news/entertainment/oi-pantheoi-i-nina-proeidopoiei-ti-marmo-deite-to-sneak-preview",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2023-11/marmo_0.jpg?itok=UmD9B_LD",
            "publishedAt": "2023-11-09T12:01:15Z",
            "content": ", « », 21.00, .\r\n , . , \r\n . \r\n , .\r\n sneak preview:\r\n , , , . \r\n , , . , \r\n trailer:\r\n , . \r\n;;;\r\ninstagram.com/pantheoi.official/\r\nfacebook.com/pantheoi.official/\r\n#Pantheoi\r\n .Skai.gr Google News ."
        },
        {
            "source": {
                "id": "t3n",
                "name": "T3n"
            },
            "author": "Nils Bolder",
            "title": "Ähnlich wie Whatsapp: Muss Apple iMessage bald für andere Dienste öffnen?",
            "description": "Mehrere Unternehmen wollen Apples Chat-App von der EU als „Kerndienst“ einstufen lassen. Dadurch müsste iMessage vollständig mit Konkurrenzprodukten kompatibel werden.weiterlesen auf t3n.de",
            "url": "https://t3n.de/news/dma-apple-imessage-andere-dienste-whatsapp-1588076/",
            "urlToImage": "https://t3n.de/news/wp-content/uploads/2023/11/shutterstock_2153899491.jpg",
            "publishedAt": "2023-11-09T12:01:08Z",
            "content": "Google möchte Apples Nachrichtendienst iMessage auch für seine Geräte zugänglich machen. Dafür hat sich das Unternehmen in einem Verbund mit mehreren großen Netzbetreibern wie Telekom und Vodafone an… [+2052 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Gqitalia.it"
            },
            "author": "Luca Pierattini",
            "title": "Da oggi Instagram e Facebook diventano a pagamento, se vuoi",
            "description": "Instagram e Facebook stanno per diventare a pagamento anche in Italia. Dopo l'annuncio a livello globale di qualche mese fa e i primi test in Australia e Nuova Zelanda, Meta sta iniziando a far comparire i primi avvisi per spronare gli utenti ad abbonarsi anc…",
            "url": "https://www.gqitalia.it/article/abbonamento-instagram-facebook-quanto-costa",
            "urlToImage": "https://media.gqitalia.it/photos/654ca96fb5877f8e3d9deb0a/16:9/w_1280,c_limit/ig-banner.jpg",
            "publishedAt": "2023-11-09T12:01:05Z",
            "content": "Instagram e Facebook stanno per diventare a pagamento anche in Italia. Dopo l'annuncio a livello globale di qualche mese fa e i primi test in Australia e Nuova Zelanda, Meta sta iniziando a far compa… [+3277 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Help Net Security"
            },
            "author": "Industry News",
            "title": "SnapAttack extends collaboration with Mandiant to optimize threat detection for organizations",
            "description": "SnapAttack announced an expanded partnership with Mandiant, part of Google Cloud, to extend operationalized threat intelligence to organizations of all sizes. Building on its current API integrations, the new endeavor will bring Mandiant’s threat intelligence…",
            "url": "https://www.helpnetsecurity.com/2023/11/09/snapattack-mandiant-partnership/",
            "urlToImage": "https://img.helpnetsecurity.com/wp-content/uploads/2023/05/10093706/hns-2023-large_logo.jpg",
            "publishedAt": "2023-11-09T12:00:48Z",
            "content": "SnapAttack announced an expanded partnership with Mandiant, part of Google Cloud, to extend operationalized threat intelligence to organizations of all sizes. \r\nBuilding on its current API integratio… [+2916 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Wwwhatsnew.com"
            },
            "author": "Juan Diego Polo",
            "title": "Lantern – Cooperación tecnológica contra la explotación infantil",
            "description": "La Tech Coalition ha presentado Lantern, una iniciativa interplataformas diseñada para fortalecer las políticas de seguridad infantil de las empresas tecnológicas. En un esfuerzo colaborativo sin precedentes, este programa busca poner freno a dos de las amena…",
            "url": "https://wwwhatsnew.com/2023/11/09/lantern-cooperacion-tecnologica-contra-la-explotacion-infantil/",
            "urlToImage": "https://wwwhatsnew.com/wp-content/uploads/2023/11/lantern.jpg",
            "publishedAt": "2023-11-09T12:00:40Z",
            "content": "La Tech Coalitionha presentado Lantern, una iniciativa interplataformas diseñada para fortalecer las políticas de seguridad infantil de las empresas tecnológicas. En un esfuerzo colaborativo sin prec… [+3483 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Mojandroid.sk"
            },
            "author": "Laura Imrichová",
            "title": "Google Play vám povie, ako bude aplikácia vyzerať na rôznych zariadeniach",
            "description": "Google Play zobrazuje screenshoty, ktoré ukazujú výzor aplikácie pri jej používaní na smartfóne. Práve túto funkciu ide Google vylepšiť.",
            "url": "https://www.mojandroid.sk/google-play-novinka/",
            "urlToImage": "https://www.mojandroid.sk/wp-content/uploads/2023/02/google-play-titulka.jpg",
            "publishedAt": "2023-11-09T12:00:35Z",
            "content": "Obchod Google Play opä prichádza so zaujímavou novinkou. O tom, ako bude vyzera informoval portál PhoneArena. Pri sahovaní aplikácii sa momentálne zobrazujú aj screenshoty, ktoré ukazujú to, ako bude… [+1572 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Compradiccion.com"
            },
            "author": "Álvaro Núñez",
            "title": "El DJI Mini 2 SE es el dron ultraligero ideal para principiantes: con grabación 2,7K y buena autonomía de vuelo",
            "description": "Aunque una gran variedad de drones que se enfocan simplemente en ofrecer una experiencia divertida al hacerlos volar, los más impresionantes están equipados con cámaras de gran calidad para obtener grabaciones en vídeo impresionantes desde las alturas. Uno de…",
            "url": "https://www.compradiccion.com/drones-y-robotica/l-dji-mini-2-se-dron-ultraligero-ideal-para-principiantes-grabacion-2-7k-buena-autonomia-vuelo",
            "urlToImage": "https://i.blogs.es/b96d01/portada-dji-2-/840_560.jpeg",
            "publishedAt": "2023-11-09T12:00:33Z",
            "content": "Aunque una gran variedad de drones que se enfocan simplemente en ofrecer una experiencia divertida al hacerlos volar, los más impresionantes están equipados con cámaras de gran calidad para obtener g… [+2116 chars]"
        },
        {
            "source": {
                "id": "les-echos",
                "name": "Les Echos"
            },
            "author": "Les Echos",
            "title": "Levée de fonds : comment briller face aux potentiels investisseurs",
            "description": "EXTRAIT DE LIVRE / Lever des fonds est un exercice de style qu'il faut bien préparer pour convaincre les investisseurs. Carole Juge-Llewellyn, autrice du livre « Boss Mama* » propose dans cet extrait ses conseils pour réussir pas à pas votre levée de fonds.",
            "url": "https://business.lesechos.fr/entrepreneurs/financer-sa-creation/0902852105359-levee-de-fonds-comment-briller-face-aux-potentiels-investisseurs-352997.php",
            "urlToImage": "https://business.lesechos.fr/medias/2023/11/09/352997_levee-de-fonds-comment-briller-face-aux-potentiels-investisseurs-web-tete-0902869241894.jpg",
            "publishedAt": "2023-11-09T12:00:32Z",
            "content": "Une levée de fonds est avant tout un exercice de style : il faut réussir à convaincre des gens de vous donner cet argent, autrement dit d'investir à vos côtés dans votre société, qu'elle soit au stad… [+6656 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Poynter"
            },
            "author": "Anya Schiffrin",
            "title": "Google and Meta owe US news publishers about $14 billion a year, our research estimates",
            "description": "News publishers all over the world have tried to estimate what Google and Meta owe them for the news they distribute to audiences. This is a difficult task due to […]\nThe post Google and Meta owe US news publishers about $14 billion a year, our research estim…",
            "url": "https://www.poynter.org/commentary/2023/google-and-meta-owe-us-news-publishers-about-14-billion-a-year-our-research-estimates/",
            "urlToImage": "https://www.poynter.org/wp-content/uploads/2023/11/shutterstock_1740301712.jpg",
            "publishedAt": "2023-11-09T12:00:27Z",
            "content": "News publishers all over the world have tried to estimate what Google and Meta owe them for the news they distribute to audiences. This is a difficult task due to a lack of publicly available data ab… [+5642 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Ferra.ru"
            },
            "author": "Максим Многословный",
            "title": "Ненасытный голод ИИ Bing: Microsoft обратилась к ускорителям Nvidia у Oracle",
            "description": "Microsoft объединяет усилия с Oracle для удовлетворения огромных вычислительных потребностей своих растущих сервисов искусственного интеллекта, в частности, моделей машинного обучения в Bing. В рамках многолетнего партнерства Microsoft намерена использовать о…",
            "url": "https://www.ferra.ru/news/computers/nenasytnyi-golod-ii-bing-microsoft-obratilas-k-uskoritelyam-nvidia-u-oracle-09-11-2023.htm",
            "urlToImage": "https://www.ferra.ru/imgs/2023/11/09/10/6216902/afc142bdaa609088ee629e73acd5245837dff77f.png",
            "publishedAt": "2023-11-09T12:00:27Z",
            "content": "Bing Chat, Microsoft , , , . GPU- Oracle , - Bing .\r\n Oracle Interconnect for Microsoft Azure, Azure Oracle.\r\nGoogle -, Bing Microsoft , , StatCounter."
        },
        {
            "source": {
                "id": False,
                "name": "Kevinmd.com"
            },
            "author": "Valerie LeComte, DO",
            "title": "A doctor’s thoughts on The Retrievals podcast",
            "description": "I recently listened to the podcast mini-series The Retrievals. It was fascinating and absolutely worth a listen. It’s the story of a Yale infertility clinic where a nurse was stealing fentanyl and replacing it with normal saline. As a result, women ended up g…",
            "url": "https://www.kevinmd.com/2023/11/a-doctors-thoughts-on-the-retrievals-podcast.html",
            "urlToImage": "https://www.kevinmd.com/wp-content/uploads/shutterstock_1430461481-5.jpg",
            "publishedAt": "2023-11-09T12:00:25Z",
            "content": "I recently listened to the podcast mini-series The Retrievals. It was fascinating and absolutely worth a listen. It’s the story of a Yale infertility clinic where a nurse was stealing fentanyl and re… [+5117 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Android Police"
            },
            "author": "Zachary Kew-Denniss",
            "title": "The Pixel 8 Pro has this Samsung user considering a switch to Google",
            "description": "Team red or team blue?",
            "url": "https://www.androidpolice.com/samsung-user-switch-pixel-8-pro/",
            "urlToImage": "https://static1.anpoimages.com/wordpress/wp-content/uploads/wm/2023/11/s23-ultra-pixel-8-pro-3-1.JPG",
            "publishedAt": "2023-11-09T12:00:22Z",
            "content": "If you know anything about me, you know I'm a big fan of Samsung's smartphones. In fact, next March will mark the fifth anniversary of my move to Galaxy devices. I'd spent most of the 2010s using Nex… [+11141 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "MobileSyrup"
            },
            "author": "Bradly Shankar",
            "title": "Where to stream the BlackBerry limited series in Canada",
            "description": "The story of BlackBerry is getting turned into a three-part limited series — well, sort of. BlackBerry, the show, is an extended, episodic version of Toronto filmmaker Matt Johnson’s Canadian motion picture of the same name that was released earlier this year…",
            "url": "https://mobilesyrup.com/2023/11/09/blackberry-film-limited-series-where-to-stream-canada/",
            "urlToImage": "https://cdn.mobilesyrup.com/wp-content/uploads/2023/11/blackberry-mike-scaled.jpg",
            "publishedAt": "2023-11-09T12:00:17Z",
            "content": "The story of BlackBerry is getting turned into a three-part limited series — well, sort of.\r\nBlackBerry, the show, is an extended, episodic version of Toronto filmmaker Matt Johnson’s Canadian motion… [+2229 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Googlewatchblog.de"
            },
            "author": "Jens",
            "title": "Google Drive: Neue Oberfläche für die Android-App zeigt sich; neuer Kamerabutton, Hintergrundfarben und mehr",
            "description": "Die Google Drive Android-App erhält wohl bald ein neues Design, das sich jetzt auf ersten Screenshots zeigt.Google Drive: Neue Oberfläche für die Android-App zeigt sich; neuer Kamerabutton, Hintergrundfarben und mehrKeine Google-News mehr verpassen: GoogleWat…",
            "url": "https://www.googlewatchblog.de/?p=214180",
            "urlToImage": "https://www.googlewatchblog.de/wp-content/uploads/google-drive-new-logo-2020.png",
            "publishedAt": "2023-11-09T12:00:02Z",
            "content": "Das optische Grundgerüst von Google Drive hat sich über die Jahre kaum verändert und setzt auf allen Plattformen auf ein recht ähnliches Design. Jetzt zeigt sich eine neue Oberfläche für die Android-… [+1387 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Caschys Blog"
            },
            "author": "Olli",
            "title": "Google bot Epic wohl 147 Millionen US-Dollar für Fortnite im Play Store an",
            "description": "Fornite ist ein beliebter Battle-Royal-Shooter, der auf vielen Plattformen spielbar ist. Auch unter Android kann man spielen, insofern man sich den Titel über die Website direkt besorgt und dann per Sideloading installiert. Epic umgeht den Play Store, damit m…",
            "url": "https://stadt-bremerhaven.de/google-bot-epic-wohl-147-millionen-us-dollar-fuer-fortnite-im-play-store-an/",
            "urlToImage": "https://stadt-bremerhaven.de/wp-content/uploads/2022/01/google-logo.jpg",
            "publishedAt": "2023-11-09T12:00:01Z",
            "content": "Fornite ist ein beliebter Battle-Royal-Shooter, der auf vielen Plattformen spielbar ist. Auch unter Android kann man spielen, insofern man sich den Titel über die Website direkt besorgt und dann per … [+1269 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Abertoatedemadrugada.com"
            },
            "author": "Carlos Martins",
            "title": "Developers têm que testar apps durante 2 semanas antes de as publicar na Play Store",
            "description": "A Google apresentou novas regras para developers para tentar assegurar um nível mínimo de qualidade para as apps na Play Store.",
            "url": "https://abertoatedemadrugada.com/2023/11/developers-tem-que-testar-apps-durante.html",
            "urlToImage": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiaOVT4QK4gdgaaBtyxRhD1L_NJTiFAhHFA9joar-kDgeFLgYqJwY5F7ypk_y3JJVN_Wod9TZm1lEqO-Cez8HJU07zEoPoaKhmKT-2hP-2o8cEOKi6RPja1Ln3NHIIVzksxkDO2TAPCPG5luNy8cnQ9dolDoT7rP4-j9rUfbnLsna-o_oTWyDqVDnnGuPZG/w1200-h630-p-k-no-nu/play.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "A Google apresentou novas regras para developers para tentar assegurar um nível mínimo de qualidade para as apps na Play Store, incluindo a obrigatoriedade de as testarem durante duas semanas antes d… [+1147 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Feber.se"
            },
            "author": "Roger Åberg",
            "title": "Trailer för Mr. Monk's Last Case: A Monk Movie",
            "description": "Monk har fått ett sista uppdrag och en egen film\n\n\n\n\n\n\n\n\n\n\nMr. Monk's Last Case: A Monk Movie är den långa titeln på en film som är sprungen ur en tv-serie med en kort titel: Monk. Tv-serien rullade på i åtta säsonger mellan 2002 och 2009. \n\nI filmen får vi å…",
            "url": "https://feber.se/film/trailer-for-mr-monks-last-case-a-monk-movie/458050/",
            "urlToImage": "https://i.ytimg.com/vi/Krfd3OWb4hs/hqdefault.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "+\r\nLäs artiklar före alla andra\r\nKommentera före alla andra\r\nVälj periodJu längre period, desto bättre pris. Du bestämmer! \r\nMånad\r\n39 kr/mån\r\nKvartal\r\n33 kr/mån\r\nÅr\r\n25 kr/mån\r\nVälj hur du vill beta… [+33090 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Fast Company"
            },
            "author": "Mark Wilson",
            "title": "Apple vet Imran Chaudhri is betting his reputation—and $240M—on Humane’s AI wearable",
            "description": "Humane’s Ai Pin, which debuts today, is the most hyped piece of hardware in recent memory.\n\n\n\nWith $240 million in funding from luminaries including Salesforce CEO Marc Benioff and OpenAI CEO Sam Altman, the device attaches to your lapel with magnets, listens…",
            "url": "https://www.fastcompany.com/90979863/apple-vet-imran-chaudhri-is-betting-his-reputation-and-240m-on-humanes-ai-wearable",
            "urlToImage": "https://images.fastcompany.net/image/upload/w_1280,f_auto,q_auto,fl_lossy/wp-cms/uploads/2023/11/06-90979863-mark-wilson-humane-review.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "Humane’s Ai Pin, which debuts today, is the most hyped piece of hardware in recent memory. \r\nWith $240 million in funding from luminaries including Salesforce CEO Marc Benioff and OpenAI CEO Sam Altm… [+14258 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Ferra.ru"
            },
            "author": "Андрей Кадуков",
            "title": "Google потребовала от ЕС признать доминирование Apple из-за мессенджера iMessage",
            "description": "Google потребовала от ЕС признать доминирование Apple из-за мессенджера iMessage. Google и несколько европейских телеком-операторов обратились к еврокомиссару Тьерри Бретону с требованием признать эксклюзивность мессенджера iMessage на мобильных устройствах A…",
            "url": "https://www.ferra.ru/news/apps/kto-by-govoril-google-obvinila-apple-v-nechestnoi-konkurencii-iz-za-imessage-08-11-2023.htm",
            "urlToImage": "https://www.ferra.ru/imgs/2023/11/08/16/6215814/fc7247edd23dce334901a4718ec0549e2e803c10.jpeg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "Google, Deutsche Telekom, Orange, Telefonica, Vodafone , Apple iMessage . , iMessage , Android, .\r\n Apple , iMessage , iOS. iMessage , .\r\nApple , , , , 2024 . Apple, iOS iMessage, iPhone ."
        },
        {
            "source": {
                "id": False,
                "name": "Techtarget.com"
            },
            "author": "Esther Ajao",
            "title": "DataRobot GenAI features aim to address enterprise concerns",
            "description": "The AI vendor's new capabilities addresses concerns about the new technology such as governance, cost and scale. It also helps enterprises bridge two types of AI.",
            "url": "https://www.techtarget.com/searchenterpriseai/news/366558682/DataRobot-genAI-features-aim-to-address-enterprise-concerns",
            "urlToImage": "https://cdn.ttgtmedia.com/rms/onlineimages/iot_g1182604383.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "DataRobot on Thursday introduced new governance and observability capabilities for generative and predictive AI technology for its AI platform.\r\nThe capabilities include Generative AI Guard Models, L… [+5491 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Vnexpress.net"
            },
            "author": "VnExpress",
            "title": "Samsung ra AI tương tự ChatGPT",
            "description": "Samsung Gauss là mô hình AI tạo sinh với hàng loạt tính năng thông minh, dự kiến tích hợp lên thiết bị của hãng thời gian tới.",
            "url": "https://vnexpress.net/samsung-ra-ai-tuong-tu-chatgpt-4674789.html",
            "urlToImage": "https://vcdn1-sohoa.vnecdn.net/2023/11/09/sga3-081123-231920-800-resize-1977-4764-1699499503.png?w=1200&h=0&q=100&dpr=1&fit=crop&s=hX32hsaLFP2h1d1hvkMPxA",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "Samsung Gauss là mô hình AI to sinh vi hàng lot tính nng thông minh, d kin tích hp lên thit b ca hãng thi gian ti.Theo hãng in t Hàn Quc, mô hình AI c t theo tên nhà toán hc Carl Friedrich Gauss, ngi… [+1711 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Seroundtable.com"
            },
            "author": "Barry Schwartz",
            "title": "Ghostbusters Car Outside Google Dublin",
            "description": "This might be an old photo but it seems like one Halloween week at the Google Dublin office there was the Ghostbusters car parked outside of the Dublin office there. We saw this car once at the GooglePlex in California but now at Dublin?\n\nI found this on Inst…",
            "url": "https://www.seroundtable.com/photos/ghostbusters-car-outside-google-dublin-36323.html",
            "urlToImage": "https://s3.amazonaws.com/images.seroundtable.com/ghostbusters-car-outside-google-1698936831.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "This might be an old photo but it seems like one Halloween week at the Google Dublin office there was the Ghostbusters car parked outside of the Dublin office there. We saw this car once at the Googl… [+234 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Forbes.com.mx"
            },
            "author": "Wolfgang Erhardt",
            "title": "Buró de Crédito: Las preguntas de la Semana Nacional de Educación Financiera 2023",
            "description": "Forbes México.\n Buró de Crédito: Las preguntas de la Semana Nacional de Educación Financiera 2023\n\nEl Buró de Crédito fue uno de los temas clave de la Semana Nacional de Educación Financiera de la Condusef, el evento más importante de su tipo en México.\nBuró …",
            "url": "https://www.forbes.com.mx/las-preguntas-de-la-semana-nacional-de-educacion-financiera-2023/",
            "urlToImage": "https://cdn.forbes.com.mx/2022/03/finanzas-digitales.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "Hace poco concluyó la Semana Nacional de Educación Financiera de la Condusef, el evento más importante de su tipo en México. Aquí las preguntas que recibí con mayor frecuencia sobre el Buró de Crédit… [+3809 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Dutchcowboys.nl"
            },
            "author": "Ron Smeets, Ron Smeets",
            "title": "Huawei heeft momenteel de beste smartphone camera",
            "description": "Waar ooit de toptoestellen van Samsung en Apple steevast de beste smartphone camera's hadden, hebben de Chinese concurrenten een flinke inhaalslag gemaakt.",
            "url": "https://www.dutchcowboys.nl/mobile/huawei-heeft-momenteel-de-beste-smartphone-camera",
            "urlToImage": "https://www.dutchcowboys.nl/uploads/posts/list/huawei-p60pro-620.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "Telkens als er een nieuwe (high-end) smartphone gepresenteerd wordt, dan gaan de testers van DXO Mark een van de toonaangevende sites op het gebied van smartphone camera beoordelingen aan de slag om … [+2906 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Daily Geek Show"
            },
            "author": "contact@dailygeekshow.com (DGS), DGS",
            "title": "Un astronome pense que la vie extraterrestre est une IA ultra développée",
            "description": "L’existence de la vie extraterrestre a longtemps stimulé l’imagination humaine. Mais  Lord Marin Rees affirme dans un article de la BBC que la vie au-delà de notre planète pourrait être dominée par l'intelligence artificielle plutôt que par des organismes bio…",
            "url": "https://dailygeekshow.com/vie-extraterrestre-ia/",
            "urlToImage": "https://dailygeekshow.com/wp-content/uploads/2023/11/une-ia-espace.jpg",
            "publishedAt": "2023-11-09T12:00:00Z",
            "content": "Andrey Suslov / Shutterstock.com\r\nLexistence de la vie extraterrestre a longtemps stimulé limagination humaine. Mais Martin Rees affirme dans un article de la BBC que la vie au-delà de notre planète … [+2302 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Aftonbladet.se"
            },
            "author": False,
            "title": "UD bekräftar terrormisstankar om de gripna i Tunisien",
            "description": "▸ Utrikesdepartementet bekräftar att de fem svenska medborgarna som har häktats i Tunisien är misstänkta för att tillhöra…",
            "url": "https://www.aftonbladet.se/nyheter/a/Rr77qd/aftonbladet-direkt?pinnedEntry=1184579",
            "urlToImage": "https://images.aftonbladet-cdn.se/v2/images/156fc268-adec-4fec-ac17-baa7f1dbdb35?fit=crop&format=auto&h=56&q=50&w=100&s=8d717b112fa508073dcc3292ac8f7acfdc612d33",
            "publishedAt": "2023-11-09T11:59:17Z",
            "content": "TRE NYHETER DU INTE FÅR MISSA\r\n<ul><li>UD bekräftar terrormisstankar om de gripna i Tunisien \r\nUtrikesdepartementet bekräftar att de fem svenska medborgarna som har häktats i Tunisien är misstänkta f… [+11706 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Nakedcapitalism.com"
            },
            "author": "Lambert Strether",
            "title": "Links 11/9/2023",
            "description": "Our daily links, with all mod cons",
            "url": "https://www.nakedcapitalism.com/2023/11/links-11-9-2023.html",
            "urlToImage": "https://www.nakedcapitalism.com/wp-content/uploads/2023/11/gaza_tunnels.jpeg",
            "publishedAt": "2023-11-09T11:58:56Z",
            "content": "Translucent microbe deviates from universal genetic code PNAS\r\nWhy My Recession Rule Could Go Wrong This Time Claudia Sahm, Bloomberg. URL: “one-highly-accurate-recession-indicator-could-be-wrong-thi… [+9199 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Touch Arcade"
            },
            "author": "Mikhail Madnani",
            "title": "‘Wingspan’ Oceania Expansion Release Date Announced for iOS, Android, Switch, Xbox, and PC",
            "description": "The most recent news for Wingspan following the release of the European Expansion has been that the Oceania Expansion is … Continue reading \"‘Wingspan’ Oceania Expansion Release Date Announced for iOS, Android, Switch, Xbox, and PC\"",
            "url": "https://toucharcade.com/2023/11/09/wingspan-oceania-expansion-release-date-digital-iphone-android-switch-steam-deck-pc-xbox/",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:58:02Z",
            "content": "The most recent news for Wingspan following the release of the European Expansion has been that the Oceania Expansion is due soon on all platforms. Ahead of that release, Monster Couch has pushed out… [+1176 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Businessinsider.com.pl"
            },
            "author": "Marianne Guenot",
            "title": "Zaginiony kontynent ponownie odkryty. 155 mln lat po zniknięciu",
            "description": "Kontynent Argoland, który oddzielił się od Australii i zniknął 155 mln lat temu, został w końcu odnaleziony. Potwierdza to nowe badanie naukowców z Holandii. Odkrycie tłumaczy wiele zagadek, w tym m.in. zachowanie niektórych zwierząt w tym regionie.",
            "url": "https://businessinsider.com.pl/wiadomosci/zaginiony-kontynent-argoland-ponownie-odkryty-155-mln-lat-po-zniknieciu/be0b8cm",
            "urlToImage": "https://ocdn.eu/pulscms-transforms/1/IKZk9kpTURBXy80YWFiMTIwMDk4NWM0MjE1YjViY2Y3OWQ3ZjRkODY0NC5wbmeSlQMAJM0E2M0CuZMFzQSwzQJ23gABoTAB",
            "publishedAt": "2023-11-09T11:57:47Z",
            "content": "Podziay kontynentów zwykle pozostawiaj lady w staroytnych skamieniaociach, skaach i pasmach górskich. Jednak do tej pory naukowcy nie byli w stanie znale miejsca, w którym znajdowa si Argoland.\r\nTera… [+3545 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Iz.ru"
            },
            "author": "Владимир Зайвый",
            "title": "Мошенники стали перенаправлять проверочные звонки в фейковый кол-центр",
            "description": "Телефонные мошенники научились перенаправлять проверочные звонки, совершаемые в банк, в поддельный кол-центр. Об этом 9 ноября сообщила пресс-служба Positive Technologies.Специалисты компании обнаружили новую мошенническую схему в одном из банков Южной Кореи.…",
            "url": "https://iz.ru/1602551/2023-11-09/moshenniki-stali-perenapravliat-proverochnye-zvonki-v-feikovyi-kol-tcentr",
            "urlToImage": "http://cdn.iz.ru/sites/default/files/styles/900x506/public/news-2023-11/20230731_gaf_rs74_015.jpg?itok=6td743Y2",
            "publishedAt": "2023-11-09T11:57:29Z",
            "content": ", , -. 9 - Positive Technologies.\r\n . .\r\n« , Google Play, . , - , », .\r\n , . Positive Technologies , .\r\n , , .pdf. , QR-.\r\n . , 10 5,8 , 11% 2022-.\r\n, 3 , «», . , . , , , ."
        },
        {
            "source": {
                "id": False,
                "name": "Bleeding Cool News"
            },
            "author": "Rich Johnston",
            "title": "Kate Micucci Confesses To Drawing Cartoons Outside Jazba In New York",
            "description": "Kate Micucci is one of my favourite American performers, actor, writer and one-half of the astonishing Garfunkel & Oates comedy songsters. It's possible you might also know her from Scrubs, The Big Bang Theory, Easy, Raising Hope, Imaginary Larry, Steven Univ…",
            "url": "https://bleedingcool.com/comics/kate-micucci-confesses-to-drawing-cartoons-outside-jazba-in-new-york/",
            "urlToImage": "https://bleedingcool.com/wp-content/uploads/2023/11/a-1200x628.jpg",
            "publishedAt": "2023-11-09T11:57:07Z",
            "content": "Posted in: Comics | Tagged: east village, Jazba, Junoon, Kate Micucci, new york\r\nKate Micucci turned to TikTok to confess that she drew all the cartoons on the outside of the Jazba restaurant in the … [+2878 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Aftonbladet.se"
            },
            "author": False,
            "title": "Ingen manifestation på årsdagen av kristallnatten",
            "description": "▸ Det blir ingen offentlig manifestation i Malmö på årsdagen av kristallnatten den 9 november.",
            "url": "https://www.aftonbladet.se/nyheter/a/Rr77qd/aftonbladet-direkt?pinnedEntry=1184578",
            "urlToImage": "https://images.aftonbladet-cdn.se/v2/images/156fc268-adec-4fec-ac17-baa7f1dbdb35?fit=crop&format=auto&h=56&q=50&w=100&s=8d717b112fa508073dcc3292ac8f7acfdc612d33",
            "publishedAt": "2023-11-09T11:56:33Z",
            "content": "TRE NYHETER DU INTE FÅR MISSA\r\n<ul><li>Ingen manifestation på årsdagen av kristallnatten\r\nDet blir ingen offentlig manifestation i Malmö på årsdagen av kristallnatten den 9 november.\r\n Det är primärt… [+11706 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Tabletowo.pl"
            },
            "author": "Maciej Paszkiewicz",
            "title": "Google chciało zapłacić Epic Games 147 milionów dolarów za Fortnite?",
            "description": "Google chciało zapłacić 147 milionów dolarów za Fortnite? Światło dziennie ujrzały nowe fakty w sprawie konfliktu Google z Epic Games.Przeczytaj pełny artykuł tutaj: Google chciało zapłacić Epic Games 147 milionów dolarów za Fortnite?",
            "url": "https://www.tabletowo.pl/konflikt-google-z-epic-games-o-fortnite/",
            "urlToImage": "https://www.tabletowo.pl/wp-content/uploads/2018/05/fortnite-2.jpg",
            "publishedAt": "2023-11-09T11:56:11Z",
            "content": "Konflikt pomidzy Google, a Epic Games przybiera na sile, a sprawa obecnie jest w sdzie, gdzie wiato dzienne ujrzay nowe fakty. Gigant z Mountain View chcia zapaci Epicowi a 147 milionów dolarów. Za c… [+2112 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Expansion.com"
            },
            "author": "Alejandro Sánchez",
            "title": "El valor más sensible al acuerdo de investidura amplía sus caídas en Bolsa",
            "description": "El acuerdo alcanzado entre el PSOE y Junts allana la formación de un nuevo Gobierno y aleja la opción de una repetición electoral, un escenario que pasa factura a la empresa de la Bolsa española que sufre los mayores bandazos en su cotización con los cambios …",
            "url": "https://www.expansion.com/mercados/2023/11/09/654cc7ed468aeb0f2e8b466f.html",
            "urlToImage": "https://phantom-expansion.unidadeditorial.es/47b10ad96c79d9bb62a355aaee4f1a5e/crop/168x0/1921x1167/resize/1200/f/webp/assets/multimedia/imagenes/2023/11/09/16995306800111.jpg",
            "publishedAt": "2023-11-09T11:55:54Z",
            "content": "Interior de la Bolsa de Madrid\r\n EFE\r\nEl acuerdo alcanzado entre el PSOE y Junts allana la formación de un nuevo Gobierno y aleja la opción de una repetición electoral, un escenario que pasa factura … [+555 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "Πακιστάν: Χιλιάδες Αφγανοί παράνομοι μετανάστες κρύβονται για να γλιτώσουν την απέλαση και την τιμωρία των Ταλιμπάν",
            "description": "Από την 1η Νοεμβρίου, οι πακιστανικές αρχές έχουν ξεκινήσει επιχειρήσεις «εντοπισμού και συγκέντρωσης» σε όλη τη χώρα",
            "url": "https://www.skai.gr/news/world/pakistan-xiliades-afganoi-xoris-eggrafa-kryvontai-gia-na-glitosoun-tin-apelasi",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2023-11/ap-pakistan-afganistan.jpg?itok=00fJLcw3",
            "publishedAt": "2023-11-09T11:54:07Z",
            "content": ", , . \r\n , 1 , , « »\r\n« , , , », 23 , , , .\r\n , .\r\n .\r\n 23 2019.\r\n , , \r\n, , , .\r\n« , , », , 30 , .\r\n . .\r\n , .\r\n« » - \r\n Reuters . , .\r\n35 , .\r\n , .\r\n«», 22 , .\r\n , 28 , , , .\r\n , , , , 11 , , . . ,… [+84 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Takeaways from the third Republican presidential debate - CNN",
            "description": "Takeaways from the third Republican presidential debateCNN Republican debate: 5 GOP candidates clash on abortion, TikTok and Israel-Hamas warYahoo News Alyssa Milano: GOP Debate Candidates Talked Tough, But Said NothingThe Daily Beast DeSantis was strong, Hal…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204915",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:54:05Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "A third of Gaza City damaged or destroyed by bombing, satellite imagery shows - NPR",
            "description": "A third of Gaza City damaged or destroyed by bombing, satellite imagery showsNPR US says it won't tell space-imagery companies to stop showing Gaza photosDefense One The US restricts sales of satellite images over just one state—IsraelQuartz Satellite company…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204911",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:53:47Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "After Tlaib's censure, what does 'from the river to the sea' actually mean - NPR",
            "description": "After Tlaib's censure, what does 'from the river to the sea' actually meanNPR Israel-Hamas war: List of key events, day 33Al Jazeera English Majority of House Dems won't sign statement rejecting phrase many say advocates elimination of IsraelFox News 'From th…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204907",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:53:29Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Livemint"
            },
            "author": "Bloomberg",
            "title": "Adani flagship aims big on data centers with $1.5 billion capex planned",
            "description": "Adani Enterprises, the flagship of billionaire Gautam Adani, will spend around $1.5 billion on its fledgling data center business in the next three years, as growth focus returns at the Indian conglomerate after a short seller attack sent it into months of da…",
            "url": "https://www.livemint.com/companies/news/adani-enterprises-aims-big-on-data-centers-with-1-5-billion-capex-planned-11699530057136.html",
            "urlToImage": "https://www.livemint.com/lm-img/img/2023/11/09/1600x900/Adani_Enterprises_1699530280396_1699530280617.JPG",
            "publishedAt": "2023-11-09T11:53:14Z",
            "content": "Adani Enterprises Ltd., the flagship of billionaire Gautam Adani, will spend around $1.5 billion on its fledgling data center business in the next three years, as growth focus returns at the Indian c… [+2557 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Apple should pay €13bn Irish tax, argues EU lawyer - BBC.com",
            "description": "Apple should pay €13bn Irish tax, argues EU lawyerBBC.com Apple suffers setback in fight against EU's $14 billion tax orderReuters Apple dealt blow at top EU court over €14.3bn tax bill in IrelandFinancial Times EU court adviser backs EU's $14 bln tax order t…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204903",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:53:11Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "November 2023 security update hits the Galaxy Z Flip 4 - SamMobile - Samsung news",
            "description": "November 2023 security update hits the Galaxy Z Flip 4SamMobile - Samsung news The Galaxy Z Fold 5 is still available with a whopping discount on Amazon ahead of Black Friday; save on one nowPhoneArena Samsung Takes a Trip Down Memory Lane With Its All-New Ga…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204901",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:52:53Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "Actors’ union reaches tentative deal with Hollywood film and TV studios, ending historic strike - CNN",
            "description": "Actors’ union reaches tentative deal with Hollywood film and TV studios, ending historic strikeCNN The Strike Is Over! SAG-AFTRA & Studios Reach Tentative Deal On New Three-Year ContractDeadline SAG-AFTRA committee approves deal with studios to end historic s…",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204897",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:52:35Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Slashdot.org"
            },
            "author": "feedfeeder",
            "title": "First Photos From Euclid Mission Show the Cosmos in Razor-Sharp Detail - The Wall Street Journal",
            "description": "First Photos From Euclid Mission Show the Cosmos in Razor-Sharp DetailThe Wall Street Journal Scientists show off the wide vision of Europe’s Euclid space telescopeArs Technica See the First Dazzling Images From the Euclid Space TelescopeSmithsonian Magazine …",
            "url": "https://slashdot.org/firehose.pl?op=view&amp;id=172204895",
            "urlToImage": False,
            "publishedAt": "2023-11-09T11:52:09Z",
            "content": "Sign up for the Slashdot newsletter! OR check out the new Slashdot job board to browse remote jobs or jobs in your areaDo you develop on GitHub? You can keep using GitHub but automatically sync your … [+268 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Biztoc.com"
            },
            "author": "protos.com",
            "title": "The main Bitcoin-dev mailing list might cease operating next month",
            "description": "Bitcoin developers could apparently stop operating the main Bitcoin-dev email list — the most important communication channel dedicated to coordinating the development of Bitcoin Core — by January. Bryan Bishop, one of only three named Bitcoin-Dev moderators,…",
            "url": "https://biztoc.com/x/979807dd43e59947",
            "urlToImage": "https://c.biztoc.com/p/979807dd43e59947/s.webp",
            "publishedAt": "2023-11-09T11:52:08Z",
            "content": "Bitcoin developers could apparently stop operating the main Bitcoin-dev email list the most important communication channel dedicated to coordinating the development of Bitcoin Core by January.Bryan … [+296 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Frandroid"
            },
            "author": "Bob Jouy",
            "title": "Voici les vraies performances de la nouvelle Tesla Model 3 face à l’ancienne version",
            "description": "Qui dit nouvelle Tesla Model 3, dit nouveaux tests en tous genres pour les observateurs de la firme d'Elon Musk. Aujourd'hui, nous allons voir si la nouvelle Tesla Model 3 Propulsion fait le poids face aux anciennes au niveau des performances sur un départ ar…",
            "url": "https://www.frandroid.com/marques/tesla/1850731_voici-les-vraies-performances-de-la-nouvelle-tesla-model-3-face-a-lancienne-version",
            "urlToImage": "https://images.frandroid.com/wp-content/uploads/2023/11/tesla-model-3-performance-scaled.jpg",
            "publishedAt": "2023-11-09T11:50:33Z",
            "content": "Qui dit nouvelle Tesla Model 3, dit nouveaux tests en tous genres pour les observateurs de la firme d'Elon Musk. Aujourd'hui, nous allons voir si la nouvelle Tesla Model 3 Propulsion fait le poids fa… [+2695 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "Ιτούδης: «Πολύ καλή κίνηση ο Σπανούλης στην Εθνική, ήταν δική μου ιδέα»",
            "description": "Ο Δημήτρης Ιτούδης επικρότησε την πρόσληψη του Βασίλη Σπανούλη από την ΕΟΚ τονίζοντας πως ήταν δική του ιδέα",
            "url": "https://www.skai.gr/news/world/itoudis-poly-kali-kinisi-o-spanoulis-stin-ethniki-itan-diki-mou-idea",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2023-11/3946980_132359.jpg?itok=-hVjG5wA",
            "publishedAt": "2023-11-09T11:49:32Z",
            "content": ", .\r\n« . . . , », .\r\n Kill Bill . « . .\r\n . , . (.. , ), », .\r\n .Skai.gr Google News .\r\n© 2023 skai.gr - All Rights Reserved"
        },
        {
            "source": {
                "id": False,
                "name": "Emerce.nl"
            },
            "author": "Erwin Boogert",
            "title": "‘YouTube TV is Google snelstgroeiende product’",
            "description": "De betaalde streamingdienst YouTube TV is volgens interne bronnen van Google het snelstgroeiende product van het techbedrijf.",
            "url": "https://www.emerce.nl/nieuws/youtube-tv-google-snelstgroeiende-product",
            "urlToImage": "https://www.emerce.nl/content/uploads/2023/11/getty-images-exABUVLmoYU-unsplash.jpg",
            "publishedAt": "2023-11-09T11:49:17Z",
            "content": "Nieuws -9 november 2023 - 12:49De betaalde streamingdienst YouTube TV is volgens interne bronnen van Google het snelstgroeiende product van het techbedrijf.\r\nTV groeide in het jaar vanaf oktober 2022… [+1096 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Frandroid"
            },
            "author": "Mélanie Capelli",
            "title": "De 699 € à 299 € : le prix du Xiaomi 11T Pro dégringole à quelques jours du Black Friday",
            "description": "Avec l'arrivée du Black Friday, de nombreux e-commerçants commencent les festivités. Rue du Commerce frappe fort et propose une vente flash sur le Xiaomi 11T Pro qui chute à 299 euros au lieu de 699 euros à sa sortie.",
            "url": "https://www.frandroid.com/bons-plans/1850475_de-699-e-a-299-e-le-prix-du-xiaomi-11t-pro-degringole-a-quelques-jours-du-black-friday",
            "urlToImage": "https://images.frandroid.com/wp-content/uploads/2021/09/xiaomi-11t-pro-4.jpg",
            "publishedAt": "2023-11-09T11:48:41Z",
            "content": "Avec l'arrivée du Black Friday, de nombreux e-commerçants commencent les festivités. Rue du Commerce frappe fort et propose une vente flash sur le Xiaomi 11T Pro qui chute à 299 euros au lieu de 699 … [+2460 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Independent.ie"
            },
            "author": "Adrian Weckler",
            "title": "EU rules that other countries cannot sidestep Irish DPC to regulate Google, Meta and TikTok",
            "description": "Google, Meta and TikTok have won a European court case against attempts by other EU countries to bypass Ireland’s Data Protection Commissioner, Helen Dixon, when it comes to setting rules for content.",
            "url": "https://www.independent.ie/business/technology/eu-rules-that-other-countries-cannot-sidestep-irish-dpc-to-regulate-google-meta-and-tiktok/a61193590.html",
            "urlToImage": "https://focus.independent.ie/thumbor/FafPMaAUz-4DQG4QR5EGoQWMjIg=/0x0:1504x1002/1504x1002/prod-mh-ireland/4abe5129-3891-4ba0-aabf-0213b5e9c628/f18d0c9d-6e99-41ce-a408-471fddb82926/4abe5129-3891-4ba0-aabf-0213b5e9c628.jpg",
            "publishedAt": "2023-11-09T11:47:02Z",
            "content": "The case was brought by Austria, which passed a law seeking to regulate hate speech online separately from the Irish Data Protection Commissioner\r\nGoogle, Meta and TikTok have won a European court ca… [+2080 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Independent.ie"
            },
            "author": "Adrian Weckler",
            "title": "EU rules that other countries cannot sidestep Ireland to regulate Google, Meta and TikTok",
            "description": "Google, Meta and TikTok have won a European court case against attempts by other EU countries to bypass Ireland when it comes to setting rules for content.",
            "url": "https://www.independent.ie/business/technology/eu-rules-that-other-countries-cannot-sidestep-ireland-to-regulate-google-meta-and-tiktok/a61193590.html",
            "urlToImage": "https://focus.independent.ie/thumbor/vAR0Zmb0NZKngBTcbX71VP29uu8=/136x0:1579x962/1443x962/prod-mh-ireland/2b6c8ff3-9deb-42fb-8b14-0c2a3aa5423b/88ccba86-257f-4846-bab2-e68fb97fc071/2b6c8ff3-9deb-42fb-8b14-0c2a3aa5423b.jpg",
            "publishedAt": "2023-11-09T11:47:02Z",
            "content": "The case was brought by Austria, which passed a law seeking to regulate hate speech online separately\r\nGoogle, Meta and TikTok have won a European court case against attempts by other EU countries to… [+1992 chars]"
        },
        {
            "source": {
                "id": False,
                "name": "Skai.gr"
            },
            "author": "Newsroom",
            "title": "«Venom 3»: Η πρεμιέρα της ταινίας θα γίνει στις 8 Νοεμβρίου",
            "description": "Η Sony ανακοίνωσε τη νέα ταινία της σειράς κατά τη διάρκεια του CinemaCon το 2022, ενώ παραμένει μυστικό το νέο σενάριο",
            "url": "https://www.skai.gr/news/cinema/venom-3-i-premiera-tis-tainias-tha-ginei-stis-8-noemvriou",
            "urlToImage": "https://www.skai.gr/sites/default/files/styles/article_16_9/public/2023-11/venom.jpg?itok=_jgHCj45",
            "publishedAt": "2023-11-09T11:46:57Z",
            "content": "(SAG-AFTRA) 118 Sony Pictures «Venom» 8 2024.\r\n'Venom 3' Release Date Moved to November 2024 https://t.co/EB8pctAPWL\r\nVariety (@Variety) November 9, 2023\r\n Variety, 12 2024. , . ' ', , .\r\n alter-ego … [+123 chars]"
        }
    ]
}

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        organizations = Organization.objects.all()
        return render(request, 'generate_certificate.html', {'organizations': organizations})

def validate(request):
    return render(request, 'verify_certificate.html')

def generate_certificate_id(certificate_data):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def add_certificate(request):
    certificate_id = None
    from_address = os.getenv('wallet_address')
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            # Save the certificate data to the Django model
            certificate = form.save()

            assigned_date_timestamp = int(datetime.datetime.combine(certificate.assigned_date, datetime.time()).timestamp())
            expire_date_timestamp = int(datetime.datetime.combine(certificate.expire_date, datetime.time()).timestamp())
            # Generate a certificate ID
            certificate_id = generate_certificate_id(certificate)

            # Connect to Ganache
            w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0) 

            contract = w3.eth.contract(address=C_ADDRESS, abi=C_ABI)

            # Send a transaction to add the certificate to the blockchain
            tx_hash = contract.functions.addCertificate(
                certificate.name,
                certificate.organization,
                certificate.certificate_for,    
                int(assigned_date_timestamp),  # Convert to UNIX timestamp
                int(expire_date_timestamp),  # Convert to UNIX timestamp
                certificate.email,
                certificate_id
            ).transact({'from': from_address})

            tx_receipt = None
            while tx_receipt is None:
                tx_receipt = w3.eth.get_transaction_count(from_address)
                time.sleep(2)

            # Update the Django model with the certificate ID
            certificate.certificate_id = certificate_id
            certificate.save()
        else:
            print(form.errors)

    else:
        form = CertificateForm()

    return render(request, 'generate_certificate.html', {'form': form, 'certificate_id': certificate_id})

def verify_certificate(request):
    certificate_id = None
    certificate_data = None
    certificate_valid = None
    if request.method == 'POST':
        certificate_id = request.POST.get('certificate_id', '')

        # Check if the certificate ID is valid by querying the blockchain
        w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0) 

        contract = w3.eth.contract(address=C_ADDRESS, abi=C_ABI)
        try:
            certificate_index = contract.functions.getCertificateIndex(certificate_id).call()
            if certificate_index != 0:
                # Certificate exists on the blockchain; retrieve its data
                cert_data = contract.functions.getCertificateData(certificate_id).call()
                certificate_data = {
                    'name': cert_data[0],
                    'organization': cert_data[1],
                    'certificateFor': cert_data[2],
                    'assignedDate': datetime.datetime.fromtimestamp(cert_data[3]).strftime("%d %B, %Y"),
                    'expireDate': datetime.datetime.fromtimestamp(cert_data[4]).strftime("%d %B, %Y"),
                }
                certificate_valid = True
        except:
            certificate_valid = False

    return render(request, 'verify_certificate.html', {
        'certificate_id': certificate_id,
        'certificate_data': certificate_data,
        'certificate_valid': certificate_valid,
    })

def trust_score(request):
    domain_name = None
    trust_score = None
    if request.method == 'POST':
        domain_name = request.POST.get('domain_name', '')
        trust_score = calculate_trust_score(company_data)
        

    return render(request, 'trust_score.html', {
        'domain_name': domain_name, 
        'trust_score': trust_score,
        })

def data_extract(request):
    filename = None
    name = None
    email = None
    phone = None
    skills = None
    education = None
    experience = None

    if request.method == 'POST' and request.FILES['pdf_file']:
        output_string = StringIO()
        pdf_file = request.FILES['pdf_file']
        file_content = pdf_file.read()
        pdf_file_object = io.BytesIO(file_content)
        text = extract_text(pdf_file_object)
        name = extract_name(text)
        email = extract_email_from_resume(text)
        phone = extract_contact_number_from_resume(text)
        skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau', 'Machine Learning', 'Web Development', 'Django', 'Flask', 'FastAPI', 'API Development', 'Data Analysis', 'Data Visualization', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Natural Language Processing', 'Computer Vision', 'Deep Learning', 'SQL', 'Database Management', 'MongoDB', 'PostgreSQL', 'RESTful APIs', 'GraphQL', 'Git', 'Version Control', 'Linux', 'Bash Scripting', 'Containerization', 'Docker', 'Kubernetes', 'DevOps', 'Continuous Integration/Continuous Deployment (CI/CD)', 'Testing', 'Unit Testing', 'Selenium', 'Agile Methodologies', 'Scrum', 'AWS', 'Azure', 'Google Cloud Platform (GCP)', 'Serverless Architecture', 'Microservices', 'Blockchain', 'Cybersecurity', 'Automation', 'CI/CD Tools (Jenkins, Travis CI)', 'Web Scraping', 'RESTful APIs', 'GraphQL', 'OAuth', 'JSON Web Tokens (JWT)', 'WebSocket', 'Asynchronous Programming', 'Concurrency', 'Multithreading', 'Design Patterns', 'Algorithms', 'Data Structures', 'Cybersecurity', 'IoT (Internet of Things)', 'Robotics', 'UI/UX Design', 'Frontend Frameworks (React, Angular, Vue)', 'HTML', 'CSS', 'JavaScript', 'Responsive Web Design', 'Cross-browser Compatibility', 'Mobile App Development', 'Flutter', 'React Native', 'RESTful APIs', 'GraphQL', 'OAuth', 'JSON Web Tokens (JWT)', 'WebSocket', 'Game Development', 'Pygame', 'Unity with Python', 'AR/VR Development', 'Big Data', 'Apache Spark', 'Hadoop', 'Elasticsearch', 'CI/CD Tools (Jenkins, Travis CI)', 'Business Intelligence (BI)', 'Tableau', 'Power BI', 'Communication Skills', 'Problem-Solving', 'Critical Thinking', 'Team Collaboration', 'Project Management', 'Time Management', 'Adaptability', 'Continuous Learning']
        extracted_skills = extract_skills_from_resume(text, skills_list)
        extracted_education = extract_education_from_resume(text)
        return render(request, 'data_extract.html', {
            'filename': pdf_file.name,
            'name': name,
            'email': email,
            'phone': phone,
            'skills': extracted_skills,
            'education': extracted_education,
            })
    
    return render(request, 'data_extract.html')

def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number

def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email
    
def extract_skills_from_resume(text, skills_list):
    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return ', '.join(skills)

def extract_education_from_resume(text):
    education = []

    # Use regex pattern to find education information
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPhD(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())

    return ', '.join(education)

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    # Define name patterns
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
        # Add more patterns as needed
    ]

    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text

    return None

def analyze_sentiment(description):
    # Use TextBlob for sentiment analysis
    blob = TextBlob(description)
    sentiment_score = blob.sentiment.polarity  # Sentiment polarity ranges from -1 to 1

    # Normalize the sentiment score to a scale of 0 to 1
    normalized_score = (sentiment_score + 1) / 2

    return normalized_score

def get_media_mentions(company_name):
    six_months_ago = datetime.datetime.now() - timedelta(days=30)
    formatted_date = six_months_ago.strftime("%Y-%m-%d")
    api_key = os.getenv('news_api_key')
    news_api_url = 'https://newsapi.org/v2/everything?q={}&from={}&sortBy=publishedAt&apiKey={}'.format(company_name, formatted_date, api_key)

    try:
        response = requests.get(news_api_url)
        if response.status_code == 200:
            media_mentions = response.json()
            return media_mentions
        # if new_data:
        #     return(new_data)
        else:
            print(f"Error: Unable to fetch media mentions. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    return 0

def get_domain_reputation(domain):
    
    api_key = os.getenv('whoisxmlapi_key')
    api_url = "https://domain-reputation.whoisxmlapi.com/api/v2?apiKey={}&domainName={}".format(api_key, domain)
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['reputationScore']
    else:
        return 0

def normalize_score(score, max_value):
    return min(score / max_value, 1.0)
    
def calculate_trust_score(company_data):
    trust_score = 0

    

    # Method 1: Media Mentions
    media_mentions = get_media_mentions(company_data['name'])
    media_mentions_score = media_mentions['totalResults']
    trust_score += normalize_score(media_mentions_score, 1000)

    # Method 2: Domain Reputation (Assuming the use of a hypothetical API)
    #domain_reputation = get_domain_reputation(company_data['domain'])
    domain_reputation = 88.88
    trust_score += normalize_score(domain_reputation, 100)

    # Method 3: Number of Employees
    employees_score = min(5, company_data['metrics']['employees'] / 1000)  # Cap the score at 5 for employee count
    trust_score += normalize_score(employees_score, 5)

    # Method 4: Financial Metrics
    revenue_score = company_data['metrics']['annualRevenue']  # Cap the score at 5 for revenue
    trust_score += normalize_score(revenue_score, 100000000)

    # Method 5: Description Sentiment Analysis
    data = media_mentions
    titles = [article["title"] for article in data["articles"]]
    titles_string = "\n".join(titles)
    description_sentiment = analyze_sentiment(titles_string)
    trust_score += description_sentiment

    # Method 6: Facebook Likes
    facebook_likes_score = company_data['facebook']['likes']
    trust_score += normalize_score(facebook_likes_score, 100000)

    # Method 6: Twitter followers
    Twitter_likes_score = company_data['twitter']['followers']
    trust_score += normalize_score(Twitter_likes_score, 100000)

    # Method 7: LinkedIn Handle
    linkedin_handle_score = 1 if 'linkedin' in company_data else 0
    trust_score += linkedin_handle_score

    # Method 8: Crunchbase Information
    crunchbase_info_score = 1 if 'crunchbase' in company_data else 0
    trust_score += crunchbase_info_score

    # Method 9: Domain Age
    current_year = datetime.datetime.now().year
    domain_age = current_year - company_data['foundedYear']
    trust_score += normalize_score(min(10, domain_age), 10)

    return normalize_score(trust_score, 10)*100

def fetch_company_data(company_name):
    headers = {
        'Authorization': 'Bearer {}'.format(os.getenv('clearbitapi_key'))
    }

    api_url = 'https://company.clearbit.com/v2/companies/find?domain={}'.format(company_name)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    # if company_data:
    #     return(company_data)
    else:
        return None