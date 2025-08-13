import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import codecs
import re
import os

from controllers.image_handle import image_handle

from deep_translator import GoogleTranslator

def translate_text(text):
    strings = text.split()
    translated = ""
    for string in strings:
        translated_string = GoogleTranslator(source='it', target='ja').translate(string)
        if translated_string:
            translated += translated_string + " "
    return translated

# initial variables
color_list = {
    "bianco": "ホワイト（白）系",
    "nero": "ブラック（黒）系",
    "grigio": "グレー（灰色）系",
    "marrone": "ブラウン（茶色）系",
    "beige": "ベージュ系",
    "verde": "グリーン（緑）系",
    "blu": "ブルー（青）系",
    "viola": "パープル（紫）系",
    "giallo": "イエロー（黄色）系",
    "rosa": "ピンク系",
    "rosso": "レッド（赤）系",
    "arancione": "オレンジ系",
    "argento": "シルバー（銀色）系",
    "argento": "ゴールド（金色）系",
    "oro": "ゴールド（金色）系",
    "dorato": "ゴールド（金色）系",
    "metals & Alloys": "ゴールド（金色）系",
    "trasparente": "クリア（透明）系",
    "blu navy": "ネイビー（紺）系"
}

shipping_cost_list = {
    "donna>abiti>abito corto m/c" : 20
}

