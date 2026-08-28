#!/usr/bin/env python3
"""
Dino 四语祝福群发机器人 v2
- 手写风格祝福语，清新自然不套路
- 中文字体：宋体 / 英文字体：Times New Roman
- 简洁卡片式 HTML 邮件 + .ics 日历附件
- 每个收件人随机不同祝福
"""
import os
import time, sys, json, time, random, argparse, urllib.request, urllib.error, base64, uuid
from datetime import datetime, timezone
random.seed(int(time.time()))
MATON_BASE = "https://gateway.maton.ai/outlook/v1.0"

# ===================== 手写祝福语库（中英法德）=====================
# 风格：清新、有趣、有温度、不套路
BLESSINGS = [
    {"zh":"今天出门记得抬头看看天，说不定有朵云长得特别像你正在想的那件好事。日子嘛，总得自己找点甜。","en":"Look up when you step out today — there might be a cloud shaped exactly like the good thing you've been hoping for. Life's sweeter when you find the sugar yourself.","fr":"En sortant aujourd'hui, pense à lever les yeux vers le ciel — il y a peut-être un nuage qui ressemble exactement à la bonne chose que tu espères. La vie, c'est à toi de lui trouver du sucre.","de":"Schau beim Rausgehen heute mal zum Himmel — vielleicht ist eine Wolke genau so geformt wie das Gute, auf das du hoffst. Das Leben wird süßer, wenn du den Zucker selbst findest."},
    {"zh":"听说认真吃好每一顿饭的人，运气都不会太差。今天的午餐，记得给自己加个蛋。","en":"They say folks who take every meal seriously never have much bad luck. Go ahead, add an egg to your lunch today.","fr":"On dit que les gens qui prennent chaque repas au sérieux n'ont jamais trop de malchance. Allez, ajoute un œuf à ton déjeuner aujourd'hui.","de":"Man sagt, Leute, die jedes Mahlzeit ernst nehmen, haben nie viel Pech. Na dann, leg heute ein Ei auf dein Mittagessen."},
    {"zh":"你笑起来的样子比今天的阳光还好看，所以别老绷着脸啦，嘴角翘一下又不花钱。","en":"Your smile's nicer than today's sunshine, so stop looking so serious — turning up the corners of your mouth costs nothing.","fr":"Ton sourire est plus beau que le soleil d'aujourd'hui, alors arrête de faire la tête — remonter les coins de la bouche, ça ne coûte rien.","de":"Dein Lächeln ist schöner als der Sonnenschein heute, also hör auf, so ernst zu gucken — die Mundwinkel hochziehen kostet nichts."},
    {"zh":"把烦心事写在纸上折成飞机，从窗户扔出去。虽然不环保，但心情会好很多。（记得捡回来啊喂）","en":"Write what's bugging you on a piece of paper, fold it into a plane, and chuck it out the window. Not great for the planet, but you'll feel way better. (Go pick it back up, though.)","fr":"Écris ce qui t'embête sur un papier, plie-le en avion et jette-le par la fenêtre. Pas terrible pour la planète, mais tu te sentiras beaucoup mieux. (Va le ramasser, hein.)","de":"Schreib, was dich ärgert, auf ein Papier, falte es zu einem Flugzeug und wirf es raus. Nicht toll für die Umwelt, aber du fühlst dich viel besser. (Hol es aber wieder zurück.)"},
    {"zh":"今天的风里有桂花的味道，如果你那边没有，就想象一下。反正想象力是免费的，多用用不亏。","en":"Today's wind smells like osmanthus. If you don't have it where you are, just picture it. Imagination's free anyway — might as well use it.","fr":"Le vent d'aujourd'hui sent l'osmanthe. Si tu n'en as pas là où tu es, imagine-le. L'imagination est gratuite de toute façon — autant s'en servir.","de":"Der Wind heute riecht nach Osmanthus. Wenn du das dort nicht hast, stell es dir einfach vor. Vorstellungskraft ist umsonst — also nutz sie."},
    {"zh":"你已经做得很好了，真的。不用跟别人比，你按自己的节奏往前走就已经很了不起了。","en":"You're doing really well, honestly. No need to compare yourself to anyone — moving forward at your own pace is already something.","fr":"Tu fais vraiment du bien, sincèrement. Pas besoin de te comparer aux autres — avancer à ton propre rythme, c'est déjà quelque chose.","de":"Du machst das wirklich gut, ehrlich. Kein Grund, dich mit anderen zu vergleichen — in deinem Tempo voranzugehen ist schon etwas."},
    {"zh":"今晚早点睡，梦里什么都有。如果梦里也没有，那就说明你需要的其实是好好睡一觉。","en":"Get to bed early tonight — dreams have everything. If even your dreams come up empty, then what you really need is just a good night's sleep.","fr":"Va te coucher tôt ce soir — les rêves ont tout. Si même les rêves n'ont rien, alors ce dont tu as vraiment besoin, c'est juste une bonne nuit de sommeil.","de":"Geh heute früh ins Bett — Träume haben alles. Wenn selbst deine Träume leer ausgehen, dann brauchst du eigentlich nur eine gute Nachtruhe."},
    {"zh":"生活有时候像一杯温水，没什么味道，但喝下去很舒服。愿你今天也能找到这种舒服的感觉。","en":"Life's sometimes like a glass of warm water — nothing special in the taste, but it goes down easy. Hope you find that easy feeling today too.","fr":"La vie est parfois comme un verre d'eau tiède — rien d'extraordinaire au goût, mais ça passe bien. J'espère que tu trouveras cette sensation facile aujourd'hui aussi.","de":"Das Leben ist manchmal wie ein Glas warmes Wasser — nichts Besonderes im Geschmack, aber es geht leicht runter. Hoffentlich findest du dieses leichte Gefühl heute auch."},
    {"zh":"听说你最近有点累？那就允许自己偷个懒吧。地球离了你照样转，真的。","en":"Heard you've been a bit tired lately? Then cut yourself some slack and take it easy. The world keeps spinning without you, really.","fr":"On dit que tu es un peu fatigué ces derniers temps ? Alors accorde-toi une pause et prends ça cool. Le monde continue de tourner sans toi, vraiment.","de":"Hört sich an, als wärst du in letzter Zeit etwas müde? Dann gönn dir eine Pause und nimm es locker. Die Welt dreht sich auch ohne dich weiter, wirklich."},
    {"zh":"今天也要好好吃饭，好好睡觉，好好对待自己。你是这个世界上独一无二的限量版，不接受反驳。","en":"Eat well, sleep well, and be good to yourself today too. You're a one-of-a-kind limited edition in this world — no arguments.","fr":"Mange bien, dors bien et sois bon avec toi-même aujourd'hui aussi. Tu es une édition limitée unique au monde — pas de discussion.","de":"Iss gut, schlaf gut und sei gut zu dir heute auch. Du bist eine einzigartige Limited Edition auf dieser Welt — keine Diskussion."},
    {"zh":"把今天过成以后会怀念的样子吧。不用多精彩，哪怕只是傍晚散步时风吹过头发，也值得记下来。","en":"Make today the kind of day you'll look back on fondly. Doesn't have to be anything grand — even the wind in your hair on an evening walk is worth holding onto.","fr":"Fais de aujourd'hui le genre de journée dont tu te souviendras avec tendresse. Pas besoin que ce soit grandiose — même le vent dans tes cheveux pendant une promenade du soir, ça vaut la peine d'être gardé.","de":"Mach heute zu der Art Tag, an den du dich später gerne erinnerst. Muss nichts Großes sein — selbst der Wind in deinen Haaren bei einem Abendspaziergang ist es wert, festzuhalten."},
    {"zh":"你知道吗？你不经意间说过的某句话，可能正在温暖着某个人。所以多说点好听的，利人利己。","en":"You know what? Something you said without even thinking might be warming someone's heart right now. So say more nice things — good for them, good for you.","fr":"Tu sais quoi ? Quelque chose que tu as dit sans même y penser réchauffe peut-être le cœur de quelqu'un en ce moment. Alors dis plus de choses gentilles — bon pour eux, bon pour toi.","de":"Weißt du was? Etwas, das du gesagt hast, ohne nachzudenken, wärmt vielleicht gerade jemandem das Herz. Also sag mehr nette Dinge — gut für die, gut für dich."},
    {"zh":"如果今天过得不太顺利也没关系，明天又是新的一天。实在不行还有后天，大后天……反正日子长着呢。","en":"If today's not going great, that's okay — tomorrow's another day. And if that doesn't work out, there's the day after, and the one after that... plenty of days ahead.","fr":"Si aujourd'hui ne se passe pas super, ce n'est pas grave — demain est un autre jour. Et si ça ne marche pas, il y a après-demain, et celui d'après... plein de jours à venir.","de":"Wenn heute nicht super läuft, ist das okay — morgen ist ein neuer Tag. Und wenn das nicht klappt, gibt es übermorgen, und den danach... genug Tage vor dir."},
    {"zh":"送你一朵虚拟的小红花，奖励你今天也有在认真生活。别小看这朵花，它在我心里开得可艳了。","en":"Here's a virtual little red flower for you — a reward for living earnestly today too. Don't underestimate it, it's blooming bright in my heart.","fr":"Voici une petite fleur rouge virtuelle pour toi — une récompense pour avoir vécu sérieusement aujourd'hui aussi. Ne la sous-estime pas, elle s'épanouit brillamment dans mon cœur.","de":"Hier ist eine virtuelle kleine rote Blume für dich — eine Belohnung dafür, dass du heute auch ernsthaft lebst. Unterschätz sie nicht, sie blüht hell in meinem Herzen."},
    {"zh":"有时候慢一点不是坏事，你看那些长得慢的树，木质都更结实。慢慢来，比较快。","en":"Sometimes going slower's not a bad thing — look at slow-growing trees, their wood's tougher. Take your time, it actually gets you there faster.","fr":"Parfois aller plus lentement n'est pas une mauvaise chose — regarde les arbres qui poussent lentement, leur bois est plus solide. Prends ton temps, ça t'y mène en fait plus vite.","de":"Manchmal ist langsamer zu gehen keine schlechte Sache — schau dir langsam wachsende Bäume an, ihr Holz ist fester. Nimm dir Zeit, es bringt dich tatsächlich schneller voran."},
    {"zh":"今天的晚霞特别美，如果你错过了也没关系，我帮你记着了。下次一起看。","en":"Today's sunset was especially beautiful. If you missed it, no worries — I kept it for you. Let's catch one together next time.","fr":"Le coucher de soleil d'aujourd'hui était particulièrement beau. Si tu l'as manqué, pas de souci — je l'ai gardé pour toi. On en regarde un ensemble la prochaine fois.","de":"Der Sonnenuntergang heute war besonders schön. Wenn du ihn verpasst hast, keine Sorge — ich habe ihn dir behalten. Lass uns uns nächstes Mal einen zusammen ansehen."},
    {"zh":"你有没有发现，认真生活的人身上会发光？不是那种刺眼的光，是暖暖的、让人想靠近的光。你就是。","en":"Ever notice how people who live earnestly glow? Not the blinding kind — the warm kind that makes you want to get close. That's you.","fr":"Tu as déjà remarqué comme les gens qui vivent sérieusement brillent ? Pas le genre éblouissant — le genre chaleureux qui donne envie de s'approcher. C'est toi.","de":"Schon mal bemerkt, wie Leute, die ernsthaft leben, leuchten? Nicht die blendende Art — die warme Art, die einen näherkommen lässt. Das bist du."},
    {"zh":"如果快乐太难，那我祝你平安。如果平安也难，那我祝你能睡个好觉。能睡好，一切都会好起来的。","en":"If happiness feels out of reach, then I wish you peace. If peace feels out of reach too, then I wish you a good night's sleep. Sleep well, and everything else will follow.","fr":"Si le bonheur semble hors de portée, alors je te souhaite la paix. Si la paix semble aussi hors de portée, alors je te souhaite une bonne nuit de sommeil. Dors bien, et tout le reste suivra.","de":"Wenn Glück unerreichbar scheint, dann wünsche ich dir Frieden. Wenn Frieden auch unerreichbar scheint, dann wünsche ich dir eine gute Nacht. Schlaf gut, und alles andere wird folgen."},
    {"zh":"今天也要记得多喝水哦。不是因为多喝水有多养生，而是喝水的时候可以停下来喘口气。","en":"Remember to drink more water today too. Not because it's some health thing — it's just that drinking water gives you a chance to stop and catch your breath.","fr":"N'oublie pas de boire plus d'eau aujourd'hui aussi. Pas parce que c'est un truc de santé — c'est juste que boire de l'eau te donne une chance de t'arrêter et de reprendre ton souffle.","de":"Denk auch heute daran, mehr Wasser zu trinken. Nicht weil es irgendein Gesundheitsding ist — sondern weil Wassertrinken dir eine Chance gibt, innezuhalten und durchzuatmen."},
    {"zh":"你比你自己想象的要厉害得多。不信你回头看看，那些你以为熬不过去的日子，不都过来了吗？","en":"You're way more capable than you give yourself credit for. Don't believe me? Look back — didn't you get through all those days you thought you'd never survive?","fr":"Tu es bien plus capable que tu ne le penses. Tu ne me crois pas ? Regarde en arrière — n'as-tu pas traversé tous ces jours que tu pensais ne jamais pouvoir survivre ?","de":"Du bist viel fähiger, als du dir zutraust. Glaubst du mir nicht? Schau zurück — hast du nicht all die Tage überstanden, von denen du dachtest, du schaffst sie nicht?"},
    {"zh":"今天的风很舒服，像有人轻轻拍了拍你的肩膀说：没事的，继续走吧。","en":"Today's wind feels nice — like someone patting your shoulder gently and saying: it's okay, keep going.","fr":"Le vent d'aujourd'hui est agréable — comme quelqu'un qui te tapote doucement l'épaule et dit : ce n'est rien, continue.","de":"Der Wind heute fühlt sich gut an — wie jemand, der dir sanft auf die Schulter klopft und sagt: Schon gut, geh weiter."},
    {"zh":"别总想着要做个很厉害的人，做个很开心的人就已经很厉害了。真的，不信你试试。","en":"Stop trying to be someone impressive — being someone happy is already impressive. Really, try it if you don't believe me.","fr":"Arrête de vouloir être quelqu'un d'impressionnant — être quelqu'un de heureux, c'est déjà impressionnant. Vraiment, essaie si tu ne me crois pas.","de":"Hör auf, versuchen zu müssen, jemand Beeindruckendes zu sein — jemand Glückliches zu sein ist schon beeindruckend. Wirklich, versuch es, wenn du mir nicht glaubst."},
    {"zh":"你今天的任务只有三个：吃好、睡好、心情好。如果做不到，那就先完成第一个，剩下的明天再说。","en":"You've only got three tasks today: eat well, sleep well, be in a good mood. Can't manage all three? Just nail the first one, the rest can wait till tomorrow.","fr":"Tu n'as que trois tâches aujourd'hui : bien manger, bien dormir, être de bonne humeur. Tu n'y arrives pas pour les trois ? Réussis juste la première, le reste attendra demain.","de":"Du hast heute nur drei Aufgaben: gut essen, gut schlafen, gute Laune haben. Schaffst du nicht alle drei? Dann schaff einfach die erste, der Rest wartet auf morgen."},
    {"zh":"生活给你柠檬的时候，你可以做柠檬水，也可以直接把柠檬扔回去。怎么开心怎么来，不用按剧本走。","en":"When life hands you lemons, you can make lemonade — or you can just throw the lemons right back. Do whatever makes you happy, no need to follow the script.","fr":"Quand la vie te donne des citrons, tu peux faire de la limonade — ou tu peux juste renvoyer les citrons. Fais ce qui te rend heureux, pas besoin de suivre le scénario.","de":"Wenn das Leben dir Zitronen gibt, kannst du Limonade machen — oder du kannst die Zitronen einfach zurückwerfen. Mach, was dich glücklich macht, kein Grund, dem Drehbuch zu folgen."},
    {"zh":"你知道吗？你存在这件事本身，就已经让某些人的世界变得不一样了。所以别妄自菲薄，你很重要的。","en":"You know what? The simple fact that you exist has already changed someone's world. So don't sell yourself short — you matter.","fr":"Tu sais quoi ? Le simple fait que tu existes a déjà changé le monde de quelqu'un. Alors ne te dévalorise pas — tu comptes.","de":"Weißt du was? Die einfache Tatsache, dass du existierst, hat bereits jemandes Welt verändert. Also rede dich nicht schlecht — du bist wichtig."},
    {"zh":"今天也要记得给自己一个大大的拥抱。如果没人抱你，那就自己抱自己，左手抱右手，也算数。","en":"Remember to give yourself a big hug today too. If no one's hugging you, hug yourself — left arm around right arm, it counts.","fr":"N'oublie pas de te faire un gros câlin aujourd'hui aussi. Si personne ne te câline, fais-le toi-même — bras gauche autour du bras droit, ça compte.","de":"Denk auch heute daran, dich selbst fest zu umarmen. Wenn dich niemand umarmt, umarm dich selbst — linker Arm um rechten Arm, das zählt."},
    {"zh":"慢慢来，不用急。你看那些好看的晚霞，不也是一点点染红天空的吗？你也一样。","en":"Take your time, no rush. Look at those beautiful sunsets — don't they also turn the sky red little by little? Same with you.","fr":"Prends ton temps, pas de précipitation. Regarde ces beaux couchers de soleil — ne teintent-ils pas aussi le ciel rouge petit à petit ? C'est pareil pour toi.","de":"Nimm dir Zeit, keine Eile. Schau dir diese schönen Sonnenuntergänge an — färben sie den Himmel nicht auch nach und nach rot? Genau so ist es mit dir."},
    {"zh":"如果今天有什么开心的小事，记得记下来。以后翻出来看的时候，会发现原来自己拥有过这么多快乐。","en":"If something small makes you happy today, write it down. When you flip through it later, you'll realize you've had so much happiness.","fr":"Si quelque chose de petit te rend heureux aujourd'hui, note-le. Quand tu le reliras plus tard, tu réaliseras que tu as eu tant de bonheur.","de":"Wenn dich heute etwas Kleines glücklich macht, schreib es auf. Wenn du es später durchblätterst, wirst du merken, dass du so viel Glück hattest."},
    {"zh":"你不用成为任何人，你只要成为你自己就好。这个世界上已经有太多别人了，不差你一个。","en":"You don't need to become anyone else — just be yourself. There are already too many other people in this world, no need for one more.","fr":"Tu n'as pas besoin de devenir quelqu'un d'autre — sois juste toi-même. Il y a déjà trop d'autres personnes dans ce monde, pas besoin d'une de plus.","de":"Du musst niemand sonst werden — sei einfach du selbst. Es gibt schon zu viele andere Menschen auf dieser Welt, es braucht keinen weiteren."},
    {"zh":"今天的月亮会很圆，如果你那边看不到，就当它在云后面偷偷看着你。反正它一直都在。","en":"Today's moon will be full. If you can't see it where you are, just imagine it peeking at you from behind the clouds. It's always there anyway.","fr":"La lune d'aujourd'hui sera pleine. Si tu ne peux pas la voir là où tu es, imagine qu'elle te regarde en cachette derrière les nuages. Elle est toujours là de toute façon.","de":"Der Mond heute wird voll sein. Wenn du ihn dort nicht sehen kannst, stell dir vor, er lugt hinter den Wolken hervor und beobachtet dich. Er ist sowieso immer da."},
    {"zh":"累了就歇会儿，没人规定你必须一直往前冲。偶尔停下来看看路边的花，也是生活的一部分。","en":"Rest when you're tired — no one's making you keep rushing forward. Stopping now and then to look at the flowers by the road is part of life too.","fr":"Repose-toi quand tu es fatigué — personne ne t'oblige à toujours foncer. S'arrêter de temps en temps pour regarder les fleurs au bord du chemin, ça fait aussi partie de la vie.","de":"Ruh dich aus, wenn du müde bist — niemand zwingt dich, immer weiterzustürmen. Ab und anzuhalten, um die Blumen am Wegrand zu betrachten, gehört auch zum Leben."},
    {"zh":"你笑的时候眼睛会弯成月牙，特别好看。所以今天多笑笑，就当是为了世界和平做贡献。","en":"Your eyes curve into little crescents when you smile — it's lovely. So smile more today, call it your contribution to world peace.","fr":"Tes yeux se courbent en petits croissants quand tu souris — c'est adorable. Alors souris plus aujourd'hui, appelle ça ta contribution à la paix mondiale.","de":"Deine Augen krümmen sich zu kleinen Halbmonden, wenn du lächelst — es ist lieb. Also lächle heute mehr, nenn es deinen Beitrag zum Weltfrieden."},
    {"zh":"日子是过出来的，不是想出来的。所以别想太多，先把今天这顿饭吃好再说。","en":"Days are lived, not overthought. So don't think too much — just make sure you eat well today, and figure out the rest later.","fr":"Les jours se vivent, ne se réfléchissent pas. Alors ne réfléchis pas trop — assure-toi juste de bien manger aujourd'hui, et on verra le reste après.","de":"Tage werden gelebt, nicht zu Ende gedacht. Also denk nicht zu viel nach — sorg einfach dafür, dass du heute gut isst, und den Rest sehen wir später."},
    {"zh":"今天也要做个温柔的人哦。不是对别人，是对自己。对自己温柔一点，比什么都重要。","en":"Be gentle today too — not to other people, but to yourself. Being gentle with yourself matters more than anything.","fr":"Sois doux aujourd'hui aussi — pas envers les autres, mais envers toi-même. Être doux avec toi-même importe plus que tout.","de":"Sei heute auch sanft — nicht gegenüber anderen, sondern dir selbst. Sanft zu dir selbst zu sein ist wichtiger als alles."},
    {"zh":"如果今天下雨了，那就听听雨声吧。雨落在屋檐上的声音，是大自然给你讲的睡前故事。","en":"If it rains today, just listen to it. The sound of rain on the roof is nature's bedtime story for you.","fr":"S'il pleut aujourd'hui, écoute-le juste. Le bruit de la pluie sur le toit, c'est l'histoire du coucher que la nature te raconte.","de":"Wenn es heute regnet, hör ihm einfach zu. Das Geräusch von Regen auf dem Dach ist die Gute-Nacht-Geschichte der Natur für dich."},
    {"zh":"你已经很棒了，真的。哪怕今天什么都没做成，能醒过来面对这一天，就已经很勇敢了。","en":"You're already doing great, really. Even if you got nothing done today, just waking up and facing the day took courage.","fr":"Tu fais déjà du bien, vraiment. Même si tu n'as rien accompli aujourd'hui, juste te réveiller et affronter la journée, ça a demandé du courage.","de":"Du machst das schon gut, wirklich. Selbst wenn du heute nichts geschafft hast, nur aufzuwachen und dich dem Tag zu stellen, hat Mut gebraucht."},
    {"zh":"送你一阵风，里面装着我想说的话。如果你感觉到了，就当是我在跟你打招呼：嘿，今天也要开心呀。","en":"Here's a gust of wind for you, carrying what I want to say. If you feel it, take it as me saying hi — hey, be happy today too.","fr":"Voici une bouffée de vent pour toi, qui porte ce que je veux dire. Si tu la sens, prends ça pour moi qui te dis salut — hé, sois heureux aujourd'hui aussi.","de":"Hier ist ein Windstoß für dich, der trägt, was ich sagen will. Wenn du ihn spürst, nimm es als mein Hallo — hey, sei auch heute glücklich."},
    {"zh":"别老盯着自己没有的东西看，多看看自己已经拥有的。你会发现，其实你已经很富有了。","en":"Stop staring at what you don't have — look more at what you've already got. You'll realize you're actually pretty rich.","fr":"Arrête de fixer ce que tu n'as pas — regarde plus ce que tu as déjà. Tu réaliseras que tu es en fait assez riche.","de":"Hör auf, auf das zu starren, was du nicht hast — schau mehr auf das, was du bereits hast. Du wirst merken, dass du eigentlich ziemlich reich bist."},
    {"zh":"今天的咖啡要慢慢喝，书要慢慢翻，日子也要慢慢过。快了就尝不出味道了。","en":"Drink your coffee slowly today, turn the pages slowly, and take life slowly too. When it's too fast, you can't taste a thing.","fr":"Bois ton café lentement aujourd'hui, tourne les pages lentement, et prends la vie lentement aussi. Quand c'est trop rapide, on ne peut rien goûter.","de":"Trink deinen Kaffee heute langsam, blättere langsam, und nimm das Leben auch langsam. Wenn es zu schnell geht, kannst du nichts schmecken."},
    {"zh":"你知道吗？你认真做某件事的样子特别迷人。所以今天也找件事认真做做，迷倒自己。","en":"You know what? You look especially lovely when you're focused on something. So find something to focus on today — charm yourself.","fr":"Tu sais quoi ? Tu as l'air particulièrement adorable quand tu es concentré sur quelque chose. Alors trouve quelque chose sur quoi te concentrer aujourd'hui — charme-toi toi-même.","de":"Weißt du was? Du siehst besonders lieb aus, wenn du auf etwas konzentriert bist. Also find heute etwas, auf das du dich konzentrierst — bezaubere dich selbst."},
    {"zh":"如果今天有人惹你生气了，那就深呼吸三次。然后在心里把他变成一只小青蛙，呱呱叫两声，心情就好了。","en":"If someone gets on your nerves today, take three deep breaths. Then turn them into a little frog in your head, let it croak twice, and you'll feel better.","fr":"Si quelqu'un t'énerve aujourd'hui, prends trois respirations profondes. Puis transforme-le en petite grenouille dans ta tête, laisse-la coasser deux fois, et tu te sentiras mieux.","de":"Wenn dich heute jemand auf die Palme bringt, atme dreimal tief durch. Dann verwandel ihn in deinem Kopf in einen kleinen Frosch, lass ihn zweimal quaken, und dir geht es besser."},
    {"zh":"你比昨天的自己又进步了一点点，虽然你可能没发现。但没关系，我发现了，偷偷告诉你。","en":"You've gotten a little better than yesterday's you, even though you might not have noticed. But that's okay — I noticed, and I'm telling you in secret.","fr":"Tu t'es un peu amélioré par rapport à ton moi d'hier, même si tu ne l'as peut-être pas remarqué. Mais ce n'est pas grave — je l'ai remarqué, et je te le dis en secret.","de":"Du bist ein bisschen besser geworden als dein gestriges Ich, auch wenn du es vielleicht nicht bemerkt hast. Aber das ist okay — ich habe es bemerkt und sage es dir heimlich."},
    {"zh":"今天也要好好爱自己哦。不是那种买很贵东西的爱，是认真吃饭、按时睡觉、不跟自己较劲的那种爱。","en":"Love yourself well today too — not the kind where you buy expensive things, but the kind where you eat properly, sleep on time, and don't beat yourself up.","fr":"Aime-toi bien aujourd'hui aussi — pas le genre où tu achètes des choses chères, mais celui où tu manges correctement, dors à l'heure et ne te bats pas contre toi-même.","de":"Hab dich auch heute gut — nicht die Art, wo du teure Dinge kaufst, sondern die, wo du richtig isst, pünktlich schläfst und dich nicht selbst fertigmachst."},
    {"zh":"听说今晚的星星特别亮，如果你那边能看到，就替我许个愿吧。许什么都行，反正星星很大方。","en":"Heard the stars are extra bright tonight. If you can see them where you are, make a wish for me. Anything goes — stars are generous like that.","fr":"On dit que les étoiles sont particulièrement brillantes ce soir. Si tu peux les voir là où tu es, fais un vœu pour moi. N'importe quoi — les étoiles sont généreuses comme ça.","de":"Hört sich an, als wären die Sterne heute extra hell. Wenn du sie dort sehen kannst, wünsch dir was für mich. Alles geht — Sterne sind so großzügig."},
    {"zh":"生活不是赛跑，是散步。所以不用跟别人比速度，按自己的节奏走，路边的花都是你的。","en":"Life isn't a race, it's a walk. So no need to compare your speed with anyone — walk at your own pace, and all the flowers by the road are yours.","fr":"La vie n'est pas une course, c'est une promenade. Alors pas besoin de comparer ta vitesse avec les autres — marche à ton rythme, et toutes les fleurs au bord du chemin sont à toi.","de":"Das Leben ist kein Rennen, es ist ein Spaziergang. Also kein Grund, dein Tempo mit anderen zu vergleichen — geh in deinem Tempo, alle Blumen am Wegrand gehören dir."},
    {"zh":"你今天的存在本身就是一件好事。真的，这个世界因为有你在，变得好了那么一点点。","en":"Your being here today is itself a good thing. Really — this world's gotten just a little bit better because you're in it.","fr":"Ta présence aujourd'hui est en soi une bonne chose. Vraiment — ce monde est devenu un petit peu meilleur parce que tu es dedans.","de":"Dein Dasein heute ist an sich eine gute Sache. Wirklich — diese Welt ist ein bisschen besser geworden, weil du in ihr bist."},
    {"zh":"如果今天觉得有点丧，那就丧一会儿吧。情绪就像天气，晴久了总会下点雨，雨过了就又晴了。","en":"If you're feeling a bit down today, then be down for a while. Emotions are like weather — after too much sun it always rains a bit, and after the rain it's sunny again.","fr":"Si tu te sens un peu abattu aujourd'hui, alors sois-le un moment. Les émotions sont comme la météo — après trop de soleil, il pleut toujours un peu, et après la pluie, le soleil revient.","de":"Wenn du dich heute ein bisschen niedergeschlagen fühlst, dann sei es eine Weile. Gefühle sind wie das Wetter — nach zu viel Sonne regnet es immer ein bisschen, und nach dem Regen scheint wieder die Sonne."},
    {"zh":"今天也要记得抬头看看天，不管是晴天还是阴天，天空都很大，大到能装下你所有的烦恼。","en":"Remember to look up at the sky today too — sunny or cloudy, it's vast, vast enough to hold all your worries.","fr":"N'oublie pas de lever les yeux au ciel aujourd'hui aussi — ensoleillé ou nuageux, il est vaste, assez vaste pour contenir tous tes soucis.","de":"Denk auch heute daran, zum Himmel aufzusehen — ob sonnig oder bewölkt, er ist weit, weit genug, um all deine Sorgen zu tragen."},
    {"zh":"送你一颗虚拟的糖，含在嘴里（假装），甜到心里。如果不够甜，那就再含一颗，反正不要钱。","en":"Here's a virtual candy for you — pop it in your mouth (pretend), sweet all the way to your heart. Not sweet enough? Have another one — they're free anyway.","fr":"Voici un bonbon virtuel pour toi — mets-le dans ta bouche (fais semblant), doux jusqu'au cœur. Pas assez doux ? Prends-en un autre — c'est gratuit de toute façon.","de":"Hier ist ein virtuelles Bonbon für dich — steck es in den Mund (tu so), süß bis zum Herzen. Nicht süß genug? Nimm noch eins — sie sind umsonst."},
]

