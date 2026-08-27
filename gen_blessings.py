#!/usr/bin/env python3
"""
生成1000条中英法德四语祝福语，每条中文 > 30 字。
输出 blessings.json
"""
import json
import random
import itertools

random.seed(42)

# ============ 四语词汇库（按索引对应） ============

# 美好事物 / 名词
NOUNS = [
    ("阳光", "sunshine", "soleil", "Sonnenschein"),
    ("微风", "breeze", "brise", "Brise"),
    ("星光", "starlight", "lumière des étoiles", "Sternenlicht"),
    ("花香", "fragrance of flowers", "parfum des fleurs", "Blütenduft"),
    ("晨曦", "morning glow", "lueur matinale", "Morgendämmerung"),
    ("晚霞", "sunset glow", "lueur du coucher", "Abendröte"),
    ("清泉", "clear spring", "source claire", "klarer Quell"),
    ("彩虹", "rainbow", "arc-en-ciel", "Regenbogen"),
    ("月光", "moonlight", "claire de lune", "Mondlicht"),
    ("绿叶", "green leaves", "feuilles vertes", "grüne Blätter"),
    ("海浪", "ocean waves", "vagues de l'océan", "Meereswellen"),
    ("山岚", "mountain mist", "brume montagneuse", "Bergnebel"),
    ("灯火", "lamplight", "lumière des lampes", "Lampenlicht"),
    ("雪花", "snowflakes", "flocons de neige", "Schneeflocken"),
    ("鸟鸣", "birdsong", "chant des oiseaux", "Vogelgesang"),
    ("蝴蝶", "butterfly", "papillon", "Schmetterling"),
    ("露珠", "dewdrops", "gouttes de rosée", "Tautropfen"),
    ("枫林", "maple forest", "forêt d'érables", "Ahornwald"),
    ("溪流", "stream", "ruisseau", "Bach"),
    ("星空", "starry sky", "ciel étoilé", "Sternenhimmel"),
    ("暖阳", "warm sun", "soleil chaud", "warme Sonne"),
    ("细雨", "gentle rain", "pluie douce", "sanfter Regen"),
    ("白云", "white clouds", "nuages blancs", "weiße Wolken"),
    ("翠竹", "green bamboo", "bambou vert", "grüner Bambus"),
    ("寒梅", "winter plum", "prunier d'hiver", "Winterpflaume"),
    ("春芽", "spring buds", "bourgeons de printemps", "Frühlingsknospen"),
    ("夏荷", "summer lotus", "lotus d'été", "Sommerlotus"),
    ("秋实", "autumn harvest", "récolte d'automne", "Herbsternte"),
    ("冬雪", "winter snow", "neige d'hiver", "Winterschnee"),
    ("远山", "distant mountains", "montagnes lointaines", "ferne Berge"),
]

# 积极形容词
ADJ = [
    ("温暖的", "warm", "chaud(e)", "warm"),
    ("明亮的", "bright", "brillant(e)", "hell"),
    ("宁静的", "peaceful", "paisible", "friedlich"),
    ("美好的", "wonderful", "merveilleux(euse)", "wunderbar"),
    ("灿烂的", "splendid", "splendide", "strahlend"),
    ("温柔的", "gentle", "doux(douce)", "sanft"),
    ("坚定的", "steadfast", "inébranlable", "standhaft"),
    ("轻盈的", "lighthearted", "léger(ère)", "leicht"),
    ("深邃的", "profound", "profond(e)", "tief"),
    ("纯净的", "pure", "pur(e)", "rein"),
    ("灵动的", "vivid", "vif(vive)", "lebendig"),
    ("悠然的", "leisurely", "tranquille", "gelassen"),
    ("璀璨的", "dazzling", "éclatant(e)", "funkelnd"),
    ("和煦的", "genial", "généreux(euse)", "heiter"),
    ("清新的", "refreshing", "rafraîchissant(e)", "erfrischend"),
    ("浪漫的", "romantic", "romantique", "romantisch"),
    ("质朴的", "simple", "simple", "schlicht"),
    ("华丽的", "gorgeous", "magnifique", "prächtig"),
    ("安详的", "serene", "serein(e)", "ruhig"),
    ("蓬勃的", "vibrant", "vibrant(e)", "lebhaft"),
]

