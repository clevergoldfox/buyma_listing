from controllers.scraping.special import special_scraping

import requests

def get_eur_jpy_rate():
    try:
        # Using exchangerate-api.com (free tier available)
        url = "https://api.exchangerate-api.com/v4/latest/EUR"
        response = requests.get(url)
        data = response.json()
        eur_jpy_rate = data['rates']['JPY']
        return eur_jpy_rate
    except Exception as e:
        print(f"Error: {e}")
        return None

special_brand_id = [
    "",
    "110000108", 
    "1980000135", #  7 for all mankind
    "840000207", #  a.p.c.
    "1980000794", #  acne studios
    "1980000020", #  adidas by stella mccartney
    "110000088", #  adidas by wales bonner
    "aesop", #aesop
    "190000029", #  afri-cani
    "110000130", #  ag jeans
    "110000102", #  agolde
    "1980000021", #  alaïa
    "1980000676", #  alanui
    "1980000351", #  alberto biani
    "840000358", #  alessandra rich
    "840000114", #  alessandro enriquez
    "1980000921", #  alexander mcqueen
    "1980000568", #  alice+olivia
    "840000029", #  alysi
    "ALYSON OLDOINI", #ALYSON OLDOINI
    "830000020", #  ami paris
    "1980000913", #  amina muaddi
    "1980000352", #  apuntob
    "1980000026", #  ash
    "840000336", #  auralee
    "830000196", #  autry
    "1980000757", #  avant toi
    "840000147", #  avenue montaigne
    "110000044", #  awake ny
    "1980000003", #  balenciaga
    "1980000172", #  bally
    "1980000013", #  balmain
    "1980000081", #  baobao issey miyake
    "1980000174", #  baracuta
    "1980000249", #  barbour
    "1980000358", #  base
    "1980000681", #  benedetta bruzziches
    "840000106", #  billionaire boys club
    "1980000909", #  birkenstock
    "840000157", #  blue sky inn
    "830000255", #  blumarine
    "1980000208", #  boglioli
    "BORNTOSTANDOUT", #BORNTOSTANDOUT
    "1980000210", #  borsalino
    "1980000002", #  bottega veneta
    "1980000634", #  boyy
    "840000153", #  briglia 1949
    "880000001", #  brunello cucinelli
    "1980000032", #  burberry
    "1980000261", #  c.p. company
    "1980000499", #  canada goose
    "840000447", #  carel paris
    "840000126", #  carhartt wip
    "830000176", #  casablanca
    "1980000891", #  casadei
    "1980000926", #  castaner since 1927
    "1980000004", #  celine
    "9", #  chloé
    "1980000925", #  christian louboutin
    "1980000265", #  church's
    "840000094", #  circolo 1901
    "1980000180", #  closed
    "1980000038", #  coach
    "1980000039", #  comme des garçons
    "1980000421", #  comme des garçons comme des ga
    "1980000861", #  comme des garçons play
    "830000017", #  comme des garçons shirt
    "1980000547", #  common projects
    "830000034", #  converse
    "840000271", #  converse x drkshdw
    "190000019", #  converse x kenzo
    "840000076", #  coperni
    "1980000762", #  cortana
    "1980000193", #  courrèges
    "1980000218", #  ct plage
    "190000011", #  cuba lab
    "1980000042", #  daniela gregis
    "840000321", #  darkpark
    "190000021", #  daytona 73
    "DE SIENA", #DE SIENA
    "110000032", #  diesel
    "190000012", #  disney x coperni
    "4", #  dolce &amp; gabbana
    "840000041", #  dr. martens
    "190000014", #  dragon diffusion
    "1980000049", #  dries van noten
    "DS&DURGA", #DS&DURGA
    "1", #  dsquared2
    "110000068", #  dunst
    "110000010", #  e.l.v. denim
    "1980000896", #  ea7 emporio armani
    "190000009", #  elios milano
    "190000008", #  elisabetta franchi
    "6", #  emporio armani
    "110000076", #  enes
    "110000029", #  enfants riches déprimés
    "840000242", #  equipment
    "1980000485", #  erika cavallini
    "1980000549", #  ermanno
    "1980000133", #  ermanno scervino
    "840000037", #  etro
    "110000131", #  extreme cashmere
    "840000100", #  fabiana filippi
    "1980000059", #  faliero sarti
    "1980000181", #  fay
    "1980000007", #  fendi
    "110000089", #  fermas.club
    "1980000063", #  ferragamo
    "110000090", #  filippa k
    "1980000274", #  filson
    "840000208", #  finamore 1925 napoli
    "190000026", #  floyd
    "1980000493", #  for restless sleepers
    "FORNICE OBJECTS", #FORNICE OBJECTS
    "1980000224", #  forte forte
    "830000097", #  front street 8
    "840000294", #  furling by giani
    "1980000800", #  ganni
    "840000190", #  ghoud
    "1980000068", #  gianluca capannolo
    "1980000069", #  gianvito rossi
    "840000013", #  giuseppe di morabito
    "10", #  givenchy
    "840000209", #  golden goose
    "1980000720", #  goldhawk
    "1980000005", #  gucci
    "830000041", #  haikure
    "1980000506", #  harris wharf london
    "1980000182", #  hartford
    "110000018", #  hereu
    "1980000507", #  herno
    "110000132", #  herskind
    "190000013", #  hidesins
    "1980000076", #  hogan
    "1980000932", #  homme plisse' issey miyake
    "840000077", #  i love my pants
    "840000210", #  icecream
    "1980000078", #  iro
    "1980000080", #  isabel marant
    "11", #  issey miyake
    "1980000512", #  jacob cohen
    "1980000538", #  jacquemus
    "110000041", #  jean paul gaultier
    "830000010", #  jil sander
    "1980000470", #  jimmy choo
    "JOZICA", #JOZICA
    "110000006", #  juicy couture
    "1980000197", #  junya watanabe
    "110000125", #  junya watanabe x carhartt
    "840000138", #  k.jacques
    "1980000015", #  kenzo
    "840000149", #  khaite
    "840000028", #  kired
    "840000019", #  kiton
    "840000345", #  la milanesa
    "1980000089", #  lanvin
    "840000089", #  lemaire
    "110000060", #  lisa yang
    "840000085", #  liviana conti
    "1980000516", #  loewe
    "840000289", #  loewe paula's ibiza
    "840000288", #  mach &amp; mach
    "840000088", #  maison kitsune'
    "1980000843", #  maison margiela
    "1980000096", #  majestic
    "110000129", #  malin franke
    "MALIN+GOETZ", #MALIN+GOETZ
    "1980000883", #  malone souliers
    "840000069", #  manebi
    "1980000056", #  marant etoile
    "1980000098", #  marc jacobs
    "1980000797", #  marine serre
    "1980000101", #  marni
    "1980000791", #  max mara
    "110000109", #  max mara the cube
    "840000134", #  mc2 saint barth
    "1980000011", #  michael michael kors
    "830000207", #  missoni
    "840000449", #  missoni beachwear
    "1980000892", #  miu miu
    "1980000100", #  mm6 maison margiela
    "MM6 X DR.MARTENS", #MM6 X DR.MARTENS
    "840000355", #  mm6 x salomon
    "110000128", #  moismont
    "1980000010", #  moncler
    "110000061", #  moncler + rick owens
    "1980000107", #  moncler grenoble
    "1980000429", #  monies
    "840000023", #  moon boot
    "840000181", #  mother
    "1980000112", #  mou
    "840000189", #  mugler
    "110000005", #  new arrivals ilkyaz ozel
    "830000002", #  new balance
    "840000124", #  new era
    "840000397", #  new era capsule
    "110000099", #  norda
    "1980000115", #  norma kamali
    "1980000832", #  obidi
    "1980000449", #  off-white
    "840000229", #  on
    "840000297", #  ottolinger
    "1980000474", #  palm angels
    "110000120", #  palm angels x suicoke
    "1980000318", #  palto'
    "840000160", #  paraboot
    "1980000625", #  paris texas
    "1980000009", #  parosh
    "3", #  paul smith
    "1980000189", #  peuterey
    "1980000564", #  pierre-louis mascia
    "840000144", #  pleasures
    "1980000203", #  pleats please issey miyake
    "110000063", #  post archive faction (paf)
    "1980000893", #  prada
    "830000009", #  ps paul smith
    "110000112", #  pucci
    "840000155", #  red wing shoes
    "190000017", #  relax re-lux
    "840000198", #  rené caovilla
    "12", #  rick owens
    "1980000860", #  rick owens drkshdw
    "1980000001", #  roger vivier
    "110000108", #  's max mara
    "1980000131", #  sacai
    "110000104", #  sacai x carhartt wip
    "1980000006", #  saint laurent
    "840000200", #  saint mxxxxxx
    "1980000614", #  samantha sung
    "110000121", #  sandbeige
    "110000012", #  sarahwear
    "1980000134", #  self portrait
    "1980000195", #  semicouture
    "840000252", #  silk95five
    "1980000782", #  siyu
    "190000001", #  soft goat
    "1980000536", #  solace london
    "840000390", #  sonora
    "110000113", #  sosue
    "110000049", #  sportmax
    "1980000772", #  st.piece of london
    "2", #  stella mccartney
    "1980000234", #  stone island
    "190000034", #  strike anywhere vintage
    "110000020", #  studio nicholson
    "840000127", #  stussy
    "1980000337", #  tagliatore
    "840000428", #  taller marmo
    "840000052", #  the attico
    "190000003", #  the latest
    "110000110", #  the nina studio
    "1980000677", #  the row
    "840000078", #  themoire'
    "1980000236", #  thom browne
    "1980000613", #  tod's
    "830000195", #  tom ford
    "1980000008", #  tory burch
    "840000116", #  toteme
    "190000015", #  trame auree
    "1980000205", #  ugg australia
    "1980000152", #  valentino
    "1980000153", #  valentino garavani
    "1980000850", #  valextra
    "840000350", #  veja
    "1980000416", #  versace
    "1980000491", #  vetements
    "1980000410", #  via masini 80
    "1980000012", #  victoria beckham
    "190000018", #  vipera
    "830000271", #  vivienne westwood
    "840000183", #  wardrobe.nyc
    "1980000729", #  white sand
    "110000066", #  wild cashmere
    "840000150", #  wolford
    "1980000157", #  woolrich
    "1980000657", #  y/project
    "1980000237", #  y-3
    "1980000160", #  zanellato
    "1980000668" #  zimmermann
]