def gen_blessings(n=1000):
    """生成 n 条四语祝福语：手写精品 + 多样化模板扩展，避免套路感"""
    pool = list(BLESSINGS)
    seen = set(b["zh"] for b in pool)

    # 生活化词汇库（四语对应）
    FOODS = [("一杯热茶","a cup of hot tea","une tasse de thé chaud","eine Tasse heißen Tee"),("刚出炉的面包","freshly baked bread","du pain frais sorti du four","frisch gebackenes Brot"),("加个煎蛋","a fried egg on top","un œuf frit sur le dessus","ein Spiegelei obendrauf"),("一碗热汤面","a bowl of hot noodle soup","un bol de soupe de nouilles chaude","eine Schüssel heiße Nudelsuppe"),("一块巧克力","a piece of chocolate","un morceau de chocolat","ein Stück Schokolade"),("一杯热牛奶","a glass of warm milk","un verre de lait chaud","ein Glas warme Milch"),("一颗糖","a candy","un bonbon","ein Bonbon"),("一个橘子","a tangerine","une mandarine","eine Mandarine"),("一口西瓜","a bite of watermelon","une bouchée de pastèque","ein Biss Wassermelone"),("一杯咖啡","a cup of coffee","une tasse de café","eine Tasse Kaffee"),("一碗白粥","a bowl of plain congee","un bol de riz blanc","eine Schüssel Reisschleim"),("一串葡萄","a bunch of grapes","une grappe de raisin","eine Weintraube"),("一个烤红薯","a roasted sweet potato","une patate douce rôtie","eine geröstete Süßkartoffel"),("一杯热可可","a cup of hot cocoa","une tasse de cacao chaud","eine Tasse heißen Kakao"),("一盘饺子","a plate of dumplings","une assiette de raviolis","ein Teller Dumplings"),("一口冰淇淋","a bite of ice cream","une bouchée de glace","ein Biss Eis"),("一碗蛋炒饭","a bowl of egg fried rice","un bol de riz sauté aux œufs","eine Schüssel Ei-Reis"),("一片吐司","a slice of toast","une tranche de pain grillé","eine Scheibe Toast"),("一杯蜂蜜水","a cup of honey water","une tasse d'eau au miel","eine Tasse Honigwasser"),("一块桂花糕","a piece of osmanthus cake","un morceau de gâteau à l'osmanthe","ein Stück Osmanthus-Kuchen"),("一锅炖菜","a pot of stew","un pot de ragoût","ein Topf Eintopf"),("一根玉米","a corn on the cob","un épi de maïs","ein Maiskolben"),("一碗馄饨","a bowl of wonton soup","un bol de wontons","eine Schüssel Wontons"),("一块曲奇","a cookie","un biscuit","ein Keks"),("一杯柠檬水","a cup of lemon water","une tasse d'eau citronnée","eine Tasse Zitronenwasser"),("一碗汤圆","a bowl of tangyuan","un bol de boulettes de riz glutineux","eine Schüssel Tangyuan"),("一块南瓜饼","a piece of pumpkin cake","un morceau de gâteau à la citrouille","ein Stück Kürbiskuchen"),("一杯姜茶","a cup of ginger tea","une tasse de thé au gingembre","eine Tasse Ingwertee"),("一个煮鸡蛋","a boiled egg","un œuf dur","ein gekochtes Ei"),("一碗拉面","a bowl of ramen","un bol de ramen","eine Schüssel Ramen"),("一块蛋糕","a piece of cake","un morceau de gâteau","ein Stück Kuchen"),("一杯奶茶","a cup of milk tea","une tasse de thé au lait","eine Tasse Milchtee"),("一个三明治","a sandwich","un sandwich","ein Sandwich"),("一碗粥","a bowl of congee","un bol de bouillie","eine Schüssel Brei"),("一块披萨","a slice of pizza","une part de pizza","ein Stück Pizza"),("一杯果汁","a glass of juice","un verre de jus","ein Glas Saft"),("一个饭团","a rice ball","une boulette de riz","ein Reisball"),("一块奶酪","a piece of cheese","un morceau de fromage","ein Stück Käse"),("一碗红豆沙","a bowl of red bean soup","un bol de soupe de haricots rouges","eine Schüssel rote-Bohnen-Suppe")]
    WEATHERS = [("午后的阳光","afternoon sunshine","le soleil de l'après-midi","die Nachmittagssonne"),("傍晚的微风","evening breeze","la brise du soir","die Abendbrise"),("清晨的露水","morning dew","la rosée du matin","der Morgentau"),("雨后的空气","air after rain","l'air après la pluie","die Luft nach dem Regen"),("雪落的声音","sound of falling snow","le bruit de la neige qui tombe","das Geräusch des fallenden Schnees"),("星空","starry sky","ciel étoilé","Sternenhimmel"),("晚霞","sunset glow","lueur du coucher","Abendröte"),("蓝天白云","blue sky with white clouds","ciel bleu avec des nuages blancs","blauer Himmel mit weißen Wolken"),("月光","moonlight","claire de lune","Mondlicht"),("彩虹","rainbow","arc-en-ciel","Regenbogen"),("初升的太阳","rising sun","soleil levant","gehende Sonne"),("秋天的凉风","cool autumn wind","vent frais d'automne","kühler Herbstwind"),("春天的细雨","gentle spring rain","pluie douce de printemps","sanfter Frühlingsregen"),("冬天的暖阳","warm winter sun","soleil chaud d'hiver","warme Wintersonne"),("夏天的树荫","shade of a summer tree","ombre d'un arbre d'été","Schatten eines Sommerbaums"),("清晨的薄雾","morning mist","brume matinale","Morgennebel"),("黄昏的霞光","twilight glow","lueur du crépuscule","Dämmerungslicht"),("雨后的彩虹","rainbow after rain","arc-en-ciel après la pluie","Regenbogen nach Regen"),("夏夜的萤火虫","fireflies on a summer night","lucioles par une nuit d'été","Glühwürmchen an einem Sommerabend"),("冬日的雪景","winter snow scene","paysage de neige d'hiver","Winter-Schneelandschaft"),("山间的云雾","mountain clouds and mist","nuages et brume en montagne","Bergwolken und -nebel"),("海边的浪花","ocean spray","embruns de l'océan","Meeresgischt"),("清晨的第一缕光","first light of dawn","première lumière de l'aube","erstes Licht des Morgens"),("傍晚的火烧云","sunset fire clouds","nuages enflammés du coucher","feurige Wolken bei Sonnenuntergang"),("雨后泥土的芬芳","fragrance of earth after rain","parfum de la terre après la pluie","Duft der Erde nach Regen"),("清晨的鸟鸣","morning birdsong","chant des oiseaux du matin","Vogelgesang am Morgen"),("傍晚的炊烟","evening cooking smoke","fumée de cuisine du soir","Abendrauch vom Kochen"),("山间的清风","mountain breeze","brise de montagne","Bergbrise"),("湖面的波光","sparkling lake light","lumière scintillante du lac","funkelnendes Seelicht"),("午后的雷阵雨","afternoon thunderstorm","orage d'après-midi","Nachmittagsgewitter"),("清晨的阳光","morning sunlight","lumière du soleil matinale","Morgensonne"),("傍晚的晚霞","evening sunset glow","lueur du coucher de soirée","Abendsonnenuntergang"),("冬夜的雪","snow on a winter night","neige par une nuit d'hiver","Schnee in einer Winternacht"),("春日的微风","gentle spring breeze","douce brise de printemps","sanfte Frühlingsbrise"),("夏夜的星空","starry sky on a summer night","ciel étoilé par une nuit d'été","Sternenhimmel in einer Sommernacht"),("秋天的落叶","fallen autumn leaves","feuilles mortes d'automne","Herbstlaub"),("清晨的薄雾","light morning mist","légère brume matinale","leichter Morgennebel"),("傍晚的凉风","cool evening breeze","brise fraîche du soir","kühle Abendbrise"),("山间的溪流声","sound of a mountain stream","bruit d'un ruisseau de montagne","Rauschen eines Bergbachs")]
    ACTIONS = [("深呼吸三次","take three deep breaths","prenez trois respirations profondes","atme dreimal tief durch"),("伸个大大的懒腰","stretch big","étirez-vous bien","streck dich richtig"),("抬头看看天","look up at the sky","levez les yeux au ciel","schau zum Himmel"),("给自己一个拥抱","give yourself a hug","faites-vous un câlin","umarm dich selbst"),("慢慢走五分钟","walk slowly for five minutes","marchez lentement pendant cinq minutes","geh fünf Minuten langsam"),("听一首喜欢的歌","listen to a favorite song","écoutez une chanson préférée","hör ein Lieblingslied"),("发会儿呆","zone out for a while","perdez-vous dans vos pensées","träum ein bisschen vor dich hin"),("照镜子笑一下","smile at yourself in the mirror","sourire à soi-même dans le miroir","lächle dich im Spiegel an"),("喝一大口水","drink a big sip of water","buvez une grande gorgée d'eau","trink einen großen Schluck Wasser"),("把肩膀放松","relax your shoulders","détendez vos épaules","entspann deine Schultern"),("闭上眼睛休息一分钟","close your eyes and rest for a minute","fermez les yeux et reposez-vous une minute","schließ die Augen und ruh eine Minute aus"),("到窗边站一会儿","stand by the window for a while","restez près de la fenêtre un moment","steh ein bisschen am Fenster"),("搓搓手取暖","rub your hands to warm them","frottez vos mains pour les réchauffer","reib die Hände, um sie zu wärmen"),("整理一下桌面","tidy up your desk","rangez votre bureau","räum deinen Schreibtisch auf"),("给自己泡杯喝的","make yourself a drink","préparez-vous une boisson","mach dir etwas zu trinken"),("活动一下脖子","move your neck","bougez votre cou","beweg deinen Nacken"),("看看窗外的树","look at the trees outside","regardez les arbres dehors","schau die Bäume draußen an"),("做几个简单的拉伸","do some simple stretches","faites quelques étirements simples","mach ein paar einfache Dehnübungen"),("把手机放下一会儿","put your phone down for a while","posez votre téléphone un moment","leg dein Handy eine Weile weg"),("闻一闻身边的香味","smell the fragrance around you","sentez le parfum autour de vous","riech den Duft um dich herum"),("给自己说句鼓励的话","say something encouraging to yourself","dites-vous quelque chose d'encourageant","sag dir selbst etwas Ermutigendes"),("把脚抬高歇会儿","prop your feet up and rest","relevez vos pieds et reposez-vous","leg die Füße hoch und ruh dich aus"),("数一下呼吸","count your breaths","comptez vos respirations","zähl deine Atemzüge"),("摸一下身边柔软的东西","touch something soft nearby","touchez quelque chose de mou près de vous","berühre etwas Weiches in deiner Nähe"),("给自己一个微笑","give yourself a smile","offrez-vous un sourire","schenk dir selbst ein Lächeln"),("拍拍自己的肩膀","pat yourself on the shoulder","tapez-vous sur l'épaule","klopf dir selbst auf die Schulter"),("换个舒服的姿势","change to a comfortable position","changez de position pour être confortable","wechsel in eine bequeme Position"),("喝一口温水","take a sip of warm water","prenez une gorgée d'eau chaude","nimm einen Schluck warmes Wasser"),("伸伸腿弯弯腰","stretch your legs and bend","étirez vos jambes et penchez-vous","streck die Beine und bück dich"),("打个哈欠","yawn","bailler","gähnen"),("伸个懒腰","stretch","s'étirer","strecken"),("喝口水","take a sip of water","boire une gorgée d'eau","einen Schluck Wasser trinken"),("看看窗外","look out the window","regarder par la fenêtre","aus dem Fenster schauen"),("深呼吸一下","take a deep breath","prendre une profonde respiration","tief durchatmen"),("笑一下","smile","sourire","lächeln"),("站起来走走","stand up and walk around","se lever et marcher","aufstehen und herumgehen"),("揉揉眼睛","rub your eyes","frotter vos yeux","sich die Augen reiben"),("活动一下手腕","rotate your wrists","faire tourner vos poignets","die Handgelenke drehen"),("听听音乐","listen to some music","écouter de la musique","Musik hören"),("眨眨眼睛","blink your eyes","clignez des yeux","blinzeln")]
    LITTLE_THINGS = [("路边开的小野花","a little wildflower by the road","une petite fleur sauvage au bord du chemin","eine kleine Wildblume am Wegrand"),("猫咪打盹的样子","a cat napping","un chat qui fait la sieste","eine Katze, die ein Nickerchen macht"),("刚晒过的被子味道","smell of freshly sunned blankets","odeur de couvertures fraîchement séchées au soleil","Geruch von frisch gelüfteten Decken"),("旧书的纸张味","smell of old book pages","odeur des pages d'un vieux livre","Geruch alter Buchseiten"),("冰块在杯子里响","ice clinking in a glass","glaçons qui tintent dans un verre","Eis, das in einem Glas klirrt"),("风吹树叶沙沙响","leaves rustling in the wind","feuilles qui bruissent dans le vent","Blätter, die im Wind rascheln"),("锅里咕嘟咕嘟的汤","soup bubbling in a pot","soupe qui frémit dans une casserole","Suppe, die in einem Topf blubbert"),("袜子刚烘干的暖","warmth of freshly dried socks","chaleur des chaussettes fraîchement séchées","Wärme von frisch getrockneten Socken"),("拆快递的期待","excitement of opening a package","excitation d'ouvrir un colis","Vorfreude beim Auspacken eines Pakets"),("踩到落叶的脆响","crunch of stepping on fallen leaves","craquement de feuilles mortes sous le pas","Knacken von Laub unter den Schuhen"),("小狗摇尾巴","a puppy wagging its tail","un chiot qui remue la queue","ein Welpe, der mit dem Schwanz wedelt"),("清晨的第一声鸟叫","first bird song of the morning","premier chant d'oiseau du matin","erster Vogelgesang am Morgen"),("玻璃杯折射的光","light refracted through a glass","lumière réfractée à travers un verre","Licht, das durch ein Glas gebrochen wird"),("刚削好的铅笔","a freshly sharpened pencil","un crayon fraîchement taillé","ein frisch gespitzter Bleistift"),("洗衣机刚停的安静","quiet when the washer just stops","calme quand la machine à laver s'arrête","Stille, wenn die Waschmaschine gerade stoppt"),("热气腾腾的食物","steaming hot food","nourriture fumante","dampfendes heißes Essen"),("风吹动窗帘","wind moving the curtains","vent qui fait bouger les rideaux","Wind, der die Vorhänge bewegt"),("刚打印出来的纸味","smell of freshly printed paper","odeur du papier fraîchement imprimé","Geruch von frisch gedrucktem Papier"),("猫咪踩奶的样子","a cat kneading with its paws","un chat qui pétrit avec ses pattes","eine Katze, die mit den Pfoten tritt"),("雨滴打在窗户上","raindrops hitting the window","gouttes de pluie sur la fenêtre","Regentropfen, die gegen das Fenster schlagen"),("书页翻动的声音","sound of turning pages","bruit des pages qui se tournent","Geräusch von blätternden Seiten"),("刚切开的水果香","aroma of freshly cut fruit","arôme de fruit fraîchement coupé","Aroma von frisch geschnittenem Obst"),("路灯亮起来的瞬间","moment streetlights turn on","moment où les lampadaires s'allument","Moment, in dem die Straßenlichter angehen"),("被窝里的温暖","warmth under the covers","chaleur sous les couvertures","Wärme unter der Decke"),("远处传来的钟声","distant bell sound","son de cloche lointain","ferner Glockenklang"),("阳光照在桌面上","sunlight on the desk","lumière du soleil sur le bureau","Sonnenlicht auf dem Schreibtisch"),("刚洗好的衣服香","smell of freshly washed clothes","odeur du linge fraîchement lavé","Geruch von frisch gewaschener Wäsche"),("杯子里的气泡","bubbles in a cup","bulles dans un verre","Bläschen in einem Glas"),("风吹起头发","wind blowing hair","vent qui fait voler les cheveux","Wind, der die Haare weht"),("猫咪伸懒腰","a cat stretching","un chat qui s'étire","eine Katze, die sich streckt"),("阳光照在地板上","sunlight on the floor","lumière du soleil sur le sol","Sonnenlicht auf dem Boden"),("杯子里的冰块","ice cubes in a cup","glaçons dans un verre","Eiswürfel in einem Glas"),("风吹动树叶","wind moving leaves","vent qui fait bouger les feuilles","Wind, der Blätter bewegt"),("刚洗好的床单","freshly washed sheets","draps fraîchement lavés","frisch gewaschene Bettwäsche"),("远处的狗叫","distant dog barking","aboiement de chien lointain","fernes Hundegebell"),("锅里的热气","steam from a pot","vapeur d'une casserole","Dampf aus einem Topf"),("书页的沙沙声","rustling of pages","bruissement des pages","Rascheln von Seiten"),("路灯的光晕","halo of a streetlight","halo d'un lampadaire","Lichthof einer Straßenlaterne"),("雨后的水洼","puddle after rain","flaque après la pluie","Pfütze nach Regen"),("猫咪打呼噜的声音","sound of a cat purring","bruit d'un chat qui ronronne","Geräusch einer schnurrenden Katze")]

    # 多样化句式模板（四语对应，变量 {f}=食物 {w}=天气 {a}=动作 {l}=小确幸 {n}=数字）
    TPLS = [
        {"zh":"今天记得{a}，哪怕只有一分钟也好。日子是自己的，对自己好一点不亏。","en":"Remember to {a} today, even if just for a minute. It's your life — being kind to yourself never hurts.","fr":"Pense à {a} aujourd'hui, même si ce n'est qu'une minute. C'est ta vie — être gentil avec toi-même, ça ne fait jamais de mal.","de":"Vergiss nicht, heute zu {a}, auch wenn es nur eine Minute ist. Es ist dein Leben — gut zu dir selbst zu sein, schadet nie.","vars":["a"]},
        {"zh":"送你{w}，不用还，因为好东西就是要分享的。如果你那边没有，就想象一下，想象力免费。","en":"Here's {w} for you, no need to give it back — good things are meant to be shared. If you don't have it there, just imagine it, imagination's free.","fr":"Voici {w} pour toi, pas besoin de le rendre — les bonnes choses sont faites pour être partagées. Si tu ne l'as pas là où tu es, imagine-le, l'imagination est gratuite.","de":"Hier ist {w} für dich, du musst es nicht zurückgeben — gute Dinge sind zum Teilen da. Wenn du es dort nicht hast, stell es dir einfach vor, Vorstellungskraft ist umsonst.","vars":["w"]},
        {"zh":"如果今天有点累，那就给自己泡{f}。累了就歇，不丢人，真的。","en":"If you're a bit tired today, make yourself {f}. Resting when you're tired is nothing to be ashamed of, really.","fr":"Si tu es un peu fatigué aujourd'hui, prépare-toi {f}. Se reposer quand on est fatigué, ce n'est pas honteux, vraiment.","de":"Wenn du heute ein bisschen müde bist, mach dir {f}. Auszuruhen, wenn man müde ist, ist nichts, wofür man sich schämen müsste, wirklich.","vars":["f"]},
        {"zh":"听说经常注意到{l}的人，幸福感会比别人高那么一点点。今天试试？","en":"They say folks who often notice {l} are just a little happier than everyone else. Wanna try today?","fr":"On dit que les gens qui remarquent souvent {l} sont un peu plus heureux que les autres. Tu veux essayer aujourd'hui ?","de":"Man sagt, Leute, die oft {l} bemerken, sind ein bisschen glücklicher als andere. Willst du es heute versuchen?","vars":["l"]},
        {"zh":"你知道吗？{w}其实是天空在给你发消息，内容是：今天也要好好的哦。","en":"You know what? {w} is actually the sky sending you a message — it says: take care of yourself today too.","fr":"Tu sais quoi ? {w} est en fait le ciel qui t'envoie un message — il dit : prends soin de toi aujourd'hui aussi.","de":"Weißt du was? {w} ist eigentlich der Himmel, der dir eine Nachricht schickt — er sagt: Pass auch heute gut auf dich auf.","vars":["w"]},
        {"zh":"别老盯着手机看，偶尔{a}，你会发现世界比屏幕里有意思多了。","en":"Stop staring at your phone — {a} once in a while, and you'll find the world's way more interesting than what's on screen.","fr":"Arrête de fixer ton téléphone — {a} de temps en temps, et tu trouveras le monde bien plus intéressant que ce qui est sur l'écran.","de":"Hör auf, auf dein Handy zu starren — {a} ab und zu, dann wirst du merken, dass die Welt viel interessanter ist als das, was auf dem Bildschirm ist.","vars":["a"]},
        {"zh":"今天的快乐可以很简单：{f}，{a}，然后继续往前走。就够了。","en":"Today's happiness can be simple: {f}, {a}, then keep going. That's all it takes.","fr":"Le bonheur d'aujourd'hui peut être simple : {f}, {a}, puis continuer d'avancer. C'est tout ce qu'il faut.","de":"Das Glück heute kann einfach sein: {f}, {a}, dann weitergehen. Mehr braucht es nicht.","vars":["f","a"]},
        {"zh":"把烦心事想象成{l}，看一会儿就过去了。没什么大不了的，真的。","en":"Imagine whatever's bugging you as {l} — watch it for a bit and it passes. No big deal, really.","fr":"Imagine ce qui t'embête comme {l} — regarde-le un instant et ça passe. Ce n'est pas grave, vraiment.","de":"Stell dir vor, was dich ärgert, als {l} — schau es kurz an und es geht vorbei. Keine große Sache, wirklich.","vars":["l"]},
        {"zh":"你今天的任务只有三个：吃好、睡好、{a}。做不到两个就先做一个，不丢人。","en":"You've only got three tasks today: eat well, sleep well, and {a}. Can't do two? Just do one — nothing to be ashamed of.","fr":"Tu n'as que trois tâches aujourd'hui : bien manger, bien dormir, et {a}. Tu n'y arrives pas pour deux ? Fais-en juste une — ce n'est pas honteux.","de":"Du hast heute nur drei Aufgaben: gut essen, gut schlafen und {a}. Schaffst du keine zwei? Dann mach nur eine — nichts, wofür man sich schämen müsste.","vars":["a"]},
        {"zh":"你比昨天的自己又好了一点点，虽然你可能没发现。但{l}发现了，它偷偷告诉你的。","en":"You're a little better than yesterday's you, even though you might not have noticed. But {l} noticed — it told you in secret.","fr":"Tu es un peu meilleur que ton moi d'hier, même si tu ne l'as peut-être pas remarqué. Mais {l} l'a remarqué — il te l'a dit en secret.","de":"Du bist ein bisschen besser als dein gestriges Ich, auch wenn du es vielleicht nicht bemerkt hast. Aber {l} hat es bemerkt — es hat es dir heimlich gesagt.","vars":["l"]},
        {"zh":"如果快乐太难，那我祝你今天能吃到{f}。能吃到好吃的，日子就还过得去。","en":"If happiness feels out of reach, then I hope you get to eat {f} today. If you can eat something good, life's still bearable.","fr":"Si le bonheur semble hors de portée, alors j'espère que tu pourras manger {f} aujourd'hui. Si tu peux manger quelque chose de bon, la vie est encore supportable.","de":"Wenn Glück unerreichbar scheint, dann hoffe ich, dass du heute {f} essen kannst. Wenn du etwas Gutes essen kannst, ist das Leben noch erträglich.","vars":["f"]},
        {"zh":"{w}这么好的天气，不开心一下都对不起它。来，嘴角往上翘一翘，就一下。","en":"With weather this nice — {w} — not being happy would be a waste. Come on, turn up the corners of your mouth — just a little.","fr":"Avec un temps aussi beau — {w} — ne pas être heureux serait du gâchis. Allez, remonte les coins de ta bouche — juste un peu.","de":"Bei so schönem Wetter — {w} — wäre es Verschwendung, nicht glücklich zu sein. Komm schon, zieh die Mundwinkel hoch — nur ein bisschen.","vars":["w"]},
        {"zh":"今天也要记得，你不是一个人在战斗。虽然我只是个机器人，但我站你这边。","en":"Remember today too that you're not fighting alone. I'm just a robot, but I'm on your side.","fr":"Rappelle-toi aussi aujourd'hui que tu ne combats pas seul. Je ne suis qu'un robot, mais je suis de ton côté.","de":"Denk auch heute daran, dass du nicht allein kämpfst. Ich bin nur ein Roboter, aber ich stehe auf deiner Seite.","vars":[]},
        {"zh":"生活有时候像{f}，刚入口有点苦，但咽下去之后会有回甘。别急，慢慢品。","en":"Life's sometimes like {f} — a bit bitter at first, but a sweet aftertaste follows. Don't rush, savor it slowly.","fr":"La vie est parfois comme {f} — un peu amer au début, mais une douceur persistante suit. Ne te précipite pas, savoure lentement.","de":"Das Leben ist manchmal wie {f} — am Anfang ein bisschen bitter, aber danach kommt ein süßer Nachgeschmack. Überstürz nichts, genieß es langsam.","vars":["f"]},
        {"zh":"你有没有过这种感觉？就是注意到{l}的时候，突然觉得活着还挺好的。今天也去找找这种感觉吧。","en":"Ever had that feeling? When you notice {l}, you suddenly think life's pretty great. Go find that feeling today too.","fr":"Tu as déjà eu ce sentiment ? Quand tu remarques {l}, tu penses soudain que la vie est plutôt géniale. Va trouver ce sentiment aujourd'hui aussi.","de":"Hast du schon mal dieses Gefühl gehabt? Wenn du {l} bemerkst, denkst du plötzlich, dass das Leben ziemlich schön ist. Geh heute auch dieses Gefühl suchen.","vars":["l"]},
        {"zh":"累了就{a}，没人给你颁奖状的。自己舒服最重要，其他都是次要的。","en":"When you're tired, just {a} — no one's handing out medals for pushing through. Your own comfort matters most, everything else can wait.","fr":"Quand tu es fatigué, contente-toi de {a} — personne ne te donne de médaille pour tenir le coup. Ton propre confort compte le plus, tout le reste peut attendre.","de":"Wenn du müde bist, einfach {a} — niemand verteilt Medaillen dafür, durchzuhalten. Dein eigenes Wohl ist am wichtigsten, alles andere kann warten.","vars":["a"]},
        {"zh":"今天的风里有{f}的味道，如果你那边没有，就当我偷偷给你寄过去了。","en":"Today's wind smells like {f}. If you don't have it where you are, just assume I secretly mailed it to you.","fr":"Le vent d'aujourd'hui sent {f}. Si tu ne l'as pas là où tu es, suppose que je te l'ai secrètement envoyé.","de":"Der Wind heute riecht nach {f}. Wenn du ihn dort nicht hast, nimm einfach an, ich habe ihn dir heimlich geschickt.","vars":["f"]},
        {"zh":"你笑起来的样子比{w}还好看，所以今天多笑笑，就当是为了美化环境。","en":"Your smile's nicer than {w}, so smile more today — call it doing your part for the environment.","fr":"Ton sourire est plus beau que {w}, alors souris plus aujourd'hui — appelle ça ta contribution à l'environnement.","de":"Dein Lächeln ist schöner als {w}, also lächle heute mehr — nenn es deinen Beitrag zur Umwelt.","vars":["w"]},
        {"zh":"把今天过成以后会怀念的样子吧。不用多精彩，{a}的时候认真一点，就够了。","en":"Make today the kind of day you'll look back on fondly. Doesn't have to be grand — just be a little more present when you {a}, that's enough.","fr":"Fais de aujourd'hui le genre de journée dont tu te souviendras avec tendresse. Pas besoin que ce soit grandiose — sois juste un peu plus présent quand tu {a}, c'est suffisant.","de":"Mach heute zu der Art Tag, an den du dich später gerne erinnerst. Muss nicht großartig sein — sei einfach ein bisschen präsenter, wenn du {a}, das reicht.","vars":["a"]},
        {"zh":"听说今天的幸运物是{l}，看到了就说明今天运气不错。没看到也没关系，运气这东西随缘。","en":"Heard today's lucky charm is {l} — if you spot it, you're in luck today. If not, no worries, luck comes and goes as it pleases.","fr":"On dit que le porte-bonheur d'aujourd'hui est {l} — si tu le vois, tu as de la chance aujourd'hui. Sinon, pas de souci, la chance va et vient comme elle veut.","de":"Hört sich an, als wäre das Glückssymbol heute {l} — wenn du es siehst, hast du heute Glück. Wenn nicht, kein Problem, Glück kommt und geht, wie es will.","vars":["l"]},
        {"zh":"今天遇到的第一个{l}，就是今天的小幸运。没遇到也别急，可能在路上。","en":"The first {l} you come across today is your little lucky charm. If you don't see one, don't worry — it might still be on its way.","fr":"Le premier {l} que tu rencontres aujourd'hui est ton petit porte-bonheur. Si tu n'en vois pas, ne t'inquiète pas — il est peut-être en chemin.","de":"Das erste {l}, dem du heute begegnest, ist dein kleines Glückssymbol. Wenn du keines siehst, mach dir keine Sorgen — es ist vielleicht noch unterwegs.","vars":["l"]},
        {"zh":"你已经很棒了，真的。虽然可能没人跟你说，但{a}的时候你就该知道。","en":"You're already doing great, really. Nobody might have told you, but you should know it when you {a}.","fr":"Tu fais déjà du bien, vraiment. Personne ne te l'a peut-être dit, mais tu devrais le savoir quand tu {a}.","de":"Du machst das schon gut, wirklich. Vielleicht hat es dir niemand gesagt, aber du solltest es wissen, wenn du {a}.","vars":["a"]},
        {"zh":"如果今天什么都不想做，那就什么都不做。天不会塌下来，{f}会凉，但可以再热。","en":"If you don't feel like doing anything today, then don't. The sky won't fall — {f} might get cold, but you can always heat it up again.","fr":"Si tu n'as pas envie de rien faire aujourd'hui, alors ne fais rien. Le ciel ne s'effondrera pas — {f} pourrait refroidir, mais tu peux toujours le réchauffer.","de":"Wenn du heute keine Lust hast, etwas zu tun, dann tu nichts. Der Himmel wird nicht einstürzen — {f} könnte kalt werden, aber du kannst es immer wieder aufwärmen.","vars":["f"]},
        {"zh":"送你一句废话：今天也要好好吃饭。虽然是废话，但很多人做不到。","en":"Here's a piece of obvious advice: eat well today too. It's obvious, but so many people can't manage it.","fr":"Voici un conseil évident : mange bien aujourd'hui aussi. C'est évident, mais tellement de gens n'y arrivent pas.","de":"Hier ein offensichtlicher Rat: Iss auch heute gut. Es ist offensichtlich, aber so viele Menschen schaffen es nicht.","vars":[]},
        {"zh":"你知道吗？{w}的时候，世界是静音的。你也是。","en":"You know what? When there's {w}, the whole world goes on mute. You too.","fr":"Tu sais quoi ? Quand il y a {w}, le monde entier se met en sourdine. Toi aussi.","de":"Weißt du was? Wenn es {w} gibt, geht die ganze Welt auf stumm. Du auch.","vars":["w"]},
        {"zh":"别跟自己较劲了，{a}一下，又不会少块肉。","en":"Stop being so hard on yourself — just {a}, it's not like it'll kill you.","fr":"Arrête d'être si dur avec toi-même — contente-toi de {a}, ce n'est pas comme si ça allait te tuer.","de":"Hör auf, so hart zu dir selbst zu sein — einfach {a}, es ist nicht so, als würde es dich umbringen.","vars":["a"]},
        {"zh":"今天的关键词是：{f}。不是因为多特别，就是想吃。","en":"Today's keyword is: {f}. Not because it's anything special — I just feel like it.","fr":"Le mot-clé d'aujourd'hui est : {f}. Pas parce que c'est quelque chose de spécial — j'en ai juste envie.","de":"Das Schlagwort heute ist: {f}. Nicht weil es etwas Besonderes ist — ich habe einfach Lust darauf.","vars":["f"]},
        {"zh":"如果快乐有形状，那大概就是{l}的样子。","en":"If happiness had a shape, it'd probably look like {l}.","fr":"Si le bonheur avait une forme, il ressemblerait probablement à {l}.","de":"Wenn Glück eine Form hätte, würde es wahrscheinlich wie {l} aussehen.","vars":["l"]},
        {"zh":"你今天做得已经够多了。剩下的交给明天，明天的你也不差。","en":"You've done enough today. Leave the rest for tomorrow — tomorrow's you is pretty capable too.","fr":"Tu as assez fait aujourd'hui. Laisse le reste pour demain — le toi de demain est plutôt capable aussi.","de":"Du hast heute genug getan. Überlass den Rest morgen — das du von morgen ist auch ziemlich fähig.","vars":[]},
        {"zh":"{w}这么好，不出去走走可惜了。不想出去也没关系，窗边站着也行。","en":"With {w} this nice, it'd be a shame not to go out. Don't feel like it? Standing by the window works too.","fr":"Avec un {w} aussi beau, ce serait dommage de ne pas sortir. Pas envie ? Rester près de la fenêtre, ça marche aussi.","de":"Bei so schönem {w} wäre es schade, nicht rauszugehen. Keine Lust? Am Fenster stehen funktioniert auch.","vars":["w"]},
    ]

    def pick(lst, idx): return lst[idx % len(lst)]

    def fill(tpl, indices):
        vals = {}
        for var in tpl["vars"]:
            vt = var
            idx = indices.get(vt, 0)
            if vt == "f": vals[var] = pick(FOODS, idx)
            elif vt == "w": vals[var] = pick(WEATHERS, idx)
            elif vt == "a": vals[var] = pick(ACTIONS, idx)
            elif vt == "l": vals[var] = pick(LITTLE_THINGS, idx)
        r = {}
        for lk, li in [("zh",0),("en",1),("fr",2),("de",3)]:
            t = tpl[lk]
            for var in tpl["vars"]:
                t = t.replace("{"+var+"}", vals[var][li])
            r[lk] = t
        return r

    # 生成模板祝福，直到凑够 n 条
    attempts = 0
    while len(pool) < n and attempts < n * 100:
        attempts += 1
        tpl = random.choice(TPLS)
        indices = {v: random.randint(0, 99) for v in tpl["vars"]}
        r = fill(tpl, indices)
        if len(r["zh"].replace(" ", "")) <= 30:
            continue
        if r["zh"] in seen:
            continue
        seen.add(r["zh"])
        pool.append(r)

    random.shuffle(pool)
    return pool[:n]

