import string
import csv
import os


# ---------------------------------------------------------------------
#   Method
# ---------------------------------------------------------------------


def prt_more(func):
    """
    デコレーター  - メッセージの装飾
    :param func:
    :return:
    """

    def wrapper1(*arg, **kwargs):
        print('=========================')
        result = func(*arg, **kwargs)  # 引数として受け取ったメソッドを処理する
        print('=========================')

    def wrapper2(*arg, **kwargs):
        print('#########################')
        result = func(*arg, **kwargs)  # 引数として受け取ったメソッドを処理する
        print('#########################')

    return wrapper1


@prt_more
def make_message(msg: str):
    """
    メッセージの作成
    ① 先に@を付けたメソッドを開始する -> オブジェクト（メソッドと引数）を渡す [func]
    :param msg:
    :return:
    """
    print(msg)


def create_csv_list(path):
    """
    CSVの読み込み
    :param path: CSVのファイルパス
    :return: CSVのデータ(辞書)
    """
    with open('memory.csv', newline='') as f:
        reader = csv.reader(f)
        dict = {x: y for x, y in reader}
    return dict


def str_trim(str):
    str = str.strip(' ')
    str = str.strip('　')
    return str

# ---------------------------------------------------------------------
#   Main
# ---------------------------------------------------------------------
csv_dict = {}
sorted_csv = []

try:
    # メモリ
    path = 'memory.csv'

    # ファイルチェック
    if os.path.exists(path):

        # CSVの読み込み
        csv_dict = create_csv_list(path)

        # 降順ソート
        sorted_csv = sorted(csv_dict.items(), key=lambda x: -int(x[1]))

except csv.Error:
    make_message('CSV_FormatError')
    exit()

# ▼ 質問１ ----------------------------------
make_message('こんにちはRoboterです! あなたのお名前は？')

name = ''
while len(name) <= 0:
    name = input()

    # 隠しコマンド
    if name == '_000':
        print('_000', csv_dict)
        name = ''

# ▼ 質問２ ----------------------------------
msg = 'こんにちは! {}!\n'.format(name)

# CSVデータを出力
order = 0
for restaurant in sorted_csv:

    # 同着の有無を確認
    if order > int(restaurant[1]):
        break

    # ラインキング１位を薦める
    msg += 'オススメのレストランは{}です。\n'.format(restaurant[0])
    msg += '{}は好きですか？ [Yes/No]'.format(restaurant[0])
    make_message(msg)

    # 入力待ち
    update_csv = False
    while True:
        answer = input()
        if str(answer).capitalize() == 'Yes':
            msg = ''
            update_csv = True
            break
        elif str(answer).capitalize() == 'No':
            msg = '次に'
            order = int(restaurant[1])
            break
        else:
            make_message('Yes/Noでお答え下さいね！')

    # 更新処理
    if update_csv:
        order = int(restaurant[1]) + 1
        csv_dict[restaurant[0]] = order
        break

# ▼ 質問３
msg += 'オススメのレストランを教えてください！'
make_message(msg)

# 入力待ち
while True:
    recommend = input()
    recommend = str_trim(recommend)

    # 隠しコマンド
    if recommend == '_001':
        print('_001', csv_dict)
        recommend = ''
        continue

    if len(recommend) > 0:
        msg = 'ありがとう！「{}」だね!'.format(recommend)
        break
    else:
        make_message('1文字以上入力して下さい！')

# データの更新
if recommend in csv_dict:
    cnt = csv_dict[recommend]
    csv_dict[recommend] = int(cnt) + 1
else:
    csv_dict.setdefault(recommend, 1)

# ファイルへの書き込み
with open('memory.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for k, v in csv_dict.items():
        row = [k, v]
        writer.writerow(row)

# おしまい
msg += '\nではでは、よい一日を！'
make_message(msg)
