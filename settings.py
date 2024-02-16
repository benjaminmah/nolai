from utils import threshold_calculator

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RECTANGLE_COLOR = (40, 40, 40)
HIGHLIGHT_COLOR = (240, 240, 240)
BACKGROUND_HIGHLIGHT_COLOR = (123, 52, 46)  
BAR_COLOR = (245, 123, 158)  
NOTE_COLOR = (245, 123, 158)  
RECTANGLE_WIDTH = 80
RECTANGLE_HEIGHT = 40
RECTANGLE_GAP = 20
RECTANGLE_Y = SCREEN_HEIGHT - RECTANGLE_HEIGHT - 50
PRESSED_OFFSET = 5  # Offset to simulate the button being pressed
SPEED = 800  # Adjust this value as needed
CUSTOM_FONT = "assets/outerlimits.ttf"
JAPANESE_FONT = "assets/noto.ttf"
KOREAN_FONT = "assets/notokorean.ttf"

# lyrics
ima_lyrics = [
    (29, "たったひとつを守りたいんだ"),
    (34, "少し上がった唇 その笑顔を"),
    (40, "平凡な日々集め 大人へと 大変だけど後悔はない"),
    (50, "今日を経て明日に巡り会う喜び この想い全部が美しい"),
    (62, "もしも世界最後の夜が来たら 僕は君のために何ができる?"),
    (73, "君に last dance まぶしすぎるその笑顔を"),
    (81, "守れるなら もしできるなら"),
    (85, "僕ら last dance and last chance 今夜 世界が終わっても"),
    (92, "大事にしたいのは 僕らの「今」"),
    (97, ""),
    (120, "今日を経て明日に巡り会う喜び この想い全部が美しい"),
    (131, "もしも世界最後の夜が来たら 僕は君のために何ができる?"),
    (142, "君に last dance まぶしすぎるその笑顔を"),
    (149, "守れるなら もしできるなら"),
    (154, "僕ら last dance and last chance 今夜 世界が終わっても"),
    (160, "大事にしたいのは 僕らの「今」"),
    (167, ""),
    (177, "世界最後の夜が来たら"),
    (183, "大事にしたいのは 僕らの「今」"),
]
allergy_lyrics = [
    (3, "얼굴 없는 feed 파리 날리는 followers"),
    (8, "I'm a hater of Instagram Hater of TikTok"),
    (13, "Lock 걸린 gallery"),
    (15, "볼품없는 fit 뭔데 운동도 안 하고"),
    (19, "메이크업 하나도 못하고 그래 난 내가 봐도 별로인걸"),
    (26, "매일 밤 in 탐색 tab 나만 없는 Chanel 왠지 나보다 성숙한 요즘 십대"),
    (32, "MZ 해시태그 what the Y2K 세상은 나 빼고 잘 돌아가"),
    (39, "Please give me the hate button 난 내가 너무 싫거든 (거든) Alright (alright), yeah"),
    (47, "Oh my, oh my 빌어먹을 my name"),
    (50, "Why ain't I pretty? why ain't I lovely? Why ain't I sexy? why am I me?"),
    (56, "Love me, love me, love me, love me, love me, want Love me, love me, love me, love me, love me, want"),
    (61, "She's so pretty, yeah, so lovely Shе got everything, why am I not her?"),
    (67, "Lovе me, love me, love me, love me, love me but 빌어먹을 huh 내 거울 알러지"),
    (76, "나도 want to dance \"Hype Boy\" But 화면 속엔 like \"TOMBOY\""),
    (81, "비웃을 거야 그래 그 boy, oh"),
    (87, "Oh, God, it's so funny 말투는 왜 too much dope?"),
    (90, "내가 뭔데 성격까지 좋지 않어 그래 맞아, 나는 평생 혼자일지도"),
    (100, "Please give me your like button 나도 사랑받고 싶거든 (거든) Alright (alright), yeah"),
    (108, "Oh my, oh my 빌어먹을 my name"),
    (111, "Why ain't I pretty? Why ain't I lovely? Why ain't I sexy? Why am I me?"),
    (116, "Love me, love me, love me, love me, love me, want Love me, love me, love me, love me, love me, want"),
    (122, "She's so pretty, yeah, so lovely She got everything, why am I not her?"),
    (127, "Love me, love me, love me, love me, love me but 빌어먹을 huh 내 거울 알러지"),
    (134, "La-la-la-la-la, la-la-la, la-la-la La-la-la-la-la, la-la-la, la"),
    (145, "La-la-la-la-la, la-la-la, la-la-la La-la-la-la-la, la-la-la, la"),
    (156, "빌어먹을 huh 내 거울 알러지"),
]



# SONGS dictionary with paths and grade thresholds
songs = {
    "allergy": ["assets/allergy/allergy.mp3", "assets/allergy/gidle.jpg", "assets/allergy/allergy.txt", threshold_calculator("assets/allergy/allergy.txt"), allergy_lyrics, KOREAN_FONT],
    "ima": ["assets/ima/ima.mp3", "assets/ima/ima.jpg", "assets/ima/ima.txt", threshold_calculator("assets/ima/ima.txt"), ima_lyrics, JAPANESE_FONT],
    "afterlike": ["assets/afterlike/afterlike.mp3", "assets/afterlike/afterlike.png", "assets/afterlike/afterlike.txt", threshold_calculator("assets/afterlike/afterlike.txt"), ima_lyrics, KOREAN_FONT],
    "girlscapitalism": ["assets/girlscapitalism/girlscapitalism.mp3", "assets/girlscapitalism/girlscapitalism.jpg", "assets/girlscapitalism/girlscapitalism.txt", threshold_calculator("assets/girlscapitalism/girlscapitalism.txt"), [(0, "")], KOREAN_FONT],
    "fate": ["assets/fate/fate.mp3", "assets/fate/fate.jpg", "assets/fate/fate.txt", threshold_calculator("assets/fate/fate.txt"), [(0, "")], KOREAN_FONT]
    }