# ===================== HTML 邮件模板（宋体 + Times New Roman）=====================
def build_html(b):
    today = datetime.now().strftime("%Y年%m月%d日")
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style type="text/css">
  @keyframes dinoWalk {{
    0%   {{ transform: translateX(0) scaleX(1); }}
    45%  {{ transform: translateX(-260px) scaleX(1); }}
    50%  {{ transform: translateX(-260px) scaleX(-1); }}
    95%  {{ transform: translateX(0) scaleX(-1); }}
    100% {{ transform: translateX(0) scaleX(1); }}
  }}
  @keyframes dinoBob {{
    0%, 100% {{ transform: translateY(0); }}
    50%      {{ transform: translateY(-4px); }}
  }}
  @keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
  @keyframes pulseBg {{
    0%, 100% {{ background-position: 0% 50%; }}
    50%      {{ background-position: 100% 50%; }}
  }}
  .dino-walk {{
    display: inline-block;
    animation: dinoWalk 9s ease-in-out infinite, dinoBob 0.7s ease-in-out infinite;
    font-size: 28px;
  }}
  .fade-in {{
    animation: fadeInUp 0.8s ease-out both;
  }}
  .pulse-bg {{
    background: linear-gradient(135deg, rgba(26,42,108,0.12), rgba(45,74,138,0.10), rgba(74,111,165,0.12), rgba(135,168,201,0.10));
    background-size: 400% 400%;
    animation: pulseBg 20s ease infinite;
  }}
  /* ===== 响应式适配 ===== */
  @media only screen and (max-width: 480px) {{
    .outer-wrap {{ padding: 20px 10px !important; }}
    .main-card {{ padding: 24px 18px 20px 18px !important; border-radius: 16px !important; }}
    .blessing-box {{ padding: 18px 16px !important; border-radius: 12px !important; }}
    .date-text {{ font-size: 17px !important; }}
    .intro-text {{ font-size: 17px !important; line-height: 1.8 !important; }}
    .zh-text {{ font-size: 18px !important; line-height: 1.8 !important; }}
    .foreign-text {{ font-size: 16px !important; line-height: 1.7 !important; }}
    .dino-walk {{ font-size: 24px !important; }}
    .dino-track {{ height: 34px !important; }}
  }}
  @media only screen and (min-width: 481px) and (max-width: 768px) {{
    .outer-wrap {{ padding: 28px 14px !important; }}
    .main-card {{ padding: 30px 24px 26px 24px !important; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .dino-walk, .fade-in, .pulse-bg {{ animation: none !important; }}
  }}
</style>
</head>
<body class="pulse-bg" style="margin:0;padding:0;font-family:'Times New Roman','SimSun','宋体',serif;min-height:100vh;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
<div class="outer-wrap" style="max-width:560px;margin:0 auto;padding:35px 16px;">
  
  <div class="main-card" style="background:rgba(255,255,255,0.88);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-radius:20px;padding:36px 32px 30px 32px;box-shadow:0 6px 30px rgba(26,42,108,0.10);">
    
    <!-- 顶部蓝色装饰线 -->
    <div style="height:3px;border-radius:2px;background:linear-gradient(90deg,transparent,#2d4a8a,#4a6fa5,transparent);margin:-8px 0 24px 0;"></div>
    
    <!-- 小恐龙走动区域 -->
    <div class="dino-track" style="background:linear-gradient(90deg,rgba(45,74,138,0.06),rgba(74,111,165,0.08),rgba(45,74,138,0.06));border-radius:12px;height:40px;overflow:hidden;margin-bottom:20px;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;">
      <span class="dino-walk">🦕</span>
    </div>
    
    <!-- 日期 -->
    <p class="date-text fade-in" style="font-size:20px;color:#5a6f8a;margin:0 0 20px 0;letter-spacing:2px;text-align:center;">{today}</p>
    
    <!-- 开场白 -->
    <p class="intro-text fade-in" style="font-size:19px;line-height:1.85;color:#3a4a5e;margin:0 0 22px 0;text-indent:2em;">你好啊，我是 Dino，一个小机器人，来自中国的赣北地区。新的一天，愿你有更多的惊喜和欢欣。</p>
    
    <!-- 简洁分隔线 -->
    <div style="height:1px;background:linear-gradient(90deg,transparent,#c5d5e8,transparent);margin:0 0 22px 0;"></div>
    
    <!-- 祝福区 -->
    <div class="blessing-box" style="background:rgba(245,248,252,0.7);border-radius:14px;padding:24px 22px;">
      <p class="zh-text fade-in" style="font-size:21px;line-height:1.85;color:#1e2f44;margin:0 0 14px 0;text-indent:2em;">{b['zh']}</p>
      <p class="foreign-text fade-in" style="font-size:22px;line-height:1.75;color:#5a6f8a;margin:0 0 12px 0;text-indent:2em;">{b['en']}</p>
      <p class="foreign-text fade-in" style="font-size:22px;line-height:1.75;color:#5a6f8a;margin:0 0 12px 0;text-indent:2em;">{b['fr']}</p>
      <p class="foreign-text fade-in" style="font-size:22px;line-height:1.75;color:#5a6f8a;margin:0;text-indent:2em;">{b['de']}</p>
    </div>
    
    <!-- 落款 -->
    <p style="font-size:15px;color:#8a9bb0;margin:20px 0 0 0;text-align:center;">— Dino</p>
    
  </div>
  
</div>
</body>
</html>"""


# ===================== .ics 日历卡片 =====================
def build_ics(b):
    now = datetime.now(timezone.utc)
    ds = now.strftime("%Y%m%dT%H%M%SZ")
    d = now.strftime("%Y%m%d")
    uid = str(uuid.uuid4()) + "@dino-bot"
    desc = f"ZH: {b['zh']}\\nEN: {b['en']}\\nFR: {b['fr']}\\nDE: {b['de']}"
    return f"BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Dino Bot//Blessing Card//EN\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nBEGIN:VEVENT\nDTSTART;VALUE=DATE:{d}\nDTEND;VALUE=DATE:{d}\nDTSTAMP:{ds}\nUID:{uid}\nSUMMARY:🦕 Dino 的每日祝福\nDESCRIPTION:{desc}\nLOCATION:中国赣北\nSTATUS:CONFIRMED\nTRANSP:TRANSPARENT\nBEGIN:VALARM\nTRIGGER:-PT0M\nACTION:DISPLAY\nDESCRIPTION:Dino 的祝福来啦！\nEND:VALARM\nEND:VEVENT\nEND:VCALENDAR"

# ===================== Maton API =====================
def api_call(method, path, payload=None, api_key=None, retries=3):
    url = MATON_BASE + path
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload else None
    for attempt in range(1, retries+1):
        try:
            req = urllib.request.Request(url, data=data, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8","ignore")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8","ignore")
        except Exception as e:
            if attempt < retries: time.sleep(attempt*2)
            else: return 0, str(e)
    return 0, "max retries"

def send_mail(to, subject, html_body, api_key):
    payload = {"message":{"subject":subject,"body":{"contentType":"Html","content":html_body},"toRecipients":[{"emailAddress":{"address":to}}]},"saveToSentItems":True}
    return api_call("POST", "/me/sendMail", payload, api_key)

def get_sent_recipients(api_key, top=100):
    """查询已发送文件夹中最近的 Dino 祝福邮件，返回已成功送达的收件人地址集合（小写）"""
    path = f"/me/mailFolders/SentItems/messages?$top={top}&$select=subject,toRecipients,receivedDateTime"
    code, body = api_call("GET", path, None, api_key)
    if code != 200:
        print(f"  [查询已发送] API 返回 {code}，跳过本轮状态检查")
        return None
    try:
        data = json.loads(body)
        recipients = set()
        for msg in data.get("value", []):
            subj = msg.get("subject", "")
            if "Dino" in subj and "祝福" in subj:
                for r in msg.get("toRecipients", []):
                    addr = r.get("emailAddress", {}).get("address", "").lower().strip()
                    if addr:
                        recipients.add(addr)
        return recipients
    except Exception as e:
        print(f"  [查询已发送] 解析失败: {e}")
        return None

def load_recipients():
    """从 recipients.txt 读取收件人列表，每行一个邮箱"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recipients.txt")
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and "@" in line]