# 动作 / 动词短语
VERBS = [
    ("照亮你的每一天", "brighten your every day", "illumine chacun de tes jours", "erhelle jeden deiner Tage"),
    ("温暖你的心房", "warm your heart", "réchauffe ton cœur", "wärme dein Herz"),
    ("陪伴你的旅程", "accompany your journey", "accompagne ton voyage", "begleite deinen Weg"),
    ("守护你的梦想", "guard your dreams", "protège tes rêves", "beschütze deine Träume"),
    ("点亮你的希望", "ignite your hope", "allume ton espoir", "entfache deine Hoffnung"),
    ("丰盈你的生命", "enrich your life", "enrichis ta vie", "bereichere dein Leben"),
    ("抚慰你的疲惫", "soothe your weariness", "apaise ta fatigue", "lindere deine Müdigkeit"),
    ("唤起你的勇气", "awaken your courage", "éveille ton courage", "wecke deinen Mut"),
    ("装点你的岁月", "adorn your years", "orne tes années", "schmücke deine Jahre"),
    ("滋润你的心田", "nourish your soul", "nourris ton âme", "durchdringe deine Seele"),
    ("拥抱你的世界", "embrace your world", "embrasse ton monde", "umarme deine Welt"),
    ("见证你的成长", "witness your growth", "témoigne de ta croissance", "zeuge deinem Wachstum"),
    ("分享你的喜悦", "share your joy", "partage ta joie", "teile deine Freude"),
    ("分担你的忧愁", "lighten your sorrows", "allège tes peines", "teile deine Sorgen"),
    ("开启你的可能", "unlock your potential", "libère ton potentiel", "öffne deine Möglichkeiten"),
    ("延伸你的远方", "extend your horizon", "élargis ton horizon", "erweitere deinen Horizont"),
    ("沉淀你的智慧", "deepen your wisdom", "approfondis ta sagesse", "vertiefe deine Weisheit"),
    ("绽放你的光芒", "unfold your radiance", "épanouis ton éclat", "entfalte dein Strahlen"),
    ("安放你的身心", "settle your mind and body", "apaise ton esprit et ton corps", "bringen deinen Geist und Körper zur Ruhe"),
    ("丰盈你的灵魂", "fulfill your soul", "remplis ton âme", "erfülle deine Seele"),
]

# 时间/场景状语
TIMEPHRASES = [
    ("在每一个清晨", "every morning", "chaque matin", "jeden Morgen"),
    ("在每一个黄昏", "every evening", "chaque soir", "jeden Abend"),
    ("在风起的时候", "when the wind rises", "quand le vent se lève", "wenn der Wind aufkommt"),
    ("在花落的瞬间", "when flowers fall", "quand les fleurs tombent", "wenn Blumen fallen"),
    ("在月光下", "beneath the moonlight", "sous le clair de lune", "im Mondlicht"),
    ("在星空下", "beneath the starry sky", "sous le ciel étoilé", "unter dem Sternenhimmel"),
    ("在雨后", "after the rain", "après la pluie", "nach dem Regen"),
    ("在雪落时", "when snow falls", "quand la neige tombe", "wenn Schnee fällt"),
    ("在春暖花开时", "when spring blooms", "quand le printemps fleurit", "wenn der Frühling blüht"),
    ("在秋高气爽时", "in the crisp autumn air", "dans l'air vif d'automne", "in der herbstlichen Luft"),
    ("在你疲惫时", "when you are weary", "quand tu es fatigué(e)", "wenn du müde bist"),
    ("在你迷茫时", "when you feel lost", "quand tu te sens perdu(e)", "wenn du dich verloren fühlst"),
    ("在你欢笑时", "when you laugh", "quand tu ris", "wenn du lachst"),
    ("在你沉思时", "when you ponder", "quand tu réfléchis", "wenn du nachdenkst"),
    ("在新的一天", "on a new day", "en ce nouveau jour", "an einem neuen Tag"),
    ("在每一个当下", "in every present moment", "à chaque instant présent", "in jedem gegenwärtigen Moment"),
    ("在岁月长河里", "in the river of time", "dans le fleuve du temps", "im Fluss der Zeit"),
    ("在人生旅途上", "on the journey of life", "sur le chemin de la vie", "auf der Reise des Lebens"),
    ("在灯火阑珊处", "where the lights dim", "là où les lumières s'éteignent", "wo die Lichter erlöschen"),
    ("在心花怒放时", "when your heart blossoms", "quand ton cœur s'épanouit", "wenn dein Herz aufblüht"),
]