special_category_id = [
    "",
    "abbigliamento-",
    "accessori-",
    "borse-",
    "calzature-",
    "gioielli-",
    "intimo-",
    "profumeria-",
]

hermes_categories = [
    "women/ready-wear",
    "women/ready-wear/coats-and-jackets",
    "women/ready-wear/dresses" ,
    "women/ready-wear/tops-and-shirts",
    "women/ready-wear/pants-skirts-and-shorts/",
    "women/ready-wear/knitwear-and-twillaines",
    "women/ready-wear/beachwear",
    "women/scarves-shawls-and-stoles",
    "women/scarves-shawls-and-stoles/silk-scarves-and-accessories/",
    "women/scarves-shawls-and-stoles/cashmere-shawls-and-stoles/",
    "women/scarves-shawls-and-stoles/twillys-and-other-small-formats",
    "women/shoes",
    # "レディース>アイコン モデル",
    "women/shoes/sandals",
    "women/shoes/sneakers",
    "women/shoes/ballet-flats-and-pumps",
    "women/shoes/mules",
    "women/shoes/espadrilles",
    "women/shoes/loafers-and-derbies",
    "women/shoes/boots-and-ankle-boots",
    "women/bags-and-small-leather-goods",
    "women/bags-and-small-leather-goods/bags-and-clutches",
    "women/bags-and-small-leather-goods/small-leather-goods",
    "women/bags-and-small-leather-goods/luggage",
    "women/bags-and-small-leather-goods/leather-accessories",
    "women/belts",
    "women/accessories",
    "men/ready-wear",
    "men/ready-wear/coats-and-jackets",
    "men/ready-wear/sportswear",
    "men/ready-wear/shirts",
    "men/ready-wear/pants-and-shorts",
    "men/ready-wear/knitwear-and-sweatshirts",
    "men/ready-wear/t-shirts-and-polos",
    "men/ready-wear/beachwear",
    "men/ties-stoles-and-scarves",
    "men/ties-stoles-and-scarves/ties-bow-ties-and-pocket-squares",
    "men/ties-stoles-and-scarves/stoles-and-scarves",
    "men/shoes",
    # "メンズ>アイコン モデル",
    "men/shoes/sneakers",
    "men/shoes/sandals",
    "men/shoes/espadrilles-and-mules",
    "men/shoes/loafers-and-derbies",
    "men/shoes/ankle-boots",
    "men/bags-and-small-leather-goods",
    "men/bags-and-small-leather-goods/bags",
    "men/bags-and-small-leather-goods/small-leather-goods",
    "men/bags-and-small-leather-goods/luggage",
    "men/bags-and-small-leather-goods/leather-accessories",
    "men/belts",
    "men/accessories/fashion-jewelry",
    "men/accessories/hats-and-gloves",
    "men/accessories/tech-accessories",
    "home",
    "home/textiles",
    "home/objects",
    "content/308299-tableware-collections",
    # "ホーム・アウトドア>家具と照明",
    "home/office-and-writing",
    "home/beach",
    "home/games-and-sports",
    "category/jewelry",
    "category/jewelry/gold-jewelry",
    "jewelry/silver-jewelry",
    "content/292318-watches-women, content/292317-watches-men",
    "content/292318-watches-women",
    "content/292317-watches-men",
    "watches/apple-watch-hermes",
    "category/fragrances",
    "category/fragrances/women",
    "category/fragrances/men",
    "fragrances/exclusives",
    "fragrances/art-living",
    "make-up",
    "make-up/face",
    "make-up/eyes",
    "make-up/hands",
    "make-up/accessories",
    "gifts-and-petit-h/gifts-for-women",
    "gifts-and-petit-h/gifts-for-women",
    "gifts-and-petit-h/gifts-for-men",
    "gifts-and-petit-h/baby-gifts"
]

