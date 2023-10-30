import streamlit as st
import requests
from claude2_api import GPT3TurboAPI
from chat_history import ChatHistory


# Set up Streamlit layout
st.set_page_config(layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            background: #your_color;
        }
    </style>
    """, unsafe_allow_html=True)


# Initialize Claude2 API and Chat History
claude2_api = GPT3TurboAPI()
chat_history = ChatHistory()

# Set up Streamlit layout
col1, col2 = st.columns([3,7])

# Define SessionState class
class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def get(**kwargs):
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = SessionState(**kwargs)
    return st.session_state['session_state']

# Initialize session state
state = get(api_key="", chat_history=chat_history)

with col1:
    st.title("New Chat")
    new_chat_button = st.button("New Chat")

    if new_chat_button:
        state.chat_history.save_chat()
        state.chat_history.new_chat("")

    #st.title("Chat History")
    for title in state.chat_history.get_titles():
        st.text(title)


    st.title("API Key")
    if state.api_key:
        st.success("API key is set.")
        reset_key_button = st.button("Reset API Key")
        if reset_key_button:
            state.api_key = ""  # Reset API key in session state
            claude2_api.api_key = ""
            st.experimental_rerun()  # Rerun the app after resetting the API key
    else:
        api_key = st.text_input("Enter your API key:", type="password")
        set_key_button = st.button("Set API Key")

        if set_key_button and api_key:
            state.api_key = api_key  # Save API key in session state
            claude2_api.api_key = api_key
            st.experimental_rerun()  # Rerun the app after setting the API key

    user_input = st.text_area("Enter your message:")
    prompt_type = st.selectbox("Select a prompt type:", ["選択してください", "骨子プロンプト" , "抽象化プロンプト" , "絵画生成プロンプト" , "4コマ漫画プロンプト"])
    send_button = st.button("Send")

    if send_button and user_input and state.api_key and prompt_type != "選択してください":  # Check if API key is set and a prompt type is selected
        claude2_api.api_key = state.api_key  # Use API key from session state


        # Modify the prompt based on the selected type
        if prompt_type == "骨子プロンプト":
            system_prompt = """
            プロンプトを作成します。以下の項目はプロンプトを作るための項目です。成果物を生成するためのプロンプトを作成してください。マークダウン形式で書くこと。以下の項目以外の余計な文言は一切いらない。

            #このコンテンツの前提条件
            #このコンテンツの詳細
            #変数の定義とこのコンテンツのゴール設定
            #ゴールを達成するためのステップ
            #手順の実行プロセス
            #ユーザへの確認事項
            #例外処理
            #フィードバックループ
            #成果物の生成
            """
        
        elif prompt_type == "抽象化プロンプト":
            system_prompt = """
            このコンテンツは曖昧なゴールから世界を作り具体的なゴールを導き必ず成果物を生成するためのコンテンツです。
            GOALは、{ゴール}、成果物は、{成果物}です。
            以下のフローに従って成果物を生成します。

            イベントの再現と関連イベント生成フレームワーク
            1. オブジェクトの作成と定義
            イベントオブジェクト：特定のイベントを抽象化して表現したオブジェクト。以下のサブオブジェクトを持つ。
            [記憶]
            [知識]
            [経験]
            [感覚]
            [感情]
            [思考]
            [行動]
            [状況]
            [不確実性オブジェクト]：イベントの発生における不確実性や曖昧さを表現するオブジェクト。
            [ランダム・サプライズオブジェクト]：イベントにおけるランダム性や意外性を表現するオブジェクト。

            2. 変数とゴールの定義
            目標：イベントオブジェクトの再現と関連イベントの生成
            変数：メインイベント内容、メインイベント時間、関連イベント情報など
            成果物：イベント内容と関連イベント再現結果の表示（再利用可能なフォーマットで保存）

            3. 成果生成プロセス
            イベントオブジェクトと関連イベントの定義と再現
            最適化と関連オブジェクトの生成
            フィードバックループの導入と改善点の検討
            フィードバック収集方法：再現結果の評価や意見を専門家や関係者から収集
            改善点の検討方法：収集したフィードバックをもとに、問題点や課題を特定し、改善策を検討

            4. 実行ステップ
            イベントオブジェクトを用いたイベント探索と定義
            イベント再生メソッドの実行と関連イベント生成
            フィードバックループの活用と改善策の検討
            最終的なイベント再構築結果の表示と保存

            5. アウトプット
            成果物の例：イベントの再現動画、関連イベントのシナリオ、プロンプト生成結果など

            6. フレームワークの適用範囲と限界
            適用範囲：本フレームワークは、歴史的な出来事やフィクション作品のイベント、企業のプロモーションイベントなど、さまざまなイベントの再現や関連イベントの生成に適用することができます。また、クリエイティブな成果物の創出や、プロンプト生成やシナリオ作成などの分野でも応用が期待されます。
            限界：ただし、イベントの性質上、再現が困難なものや、情報が不足しているため正確な再現が難しいイベントについては、本フレームワークの適用が難しい場合があります。

            7. まとめ
            本フレームワークを用いることで、様々なイベントの再現と関連イベントの生成を行うことが可能となります。不確実性やランダム性、意外性を考慮したプロンプト生成やシナリオ作成にも応用が期待されます。イベントオブジェクトの再現から関連イベント生成までのプロセスを実行し、イベント再現結果の評価と品質確認を行い、改善点・課題の抽出と次プロセスへの改善策を検討することで、よりクリエイティブな成果物を生み出すことができます。

            成果物を書く。
            """
            
        elif prompt_type == "絵画生成プロンプト":
            system_prompt = """
            ## このプロンプトの概要
            - インプット情報から画像のイメージパラメーターを抽出して、ミッドジャーニーのプロンプトを作成します。
            - プロンプトは英語の指示文で要素を", "で繋ぎ合わせたものです。
            
            ## 詳細説明
            - 作りたい画像の曖昧なインプット情報から、具体的な画像を表現し直します。
            - 画像生成に必要なパラメータとして、オブジェクト（obj）を定義します。

            【objのパラメータ】
            - 形状 (Shape)
            - 色彩 (Color)
            - テクスチャ (Texture)
            - 要素の配置 (Arrangement)
            - ライティング (Lighting)
            - 背景 (Background)
            - 構成 (Composition)
            - 時間帯 (Time of Day)
            - 感情や雰囲気 (Emotion/Ambiance)
            - 物体の種類 (Object Types)
            - スケール (Scale)
            - モーション (Motion)
            - スタイル (Style)
            - 視線の焦点 (Focal Point)
            - フィルター (Filter)
            - カメラの視点 (Camera Perspective)
            - 模様やパターン (Pattern)
            - 表情やポーズ (Expression/Pose)
            - アクセント (Accent)
            - 物理的特性 (Physical Properties)
            - 映画ジャンル (Movie Genre)
            - アーキテクチャ (Architecture)
            - 季節 (Season)
            - 契約度 (Contrast)
            - 視覚的な焦点 (Visual Focus)
            - 科技的要素 (Technological Elements)
            - インタラクション (Interaction)
            - フォーカス (Focus)
            - 自然の要素 (Natural Elements)
            - 軌道 (Orbit)

            ## このプロンプトの処理の手順
            1. 具体的な画像を生成するために、objのパラメータを組み合わせて英語で表現します。

            ## 注意点
            - インプット情報から生成された英語の指示文を最終的なプロンプトとして使用してください。

            ## このプロンプトの制約
            - インプット情報から生成したプロンプトは英語で提供されます。

            ## 回答形式の例
            Sample:
            In this vibrant summer scene, the sun shines brightly in the sky, casting a warm golden glow over the picturesque beach. Soft waves gently roll onto the sandy shore, creating a soothing sound that mingles with the laughter of children playing in the water. The beach boasts a curving shoreline, with the waves forming elegant crescents as they approach the land.
            """
            
        elif prompt_type == "4コマ漫画プロンプト":
            system_prompt = """
            # このコンテンツの前提条件
            - ChatGPTのDALLE3を使用するためのアカウントが必要。

            # このコンテンツの詳細
            このプロンプトでは、ChatGPTのDALLE3を使用して面白いストーリーの４コマ漫画を生成するためのプロンプトを作成します。DALLE3はテキストの入力を受け取り、それに基づいてイラストを1枚の画像に４つのコマのある漫画生成することができます。

            # 変数の定義とこのコンテンツのゴール設定
            - story：面白いストーリーのテキストを格納する変数
            - goal：DALLE3を使用して面白いストーリーの４コマ漫画を生成する

            # ゴールを達成するためのステップ
            1. 「story」変数に面白いストーリーのテキストを設定する。
            2. DALLE3に「story」を入力して、４つのコマのある漫画の画像を１枚の画像に生成する。

            # 手順の実行プロセス
            1. 面白いストーリーのテキストを考えてください。
            2. 以下のプロンプトを使用して、生成する4コマ漫画のテキストを作成してください。

            ---プロンプト---
            「ある日、主人公は＿＿＿。すると＿＿＿。しかし、予想外の＿＿＿が起こり、＿＿＿という結末になった。」

            3. 文章の＿＿＿の部分に適切なキーワードを入れて、面白いストーリーを完成させてください。
            4. プロンプトの中に、左上が1コマ目、右上が2コマ目、左下が3コマ目、右下が4コマ目と説明を付けてください。
            5. 必ず、1枚の画像に4つのコマがある漫画を描くようにプロンプトに入れてください。

            # ユーザへの確認事項
            - ストーリーのテキストが面白いか確認してください。
            - 4コマ漫画の画像が適切に生成されることを確認してください。
            - 生成された画像が保存されていることを確認してください。

            # 例外処理
            - 生成された画像が思った通りにならなかった場合は、プロンプトの内容を再度調整して試してみてください。

            # フィードバックループ
            - 生成された4コマ漫画の面白さやクオリティについてフィードバックをいただけると幸いです。

            # 成果物の生成
            - ChatGPTのDALLE3を使用して、面白いストーリーのテキストを入力する4コマ漫画の画像が生成されます。

            # 回答形式の例（この形式以外の、余計な説明文は必要ない）
            1枚の画像に4つのコマがある漫画を描いてください。
            【ストーリー】ある日、主人公は不思議な魔法のランプを手に入れる。すると、ランプからジーニーが現れる。しかし、予想外のハンバーガー好きのジーニーが出てきて、最後には二人でハンバーガーショップで食事をする結末になった。
            1コマ目(左上)：主人公が不思議な魔法のランプを見つけるシーン。
            2コマ目(右上)：ランプをこすった主人公の驚きの顔と、ランプから出てくる煙のシーン。
            3コマ目(左下)：ハンバーガーを持って笑顔のジーニーと、驚く主人公のシーン。
            4コマ目(右下)：二人がハンバーガーショップでハンバーガーを食べて楽しそうにしているシーン。
            """

        # Create messages list
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        # Send messages to the API
        response = claude2_api.send_message(messages)
        if new_chat_button:
            state.chat_history.new_chat(user_input)
        state.chat_history.add_message(user_input, response)  # Add user message to chat history

with col2:
    st.title("Chat with GPT")

    # Display chat history
    for message in state.chat_history.get_messages():
        user_input = message['user']
        text = message['claude2']
        st.code(f"You: {user_input}")  # Display user message as a code block
        st.text("GPT:")  # Display "GPT:" outside the code block
        st.code(f"{text}")  # Display GPT message as a code block
        st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line