# 结尾祝愿
ENDINGS = [
    ("愿你被这世界温柔以待。", "May the world treat you gently.", "Que le monde te traite avec douceur.", "Möge die Welt dich sanft behandeln."),
    ("愿你眼中有光，心中有爱。", "May there be light in your eyes and love in your heart.", "Que la lumière soit dans tes yeux et l'amour dans ton cœur.", "Möge Licht in deinen Augen und Liebe in deinem Herzen sein."),
    ("愿你所有的努力都不被辜负。", "May all your efforts be rewarded.", "Que tous tes efforts soient récompensés.", "Mögen all deine Anstrengungen belohnt werden."),
    ("愿你走出半生，归来仍是少年。", "May you return with a young heart after years of wandering.", "Puisses-tu revenir avec un cœur jeune après des années d'errance.", "Mögest du nach Jahren der Wanderung mit jungem Herzen zurückkehren."),
    ("愿你一生努力，一生被爱。", "May you strive and be loved all your life.", "Puisses-tu lutter et être aimé(e) toute ta vie.", "Mögest du dein ganzes Leben streben und geliebt werden."),
    ("愿你想要的都拥有，得不到的都释怀。", "May you have what you desire and release what you cannot.", "Puisses-tu avoir ce que tu désires et lâcher ce que tu ne peux avoir.", "Mögest du haben, was du begehrst, und loslassen, was du nicht haben kannst."),
    ("愿你成为自己的太阳，无需凭借谁的光。", "May you be your own sun, needing no one else's light.", "Puisses-tu être ton propre soleil, sans avoir besoin de la lumière d'autrui.", "Mögest du deine eigene Sonne sein, ohne jemandes Licht zu brauchen."),
    ("愿你历经山河，仍觉人间值得。", "May you traverse mountains and rivers and still find life worthwhile.", "Puisses-tu traverser montagnes et rivières et trouver la vie valoir la peine.", "Mögest du Berge und Flüsse durchqueren und das Leben immer noch wert finden."),
    ("愿你前程似锦，未来可期。", "May your future be bright and promising.", "Que ton avenir soit radieux et prometteur.", "Möge deine Zukunft strahlend und voller Verheißung sein."),
    ("愿你平安喜乐，得偿所愿。", "May you be safe, joyful, and fulfilled.", "Puisses-tu être en sécurité, joyeux(se) et accompli(e).", "Mögest du sicher, fröhlich und erfüllt sein."),
    ("愿你温柔且坚定，知足且上进。", "May you be gentle yet firm, content yet striving.", "Puisses-tu être doux(ce) mais ferme, satisfait(e) mais ambitieux(se).", "Mögest du sanft und doch standhaft, zufrieden und doch ehrgeizig sein."),
    ("愿你眼里藏着星辰大海，心中装着诗和远方。", "May your eyes hold oceans of stars and your heart hold poetry and distant horizons.", "Que tes yeux retiennent des océans d'étoiles et ton cœur la poésie et l'horizon lointain.", "Mögen deine Augen Ozeane aus Sternen bergen und dein Herz Poesie und ferne Horizonte."),
    ("愿你活成自己喜欢的模样。", "May you live as the person you wish to be.", "Puisses-tu vivre comme la personne que tu souhaites être.", "Mögest du so leben, wie du es dir wünschst."),
    ("愿你所有的美好都如期而至。", "May all good things come to you in due time.", "Que toutes les bonnes choses te parviennent en temps voulu.", "Mögen alle guten Dinge zu dir kommen zur rechten Zeit."),
    ("愿你不惧岁月长，心中有暖阳。", "May you not fear the passing years, with a warm sun in your heart.", "Puisses-tu ne pas craindre les années qui passent, avec un soleil chaud dans ton cœur.", "Möchtest du die vergehenden Jahre nicht fürchten, mit einer warmen Sonne im Herzen."),
    ("愿你以梦为马，不负韶华。", "May you ride your dreams and not waste your youth.", "Puisses-tu galoper sur tes rêves et ne pas gâcher ta jeunesse.", "Mögest du auf deinen Träumen reiten und deine Jugend nicht verschwenden."),
    ("愿你保持热爱，奔赴山海。", "May you keep your passion and journey to mountains and seas.", "Puisses-tu garder ta passion et voyager vers montagnes et mers.", "Mögest du deine Leidenschaft bewahren und zu Bergen und Meeren reisen."),
    ("愿你慢慢长大，不慌不忙。", "May you grow slowly, unhurried and calm.", "Puisses-tu grandir lentement, sans hâte ni agitation.", "Mögest du langsam wachsen, ohne Eile und Unruhe."),
    ("愿你被爱包围，与温暖同行。", "May you be surrounded by love and walk with warmth.", "Puisses-tu être entouré(e) d'amour et marcher avec la chaleur.", "Mögest du von Liebe umgeben sein und mit Wärme gehen."),
    ("愿你心中有景，处处花开。", "May there be scenery in your heart and flowers everywhere.", "Qu'il y ait un paysage dans ton cœur et des fleurs partout.", "Möge eine Landschaft in deinem Herzen sein und Blumen überall."),
]