buyma_category_list = {
    "donna/abiti/abito": "レディースファッション/ワンピース・オールインワン/ワンピースその他",
    "donna/abiti/abito corto m/c": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/abito corto m/l": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/abito corto s/m": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/abito lungo m/c": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/abito lungo m/l": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/abito lungo s/m": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/kaftano": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/kimono": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/tunica": "レディースファッション/ワンピース・オールインワン/ワンピース",
    "donna/abiti/tuta": "レディースファッション/ワンピース・オールインワン/オールインワン・サロペット",
    "donna/camicie/body": "レディースファッション/トップス/トップスその他",
    "donna/camicie/camicia": "レディースファッション/トップス/ブラウス・シャツ",
    "donna/camicie/gilet": "レディースファッション/トップス/ベスト・ジレ",
    "donna/camicie/top": "レディースファッション/トップス/Tシャツ・カットソー",
    "donna/capi spalla/caban": "レディースファッション/アウター/コート",
    "donna/capi spalla/cappa": "レディースファッション/アウター/ポンチョ・ケープ",
    "donna/capi spalla/cappotto": "レディースファッション/アウター/コート",
    "donna/capi spalla/gilet piumino": "レディースファッション/アウター/ダウンベスト",
    "donna/capi spalla/giubbino": "レディースファッション/アウター/ジャケット",
    "donna/capi spalla/giubbotto": "レディースファッション/アウター/ジャケット",
    "donna/capi spalla/impermeabile": "レディースファッション/アウター/コート",
    "donna/capi spalla/mantella": "レディースファッション/アウター/ポンチョ・ケープ",
    "donna/capi spalla/parka": "レディースファッション/トップス/パーカー・フーディ",
    "donna/capi spalla/piumino": "レディースファッション/アウター/ダウンジャケット・コート",
    "donna/capi spalla/poncho": "レディースファッション/アウター/ポンチョ・ケープ",
    "donna/capi spalla/trench": "レディースファッション/アウター/トレンチコート",
    "donna/completi/tailleur pantalone": "レディースファッション/水着・ビーチグッズ/水着・ビーチグッズその他",
    "donna/costumi da bagno/reggiseno mare": "レディースファッション/水着・ビーチグッズ/水着・ビーチグッズその他",
    "donna/costumi da bagno/slip mare": "レディースファッション/水着・ビーチグッズ/水着・ビーチグッズその他",
    "donna/felpe/felpa + zip": "レディースファッション/トップス/スウェット・トレーナー",
    "donna/felpe/felpa c/cappuccio": "レディースファッション/トップス/パーカー・フーディ",
    "donna/felpe/felpa g.collo": "レディースファッション/トップス/スウェット・トレーナー",
    "donna/giacche/bomber": "レディースファッション/アウター/ジャケット",
    "donna/giacche/giacca": "レディースファッション/アウター/ジャケット",
    "donna/giacche/giubbino jeans": "レディースファッション/アウター/ジャケット",
    "donna/gonne/gonna": "レディースファッション/ボトムス/スカート",
    "donna/gonne/gonna jeans": "レディースファッション/ボトムス/スカート",
    "donna/gonne/gonna lunga": "レディースファッション/ボトムス/スカート",
    "donna/jeans/shorts denim": "レディースファッション/ボトムス/ショートパンツ",
    "donna/maglieria/cardigan": "レディースファッション/トップス/ニット・セーター",
    "donna/maglieria/maglia + zip": "レディースファッション/トップス/ニット・セーター",
    "donna/maglieria/maglia c.alto": "レディースファッション/トップス/ニット・セーター",
    "donna/maglieria/maglia g.collo": "レディースファッション/トップス/ニット・セーター",
    "donna/maglieria/maglia s/barca": "レディースファッション/トップス/ニット・セーター",
    "donna/maglieria/maglia scollo v": "レディースファッション/トップス/ニット・セーター",
    "donna/mare/bikini": "レディースファッション/水着・ビーチグッズ/ビキニ",
    "donna/mare/copricostume": "レディースファッション/水着・ビーチグッズ/水着・ビーチグッズその他",
    "donna/mare/costume intero": "レディースファッション/水着・ビーチグッズ/ワンピース水着",
    "donna/pantalone/jeans denim": "レディースファッション/ボトムス/デニム・ジーパン",
    "donna/pantalone/leggings": "レディースファッション/ボトムス/ボトムスその他",
    "donna/pantalone/pantalone": "レディースファッション/ボトムス/ボトムスその他",
    "donna/pantalone/pantalone tuta": "レディースファッション/ボトムス/ボトムスその他",
    "donna/pantalone/salopette": "レディースファッション/ボトムス/ボトムスその他",
    "donna/pelle/pelliccia/  giacca pelle": "レディースファッション/アウター/レザージャケット・コート",
    "donna/pelle/pelliccia/  montone": "レディースファッション/アウター/ムートン・ファーコート",
    "donna/shorts/bermuda": "レディースファッション/ボトムス/ショートパンツ",
    "donna/shorts/shorts": "レディースファッション/ボトムス/ショートパンツ",
    "donna/soprabiti/soprabito": "レディースファッション/アウター/コート",
    "donna/top/canotta": "レディースファッション/トップス/タンクトップ",
    "donna/top/polo m/c": "レディースファッション/トップス/ポロシャツ",
    "donna/top/polo m/l": "レディースファッション/トップス/ポロシャツ",
    "donna/top/t-shirt m/c": "レディースファッション/トップス/Tシャツ・カットソー",
    "donna/top/t-shirt m/l": "レディースファッション/トップス/Tシャツ・カットソー",
    "donna/accessori": "レディースファッション/アクセサリー/アクセサリーその他",
    "donna/accessori per capelli/cerchietto": "レディースファッション/アクセサリー/ヘアアクセサリー",
    "donna/accessori per capelli/elastico x capelli": "レディースファッション/アクセサリー/ヘアアクセサリー",
    "donna/accessori per capelli/fascia x capelli": "レディースファッション/アクセサリー/ヘアアクセサリー",
    "donna/accessori per capelli/fermaglio": "レディースファッション/アクセサリー/ヘアアクセサリー",
    "donna/cappelli/berretto": "レディースファッション/帽子/帽子・その他",
    "donna/cappelli/cappello": "レディースファッション/帽子/帽子・その他",
    "donna/cappelli/cappello baseball": "レディースファッション/帽子/キャップ",
    "donna/cappelli/passamontagna": "レディースファッション/帽子/帽子・その他",
    "donna/cintura/cintura": "レディースファッション/ファッション雑貨・小物/ベルト",
    "donna/guanti/guanti": "レディースファッション/ファッション雑貨・小物/手袋",
    "donna/guanti/manicotti": "レディースファッション/ファッション雑貨・小物/手袋",
    "donna/mini borse/mini borsa": "レディースファッション/バッグ・カバン/バッグ・カバンその他",
    "donna/occhiali da sole/occhiali": "レディースファッション/アイウェア/サングラス",
    "donna/oggettistica/charm": "レディースファッション/アイウェア/アイウェアその他",
    "donna/oggettistica/oggett. varia": "レディースファッション/アイウェア/アイウェアその他",
    "donna/oggettistica/scatola": "レディースファッション/アイウェア/アイウェアその他",
    "donna/oggettistica/telo spugna": "ライフスタイル/ファブリック/タオル",
    "donna/portachiavi/portachiavi": "レディースファッション/財布・小物/キーホルダー・キーリング",
    "donna/portafogli/eauty-case": "レディースファッション/財布・小物/ポーチ",
    "donna/portafogli/ochette": "レディースファッション/財布・小物/ポーチ",
    "donna/portafogli/orta carte credito": "レディースファッション/財布・小物/カードケース・名刺入れ",
    "donna/portafogli/ortafoglio": "レディースファッション/バッグ・カバン/エコバッグ",
    "donna/sciarpe/foulard": "レディースファッション/ファッション雑貨・小物/スカーフ",
    "donna/sciarpe/sciarpa": "レディースファッション/ファッション雑貨・小物/スカーフ",
    "donna/sciarpe/stola": "レディースファッション/ファッション雑貨・小物/マフラー・ストール",
    "donna/borse/borsa a mano": "レディースファッション/バッグ・カバン/ハンドバッグ",
    "donna/borse/borsa a spalla": "レディースファッション/バッグ・カバン/ショルダーバッグ・ポシェット",
    "donna/borse/borsa a tracolla": "レディースファッション/バッグ・カバン/ショルダーバッグ・ポシェット",
    "donna/borse/borsa shopping": "レディースファッション/バッグ・カバン/トートバッグ",
    "donna/borse/borse clutch": "レディースファッション/バッグ・カバン/クラッチバッグ",
    "donna/borse/borsone": "レディースファッション/バッグ・カバン/ボストンバッグ",
    "donna/borse/secchiello": "レディースファッション/バッグ・カバン/ハンドバッグ",
    "donna/borse/tracolla": "レディースファッション/バッグ・カバン/ショルダーバッグ・ポシェット",
    "donna/borse/trolley": "ライフスタイル/トラベルグッズ/トラベルバッグ・旅行かばん",
    "donna/borse/zaino": "レディースファッション/バッグ・カバン/バックパック・リュック",
    "donna/ballerine/ballerina": "レディースファッション/靴・シューズ/フラットシューズ",
    "donna/ciabatte/ciabatta": "レディースファッション/靴・シューズ/サンダル・ミュール",
    "donna/ciabatte/sabot": "レディースファッション/靴・シューズ/サンダル・ミュール",
    "donna/ciabatte/slippers": "レディースファッション/靴・シューズ/パンプス",
    "donna/decolleté/decolleté": "レディースファッション/靴・シューズ/パンプス",
    "donna/decolleté/decolleté slingback": "レディースファッション/靴・シューズ/パンプス",
    "donna/flip flop/flip flops": "レディースファッション/靴・シューズ/サンダル・ミュール",
    "donna/mocassini/mocassino": "レディースファッション/靴・シューズ/ローファー・オックスフォード",
    "donna/sandali/espadrillas": "レディースファッション/靴・シューズ/フラットシューズ",
    "donna/sandali/infradito": "レディースファッション/靴・シューズ/サンダル・ミュール",
    "donna/sandali/sandalo": "レディースファッション/靴・シューズ/サンダル・ミュール",
    "donna/sandali/sandalo con tacco": "レディースファッション/靴・シューズ/サンダル・ミュール",
    "donna/sneakers/slip on": "レディースファッション/靴・シューズ/スニーカー",
    "donna/sneakers/sneaker": "レディースファッション/靴・シューズ/スニーカー",
    "donna/stivali/biker": "レディースファッション/ブーツ/ブーツその他",
    "donna/stivali/stivale": "レディースファッション/ブーツ/ブーツその他",
    "donna/stivali/stivale con tacco": "レディースファッション/ブーツ/ブーツその他",
    "donna/stivali/stivale pioggia": "レディースファッション/ブーツ/レインブーツ",
    "donna/stivali/stivaletto": "レディースファッション/ブーツ/ショートブーツ・ブーティ",
    "donna/stivali/stivaletto con tacco": "レディースファッション/ブーツ/ショートブーツ・ブーティ",
    "donna/stivali/stivaletto pioggia": "レディースファッション/ブーツ/レインブーツ",
    "donna/stringate/brogues": "レディースファッション/ブーツ/ブーツその他",
    "donna/anelli/anello": "レディースファッション/アクセサリー/指輪・リング",
    "donna/bracciali/bracciale": "レディースファッション/アクセサリー/ブレスレット",
    "donna/ciondoli/spilla": "レディースファッション/アクセサリー/ブローチ・コサージュ",
    "donna/collane/collana": "レディースファッション/アクセサリー/ネックレス・ペンダント",
    "donna/orecchini/orecchini": "レディースファッション/アクセサリー/ピアス",
    "donna/body intimo": "レディースファッション/ワンピース・オールインワン/オールインワン・サロペット",
    "donna/calze/calze": "レディースファッション/インナー・ルームウェア/タイツ・ソックス",
    "donna/calze/collant": "レディースファッション/インナー・ルームウェア/タイツ・ソックス",
    "donna/corsetto/corsetto": "レディースファッション/ファッション雑貨・小物/ファッション雑貨・小物その他",
    "donna/intimo/coulottes": "レディースファッション/インナー・ルームウェア/ショーツ",
    "donna/intimo/set lingerie": "レディースファッション/インナー・ルームウェア/ブラジャー＆ショーツ",
    "donna/intimo/slip": "レディースファッション/インナー・ルームウェア/ショーツ",
    "donna/intimo notte/pigiama": "レディースファッション/インナー・ルームウェア/ルームウェア・パジャマ",
    "donna/intimo notte/pigiama lungo": "レディースファッション/インナー・ルームウェア/ルームウェア・パジャマ",
    "donna/intimo notte/sottoveste": "レディースファッション/インナー・ルームウェア/インナー・ルームウェアその他",
    "donna/reggiseni/bralette": "レディースファッション/インナー・ルームウェア/ブラジャー",
    "donna/reggiseni/reggiseno": "レディースファッション/インナー・ルームウェア/ブラジャー",
    "donna/reggiseni/reggiseno triangolo": "レディースファッション/インナー・ルームウェア/ブラジャー",
    "donna/slip/culotte": "レディースファッション/インナー・ルームウェア/ショーツ",
    "donna/slip/slip perizoma": "レディースファッション/インナー・ルームウェア/ショーツ",
    "uomo/abiti/abito": "メンズファッション/スーツ",
    "uomo/abiti/abito uomo": "メンズファッション/スーツ",
    "uomo/camicie/camicia": "メンズファッション/トップス/シャツ",
    "uomo/camicie/camicia m/c": "メンズファッション/トップス/シャツ",
    "uomo/camicie/gilet": "メンズファッション/トップス/ベスト・ジレ",
    "uomo/camicie/top": "メンズファッション/トップス/トップスその他",
    "uomo/capi spalla/caban": "メンズファッション/アウター・ジャケット/ピーコート",
    "uomo/capi spalla/cappotto": "メンズファッション/アウター・ジャケット/コートその他",
    "uomo/capi spalla/gilet piumino": "メンズファッション/アウター・ジャケット/ダウンベスト",
    "uomo/capi spalla/giubbino": "メンズファッション/アウター・ジャケット/ダウンジャケット",
    "uomo/capi spalla/parka": "メンズファッション/トップス/パーカー・フーディ",
    "uomo/capi spalla/piumino": "メンズファッション/アウター・ジャケット/ダウンジャケット",
    "uomo/capi spalla/trench": "メンズファッション/アウター・ジャケット/トレンチコート",
    "uomo/felpe/felpa": "メンズファッション/トップス/スウェット・トレーナー",
    "uomo/felpe/felpa + zip": "メンズファッション/トップス/スウェット・トレーナー",
    "uomo/felpe/felpa c/cappuccio": "メンズファッション/トップス/パーカー・フーディ",
    "uomo/felpe/felpa g.collo": "メンズファッション/トップス/スウェット・トレーナー",
    "uomo/felpe/tuta sportiva": "メンズファッション/スーツ",
    "uomo/giacche/bomber": "メンズファッション/アウター・ジャケット/MA-1",
    "uomo/giacche/giacca": "メンズファッション/アウター・ジャケット/ジャケットその他",
    "uomo/giacche/giubbino jeans": "メンズファッション/アウター・ジャケット/デニムジャケット",
    "uomo/gonne/gonna": "メンズファッション/パンツ・ボトムス/パンツ・ボトムスその他",
    "uomo/maglieria/cardigan": "メンズファッション/トップス/ニット・セーター",
    "uomo/maglieria/maglia c.alto": "メンズファッション/トップス/ニット・セーター",
    "uomo/maglieria/maglia g.collo": "メンズファッション/トップス/ニット・セーター",
    "uomo/maglieria/maglia scollo v": "メンズファッション/トップス/ニット・セーター",
    "uomo/mare/boxer mare": "メンズファッション/水着・ビーチグッズ/水着",
    "uomo/pantalone/jeans denim": "メンズファッション/パンツ・ボトムス/デニム・ジーパン",
    "uomo/pantalone/pantalone": "メンズファッション/パンツ・ボトムス/パンツ・ボトムスその他",
    "uomo/pantalone/pantalone tuta": "メンズファッション/パンツ・ボトムス/スウェットパンツ",
    "uomo/pelle/pelliccia/  giacca pelle": "メンズファッション/アウター・ジャケット/レザージャケット",
    "uomo/pelle/pelliccia/  gilet pelle": "メンズファッション/アウター・ジャケット/アウターその他",
    "uomo/shorts/bermuda": "メンズファッション/パンツ・ボトムス/ハーフ・ショートパンツ",
    "uomo/shorts/shorts": "メンズファッション/パンツ・ボトムス/ハーフ・ショートパンツ",
    "uomo/top/canotta": "メンズファッション/トップス/タンクトップ",
    "uomo/top/polo m/c": "メンズファッション/トップス/ポロシャツ",
    "uomo/top/polo m/l": "メンズファッション/トップス/ポロシャツ",
    "uomo/top/t-shirt m/c": "メンズファッション/トップス/Tシャツ・カットソー",
    "uomo/top/t-shirt m/l": "メンズファッション/トップス/Tシャツ・カットソー",
    "uomo/cappelli/berretto": "メンズファッション/帽子/帽子その他",
    "uomo/cappelli/cappello": "メンズファッション/帽子/帽子その他",
    "uomo/cappelli/cappello baseball": "メンズファッション/帽子/キャップ",
    "uomo/cintura/cintura": "メンズファッション/ファッション雑貨・小物/ベルト",
    "uomo/cravatte/cravatta": "メンズファッション/ファッション雑貨・小物/ネクタイ",
    "uomo/cravatte/papillon": "メンズファッション/ファッション雑貨・小物/ネクタイ",
    "uomo/guanti/guanti": "メンズファッション/ファッション雑貨・小物/手袋",
    "uomo/mini borse/mini borsa": "メンズファッション/バッグ・カバン/バッグ・カバンその他",
    "uomo/occhiali da sole/occhiali": "メンズファッション/アイウェア/サングラス",
    "uomo/occhiali e montature/maschera sci": "メンズファッション/アイウェア/アイウェアその他",
    "uomo/oggettistica/charm": "メンズファッション/アイウェア/アイウェアその他",
    "uomo/oggettistica/oggett. varia": "メンズファッション/アイウェア/アイウェアその他",
    "uomo/oggettistica/porta abito": "ライフスタイル/ファブリック/タオル",
    "uomo/oggettistica/telo spugna": "ライフスタイル/ファブリック/タオル",
    "uomo/portachiavi/portachiavi": "メンズファッション/財布・雑貨/キーケース・キーリング",
    "uomo/portafogli/beauty-case": "メンズファッション/財布・雑貨/コインケース・小銭入れ",
    "uomo/portafogli/pochette": "メンズファッション/バッグ・カバン/クラッチバッグ",
    "uomo/portafogli/porta carte credito": "メンズファッション/財布・雑貨/カードケース・名刺入れ",
    "uomo/portafogli/porta cellulare": "メンズファッション/スマホケース・テックアクセサリー/iPhone・スマホケース",
    "uomo/portafogli/porta documenti": "メンズファッション/財布・雑貨/雑貨・その他",
    "uomo/portafogli/portafoglio": "メンズファッション/財布・雑貨/長財布",
    "uomo/sciarpe/foulard": "メンズファッション/ファッション雑貨・小物/マフラー",
    "uomo/sciarpe/pochette fazzoletto": "メンズファッション/ファッション雑貨・小物/ハンカチ",
    "uomo/sciarpe/sciarpa": "メンズファッション/ファッション雑貨・小物/ハンカチ",
    "uomo/borse/borsa a mano": "メンズファッション/バッグ・カバン/バッグ・カバンその他",
    "uomo/borse/borsa a spalla": "メンズファッション/バッグ・カバン/ショルダーバッグ",
    "uomo/borse/borsa a tracolla": "メンズファッション/バッグ・カバン/ショルダーバッグ",
    "uomo/borse/borsa shopping": "メンズファッション/バッグ・カバン/エコバッグ",
    "uomo/borse/borsone": "メンズファッション/バッグ・カバン/ボストンバッグ",
    "uomo/borse/marsupio": "メンズファッション/バッグ・カバン/ショルダーバッグ",
    "uomo/borse/trolley": "メンズファッション/バッグ・カバン/バッグ・カバンその他",
    "uomo/borse/zaino": "メンズファッション/バッグ・カバン/バックパック・リュック",
    "uomo/ciabatte/ciabatta": "メンズファッション/靴・ブーツ・サンダル/サンダル",
    "uomo/ciabatte/pantofola": "メンズファッション/靴・ブーツ・サンダル/サンダル",
    "uomo/ciabatte/slippers": "メンズファッション/靴・ブーツ・サンダル/サンダル",
    "uomo/mocassini/mocassino": "メンズファッション/靴・ブーツ・サンダル/サンダル",
    "uomo/sandali/espadrillas": "メンズファッション/靴・ブーツ・サンダル/サンダル",
    "uomo/sandali/infradito": "メンズファッション/靴・ブーツ・サンダル/サンダル",
    "uomo/sandali/sandalo": "メンズファッション/靴・ブーツ・サンダル/サンダル",
    "uomo/sneakers/slip on": "メンズファッション/靴・ブーツ・サンダル/スニーカー",
    "uomo/sneakers/sneaker": "メンズファッション/靴・ブーツ・サンダル/スニーカー",
    "uomo/stivali/polacchino": "メンズファッション/靴・ブーツ・サンダル/ブーツ",
    "uomo/stivali/stivale pioggia": "メンズファッション/靴・ブーツ・サンダル/ブーツ",
    "uomo/stivali/stivaletto": "メンズファッション/靴・ブーツ・サンダル/ブーツ",
    "uomo/stivali/stivaletto pioggia": "メンズファッション/靴・ブーツ・サンダル/ブーツ",
    "uomo/stringate/brogues": "メンズファッション/靴・ブーツ・サンダル/ドレスシューズ・革靴・ビジネスシューズ",
    "uomo/bracciali/bracciale": "メンズファッション/アクセサリー/ブレスレット",
    "uomo/collane/collana": "メンズファッション/アクセサリー/ネックレス・チョーカー",
    "uomo/orecchini/orecchini": "メンズファッション/アクセサリー/イヤリング",
    "uomo/calze": "メンズファッション/ファッション雑貨・小物/靴下・ソックス",
    "uomo/intimo/accappatoio": "メンズファッション/インナー・ルームウェア/インナー・ルームウェアその他",
    "uomo/intimo notte/pigiama": "メンズファッション/インナー・ルームウェア/ルームウェア・パジャマ",
    "uomo/slip/boxer": "メンズファッション/インナー・ルームウェア/ブリーフ"
}

