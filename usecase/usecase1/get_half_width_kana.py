from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials
import pykakasi

@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)
def convert_to_halfwidth_kana(kanji: str)->list[str]:
    '''
    Get the half-width katakana using the specified kanji.

    :param kanji: A other than half-width katakana.
    :return: A half-width katakana.

    '''
    # 初始化pykakasi转换器，将汉字转换为平假名
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "H") # 日语汉字转平假名
    kakasi.setMode("K", "H") # 片假名转平假名
    conv = kakasi.getConverter()
    # 首先将所有汉字和片假名转换为平假名
    hiragana_text = conv.do(kanji)
    result = []
    # 半角kana的Unicode范围
    fullwidth_ASCII_start = 0xFF01
    fullwidth_ASCII_END = 0xFF5E
    half_width_start = 0x20
    half_width_end = 0x7E
    # 全角平假名到半角片假名的映射
    hiragana_to_half_kana = {
    'あ': 'ｱ', 'い': 'ｲ', 'う': 'ｳ', 'え': 'ｴ', 'お': 'ｵ',
    'か': 'ｶ', 'き': 'ｷ', 'く': 'ｸ', 'け': 'ｹ', 'こ': 'ｺ',
    'さ': 'ｻ', 'し': 'ｼ', 'す': 'ｽ', 'せ': 'ｾ', 'そ': 'ｿ',
    'た': 'ﾀ', 'ち': 'ﾁ', 'つ': 'ﾂ', 'て': 'ﾃ', 'と': 'ﾄ',
    'な': 'ﾅ', 'に': 'ﾆ', 'ぬ': 'ﾇ', 'ね': 'ﾈ', 'の': 'ﾉ',
    'は': 'ﾊ', 'ひ': 'ﾋ', 'ふ': 'ﾌ', 'へ': 'ﾍ', 'ほ': 'ﾎ',
    'ま': 'ﾏ', 'み': 'ﾐ', 'む': 'ﾑ', 'め': 'ﾒ', 'も': 'ﾓ',
    'や': 'ﾔ', 'ゆ': 'ﾕ', 'よ': 'ﾖ',
    'ら': 'ﾗ', 'り': 'ﾘ', 'る': 'ﾙ', 'れ': 'ﾚ', 'ろ': 'ﾛ',
    'わ': 'ﾜ', 'を': 'ｦ', 'ん': 'ﾝ',
    # 浊音
    'が': 'ｶﾞ', 'ぎ': 'ｷﾞ', 'ぐ': 'ｸﾞ', 'げ': 'ｹﾞ', 'ご': 'ｺﾞ',
    'ざ': 'ｻﾞ', 'じ': 'ｼﾞ', 'ず': 'ｽﾞ', 'ぜ': 'ｾﾞ', 'ぞ': 'ｿﾞ',
    'だ': 'ﾀﾞ', 'ぢ': 'ﾁﾞ', 'づ': 'ﾂﾞ', 'で': 'ﾃﾞ', 'ど': 'ﾄﾞ',
    'ば': 'ﾊﾞ', 'び': 'ﾋﾞ', 'ぶ': 'ﾌﾞ', 'べ': 'ﾍﾞ', 'ぼ': 'ﾎﾞ',
    'ぱ': 'ﾊﾟ', 'ぴ': 'ﾋﾟ', 'ぷ': 'ﾌﾟ', 'ぺ': 'ﾍﾟ', 'ぽ': 'ﾎﾟ',

    'ぁ': 'ｧ','ぃ': 'ｨ','ぅ': 'ｩ',
    'ぇ': 'ｪ','ぉ': 'ｫ',
    'ゃ': 'ｬ','ゅ': 'ｭ','ょ': 'ｮ',
    'っ': 'ｯ','ー': '-','　': ' '
    }
    for char in hiragana_text:
        code = ord(char)
        # 如果已经是半角kana，直接保留
        if half_width_start <= code <= half_width_end:
            result.append(char)
        # 处理平假名
        elif char in hiragana_to_half_kana:
            result.append(hiragana_to_half_kana[char])
        # 处理全角片假名（转换为半角）
        elif fullwidth_ASCII_start <= code <= fullwidth_ASCII_END: # 全角片假名范围
            half_width_char = chr(code - 0xFEE0)
            result.append(half_width_char)
            # 其他字符（如数字、字母等）
        else:
            # 全角转半角的通用处理（差值0xFEE0）
            converted_code = code - 0xFEE0
            if half_width_start <= converted_code <= half_width_end: # 半角ASCII范围
                result.append(chr(converted_code))
            else:
            # 无法转换的字符用问号代替
                result.append('?')

    return ''.join(result)