# ============ 句式模板（四语对应，变量用 {n1}{a1}{v1}{t1}{e1} 等） ============
# 每条模板确保中文 > 30 字

TEMPLATES = [
    # 模板1: 时间 + 愿 + 名词 + 动词 + 结尾
    {
        "zh": "{t1}，愿那{a1}{n1}{v1}，{e1}",
        "en": "{t1}, may the {a1} {n1} {v1}, {e1}",
        "fr": "{t1}, puisse le {a1} {n1} {v1}, {e1}",
        "de": "{t1}, möge das {a1} {n1} {v1}, {e1}",
        "vars": ["t1", "n1", "a1", "v1", "e1"],
    },
    # 模板2: 你好 + 名词 + 动词 + 时间 + 结尾
    {
        "zh": "你好啊，愿{a1}{n1}{v1}，{t1}都能感受到这份美好，{e1}",
        "en": "Hello, may the {a1} {n1} {v1}, so that {t1} you feel this beauty, {e1}",
        "fr": "Bonjour, puisse le {a1} {n1} {v1}, afin que {t1} tu ressentes cette beauté, {e1}",
        "de": "Hallo, möge das {a1} {n1} {v1}, sodass du {t1} diese Schönheit spürst, {e1}",
        "vars": ["a1", "n1", "v1", "t1", "e1"],
    },
    # 模板3: 双重名词 + 动词 + 结尾
    {
        "zh": "愿{a1}{n1}与{a2}{n2}一同{v1}，在平凡的日子里开出不平凡的花，{e1}",
        "en": "May the {a1} {n1} and the {a2} {n2} together {v1}, blooming extraordinary flowers in ordinary days, {e1}",
        "fr": "Puissent le {a1} {n1} et le {a2} {n2} ensemble {v1}, faisant éclore des fleurs extraordinaires dans les jours ordinaires, {e1}",
        "de": "Mögen das {a1} {n1} und das {a2} {n2} gemeinsam {v1}, und in gewöhnlichen Tagen außergewöhnliche Blumen erblühen, {e1}",
        "vars": ["a1", "n1", "a2", "n2", "v1", "e1"],
    },
    # 模板4: 时间 + 名词 + 动词 + 名词 + 结尾
    {
        "zh": "{t1}，让{a1}{n1}{v1}，让{a2}{n2}装点你前行的路，{e1}",
        "en": "{t1}, let the {a1} {n1} {v1}, and let the {a2} {n2} adorn the road ahead, {e1}",
        "fr": "{t1}, laisse le {a1} {n1} {v1}, et laisse le {a2} {n2} orner la route devant toi, {e1}",
        "de": "{t1}, lass das {a1} {n1} {v1}, und lass das {a2} {n2} den Weg vor dir schmücken, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "a2", "n2", "e1"],
    },
    # 模板5: 人生感悟式
    {
        "zh": "人生漫漫，愿你携{a1}{n1}上路，{v1}，{t1}都能遇见更好的自己，{e1}",
        "en": "Life is a long journey; may you carry the {a1} {n1} with you, {v1}, and meet a better self {t1}, {e1}",
        "fr": "La vie est un long voyage ; puisses-tu emporter le {a1} {n1} avec toi, {v1}, et rencontrer un meilleur toi-même {t1}, {e1}",
        "de": "Das Leben ist eine lange Reise; mögest du das {a1} {n1} mit dir tragen, {v1}, und {t1} einem besseren Ich begegnen, {e1}",
        "vars": ["a1", "n1", "v1", "t1", "e1"],
    },
    # 模板6: 排比式
    {
        "zh": "愿你有{a1}{n1}的明媚，有{a2}{n2}的从容，{v1}，{e1}",
        "en": "May you have the radiance of {a1} {n1}, the composure of {a2} {n2}, {v1}, {e1}",
        "fr": "Puisses-tu avoir le rayonnement du {a1} {n1}, la sérénité du {a2} {n2}, {v1}, {e1}",
        "de": "Mögest du die Strahlkraft des {a1} {n1}, die Gelassenheit des {a2} {n2} haben, {v1}, {e1}",
        "vars": ["a1", "n1", "a2", "n2", "v1", "e1"],
    },
    # 模板7: 问候+比喻
    {
        "zh": "你好啊！愿你的生活如{a1}{n1}般明媚，{v1}，{t1}都充满期待，{e1}",
        "en": "Hello! May your life be as radiant as {a1} {n1}, {v1}, and full of anticipation {t1}, {e1}",
        "fr": "Bonjour ! Puisses-tu avoir une vie aussi radieuse que le {a1} {n1}, {v1}, et pleine d'attente {t1}, {e1}",
        "de": "Hallo! Möge dein Leben so strahlend sein wie das {a1} {n1}, {v1}, und {t1} voller Vorfreude sein, {e1}",
        "vars": ["a1", "n1", "v1", "t1", "e1"],
    },
    # 模板8: 双重时间
    {
        "zh": "{t1}，{t2}，愿{a1}{n1}始终{v1}，{e1}",
        "en": "{t1}, and {t2}, may the {a1} {n1} always {v1}, {e1}",
        "fr": "{t1}, et {t2}, puisse le {a1} {n1} toujours {v1}, {e1}",
        "de": "{t1}, und {t2}, möge das {a1} {n1} immer {v1}, {e1}",
        "vars": ["t1", "t2", "a1", "n1", "v1", "e1"],
    },
    # 模板9: 三名词排比
    {
        "zh": "愿{a1}{n1}照亮前路，{a2}{n2}温暖心房，{a3}{n3}{v1}，{e1}",
        "en": "May the {a1} {n1} light your way, the {a2} {n2} warm your heart, and the {a3} {n3} {v1}, {e1}",
        "fr": "Puissent le {a1} {n1} éclairer ton chemin, le {a2} {n2} réchauffer ton cœur, et le {a3} {n3} {v1}, {e1}",
        "de": "Möge das {a1} {n1} deinen Weg erleuchten, das {a2} {n2} dein Herz wärmen, und das {a3} {n3} {v1}, {e1}",
        "vars": ["a1", "n1", "a2", "n2", "a3", "n3", "v1", "e1"],
    },
    # 模板10: 哲思式
    {
        "zh": "生活不必太匆忙，{t1}，愿你停下脚步感受{a1}{n1}，{v1}，{e1}",
        "en": "Life need not be too hurried; {t1}, may you pause to feel the {a1} {n1}, {v1}, {e1}",
        "fr": "La vie n'a pas besoin d'être trop précipitée ; {t1}, puisses-tu t'arrêter pour sentir le {a1} {n1}, {v1}, {e1}",
        "de": "Das Leben muss nicht zu eilig sein; {t1}, mögest du innehalten, um das {a1} {n1} zu spüren, {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板11: 鼓励式
    {
        "zh": "无论前方有多少风雨，愿{a1}{n1}给你力量，{v1}，{e1}",
        "en": "No matter how many storms lie ahead, may the {a1} {n1} give you strength, {v1}, {e1}",
        "fr": "Peu importe les tempêtes à venir, puisse le {a1} {n1} te donner la force, {v1}, {e1}",
        "de": "Egal wie viele Stürme vor dir liegen, möge das {a1} {n1} dir Kraft geben, {v1}, {e1}",
        "vars": ["a1", "n1", "v1", "e1"],
    },
    # 模板12: 温馨式
    {
        "zh": "你好啊，{t1}，愿这份来自远方的问候如{a1}{n1}般{v1}，{e1}",
        "en": "Hello, {t1}, may this greeting from afar {v1} like {a1} {n1}, {e1}",
        "fr": "Bonjour, {t1}, puisse ce salut venu d'ailleurs {v1} comme le {a1} {n1}, {e1}",
        "de": "Hallo, {t1}, möge dieser Gruß aus der Ferne {v1} wie das {a1} {n1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板13: 自然意象
    {
        "zh": "看那{a1}{n1}，{t1}，愿你也能如此{v1}，{e1}",
        "en": "Look at the {a1} {n1}; {t1}, may you also {v1} like it, {e1}",
        "fr": "Regarde le {a1} {n1} ; {t1}, puisses-tu aussi {v1} comme lui, {e1}",
        "de": "Schau dir das {a1} {n1} an; {t1}, mögest du auch so {v1}, {e1}",
        "vars": ["a1", "n1", "t1", "v1", "e1"],
    },
    # 模板14: 成长式
    {
        "zh": "成长是一场温柔的旅程，{t1}，愿{a1}{n1}伴你{v1}，{e1}",
        "en": "Growth is a gentle journey; {t1}, may the {a1} {n1} accompany you to {v1}, {e1}",
        "fr": "La croissance est un voyage doux ; {t1}, puisse le {a1} {n1} t'accompagner pour {v1}, {e1}",
        "de": "Wachstum ist eine sanfte Reise; {t1}, möge das {a1} {n1} dich begleiten, um zu {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板15: 诗意式
    {
        "zh": "{t1}，把日子过成诗，让{a1}{n1}{v1}，{e1}",
        "en": "{t1}, live each day as poetry, let the {a1} {n1} {v1}, {e1}",
        "fr": "{t1}, vis chaque jour comme une poésie, laisse le {a1} {n1} {v1}, {e1}",
        "de": "{t1}, lebe jeden Tag wie Poesie, lass das {a1} {n1} {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板16: 双重动词
    {
        "zh": "愿{a1}{n1}{v1}，也愿{a2}{n2}{v2}，{t1}都被美好环绕，{e1}",
        "en": "May the {a1} {n1} {v1}, and may the {a2} {n2} {v2}, so that {t1} you are surrounded by beauty, {e1}",
        "fr": "Puissent le {a1} {n1} {v1}, et le {a2} {n2} {v2}, afin que {t1} tu sois entouré(e) de beauté, {e1}",
        "de": "Möge das {a1} {n1} {v1}, und möge das {a2} {n2} {v2}, sodass du {t1} von Schönheit umgeben bist, {e1}",
        "vars": ["a1", "n1", "v1", "a2", "n2", "v2", "t1", "e1"],
    },
    # 模板17: 简短有力
    {
        "zh": "你好！{t1}，愿{a1}{n1}{v1}，愿你心中有梦、脚下有路，{e1}",
        "en": "Hello! {t1}, may the {a1} {n1} {v1}, may you have dreams in your heart and a path beneath your feet, {e1}",
        "fr": "Bonjour ! {t1}, puisse le {a1} {n1} {v1}, puisses-tu avoir des rêves au cœur et un chemin sous tes pieds, {e1}",
        "de": "Hallo! {t1}, möge das {a1} {n1} {v1}, mögest du Träume im Herzen und einen Weg unter den Füßen haben, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板18: 四季式
    {
        "zh": "春有{a1}{n1}，秋有{a2}{n2}，愿你的四季都有美好相伴，{v1}，{e1}",
        "en": "Spring has {a1} {n1}, autumn has {a2} {n2}; may your four seasons all be accompanied by beauty, {v1}, {e1}",
        "fr": "Le printemps a le {a1} {n1}, l'automne a le {a2} {n2} ; puissent tes quatre saisons être accompagnées de beauté, {v1}, {e1}",
        "de": "Der Frühling hat {a1} {n1}, der Herbst hat {a2} {n2}; mögen deine vier Jahreszeiten alle von Schönheit begleitet sein, {v1}, {e1}",
        "vars": ["a1", "n1", "a2", "n2", "v1", "e1"],
    },
    # 模板19: 深情式
    {
        "zh": "{t1}，我想告诉你，{a1}{n1}也不及你的笑容珍贵，{v1}，{e1}",
        "en": "{t1}, I want to tell you that even {a1} {n1} cannot match the preciousness of your smile, {v1}, {e1}",
        "fr": "{t1}, je veux te dire que même le {a1} {n1} ne vaut pas la précieuseté de ton sourire, {v1}, {e1}",
        "de": "{t1}, ich möchte dir sagen, dass selbst {a1} {n1} nicht die Kostbarkeit deines Lächelns erreicht, {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板20: 豁达式
    {
        "zh": "得失随缘，心无增减，{t1}，愿{a1}{n1}{v1}，{e1}",
        "en": "Let gains and losses follow fate, with an unchanging heart; {t1}, may the {a1} {n1} {v1}, {e1}",
        "fr": "Laisse les gains et les perles suivre le destin, avec un cœur immuable ; {t1}, puisse le {a1} {n1} {v1}, {e1}",
        "de": "Lass Gewinne und Verluste dem Schicksal folgen, mit unveränderlichem Herzen; {t1}, möge das {a1} {n1} {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板21: 希望式
    {
        "zh": "即使{a1}{n1}暂时被云遮住，也要相信它会再次{v1}，{t1}，{e1}",
        "en": "Even if the {a1} {n1} is temporarily hidden by clouds, trust that it will {v1} again, {t1}, {e1}",
        "fr": "Même si le {a1} {n1} est temporairement caché par les nuages, crois qu'il {v1} à nouveau, {t1}, {e1}",
        "de": "Auch wenn das {a1} {n1} vorübergehend von Wolken verdeckt ist, vertraue darauf, dass es wieder {v1}, {t1}, {e1}",
        "vars": ["a1", "n1", "v1", "t1", "e1"],
    },
    # 模板22: 行动式
    {
        "zh": "去做你想做的事吧，{t1}，让{a1}{n1}{v1}，{e1}",
        "en": "Go do what you want to do; {t1}, let the {a1} {n1} {v1}, {e1}",
        "fr": "Va faire ce que tu veux faire ; {t1}, laisse le {a1} {n1} {v1}, {e1}",
        "de": "Geh und tu, was du tun willst; {t1}, lass das {a1} {n1} {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板23: 回忆式
    {
        "zh": "多年以后回望今日，{t1}，愿{a1}{n1}般的记忆{v1}，{e1}",
        "en": "Looking back on today years later, {t1}, may memories like {a1} {n1} {v1}, {e1}",
        "fr": "En regardant aujourd'hui des années plus tard, {t1}, puissent les souvenirs comme le {a1} {n1} {v1}, {e1}",
        "de": "Wenn du in Jahren auf heute zurückblickst, {t1}, mögen Erinnerungen wie das {a1} {n1} {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
    # 模板24: 祝福叠加
    {
        "zh": "{e1}也愿{a1}{n1}{v1}，{t1}都有好事发生。",
        "en": "{e1} May the {a1} {n1} also {v1}, and may good things happen {t1}.",
        "fr": "{e1} Puissent le {a1} {n1} aussi {v1}, et que de bonnes choses arrivent {t1}.",
        "de": "{e1} Möge das {a1} {n1} auch {v1}, und mögen {t1} gute Dinge geschehen.",
        "vars": ["e1", "a1", "n1", "v1", "t1"],
    },
    # 模板25: 自然人生
    {
        "zh": "山高水长，岁月如歌，{t1}，愿{a1}{n1}{v1}，{e1}",
        "en": "Mountains high, rivers long, years like a song; {t1}, may the {a1} {n1} {v1}, {e1}",
        "fr": "Montagnes hautes, rivières longues, années comme une chanson ; {t1}, puisse le {a1} {n1} {v1}, {e1}",
        "de": "Berge hoch, Flüsse lang, Jahre wie ein Lied; {t1}, möge das {a1} {n1} {v1}, {e1}",
        "vars": ["t1", "a1", "n1", "v1", "e1"],
    },
]


def pick(lst, idx):
    """按索引取词，超出则取模"""
    return lst[idx % len(lst)]


def fill_template(tpl, indices):
    """根据模板和变量索引填充四语文本"""
    vals = {}
    for var in tpl["vars"]:
        # 解析变量类型和序号，如 n1 -> (NOUNS, 1), a2 -> (ADJ, 2)
        vtype = var[0]
        vidx = int(var[1:]) - 1
        idx = indices.get(vtype, [0])[vidx] if vidx < len(indices.get(vtype, [0])) else 0
        if vtype == "n":
            vals[var] = pick(NOUNS, idx)
        elif vtype == "a":
            vals[var] = pick(ADJ, idx)
        elif vtype == "v":
            vals[var] = pick(VERBS, idx)
        elif vtype == "t":
            vals[var] = pick(TIMEPHRASES, idx)
        elif vtype == "e":
            vals[var] = pick(ENDINGS, idx)

    # 填充时按语言取对应索引
    result = {}
    for lang_key, lang_idx in [("zh", 0), ("en", 1), ("fr", 2), ("de", 3)]:
        text = tpl[lang_key]
        for var in tpl["vars"]:
            word_tuple = vals[var]
            text = text.replace("{" + var + "}", word_tuple[lang_idx])
        result[lang_key] = text
    return result


def generate_blessings(target=1000):
    """生成 target 条独特祝福语"""
    blessings = []
    seen_zh = set()
    attempts = 0
    max_attempts = target * 20

    # 为每个模板分配生成数量
    per_template = target // len(TEMPLATES) + 5

    for tpl_idx, tpl in enumerate(TEMPLATES):
        generated = 0
        # 用笛卡尔积的子集来生成多样性
        var_counts = {}
        for var in tpl["vars"]:
            vtype = var[0]
            if vtype not in var_counts:
                var_counts[vtype] = 0
            var_counts[vtype] += 1

        # 为每种变量类型生成索引组合
        n_types = var_counts.get("n", 0)
        a_types = var_counts.get("a", 0)
        v_types = var_counts.get("v", 0)
        t_types = var_counts.get("t", 0)
        e_types = var_counts.get("e", 0)

        # 生成索引组合
        n_ranges = [range(len(NOUNS))] * n_types
        a_ranges = [range(len(ADJ))] * a_types
        v_ranges = [range(len(VERBS))] * v_types
        t_ranges = [range(len(TIMEPHRASES))] * t_types
        e_ranges = [range(len(ENDINGS))] * e_types

        all_ranges = n_ranges + a_ranges + v_ranges + t_ranges + e_ranges
        all_products = list(itertools.product(*all_ranges))
        random.shuffle(all_products)

        for combo in all_products:
            if generated >= per_template or len(blessings) >= target:
                break
            attempts += 1
            if attempts > max_attempts:
                break

            # 分配索引到变量
            ptr = 0
            indices = {"n": [], "a": [], "v": [], "t": [], "e": []}
            for vtype in ["n", "a", "v", "t", "e"]:
                cnt = var_counts.get(vtype, 0)
                indices[vtype] = list(combo[ptr:ptr + cnt])
                ptr += cnt

            result = fill_template(tpl, indices)

            # 确保中文 > 30 字
            zh_len = len(result["zh"].replace(" ", ""))
            if zh_len < 30:
                continue

            # 去重
            if result["zh"] in seen_zh:
                continue
            seen_zh.add(result["zh"])

            blessings.append(result)
            generated += 1

        if len(blessings) >= target:
            break

    # 如果不够，继续用随机组合补充
    while len(blessings) < target and attempts < max_attempts:
        attempts += 1
        tpl = random.choice(TEMPLATES)
        var_counts = {}
        for var in tpl["vars"]:
            vtype = var[0]
            var_counts[vtype] = var_counts.get(vtype, 0) + 1
        indices = {}
        for vtype in ["n", "a", "v", "t", "e"]:
            cnt = var_counts.get(vtype, 0)
            indices[vtype] = [random.randint(0, 99) for _ in range(cnt)]
        result = fill_template(tpl, indices)
        zh_len = len(result["zh"].replace(" ", ""))
        if zh_len < 30 or result["zh"] in seen_zh:
            continue
        seen_zh.add(result["zh"])
        blessings.append(result)

    return blessings[:target]


if __name__ == "__main__":
    print("正在生成1000条四语祝福语...")
    blessings = generate_blessings(1000)
    print(f"生成完成，共 {len(blessings)} 条")

    # 统计中文长度
    lengths = [len(b["zh"].replace(" ", "")) for b in blessings]
    print(f"中文长度: 最小={min(lengths)}, 最大={max(lengths)}, 平均={sum(lengths)/len(lengths):.1f}")
    print(f"小于30字的数量: {sum(1 for l in lengths if l < 30)}")

    # 保存
    output = {
        "count": len(blessings),
        "languages": ["zh", "en", "fr", "de"],
        "blessings": blessings,
    }
    with open("/home/user/.super_doubao/super-doubao-runtime/workspace/blessings.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("已保存到 blessings.json")

    # 打印前3条示例
    print("\n=== 前3条示例 ===")
    for i, b in enumerate(blessings[:3], 1):
        print(f"\n[{i}] 中文({len(b['zh'])}字): {b['zh']}")
        print(f"    EN: {b['en']}")
        print(f"    FR: {b['fr']}")
        print(f"    DE: {b['de']}")