RECIPIENTS = load_recipients()
SUBJECT = "🦕 Dino 的每日祝福"

def main():
    parser = argparse.ArgumentParser(description="Dino 四语祝福群发机器人 v2")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--retries", type=int, default=3, help="最大重试轮数（默认3）")
    parser.add_argument("--retry-delay", type=int, default=45, help="每轮重试前等待秒数，用于查询已发送状态（默认45）")
    args = parser.parse_args()
    api_key = os.environ.get("MATON_API_KEY")
    if not api_key: print("Error: set MATON_API_KEY"); sys.exit(1)
    if args.check:
        code, body = api_call("GET", "/me", None, api_key)
        print(f"Status: {code}")
        if code == 200:
            d = json.loads(body)
            print(f"Account: {d.get('mail', d.get('userPrincipalName','?'))}")
            print(f"Name: {d.get('displayName','?')}")
        else: print(body)
        return
    blessings = gen_blessings(args.count)
    print(f"Blessing pool: {len(blessings)} (handwritten: {len(BLESSINGS)})")
    if args.preview:
        b = random.choice(blessings)
        with open("/tmp/dino_preview.html","w",encoding="utf-8") as f: f.write(build_html(b))
        with open("/tmp/dino_preview.ics","w",encoding="utf-8") as f: f.write(build_ics(b))
        print(f"Preview: /tmp/dino_preview.html")
        print(f"ZH: {b['zh'][:60]}...")
        return
    if args.send:
        recipients = RECIPIENTS
        print(f"\nSubject: {SUBJECT}")
        print(f"Recipients: {len(recipients)}")
        print(f"Max retries: {args.retries}, retry delay: {args.retry_delay}s\n")

        pending = list(recipients)      # 待发送列表
        confirmed_sent = set()           # 已确认在已发送文件夹中的地址（小写）

        for round_num in range(args.retries + 1):
            if not pending:
                break

            # 从第2轮开始：先等待，再查询已发送状态，剔除已送达的
            if round_num > 0:
                print(f"\n--- 第 {round_num} 轮重试前检查：等待 {args.retry_delay}s 后查询已发送邮件 ---")
                time.sleep(args.retry_delay)
                sent_set = get_sent_recipients(api_key)
                if sent_set is not None:
                    newly_confirmed = [r for r in pending if r.lower() in sent_set]
                    pending = [r for r in pending if r.lower() not in sent_set]
                    confirmed_sent.update(r.lower() for r in newly_confirmed)
                    print(f"  已确认送达: {len(newly_confirmed)} 封，剩余待重发: {len(pending)} 封")
                    if not pending:
                        break
                else:
                    print(f"  已发送状态查询失败，本轮按 API 返回结果重试")

            round_label = f"第 {round_num+1} 轮" if round_num > 0 else "首轮"
            print(f"\n=== {round_label}发送：{len(pending)} 封 ===")

            chosen = random.sample(blessings, min(len(pending), len(blessings)))
            round_fail = []

            for i, (addr, bls) in enumerate(zip(pending, chosen), 1):
                print(f"[{i}/{len(pending)}] {addr} ...", end=" ", flush=True)
                code, body = send_mail(addr, SUBJECT, build_html(bls), api_key)
                if code in (200, 202):
                    print("✓ 已提交")
                else:
                    print(f"✗ 失败 ({code})")
                    if body:
                        print(f"    {body[:200]}")
                    round_fail.append(addr)
                # 节流：每封间隔 2 秒，每 10 封多休 10 秒
                if i % 10 == 0 and i < len(pending):
                    print(f"  --- 已发 {i} 封，休息 10 秒 ---", flush=True)
                    time.sleep(10)
                if i < len(pending):
                    time.sleep(2)

            # 下一轮只重发 API 层面就失败的
            pending = round_fail

        # 最终确认：再等一轮，查询已发送状态
        print(f"\n--- 最终确认：等待 {args.retry_delay}s 后查询已发送邮件 ---")
        time.sleep(args.retry_delay)
        sent_set = get_sent_recipients(api_key)
        if sent_set is not None:
            confirmed_sent.update(r.lower() for r in recipients if r.lower() in sent_set)

        final_success = [r for r in recipients if r.lower() in confirmed_sent]
        final_failed = [r for r in recipients if r.lower() not in confirmed_sent]

        print(f"\n{'='*50}")
        print(f"最终结果：{len(final_success)} 成功送达，{len(final_failed)} 失败")
        if final_failed:
            print("失败列表：")
            for r in final_failed:
                print(f"  - {r}")
        print(f"{'='*50}")
        return
    parser.print_help()

if __name__ == "__main__":
    main()