# Convert color_list keys to lowercase for case-insensitive matching
color_list_lower = {k.lower(): v for k, v in color_list.items()}

# Create a pattern from the lowercase keys
color_pattern = r'(' + '|'.join(re.escape(k) for k in color_list_lower.keys()) + r')'

# color_pattern = r'\b(' + '|'.join(color_list.keys()) + r')\b'

current = datetime.now()
current_date = current.strftime("%Y/%m/%d")
current_time = current.strftime("%Y_%m_%d_%H%M")

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended for headless)
chrome_options.add_argument("--no-sandbox")  # Avoid sandbox issues
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--enable-unsafe-webgpu")
# chrome_options.add_argument("--enable-unsafe-swiftshader")
# Initialize driver variable but don't create it yet
driver = None
service = None

def get_driver():
    """Get or create Chrome WebDriver instance"""
    global driver, service
    if driver is None:
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        except Exception as e:
            print(f"Failed to create Chrome WebDriver: {e}")
            return None
    return driver


def special_scraping(list_urls, set_value, user_data, logging=None):
    driver = get_driver()
    if driver is None:
        print("Failed to get Chrome WebDriver")
        return []
        
    if logging:
        logging("Special shopにログイン中...")
    
    url = f'http://specialshop.atelier98.net/it/donna'
    driver.get(url)

    email_input = driver.find_element(By.XPATH, '//input[@id="UserID"]')
    email_input.clear()
    email_input.send_keys("cocomelonsoda@gmail.com")

    password_input = driver.find_element(By.XPATH, '//input[@id="passform3"]')
    password_input.clear()
    password_input.send_keys("840308869")

    submit_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Login"]')
    submit_button.click()

    time.sleep(5)  # Wait for the page to load after login

    if logging:
        logging("ログイン完了。商品リストページに移動中...")

    item_urls = []
    for list_url in list_urls:
        driver.get(list_url)
        
        
        if logging:
            logging("商品数を取得中...")
        
        folder_path = os.path.join("assets", "images", "special", current_time)    
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        total_count = 0
        page_count = 1
        count_divs = driver.find_elements(By.XPATH, "//div[@class=' clearfix ']")
        if len(count_divs) >= 1:
            count_div = count_divs[0]
            total_count_div = count_div.find_element(By.XPATH, ".//div[contains(@class, 'articolicatalogo ')]")
            total_count_text = total_count_div.text
            match = re.search(r'\d+', total_count_text)
            if match:
                total_count = int(match.group())
            
            page_count_div = count_div.find_elements(By.XPATH, ".//ul[contains(@class, 'bloccopagine')]")
            if len(page_count_div) >= 1:
                a_tag = page_count_div[0].find_elements(By.XPATH, ".//a[contains(@class, 'nolink')]")
                li_tag = a_tag[-3]
                page_count = int(li_tag.text)
            
            if logging:
                logging(f"商品検索結果: {total_count}件、ページ数: {page_count}ページ")
                
            print(f"specialshopサイトの商品検索結果件数{total_count}\n")

            if logging:
                logging("商品URLを収集中...")

            items = driver.find_elements(By.XPATH, "//div[@class='contfoto ']")

            for item in items:
                item_id = item.get_attribute("id")
                link = f"http://specialshop.atelier98.net/it/product-{item_id.replace('cont', '')}"
                item_urls.append(link)
                print(link)
            
            if logging:
                logging(f"商品URL収集完了: {len(item_urls)}件")
            
            for i in range(2, page_count+1):
                page_url = f"{list_url}?page={i}"
                driver.get(page_url)
                items = driver.find_elements(By.XPATH, "//div[@class='contfoto ']")

                for item in items:
                    item_id = item.get_attribute("id")
                    link = f"http://specialshop.atelier98.net/it/product-{item_id.replace('cont', '')}"
                    item_urls.append(link)
                    print(link)
        else:
            continue
                
    product_datas = []
    
    if logging:
        logging("商品詳細情報を取得中...")
    
    for i, item_url in enumerate(item_urls):
        if logging:
            logging(f"商品 {i+1}/{len(item_urls)} を処理中... ({(i+1)/len(item_urls)*100:.1f}%)")
        
        print(f"\r合計{len(item_urls)}個中  {i+1} 個取得     完了率: {(i+1)/len(item_urls) * 100:.1f}%\n", end='', flush=True)
        
        product_data = get_details(i+1, item_url, set_value, folder_path, logging)
        product_datas.append(product_data)
        
    driver.quit()
    if logging:
        logging(f"商品詳細取得完了: {len(product_datas)}件")

    return product_datas
    with open("test_shop.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)
def trim_after_60_chars(s):
    return s[:60] if len(s) > 60 else s


def get_details(index, item_url, set_value, folder_path, logging=None):
    if logging:
        logging(f"商品 {index} の詳細を取得中: {item_url}")
    
    driver.get(item_url)

    item_title_div = driver.find_element(By.XPATH, "//div[@id='bloccoh1']")
    item_pre_title = item_title_div.find_element(By.XPATH, ".//h1[@class='notranslate']").text
    item_nex_title = item_title_div.find_element(By.XPATH, ".//p").text
    if set_value["pretitle"] == "記載なし":
        item_title = trim_after_60_chars(item_pre_title + item_nex_title)
    else:
        item_title = trim_after_60_chars(set_value["pretitle"] + item_pre_title + item_nex_title)
        
    item_price_text = driver.find_element(By.XPATH, "//div[@class='prezzidettaglio']").text
    item_price = float(item_price_text.split(" ")[0].replace(".", "").replace(",", "."))
    cats_div = driver.find_element(By.XPATH, "//div[@class='blocconavigazioneor ']")
    cat_divs = cats_div.find_elements(By.XPATH, ".//li")
    cats = [cat.text for cat in cat_divs if cat.text.strip()]
    brand_orginal = cats[4] if len(cats) > 4 else "Unknown Brand"
    brand = f"{brand_orginal}({translate_text(brand_orginal)})"

    if logging:
        logging(f"商品名: {item_title[:50]}...")
        logging(f"ブランド: {brand}")
        logging(f"価格: €{item_price}")

    others = driver.find_elements(By.XPATH, "//div[@class='productdescrizione']")
    mount = len(others) + 1
    product_id = driver.find_element(By.XPATH, "//div[@id='bloccoh1']/following-sibling::span").text
    # comment_title_div = driver.find_element(By.XPATH, '//div[div[h4[contains(text(), "Composizione")]]]')
    comment_div = driver.find_elements(By.XPATH,'//div[@class="aks-accordion-item"][.//h4[contains(text(), "Composizione")]]//div[contains(@class, "aks-accordion-item-content")]//p')
    if len(comment_div) >= 1:
        it_comment_text = comment_div[0].get_attribute("innerText").strip()
        product_comment = f"{set_value['comment']} \n{item_nex_title} {translate_text(it_comment_text)}"
    else:
        product_comment = item_nex_title    
    
    img_links = []
    img_tags = driver.find_elements(By.XPATH,"//div[@class='dettagli']")
    for img_tag in img_tags:
        img_link_tag = img_tag.find_element(By.XPATH, ".//a")
        img_link = img_link_tag.get_attribute("href")
        img_links.append(img_link)
        
        
    img_paths = []
    for img_index, img_link in enumerate(img_links):
        img_path = os.path.join(folder_path, f"special_{index}_{img_index}.png")
        created_path = image_handle(img_link, set_value["bg_path"] ,img_path)
        img_paths.append(created_path)
        
    cat_gender = cats[1]
    cat_parent = cats[2]
    cat_child = cats[3]
    keyname = f"{cat_gender}/{cat_parent}/{cat_child}"
    if keyname in buyma_category_list:
        buyma_category = buyma_category_list[keyname]
    else:
        if cat_gender == "uomo":
            buyma_category = "メンズファッション/その他ファッション/その他"
        else:
            buyma_category = "レディースファッション/その他ファッション/その他"
    product_comment_lower = product_comment.lower()
    match = re.search(color_pattern, product_comment_lower)
    if match:
        # Get the matched color (English)
        matched_color = match.group(0)
        # Translate to Japanese using the color_dict
        japanese_color = color_list[matched_color]
        product_color = japanese_color
    else:
        # product_color = "マルチカラー"
        product_color = "色指定なし"

    product_size = ""
    size_tags = driver.find_elements(By.XPATH, "//div[@class='tagliamobileform']")
    if len(size_tags):
        for size_tag in size_tags:
            size_text = size_tag.text.strip()
            if size_text:
                product_size += f"{size_text}\n "
    else:
        product_size = "指定なし"

    special_cat = ">".join(cats[1:4])
    if special_cat in shipping_cost_list:
        shipping_cost = shipping_cost_list[special_cat]
    else:
        shipping_cost = 50
        
        
    currency_ratio = set_value["currency_ratio"]
    buyma_fee = set_value["buyma_fee"]
    profit = set_value["profit"]
    
    product_price = (item_price + shipping_cost) * currency_ratio * buyma_fee *profit
    
    if set_value["include_tax"]:
        include_tax = "お客様負担"
    else:
        include_tax = "なし"
    listing_memo = f"仕入れ金額: {item_price}\n 為替: {currency_ratio}\n 送料: {shipping_cost}\n 利益: {profit} \n 出品日: {current_date}"

    if logging:
        logging(f"計算完了 - 出品価格: ¥{product_price:.0f}")    

    product_info = [index, item_title, brand, set_value["model_line"], buyma_category, product_comment, " ", set_value["purchase_deadline"], item_url, set_value["purchased_place"], " ", set_value["delivery_location"], " ", product_color, product_size, set_value["season"], set_value["tag"], " ", product_price, " ", set_value["shipping_method"], mount, product_id, include_tax, listing_memo, img_paths]
    return product_info