from furigana.furigana import is_kanji, jaconv, split_okurigana
import MeCab
import ipadic

def to_furigana_pairs(text):
    mecab = MeCab.Tagger('-Ochasen -d ' + ipadic.DICDIR)
    mecab.parse('')
    node = mecab.parseToNode(text)
    ret = []

    while node is not None:
        origin = node.surface
        if not origin:
            node = node.next
            continue

        if origin != "" and any(is_kanji(_) for _ in origin):
            kana = node.feature.split(",")[7]
            hiragana = jaconv.kata2hira(kana)
            for pair in split_okurigana(origin, hiragana):
                ret += [pair]
        else:
            if origin:
                ret += [(origin,)]
        node = node.next
    return ret


def to_furigana_html(text) -> str:
    res: str = ""
    for pair in to_furigana_pairs(text):
        if len(pair) == 2:
            kanji, hira = pair
            res += "<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(kanji, hira)
        else:
            res += pair[0]
    return res