def scraping(set_value, user_data, logging=None):
    if logging:
        logging("初期設定値を読み込み中...")
    
    # print("初期設定値\n")
    # print(f"タイトル開始文字{set_value['pretitle']}\n")
    # print(f"モデル・ライン{set_value['model_line']}\n")
    # print(f"性別(specialshop){set_value['special_gender']}\n")
    # print(f"ブランド(specialshop){set_value['special_brand']}\n")
    # print(f"カテゴリー(specialshop){set_value['special_category']}\n")
    # print(f"カテゴリー(HERMES){set_value['hermes_category']}\n")
    # print(f"買付地{set_value['purchased_place']}\n")
    # print(f"発送地{set_value['delivery_location']}\n")
    # print(f"シーズン{set_value['season']}\n")
    # print(f"タグ{set_value['tag']}\n")
    # print(f"配送方法{set_value['shipping_method']}\n")
    # print(f"発送までの日数{set_value['shipping_days']}\n")
    # print(f"購入期限{set_value['purchase_deadline']}\n")
    # print(f"BUYMA手数料{set_value['buyma_fee']}\n")
    # print(f"利益{set_value['profit']}\n")
    # print(f"関税を含む{set_value['include_tax']}\n")
    # print(f"商品コメント{set_value['comment']}\n")
    
    if logging:
        logging("設定値の検証を開始...")
    
    special_gender =set_value["special_gender"]
    special_brand =set_value["special_brand"]
    special_category =set_value["special_category"]
    special_url = "http://specialshop.atelier98.net/it/"
    
    if logging:
        logging("Special shop URLを構築中...")
        
    special_urls = []
        
    for brand in special_brand:
        special_url = "http://specialshop.atelier98.net/it/"

        if special_category == 0:
            if special_gender == "レディース":
                special_url += "donna"
            else:
                special_url += "uomo"
        else:
            special_url += special_category_id[special_category]
            if special_gender == "レディース":
                special_url += "donna"
            else:
                special_url += "uomo"
                    
        if not brand == 0:
            special_url += "?idt=" + special_brand_id[brand]
            
        special_urls.append(special_url)
        
        if logging:
            logging(f"Special shop URL: {special_url}")
            logging("為替レートを取得中...")
            
    # hermes_urls = []
    # hermes_category = set_value["hermes_category"]
    # for hermes_index in hermes_category:
    #     hermes_url = "https://www.hermes.com/jp/ja/category/" + hermes_categories[hermes_index]
    #     hermes_urls.append(hermes_url)
    
    # print(hermes_urls)
    # hermes_scraping(hermes_urls)
    currency_ratio = get_eur_jpy_rate()
    if currency_ratio:
        if logging:
            logging(f"為替レート取得成功: {currency_ratio}")
        
        set_value["currency_ratio"] = currency_ratio
        
        if logging:
            logging("Special shop scrapingを開始...")
            
        for url in special_urls:
            print(url)
            
        return special_scraping(special_urls, set_value, user_data, logging)
    else:
        if logging:
            logging("為替レートの取得に失敗しました")
        
        return {"code": 500, "msg": "為替レートを取得できません。"}
    
    
    
    