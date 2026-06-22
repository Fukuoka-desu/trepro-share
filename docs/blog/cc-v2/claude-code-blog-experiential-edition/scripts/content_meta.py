from __future__ import annotations

CHARACTERS = [
    {
        "name": "遥（はるか）",
        "role": "営業企画・非エンジニア",
        "description": "Cursorで既存のスライド生成Skillは使えるものの、内部で何が起きているかを0から理解し直したい学習者。",
    },
    {
        "name": "蓮（れん）",
        "role": "アプリケーション開発者",
        "description": "速く作ることより、再現性・テスト・Git・レビューを重視する実装担当。",
    },
    {
        "name": "美咲（みさき）",
        "role": "AI推進・情シス",
        "description": "個人の成功を全社員へ安全に配布し、更新・監査・ロールバックまで運用する管理者。",
    },
    {
        "name": "ナビゲーター",
        "role": "対話型学習アシスタント",
        "description": "答えだけを渡さず、次の一操作、確認すべき証拠、保存地点を示しながら伴走する。",
    },
]

PART_META = {
    0: {
        "title": "最適な教科書の設計",
        "story": "遥はすでに便利なSkillを使っていました。それでも、うまくいかなかった瞬間に直せないことが不安でした。そこで四人は、知識を並べた資料ではなく、操作・証拠・保存・再開まで含む『実行できる教科書』を作ることにします。",
        "image_concept": "A workshop where pages from a technical book unfold into interactive tools, checkpoints, a terminal, and a learning path, with four Japanese office workers collaborating",
        "usecase": {
            "situation": "ABC商事の社内勉強会で、AIツール本を回し読みしても誰も再現できない状況が続いている。",
            "action": "本ではなく、章ごとに前提・成果物・検証を持つLesson単位の実行教科書として再設計する。",
            "benefit": "読んだ／使った／検証したの段階で進捗が記録でき、勉強会後も全員が同じLevelへ到達できる。",
        },
    },
    1: {
        "title": "Claude Codeの全体像と最初の成果物",
        "story": "最初の目標は、難しい機能を暗記することではありません。会議の文字起こしを、議事録・タスク・HTMLへ変える小さな成果物を完成させます。『動いた』という体験が、その後の学習を現実のものに変えます。",
        "image_concept": "A beginner-friendly desk scene where a meeting transcript flows into notes, tasks, and a clean web dashboard, warm editorial technology illustration",
        "usecase": {
            "situation": "XYZ工業の総務チームは、毎週の議事録作成に2時間かかり、タスク漏れで翌週まで動けない。",
            "action": "Claude Codeのフォルダへ文字起こしを置き、議事録・タスク・HTMLレポートの三点セットを作るLessonを一周する。",
            "benefit": "1回の体験で『動かす・確かめる・再利用する』感覚が掴め、次の会議から再現可能な業務型として使える。",
        },
    },
    2: {
        "title": "標準作業ループ",
        "story": "一度だけ成功する指示と、何度でも再現できる仕事の型は別物です。四人は、探索から保存までを七つの段階に分け、どんな案件でも同じ順序で進められる共通言語を作ります。",
        "image_concept": "A circular seven-stage workflow on a studio floor, people moving from exploration to planning, implementation, verification, review, and commit",
        "usecase": {
            "situation": "ある製造業の社内開発チームは、担当者によって作業順序がバラバラで、レビューや戻し作業に時間を奪われている。",
            "action": "Explore→Plan→Implement→Verify→Review→Commitの七段階を共通言語にし、依頼の単位を統一する。",
            "benefit": "順序が揃うことで抜けや手戻りが減り、新人でも先輩と同じ手順で安全に進められる。",
        },
    },
    3: {
        "title": "Claude Codeを育てる拡張レイヤー",
        "story": "会話で得たコツを、その会話の中だけに置いておくと、翌日にはまた同じ説明が必要です。ここからは、知識をCLAUDE.md、Rules、Skills、Subagents、Hooksへ昇格させ、個人の工夫を仕組みに変えていきます。",
        "image_concept": "Layered transparent cards representing project guidance, rules, skills, specialist agents, and automated quality gates around an AI workspace",
        "usecase": {
            "situation": "個人で成果を出している人事の田中さん（架空）が、同じ説明を毎週新人へ繰り返し、本人の時間が削られている。",
            "action": "成功した会話をCLAUDE.md・Rules・Skillへ昇格させ、誰でも同じ手順で呼べる業務パッケージへ変える。",
            "benefit": "属人化した工夫が組織の資産になり、説明の繰り返しから解放されて改善側に時間を回せる。",
        },
    },
    4: {
        "title": "外部連携と伝わる成果物",
        "story": "仕事はパソコンの中だけでは終わりません。カレンダー、メール、Drive、社内データ、デザイン、公開先へつながります。同時に、正しいだけで読まれない成果物を、理解されるHTMLへ変える必要があります。",
        "image_concept": "Secure bridges connecting a local AI workspace to calendar, mail, cloud documents, design tools, and a polished HTML report",
        "usecase": {
            "situation": "ある広告会社の運用チームは、Drive上のレポートをそのまま送って『長すぎて読まれない』とクライアントから言われ続けている。",
            "action": "Driveとの安全な接続を設計しつつ、長文を1ページHTMLレポートへ翻訳するSkillを作る。",
            "benefit": "情報量を落とさず読解時間が半分になり、レビュー打ち返しが減って意思決定が速くなる。",
        },
    },
    5: {
        "title": "パーソナライズと自律化",
        "story": "便利な自動化ほど、止まる条件と学び方が重要です。四人は、対話履歴から関心を抽出し、明確なゴールだけを自律実行させ、必要なときに人間へ戻す設計を学びます。",
        "image_concept": "A personal knowledge garden connected to a carefully bounded automation loop with visible stop conditions and human checkpoints",
        "usecase": {
            "situation": "ある情シスのリーダーは、毎朝のニュース要約とTask Boardを手動で作っており、属人的で休めない状態が続く。",
            "action": "成功条件・最大回数・Timeout・承認地点を持つ自律実行を設計し、副作用は人間承認を残す。",
            "benefit": "毎朝の繰り返し作業が安全に自動化され、休んでも崩れず、品質が落ちた瞬間だけ人へ戻る運用になる。",
        },
    },
    6: {
        "title": "トレプロハーネスの全社実装",
        "story": "遥のMacだけで成功しても、会社の仕組みにはなりません。美咲は、同じSkillと安全策を全社員へ届け、更新失敗や誤配布が起きても戻せる配布基盤を設計します。",
        "image_concept": "An enterprise control room distributing a consistent AI coding environment to many Mac laptops with canary rings, monitoring, and rollback",
        "usecase": {
            "situation": "ある中堅企業（架空）では、AIに強い社員のSkillが個人Macだけに留まり、他部署へ広がらず会社の力にならない。",
            "action": "正本・配布・強制・個人差分を分離した配布基盤を作り、Canary→Pilot→Stableで段階展開する。",
            "benefit": "個人の成功が事故なく全社へ届き、誤配布もRollbackで戻せるため、攻めと守りを両立できる。",
        },
    },
    7: {
        "title": "実務ユースケース集",
        "story": "原則を理解したら、仕事へ戻します。請求書、会議、調査、学習、アプリ、資料、定期業務を題材に、どのレイヤーを組み合わせればよいかを実戦形式で確かめます。",
        "image_concept": "A montage of practical office workflows: invoices, meeting notes, research, a local app, an HTML report, and scheduled automation",
        "usecase": {
            "situation": "ある総務担当（架空）は、請求書整理・会議メモ・調査・週報を毎日手作業で回し、定型業務に1日の半分を奪われている。",
            "action": "業務ごとにRead-only棚卸し→Dry-run→可逆処理→Skillという同じ型を適用する。",
            "benefit": "業務種類が違っても同じ流れで処理でき、新しい業務も学習コストを抑えて自動化候補へ載せられる。",
        },
    },
    8: {
        "title": "テンプレートとアプリ化",
        "story": "最後に、学びを配れる形へ固定します。コピーできるテンプレート、構造化されたLesson、進捗データ、Feature Registryを組み合わせ、教科書そのものを対話型アプリへ育てます。",
        "image_concept": "A modular learning product made from templates, lesson cards, progress states, code samples, and a browser-based navigator",
        "usecase": {
            "situation": "教育担当の佐藤さん（架空）は、研修資料を毎回ゼロから作り直し、受講者の進捗を Excel で追えなくなっている。",
            "action": "Lesson JSON・進捗State・Feature Registryを持つ教材アプリへ変換し、章番号で再開できるようにする。",
            "benefit": "資料が再利用可能な学習プロダクトへ変わり、受講者の現在地と証拠が見える形で運用できる。",
        },
    },
}

CHAPTER_META = {
    "00": {
        "intro_human": """『AI研修、受けたのに、自席で再現できない』。
これ、ほとんどの人が一度は通る挫折ポイントです。
便利なツールには触れた。でも、自分の仕事に持ち帰れない。

ほとんどの教科書は『知識』を渡してきます。
この章で作るのは、知識じゃなく『進める単位』です。
読んだ／使った／検証した、を1ステップに圧縮した『実行できる教科書』（Lesson）。役割を非エンジニア・開発者・管理者の3つに分け、最初に作るゴールと合格証拠を1行で決めます。

この章を読み終わる頃には、『何を作れば自分は今日進んだと言えるか』が一行で言えるようになります。""",
        "features": [
            {
                "name": "3つの学習ルート",
                "summary": "非エンジニア・開発者・管理者で必要な順序を分け、自分はどこから始めるかを最初に決めるための分岐設計。",
                "input": "自分の役割、いま抱えている業務、AI使用経験の有無",
                "output": "自分が辿るべき章順、最初に作る成果物、合格証拠の定義",
            },
            {
                "name": "Lessonの標準形",
                "summary": "教科書を読み物ではなく実行単位に変える共通フォーマット。前提・成果物・検証・版情報をひと塊で扱う。",
                "input": "学びたい知識・操作・運用ルール",
                "output": "実行・検証・保存できる1Lessonへ分解された手順",
            },
            {
                "name": "進捗の4段階モデル",
                "summary": "seen/practiced/verified/applied の4段階で『読んだ』を『再現できた』へ昇格させる進捗管理。",
                "input": "Lesson実施結果、生成された成果物、検証ログ",
                "output": "本人と運用側で見える現在地と未到達Lessonの一覧",
            },
        ],
        "scene": "月曜日の朝、遥はスライド生成Skillを呼び出し、見栄えのよい資料を作りました。ところが、途中で処理が止まると、どのファイルを見ればよいのか分かりませんでした。『使える』と『理解している』の間にある距離が、この教科書の出発点です。",
        "essay": "ナビゲーターは、最初に章を読むようには言いませんでした。代わりに、誰が、何を作り、どの証拠で完成と判断するのかを決めようと提案します。教科書を実行システムにするとは、説明をLessonへ分解し、前提・成果物・検証・版情報を持たせることです。\n\n非エンジニア、開発者、管理者では必要な順序が違います。ただし全員に共通するのは、見たことではなく、再現できたことを進捗にする点です。",
        "mission": "自分が非エンジニア、開発者、管理者のどのルートから始めるかを決め、最初に作る成果物と合格証拠を一行で書いてください。",
        "takeaway": "教科書の単位はページではなく、実行・検証・保存できるLessonです。",
        "image_concept": "A technical book transforming into an interactive workshop with lesson cards, checkpoints, and executable tools",
        "image_kind": "editorial concept illustration",
        "usecases": [
            {
                "situation": "ABC商事の新人エンジニア（架空）が、社内AI研修テキストを最後まで読んだのに、自席で同じ手順を再現できず止まっている。",
                "action": "テキストを章ごとのLessonへ分解し、各章で『何を作り、どの証拠で完成と判断するか』を一行で書かせる。",
                "benefit": "読書ではなく実行が単位になり、本人が次の一操作を自分で決められるようになる。",
            },
            {
                "situation": "教育担当の田中さん（架空）が、研修動画を見せても受講者が独自に応用できず、毎回個別指導に時間が消えている。",
                "action": "動画ではなくLesson単位のテキスト＋成果物テンプレートを配り、進捗をseen/practiced/verified/appliedで管理する。",
                "benefit": "個別指導の量が減り、受講者は自分のペースで進めて、講師は詰まった人だけを救援できる。",
            },
            {
                "situation": "情シス担当（架空）が、AIガイドラインをWiki化したが、誰も読まずに同じ事故が繰り返し発生する。",
                "action": "ガイドラインを実行可能なLessonと体験ミッションに書き換え、ミッション達成を読了の証拠にする。",
                "benefit": "『読んだ』のあいまいさが消え、ミッション結果という証拠で運用状況を可視化できる。",
            },
        ],
    },
    "01": {
        "intro_human": """『この資料、まとめて』とAIに頼んで、文章だけ返ってきて止まる。
これ、AIの限界じゃありません。使ってる入口を間違えてるだけです。

ほとんどの人は、AIを『チャット画面で会話する相手』だと思ってます。
でも実は、目的を渡すとフォルダを読み・ファイルを作り・コマンドを実行し・結果を確かめるところまで、自分で走る入口（Claude Code）があります。

この章では、相談・業務処理・実装・情報設計という4つの入口を整理して、いまの仕事をどこで始めてどこへ渡すかを決めます。
読み終わる頃には、AIに渡す『仕事の単位』が10倍くっきり見えるようになります。""",
        "features": [
            {
                "name": "エージェント型Claude Code",
                "summary": "目的を渡すとフォルダ探索・ファイル編集・コマンド実行・検証まで自走するAIコーディング基盤の全体像。",
                "input": "目的、対象フォルダ、許可してよい操作の範囲",
                "output": "生成・編集されたファイル、実行ログ、検証結果",
            },
            {
                "name": "Chat / Cowork / Code / Design",
                "summary": "用途別の入口を相談・業務処理・実装・情報設計に分けて、ひとつの仕事を無理なく前へ進める使い分け。",
                "input": "目下の作業、必要な成果物、関わるツールの選択肢",
                "output": "どの入口で始め、どこへ渡すかの設計マップ",
            },
            {
                "name": "AIコーディング3世代モデル",
                "summary": "コピペ時代→エディタ補完時代→エージェント時代という変遷を理解し、人間の役割を再定義する視座。",
                "input": "現在使っているAIの形式、自分が任せたいタスク",
                "output": "次に投資すべき層（目的設計か、権限設計か、品質設計か）",
            },
        ],
        "scene": "遥が『この資料をまとめて』と頼むと、チャットAIは文章を返しました。Claude Codeへ同じ目的を渡すと、フォルダを読み、ファイルを作り、コマンドを実行し、結果を確かめ始めます。画面の向こうにいるのは、回答者ではなく作業者でした。",
        "essay": "AIコーディングは、コードを受け取って人が実行する時代から、編集環境の横で補完する時代を経て、目的を渡すと探索から検証まで進める時代へ移りました。そこで人間の役割も、タイピングから目的・権限・品質の設計へ変わります。\n\nChat、Cowork、Code、Designは競合する入口ではありません。相談、業務処理、実装、情報設計を分担させることで、ひとつの仕事を無理なく前へ進められます。",
        "mission": "いま抱えている仕事を一つ選び、Chat・Cowork・Code・Designのどこで始め、どこへ渡すかを書き分けてください。",
        "takeaway": "Claude Codeの価値はコード生成ではなく、探索・編集・実行・検証を同じ場所で回せることにあります。",
        "image_concept": "Three generations of AI work: copy-paste chat, AI editor assistance, and a full autonomous agent loop in one coherent scene",
        "image_kind": "editorial timeline illustration",
        "usecases": [
            {
                "situation": "XYZ広告のプランナー（架空）が、チャットAIに『議事録まとめて』と頼み、毎回手元のWordへコピペして整形に1時間かけている。",
                "action": "Claude Codeに目的とフォルダを渡し、議事録ファイルとタスクJSONを同じ場所で生成・確認まで一気に走らせる。",
                "benefit": "コピペ往復が消え、成果物がフォルダに残る。次回からは同じ手順で5分の作業になる。",
            },
            {
                "situation": "個人開発者の佐々木さん（架空）が、複数ファイルにまたがる修正をチャットAIで進めるたび、貼り付け漏れで動かなくなる。",
                "action": "Claude Codeに編集権限とプロジェクトを渡し、探索→修正→テスト実行までを同じセッションで完結させる。",
                "benefit": "ファイルの一貫性が保たれ、貼り付け事故と再質問のループから抜けられる。",
            },
        ],
    },
    "02": {
        "intro_human": """『rm -rf』をAIにうっかり打たせて、心臓が止まる。
『大丈夫だろう』で本番フォルダを触らせて、戻し方が分からない。
こういう事故は、油断した10秒に起きます。

ほとんどの人は、安全を『気をつけよう』というメモで済ませてます。
でも、メモは読まれません。本当に止めたい操作は、最小権限・隔離・履歴・検証・監査の5要素で物理的に止めるのが正解です。
便利な『お願い』（Guidance）と、確実に止める『強制』（Enforcement）の境界を、最初に決めます。

設定は5分。一度作った学習用フォルダの3禁（削除しない／外部公開しない／秘密情報を貼らない）が、その後ずっと自分を守ってくれます。""",
        "features": [
            {
                "name": "安全の基本式（最小権限・隔離・履歴）",
                "summary": "最小権限・隔離・戻せる履歴・検証・監査の5要素を重ね、失敗しても被害を限定する安全設計の土台。",
                "input": "扱うデータ、許可したい操作、起きうる失敗",
                "output": "5要素ごとに何で守るかをマッピングした安全表",
            },
            {
                "name": "Guidance と Enforcement の分離",
                "summary": "CLAUDE.mdのお願いと、Permissions/Sandbox/Hooksによる物理強制を区別し、本当に止めたい操作を強制する考え方。",
                "input": "守らせたいルール、お願いで済むか強制が必要かの判断",
                "output": "Guidance層とEnforcement層に振り分けたルール一覧",
            },
            {
                "name": "学習用フォルダの3禁",
                "summary": "削除しない・外部公開しない・秘密情報を貼らないの3点を最初に決め、実データから物理的に切り離す入門用境界。",
                "input": "実験したい内容、本番データへの距離",
                "output": "学習Labのフォルダと3禁を書いたProject Rule",
            },
        ],
        "scene": "最初の実習で、Claude Codeがファイル変更の許可を求めました。遥は早く進めたくて承認しかけますが、美咲が止めます。『何を許可したか説明できないなら、まだ押さない』。便利さより先に、安全の言葉を共有する瞬間でした。",
        "essay": "安全は注意書きだけでは作れません。最小権限、隔離、戻せる履歴、検証、監査を重ねて初めて、失敗しても被害を限定できます。CLAUDE.mdのお願いはGuidanceであり、絶対に止めたい操作はPermissions、Sandbox、Managed Settings、HooksでEnforcementします。\n\n初心者は、実データや本番環境から離れた学習用フォルダで始めます。外部公開、メール送信、課金、Git pushのような副作用は、ファイルの巻き戻しだけでは元に戻らないことも忘れてはいけません。",
        "mission": "学習用フォルダを作り、『削除しない』『外部公開しない』『秘密情報を貼らない』の三つをプロジェクトルールへ書いてください。",
        "takeaway": "安全はAIへのお願いではなく、権限・隔離・証拠で設計します。",
        "image_concept": "A protected sandbox workspace surrounded by layered safety rails, permission gates, checkpoints, and an audit trail",
        "image_kind": "isometric safety illustration",
        "usecases": [
            {
                "situation": "ABC商事の経理担当（架空）が、AIに『不要ファイルを整理して』と頼み、稟議添付のExcelを誤って削除する事故が起きた。",
                "action": "作業用フォルダだけを学習Labとして切り出し、削除禁止・外部公開禁止・本番フォルダ参照禁止をProject Ruleに書く。",
                "benefit": "事故が起きてもLab内で完結し、本番資料は手付かず。原状復帰がCheckpointで一発でできる。",
            },
            {
                "situation": "情シス課長（架空）が、社員のAI利用を許可したいが『何をどこまで触らせるか』を説明できず承認が止まっている。",
                "action": "Read許可・Write許可・実行許可・ネットワーク権限を分けたPermission表をプロジェクトごとに作る。",
                "benefit": "稟議で『どの範囲なら安全か』を説明でき、AI導入の承認が下りる。",
            },
            {
                "situation": "副業エンジニア（架空）が、APIキーをチャットへ貼ったまま動画キャプチャを共有し、課金を悪用される事故を経験した。",
                "action": "秘密情報は環境変数と専用ファイルのみに置き、Gitとチャットから除外する三つのルールをCLAUDE.mdへ書く。",
                "benefit": "鍵の露出が物理的に起こらず、共有・録画のたびに気を張り続ける必要がなくなる。",
            },
        ],
    },
    "03": {
        "intro_human": """『デスクトップにAI作業フォルダひとつ』で全案件を回してませんか。
そこに顧客A・顧客B・自分の実験が全部入ってる。

これ、AIから見ると地獄です。
どの顧客の話か、どこを触っていいか、まったく区別がつかない。結果、誤って別案件のファイルを書き換える事故が起きます。

この章で扱うのは、AIに見せる範囲を決める『プロジェクトフォルダ』という考え方。
案件ごとに専用フォルダを切って、docs（資料）・input（素材）・output（生成物）・tests（検証）の4つに分けるだけ。これだけで、AIが見るべき範囲と、人が確認すべき範囲がはっきり分かれます。

設定は10分。一度切ると、案件取り違えの不安が消えます。""",
        "features": [
            {
                "name": "Project Folder（文脈と権限の境界）",
                "summary": "AIに見せる範囲を明示的に切り、無関係な仕事を別Projectに分離するフォルダ設計。",
                "input": "扱う案件・顧客・テーマ、関連するファイル群",
                "output": "案件単位で閉じた専用フォルダと参照可能Path",
            },
            {
                "name": "推奨Project構造（docs/input/output/tests）",
                "summary": "ドキュメント・入力素材・生成物・検証データを役割で分けて配置し、AIも人も迷わない最小ディレクトリ構成。",
                "input": "実験・本番作業で扱うファイルの種類",
                "output": "docs/input/output/tests を持つ標準ディレクトリ",
            },
            {
                "name": "CLI / IDE連携と基本コマンド",
                "summary": "公式手順でCLI・VS Code・Cursorを接続し、まず覚える最小コマンドだけで動く状態を作る導入手順。",
                "input": "macOS環境、Node・gh等の前提パッケージ",
                "output": "Claude Code CLIとIDE接続、基本コマンドの実行確認",
            },
        ],
        "scene": "遥のデスクトップには、資料、画像、テスト用ファイルが混ざった『AI作業』フォルダがありました。蓮は新しい空のフォルダを作り、そこだけをCursorで開きます。作業場所を決めただけで、AIが見てよい範囲と人が確認すべき範囲がはっきりしました。",
        "essay": "Project Folderは単なる保存先ではなく、文脈と権限の境界です。無関係な仕事は別プロジェクトへ分け、同じ成果物へつながる仕事は共通ルートの下に整理します。ファイル構造が整うほど、AIは探索しやすく、人間は変更を追いやすくなります。\n\n導入では、公式の方法でCLIやIDE連携を用意し、最初は基本コマンドだけを覚えます。分からない操作は、その場でエージェントへ質問し、確認用のメモとしてプロジェクト内へ保存させます。",
        "mission": "空のlearning-labを作り、docs・input・output・testsの最小構造を用意してCursorでそのフォルダだけを開いてください。",
        "takeaway": "Project Folderを正しく切ると、文脈・安全・再開性が同時に整います。",
        "image_concept": "An organized digital workbench with a clearly bounded project folder, labeled zones for input, docs, output, tests, and terminal",
        "image_kind": "editorial workspace illustration",
        "usecases": [
            {
                "situation": "ある営業担当（架空）が、デスクトップに『AI作業』フォルダひとつへ複数案件を放り込み、どのSkillがどの顧客のものか分からなくなっている。",
                "action": "顧客ごとに専用Project Folderを作り、docs/input/output/testsの最小構造に分けて開く。",
                "benefit": "AIが見るべき範囲が顧客単位に閉じ、案件の取り違えと情報漏えいリスクが消える。",
            },
            {
                "situation": "中小企業の総務（架空）が、AI導入を始めたいが『どこから手を付けるか』分からず、毎週違うフォルダで実験して挫折している。",
                "action": "learning-labという練習専用フォルダを切り、その中だけで実験→検証→Skill化の小さなサイクルを回す。",
                "benefit": "練習と本番が物理的に分かれ、失敗を恐れず実験できる。成功したものだけを本番Projectへ移せる。",
            },
        ],
    },
    "04": {
        "intro_human": """『AIで何か作って』と言われて、3週間止まってる人、結構います。
題材が大きすぎて、どこから始めればいいか分からないんです。

この章で扱うのは、最初の90分で『動いた』を体験するための題材。会議の文字起こしを入れたら、議事録・タスク一覧・HTMLレポートの3点セットが出てくる、小さくて完結する成果物です。

ポイントは派手さじゃありません。要件定義→計画だけ承認→実装→検証→次回呼び出せるSkill化、までを一周することです。
この一周を経験すると、Claude Codeの基本ループが身体感覚になります。

90分後には、『次の会議から、これ呼び出すだけで5分で終わる』という業務型が手元に残ります。""",
        "features": [
            {
                "name": "会議アシスタント（最初の90分実習）",
                "summary": "雑然とした文字起こしから議事録・タスク・HTMLレポートを生成し、AIループ一周を体感する入門題材。",
                "input": "サンプル会議文字起こし、Project Folder",
                "output": "minutes.md、tasks.json、report.html、それぞれの合格証拠",
            },
            {
                "name": "要件定義テンプレ（目的/入出力/制約/完了条件）",
                "summary": "実装前に目的・入力・出力・Task Schema・制約・完了条件を埋めて、迷いどころを事前に潰す要件シート。",
                "input": "やりたいこと、扱うデータ、納品物のイメージ",
                "output": "AIに渡せる構造化された要件定義文書",
            },
            {
                "name": "Plan依頼と実装依頼の分離",
                "summary": "先に計画だけ出させてレビューし、合意できたら実装に進む2段階運用。手戻りを構造的に減らす依頼パターン。",
                "input": "要件定義、現在のコード/フォルダ状態",
                "output": "承認済みPlan、それに沿った最小diff実装",
            },
            {
                "name": "Skill昇格（成功した手順を再利用化）",
                "summary": "うまくいった会議アシスタントの一連の作業を、次回から呼び出せるSkillに変換する仕上げ工程。",
                "input": "成功した会話ログと成果物、合格基準",
                "output": "入力・処理・出力・検証を持つ議事録Skill",
            },
        ],
        "scene": "四人が最初に選んだ題材は、会議アシスタントでした。雑然とした文字起こしを入れると、議事録、タスク一覧、機械可読JSON、見やすいHTMLが出る。小さいけれど、要件・実装・検証・再利用がすべて入った題材です。",
        "essay": "最初の90分で大切なのは豪華さではありません。入力と出力を固定し、要件定義を作り、計画だけを先に確認し、小さく実装し、Schemaや画面で合格を判定することです。この一連を経験すれば、Claude Codeの基本ループが身体感覚になります。\n\n成功した後は、同じ会話を保存するのではなく、議事録作成の手順をSkillへ昇格させます。次の会議からは、再現可能な業務手順として呼び出せるようになります。",
        "mission": "サンプル文字起こしからminutes.md、tasks.json、report.htmlを作り、JSONの構造とHTMLの表示を自分の目で確認してください。",
        "takeaway": "最初の成果物は、作る・確かめる・再利用するまでを一周できるものが最適です。",
        "image_concept": "A meeting transcript flowing through an AI-assisted pipeline into minutes, a task board, structured JSON, and a polished HTML dashboard",
        "image_kind": "editorial process illustration",
        "usecases": [
            {
                "situation": "XYZ商社の営業企画（架空）が、週5本の商談記録から議事録・タスク・送付メールを手動で2時間かけて作っている。",
                "action": "サンプル文字起こしからminutes.md、tasks.json、report.htmlを作る90分実習を一周し、自分のSkillへ昇格させる。",
                "benefit": "次回からは同じテンプレで5分。文字起こしを入れる→3点セットが出る、を仕事の型として固定できる。",
            },
            {
                "situation": "ある総務リーダー（架空）が、AI活用の第一歩として何を作ればよいか分からず、3週間プロジェクトが止まっている。",
                "action": "入力・出力・検証が全部入った最小の題材として会議アシスタントを選び、90分の体験ミッションを完走する。",
                "benefit": "『動いた』体験で全員のスタート地点が揃い、その後の応用先（請求書・週報など）に展開しやすくなる。",
            },
        ],
    },
    "05": {
        "intro_human": """『いい感じにして』『なるべく早く』『よしなに』。
こういう曖昧な指示でAIに頼んで、期待と違う結果に毎回ガッカリしてませんか。

これ、AIの理解力じゃなく、依頼の解像度の問題です。
強い指示は長い呪文じゃありません。何のために・何を材料に・どこまで変え・何を作り・どうなれば終わりか、を埋めるだけ。

この章では、その6項目の依頼テンプレートと、迷ったらAI側から質問を出させる運用、それから『完成しました』を変更/検証/残リスクの3区分で証拠化する完了報告の型を覚えます。

書き方を変えると、同じAIが別物のように仕事を仕上げ始めます。""",
        "features": [
            {
                "name": "汎用依頼Template（6項目構造）",
                "summary": "目的・文脈・制約・成果物・完了条件・証拠の6項目で曖昧な依頼を構造化し、AI判断のブレを抑える依頼フォーマット。",
                "input": "曖昧な業務依頼文、関連する背景情報",
                "output": "AIに渡せる6項目テンプレ化された明確な依頼",
            },
            {
                "name": "Claudeに質問させる運用",
                "summary": "未知の要件は実装前にAIから質問を引き出す指示パターン。沈黙のまま暴走させない安全弁。",
                "input": "やや曖昧な依頼、判断に迷う設計分岐",
                "output": "Claudeからの質問リストと、それへの回答記録",
            },
            {
                "name": "完了報告の型（変更/検証/残リスク）",
                "summary": "『完成しました』を変更したもの・検証したこと・残っているリスクの3区分に分けて確認可能な証拠に変える報告書式。",
                "input": "実装が終わった作業、テスト結果",
                "output": "3区分で構造化された完了報告とリスクリスト",
            },
        ],
        "scene": "遥は『いい感じのアプリを作って』と入力し、期待と違う画面を受け取りました。蓮はプロンプトの言い回しを直す代わりに、目的、利用者、制約、成果物、完了条件を一緒に書き出します。結果は、呪文より仕事の定義で変わりました。",
        "essay": "強い指示は長文である必要はありません。何のために、何を材料に、どこまで変え、何を作り、どうなれば終わりかが明確なら、AIは判断しやすくなります。未知の要件がある場合は、実装前に質問させます。\n\n完了報告にも型が必要です。変更したもの、検証したこと、残っているリスクを分けると、『完成しました』という曖昧な宣言を、確認可能な証拠へ変えられます。",
        "mission": "曖昧な依頼を一つ選び、目的・文脈・制約・成果物・完了条件・証拠の六項目へ書き直してください。",
        "takeaway": "プロンプト技術の中心は、AI向けの言葉選びではなく、仕事の定義です。",
        "image_concept": "A vague cloud-shaped request being transformed into a clear structured brief with purpose, constraints, deliverables, and evidence",
        "image_kind": "conceptual editorial illustration",
        "usecases": [
            {
                "situation": "ある中堅メーカーのマーケ担当（架空）が、AIに『いい感じのLP作って』と頼み、期待と違う画面が出ては手戻りを繰り返している。",
                "action": "目的・利用者・制約・成果物・完了条件・証拠の六項目テンプレートを使って依頼文を書き直す。",
                "benefit": "AIの判断材料が揃って一発で意図に近い出力になり、手戻り回数が大幅に減る。",
            },
            {
                "situation": "PM経験ゼロの開発者（架空）が、上司から『この依頼を技術翻訳して』と毎回言われ、要件整理だけで一日を消費している。",
                "action": "曖昧な依頼を完了報告テンプレ（変更/検証/残リスク）まで含めて構造化し、AIへ渡す前に人へ見せる。",
                "benefit": "上司確認も同じテンプレで進み、要件と完了の認識ズレが消える。",
            },
        ],
    },
    "06": {
        "intro_human": """『一回うまくいったプロンプト』を、翌週も使えてますか。
ほとんどの人は、また最初から書き直してます。
そして、また違う結果が出る。

これ、運じゃありません。仕事の順序が決まってないからです。
速いチームは、毎回同じ7つの段階を回してます。探す→仕様を決める→計画→実装→検証→レビュー→保存（Explore/Specify/Plan/Implement/Verify/Review/Commit、頭文字でESPIVRC）。

この章を読むと、アプリ開発だけじゃなく、資料作成・調査・ファイル整理・Skill改善まで、同じ順序で進められるようになります。
速いチームは工程を省くんじゃなく、同じ工程を小さく明確に回してる。それがこの章のオチです。""",
        "features": [
            {
                "name": "ESPIVRC標準ループ",
                "summary": "Explore→Specify→Plan→Implement→Verify→Review→Commitの7段階を共通言語にし、業務種別を問わず同じ順で進める仕事の骨格。",
                "input": "新しい依頼、作業対象、関係者",
                "output": "7段階ごとの成果物（探索メモ・仕様・計画・実装・検証・レビュー・コミット）",
            },
            {
                "name": "Plan段階の変更範囲宣言",
                "summary": "実装の前に『何を触り何は触らない』を明示させ、AIの暴走と人のレビュー負荷を構造的に減らす設計。",
                "input": "仕様、現状のコード/ファイル",
                "output": "影響範囲・差分予定・前提条件を含むPlan",
            },
            {
                "name": "Verify→Review→Commit分離",
                "summary": "機械検証・別文脈レビュー・意味のある単位での保存を分けて、『動いたっぽい』を本物の完了に変える終盤フロー。",
                "input": "実装済みの変更、テストケース、レビュー観点",
                "output": "検証ログ、レビュー指摘、コミットメッセージ付き履歴",
            },
        ],
        "scene": "会議アシスタントは動きました。しかし翌週、別の素材で試すと抜けが出ます。蓮は成功した一回を称賛する前に、七つのカードを机へ並べました。Explore、Specify、Plan、Implement、Verify、Review、Commit。",
        "essay": "この七段階は、アプリ開発だけの手順ではありません。資料作成、調査、ファイル整理、Skill改善にも使える仕事の骨格です。探索で事実を集め、仕様で成功条件を固定し、計画で変更範囲を絞り、実装後は証拠で検証します。\n\nさらに、作成者とは別の文脈でレビューし、良い状態をGitへ保存します。各段階を飛ばさないことで、速さを落とすのではなく、やり直しを減らします。",
        "mission": "次に行う作業を七段階の見出しで書き、各段階の成果物を一つずつ決めてください。",
        "takeaway": "速いチームは工程を省くのではなく、同じ工程を小さく、明確に回します。",
        "image_concept": "A seven-station circular workflow with exploration, specification, planning, implementation, verification, review, and commit represented as tangible workstations",
        "image_kind": "workflow illustration",
        "usecases": [
            {
                "situation": "ABC物流の社内システム改修で、依頼→実装→『動いたっぽい』→本番→事故、という流れを毎月繰り返している。",
                "action": "Explore→Specify→Plan→Implement→Verify→Review→Commitの七段階に依頼テンプレを揃え、各段階で証拠を残す。",
                "benefit": "本番事故の発生源を段階に切り分けて潰せるようになり、改修1本あたりの平均事故件数が減る。",
            },
            {
                "situation": "Webデザイナー（架空）が、AIに『修正お願い』と頼んだら関係ない部分まで書き換えられ、何が変わったか追えない。",
                "action": "Plan段階で変更範囲をAIに宣言させ、Verifyで差分とテスト結果を見てからCommitする運用にする。",
                "benefit": "予期しない書き換えがPlanで弾かれ、レビュー時間が短く、巻き戻しも安全になる。",
            },
        ],
    },
    "07": {
        "intro_human": """『うっかり rm -rf』『git push で main を上書き』。
AIに作業を任せる時、こういう取り返しのつかない事故は、油断した5秒に起きます。

ほとんどの人は、AIに『全部許可』のまま動かしてます。
便利だから。確認が面倒だから。
でも、その『便利』と『事故』は同じスイッチで繋がってます。

Permission Modeは、操作ごとに『許可・拒否・確認』を3段階で切り替える仕組みです。
読み取りは自動で許可、書き換えは確認、削除と外部送信は必ず止める。それだけで、暴走の99%が手前で止まります。

この章を読み終わる頃には、自分が安心して任せられる範囲が、自分で決められるようになります。""",
        "features": [
            {
                "name": "Permission Mode と Permission Rule",
                "summary": "読む・編集する・実行する・ネットワーク・削除の5分類で許可と確認を切り分け、責任の境界を明示する権限設計。",
                "input": "扱うProject、許可してよい操作と確認したい操作",
                "output": "Project単位の許可ポリシー表とPermission Rule定義",
            },
            {
                "name": "Sandbox と Bypass運用",
                "summary": "Bypassは隔離された使い捨て環境のみ、本番Projectは確認モード固定とする運用ルール。便利さと事故半径を分離する。",
                "input": "実験用ワークスペース、本番Projectの一覧",
                "output": "Bypass許可Pathと禁止Pathを明示したCLAUDE.mdルール",
            },
            {
                "name": "Secrets管理ルール",
                "summary": "APIキー・トークンをチャットに貼らず、環境変数や専用ファイルへ置きGitから除外する3点ルール。",
                "input": "使う外部サービス、必要な鍵・トークン",
                "output": "Secret保存場所、.gitignore更新、CLAUDE.md記載",
            },
            {
                "name": "削除の標準手順",
                "summary": "対象一覧→件数確認→Dry-run→バックアップ→実行→結果確認の6段で、削除事故をワンクリックで起こさない手順化。",
                "input": "整理したいフォルダ、削除候補ファイル",
                "output": "削除Dry-run結果、バックアップ、削除完了レポート",
            },
        ],
        "scene": "実装中、許可確認が何度も現れ、遥は『全部自動にできないの？』と尋ねます。美咲は、自動化の速度ではなく、事故が起きたときの半径を見せました。自由度を上げる前に、どこまで壊れてもよいかを決める必要があります。",
        "essay": "Permission Modeは快適さの設定ではなく、責任の境界です。読む、編集する、コマンドを実行する、ネットワークへ出る、削除するという操作を分け、必要なものだけ許可します。Bypassは隔離された使い捨て環境に限定します。\n\nSecretsはチャットへ貼らず、環境変数や専用ファイルへ保存し、Gitから除外します。削除は対象一覧、件数、バックアップ、実行後確認を通す標準手順にします。",
        "mission": "現在のプロジェクトで許可してよい操作と、毎回確認すべき操作を二列に分けて書いてください。",
        "takeaway": "権限は便利さに合わせて広げるのではなく、被害を説明できる範囲に限定します。",
        "image_concept": "A series of permission gates around a coding workspace, from read-only to edit, command execution, network access, and destructive actions",
        "image_kind": "security concept illustration",
        "usecases": [
            {
                "situation": "ある社内開発者（架空）が、毎回出る権限確認を面倒に思いBypassを常用した結果、検証中の本番DBへ誤更新コマンドを流してしまった。",
                "action": "Bypassは隔離した使い捨て環境のみ・本番Projectは確認モード固定、というRuleをCLAUDE.mdへ書く。",
                "benefit": "便利さと事故半径のトレードオフが明示され、危険操作が必ず人の目を通るようになる。",
            },
            {
                "situation": "情シス（架空）が、AIに全権を与えるか禁止するかの二択しか出来ず、安全と業務スピードの両立に悩んでいる。",
                "action": "操作を読む・編集する・実行する・ネットワーク・削除の五分類に分け、それぞれ許可ポリシーを別に設計する。",
                "benefit": "全権でも全禁止でもなく、業務に必要な範囲だけを許可でき、稟議が通る具体度になる。",
            },
            {
                "situation": "個人事業主（架空）が、AIに『古いファイルを掃除して』と頼み、契約PDFまで巻き込まれて削除されかけた。",
                "action": "削除は対象一覧→件数確認→Dry-run→バックアップ→実行→結果確認の標準手順をSkill化する。",
                "benefit": "削除がワンクリックで進まなくなり、最悪でも実行前のリストで止められる。",
            },
        ],
    },
    "08": {
        "intro_human": """『常に最上位モデルを選んでおけば安心』。
これ、月初に利用上限を吹き飛ばす一番のパターンです。

ほとんどの人は、AIのモデルを『強さで選ぶ』と思ってます。
でも実は、計画・実装・整理・評価という役割で選ぶのが正解。簡単な整理は軽量モデル、重要レビューだけ深く考えさせる（高Effort）。
このスイッチを身につけると、月の利用上限が来なくなる上に、難所の品質も上がります。

ついでに、モデル名や料金は変わりやすいので、本文に書かず Feature Registry に分離しておく。これで教科書本体は古びません。

設定は15分。コスト効率と品質、両方が同時に上がります。""",
        "features": [
            {
                "name": "Model選択（役割で使い分け）",
                "summary": "計画・実装・軽い整理・評価という役割でモデルを選び、常に最上位を使わない使い分けの考え方。",
                "input": "業務の難易度、失敗コスト、必要なスピード",
                "output": "業務カテゴリ別のモデル割り当て表",
            },
            {
                "name": "Effort（思考量の調整）",
                "summary": "深く考える価値がある仕事だけEffortを上げ、定型変換は最小Effortで回すコスト最適化の設定軸。",
                "input": "対象タスクの判断重要度",
                "output": "タスク別Effort設定とコスト見積",
            },
            {
                "name": "Advisor と ultrathink",
                "summary": "難しい判断にだけ高Effort思考を呼び出し、相談役として併走させる使い方。常用ではなく要所投入のパターン。",
                "input": "設計分岐、複雑な原因分析、重要レビュー",
                "output": "Advisorからの追加観点、判断根拠の補強",
            },
            {
                "name": "Feature Registry（変動情報の分離）",
                "summary": "変動するモデル名・利用条件は本文ではなくRegistryへ外出しし、教科書原則を特定モデル依存から切り離す仕組み。",
                "input": "現行モデル名・料金・利用上限",
                "output": "Feature Registry更新エントリ（確認日付き）",
            },
        ],
        "scene": "遥は難しい仕事ほど常に最上位モデルを選ぼうとしました。ところが利用上限が早く来て、単純な修正まで止まります。蓮は、モデル名ではなく、計画、実装、軽い整理、評価という役割で選ぶよう提案します。",
        "essay": "ModelとEffortは品質を上げる魔法のつまみではありません。問題の難しさ、失敗コスト、必要な速度に合わせて使い分けます。深く考える価値があるのは、設計判断、複雑な原因分析、重要なレビューです。\n\n一方、定型変換や軽い修正まで最大Effortにすると、時間とコストだけが増えます。変動するモデル名や提供条件はFeature Registryへ分離し、教科書の原則を特定モデルへ依存させません。",
        "mission": "自分の典型業務を、軽量処理・標準処理・高難度判断の三つへ分類し、どこでEffortを上げるか決めてください。",
        "takeaway": "モデルは強さではなく役割で選び、変動情報は本文から切り離します。",
        "image_concept": "Three differently sized precision instruments assigned to lightweight work, standard implementation, and high-stakes planning, balanced against time and cost",
        "image_kind": "editorial metaphor illustration",
        "usecases": [
            {
                "situation": "個人開発者（架空）が、すべての作業を最上位モデル＋最大Effortで回した結果、月初に利用上限に達して残り3週間を低性能モデルで耐えている。",
                "action": "業務を軽量処理・標準処理・高難度判断の三つに分類し、Effortを上げるのは判断系のみにする。",
                "benefit": "利用上限の発火が遅れ、難所だけに高性能を集中投下できる。コスト効率が大きく改善する。",
            },
            {
                "situation": "ABC SIerのテックリード（架空）が、レビュー指摘の質に悩み、レビュー専用モデルを高Effortで分けたいが手順が決まっていない。",
                "action": "Plan/Implement/Reviewそれぞれにモデル設定を分け、変動するモデル名はFeature Registryへ外出しする。",
                "benefit": "重要レビューだけ深く考えさせる構造になり、後でモデル名が変わってもRegistry更新で済む。",
            },
        ],
    },
    "09": {
        "intro_human": """『朝から続けてるこのチャット、AIが急に変なこと言い出した』。
これ、AIの故障じゃありません。古い前提を引きずってるだけです。

ほとんどの人は、AIとのセッションを『途切れたら不便だから』と1日繋ぎっぱなしにしてます。
午前は予算検討、午後はSlack文面、夕方はバグ修正。机に資料を積み続けたら、そりゃ混乱します。

この章で扱うのは、仕事の単位でセッションを切る運用と、再開に必要な状態をRESUME.mdというファイルへ外に出しておく仕掛け。
会話履歴に頼らず、ファイルだけで翌日続けられる状態を作ります。

セッションを切ることは、忘れることじゃなく、必要なものだけを次に渡すことです。""",
        "features": [
            {
                "name": "Session分離（仕事単位で切る）",
                "summary": "目的が変わるたびに新しいセッションを開き、古い前提を引きずらせない運用。文脈混入の事故を構造的に防ぐ。",
                "input": "現在の作業内容、次に着手する別タスク",
                "output": "目的別に分かれたセッション、引き継ぎファイル",
            },
            {
                "name": "/clear・/compact・/context",
                "summary": "会話履歴の圧縮・全消去・状態確認のコマンド群。文脈節約と再開のための日常操作。",
                "input": "肥大化した会話、進行中のタスク状態",
                "output": "圧縮済みコンテキスト、または新しい起点",
            },
            {
                "name": "RESUME.md（状態の外部化）",
                "summary": "再開に必要な現在地・決定・次の一操作をファイルへ書き出し、会話履歴に依存せず復帰できるようにする。",
                "input": "進行中の判断、未完了タスク、TODO",
                "output": "再開可能なRESUME.mdと参照Path一覧",
            },
            {
                "name": "Resume運用と履歴を残さない実行",
                "summary": "Resumeは作業再開の補助、独立Stateを正本にする運用方針。画像入力・割り込みも文脈を保つ範囲で扱う。",
                "input": "中断中のセッション、機密性のある作業",
                "output": "正本としての作業State、必要に応じた履歴非保持実行",
            },
        ],
        "scene": "同じセッションで要件、雑談、バグ修正、別の資料作成まで続けた結果、Claude Codeは古い前提を引きずり始めました。机の上に資料を積み続けたような状態です。遥は、会話を続けることと文脈を守ることが同じではないと気づきます。",
        "essay": "Sessionは仕事の単位で分けます。新しい目的へ移るなら新しいセッションを開き、必要な状態はファイルへ保存します。/clearや/compactは便利ですが、重要な判断や次の操作を会話の中だけに残さないことが本質です。\n\nResumeは作業再開の補助であり、教材やチーム運用では独立したStateを正本にします。画像入力や割り込みも、現在の目的を明確に保つ範囲で使います。",
        "mission": "いまの作業について、次回再開時に必要な状態をRESUME.mdへ書き、会話を閉じても続けられるか確認してください。",
        "takeaway": "会話履歴に依存せず、再開に必要な状態をファイルへ外部化します。",
        "image_concept": "A cluttered desk of accumulated conversation context beside a clean reset desk with a concise resume note and organized project state",
        "image_kind": "before-and-after editorial illustration",
        "usecases": [
            {
                "situation": "ある経営企画（架空）が、午前は予算検討・午後はSlack文面・夕方はバグ修正を全部同じセッションで進め、AIが古い前提を引きずって変な提案を出している。",
                "action": "仕事の単位ごとにセッションを切り直し、RESUME.mdへ現在地・決定・次の一操作を残す。",
                "benefit": "AIの回答が現状に合うようになり、翌日の再開も会話履歴ではなくファイルだけで成立する。",
            },
            {
                "situation": "兼業ライター（架空）が、長時間セッションで記事執筆→AIが急に話題を取り違える→/compactしても直らない、を繰り返している。",
                "action": "話題切替時は新セッションを開き、必要な状態をresumeメモへ外部化する運用に変える。",
                "benefit": "AIの混乱が消え、文脈の引き継ぎが意図したファイルのみに限定される。",
            },
        ],
    },
    "10": {
        "intro_human": """『さっきの状態に戻して』ができないと、AIに大胆な編集を頼めません。
だから多くの人は、小さく安全な指示しか出せず、伸びしろを自分で潰してます。

実は、戻り道は2種類用意できます。
ひとつは『会話の中で素早く巻き戻す』Checkpoint。もうひとつは『セッションや人をまたいで残る正式な履歴』であるGit。
このふたつは競合しません。役割が違うだけ。

この章では、CheckpointとGitの最小運用、AIにコミットメッセージを書かせるルール、それから複数機能を同時に試したい時にファイル衝突を防ぐ Worktree という並列作業の仕組みまでまとめます。

戻れる安心が手に入ると、AIに任せる勇気が一段階上がります。""",
        "features": [
            {
                "name": "Checkpoint（会話中の素早い巻き戻し）",
                "summary": "セッション内で直前の変更を一手で戻せる機能。試行錯誤の安心担保として軽量な保存地点を作る。",
                "input": "AIに任せる大胆な変更、実験的な編集",
                "output": "巻き戻し可能なCheckpoint、戻したあとの状態",
            },
            {
                "name": "最小Git運用",
                "summary": "意味のある単位でCommitし、変更理由と検証結果を残すことで、セッションや人をまたぐ正式な履歴を作る。",
                "input": "完了した小さな変更、検証結果",
                "output": "意味あるCommitメッセージとレビュー可能なdiff",
            },
            {
                "name": "ClaudeへCommitさせるRule",
                "summary": "AIがCommitメッセージを書く際の体裁・粒度・禁止事項を定めるルール。履歴の読みやすさを保つ。",
                "input": "完了した変更、検証ログ",
                "output": "Rule準拠のCommit、PR説明文",
            },
            {
                "name": "Worktreeによる並列作業",
                "summary": "別ブランチを別ディレクトリとして展開し、同じファイルへの編集衝突なしに並列実装を進める仕組み。",
                "input": "並行して進めたい複数機能",
                "output": "機能別Worktreeディレクトリと衝突なしの差分",
            },
        ],
        "scene": "修正後の画面が崩れ、遥は『ひとつ前へ戻して』と頼みます。Checkpointで戻せる変更もありましたが、セッションをまたいだ手編集までは戻りません。蓮はGitを開き、『戻る』を偶然ではなく履歴にしようと説明します。",
        "essay": "CheckpointとGitは競合しません。Checkpointは会話中の素早い巻き戻し、Gitはセッションや人をまたぐ正式な履歴です。意味のある単位でCommitし、変更理由と検証結果を残します。\n\n並列作業ではWorktreeを使い、別の作業が同じファイルを奪い合わないようにします。保存地点を先に作ると、AIへ大胆な試行を許可しやすくなります。",
        "mission": "現在の良い状態をCommitし、その後に小さな変更を加えてDiffを確認し、元へ戻せることを試してください。",
        "takeaway": "可逆性は勇気ではなく、CheckpointとGitで設計する能力です。",
        "image_concept": "A mountain trail with frequent checkpoints and a durable map archive, symbolizing quick rewind and long-term Git history",
        "image_kind": "editorial metaphor illustration",
        "usecases": [
            {
                "situation": "中小Webサイト運営者（架空）が、AIに『大胆に作り直して』を依頼するたび、戻したい時に戻せず古い版を失っている。",
                "action": "毎回の作業開始前に良い状態をCommitし、Checkpoint＋Gitの二重保存で『戻れる』を物理的に作る。",
                "benefit": "AIへ強気に試行させても、いつでも前に戻れる安心が手に入る。",
            },
            {
                "situation": "ある個人開発（架空）が、複数機能を同時に試したくて同じファイルを並列編集し、お互いの変更を上書きして混乱した。",
                "action": "Worktreeで作業ツリーを物理的に分け、機能ごとに別ディレクトリで並列に動かす。",
                "benefit": "AIに並列実装させても衝突が起きず、後でCherry-pickで良い変更だけを統合できる。",
            },
        ],
    },
    "11": {
        "intro_human": """毎回、AIに同じ説明を書いてませんか。
『うちは TypeScript で、コメントは英語で、テストは vitest で…』
朝のチャット、昼のチャット、夜のチャット、全部に同じ前置き。
それ、書く必要、もう無いです。

この章で扱うのは、プロジェクトの前提を一箇所に書いておく『常時読まれる案内板』（CLAUDE.md）と、特定フォルダだけに効かせる Rules、AIが見つけた短い事実を自動保存する Auto Memory の使い分けです。
全部CLAUDE.mdに詰め込むと逆に重くなるので、知識には『置き場所』があるという話を体感します。

ここを整えると、AIは『汎用の何でも屋』から、『あなたのプロジェクトを知ってる同僚』に変わります。""",
        "features": [
            {
                "name": "CLAUDE.md（プロジェクトの案内板）",
                "summary": "常時読まれる短い案内板。プロジェクトの目的・前提・最低限のルールだけを簡潔に置く。",
                "input": "プロジェクトの目的、必ず守らせたい最低限ルール",
                "output": "簡潔で肥大化しないCLAUDE.md",
            },
            {
                "name": "Rules（Path固有の指示）",
                "summary": "ディレクトリ単位で適用されるルール。CLAUDE.mdを膨らませず、効く場所だけに知識を置く仕組み。",
                "input": "特定フォルダ・拡張子に限定したいルール",
                "output": "対象Path下でだけ自動適用されるRule",
            },
            {
                "name": "/init による初稿生成",
                "summary": "プロジェクトを読み込みCLAUDE.mdの叩き台を作るコマンド。生成内容をそのまま使わず短く整える前提で使う。",
                "input": "既存プロジェクト構造、目的の概略",
                "output": "CLAUDE.md初稿（編集して短くする出発点）",
            },
            {
                "name": "Auto Memory（短い事実の自動保存）",
                "summary": "AIが見つけた短い事実だけを自動保存する記憶層。常時読み込み情報を短く安定させる役割を担う。",
                "input": "会話中の決定事項、繰り返される好み",
                "output": "短い形に圧縮された自動メモ",
            },
        ],
        "scene": "毎回『日本語で』『このプロジェクトは何をするか』を説明するのに疲れた遥は、すべてをCLAUDE.mdへ詰め込みました。翌日、どの仕事でも長い指示が読み込まれ、かえって動きが鈍くなります。知識には置き場所があると分かる失敗でした。",
        "essay": "CLAUDE.mdはプロジェクトの短い案内板です。Path固有のルールはRulesへ、繰り返す業務手順はSkillsへ、AIが見つけた短い事実はAuto Memoryへ分けます。常に読み込む情報ほど短く、安定した内容にします。\n\n/initは初稿を作る助けになりますが、生成された説明をそのまま肥大化させないことが重要です。実際の失敗から、必要な最小ルールだけを追加します。",
        "mission": "CLAUDE.mdの各行を『毎回必要か』で見直し、手順はSkillへ、Path固有事項はRulesへ移してください。",
        "takeaway": "知識は量ではなく、適切なScopeへ置くことで効きます。",
        "image_concept": "A layered memory system with a small project sign, path-specific rule cards, reusable skill manuals, and compact discovered notes",
        "image_kind": "layered architecture illustration",
        "usecases": [
            {
                "situation": "ABCコンサル（架空）のCLAUDE.mdが3,000行を超え、毎回読み込みに時間がかかり、AIが本来の指示を見落とすようになっている。",
                "action": "CLAUDE.mdは『常に読みたい短い案内板』だけ残し、Path固有事項はRules、業務手順はSkillsへ移す。",
                "benefit": "起動が軽くなり、AIが本当に必要な指示を確実に拾うようになる。",
            },
            {
                "situation": "個人開発者（架空）が、Project AとProject Bで日本語化ルールが毎回ぶつかり、混乱した出力を受け取り続けている。",
                "action": "全社共通ルールはGlobal CLAUDE.mdへ、Project個別はProject CLAUDE.mdへ、Path別はRulesへと役割を分ける。",
                "benefit": "ルール衝突が物理的に起きず、どこを直せばどこへ効くかが明確になる。",
            },
        ],
    },
    "12": {
        "intro_human": """『あの時のうまくいったプロンプト、どこ行った？』
チャット履歴を漁る30分、もう何回繰り返しましたか。

ほとんどの人は、成功した会話をブックマークやコピペで残してます。
でも、別の入力で試したら再現できない。これは『プロンプトの保存』であって『業務手順の保存』じゃないからです。

Skill は、入力・処理・出力・品質基準・失敗時の対応をひと塊にした、再現可能な業務パッケージです。
名前を付けて、次回からは『あのSkillで』のひと言で同品質の成果物が出る。長文の例やコード例は references に逃がして、本体は短く保つ（Progressive Disclosure）。

この章を読み終わると、自分の最初のSkillを、人に渡せる形まで持っていけるようになります。""",
        "features": [
            {
                "name": "Skill（再現可能な業務パッケージ）",
                "summary": "名前・条件・入力・処理・出力・品質基準・参照資料を持つ、必要時だけ読み込まれる再利用単位。",
                "input": "成功した業務手順、入力例、合格基準",
                "output": "次回から呼び出せるSKILL.mdと参照資料",
            },
            {
                "name": "Custom Commands と Canonical Name",
                "summary": "SkillsへCommandsを統合する正本命名規約。/コマンドで呼び出せる名前と所有者を定義する。",
                "input": "Skill名候補、所有者、利用シーン",
                "output": "lowercase-hyphenのCanonical Nameと所有Owner",
            },
            {
                "name": "Progressive Disclosure（references分離）",
                "summary": "長文・コード例・FAQはreferencesへ逃がし、SKILL.md本体を短く保つ設計原則。",
                "input": "Skill関連の長文素材、コード例",
                "output": "短いSKILL.mdとreferences/配下の補助資料",
            },
            {
                "name": "4軸評価（明確性/実用性/保守性/整合性）",
                "summary": "Skillを4観点で採点し、合格点未満は本番配布しない品質ゲート。Generator/Evaluator分離の前段で使う。",
                "input": "完成したSkill、評価Fixture",
                "output": "4軸スコアと改善優先度のレポート",
            },
        ],
        "scene": "会議アシスタントを三度改善したあと、遥は『この成功手順を名前付きで呼びたい』と考えます。ナビゲーターは会話ログを保存するのではなく、入力、手順、検証、失敗時対応をまとめたSkillへ変換します。",
        "essay": "Skillはプロンプトの短縮形ではなく、再現可能な業務パッケージです。名前、使う条件、入力、処理、出力、品質基準、参照資料を持ち、必要なときだけ読み込まれます。長い資料はreferencesへ分け、Progressive Disclosureを守ります。\n\n最良の作り方は、先に仕事を成功させ、その過程を抽出し、別の入力で試し、独立した評価器で採点することです。Claude CodeとCodexで共通利用する場合は、正本名と配置を統一します。",
        "mission": "最近うまくいった作業を一つ選び、SKILL.mdへ入力・手順・出力・検証・失敗時対応を書き出してください。",
        "takeaway": "Skillは成功した会話ではなく、別の入力でも再現できる業務手順です。",
        "image_concept": "A well-used work process being distilled into a reusable field manual with inputs, steps, outputs, quality checks, and references",
        "image_kind": "editorial manual illustration",
        "usecases": [
            {
                "situation": "XYZ広告のプランナー（架空）が、毎週類似のレポート依頼に対して毎回プロンプトを書き直し、品質も毎回ぶれている。",
                "action": "成功した会話を入力・処理・出力・品質基準・失敗時対応の形式へ整理し、Skill化する。",
                "benefit": "次週からは『あのSkillで』の一言で同品質の成果物が出る。教育コストもSkill共有で済む。",
            },
            {
                "situation": "ある制作チーム（架空）が、複数メンバーで同じSkillを書き散らし、似て非なるSkillが乱立して使い分けに迷っている。",
                "action": "正本名・Owner・参照資料を持つSKILL.mdテンプレートを揃え、referencesに長文を逃がすProgressive Disclosureを徹底する。",
                "benefit": "Skillの重複が抑えられ、新規メンバーも『どれを使えばよいか』を迷わず選べる。",
            },
        ],
    },
    "13": {
        "intro_human": """『自分のコードを自分でレビュー』、何回も穴をすり抜けてきましたよね。
これ、AIにも同じことが起きます。実装した本人の文脈が残ってると、レビューが甘くなる（迎合バイアス）。

ほとんどの人は、AIを『1人の万能アシスタント』として使ってます。
でも、調査・実装・レビューを別の文脈で動かす（複数のSubagent）と、見落としが激減します。
実装セッションを閉じて、背景を知らないReviewer Agentに成果物だけ渡す。それだけで、要件・安全・保守性の3観点で本当の指摘が返ってきます。

複数Agentの価値は、人数じゃありません。独立した文脈と役割分担です。
この章で、レビューの質が一段階深くなります。""",
        "features": [
            {
                "name": "Subagent（文脈を分ける仕組み）",
                "summary": "役割ごとに別Agentを立てて文脈を分離し、過去会話に引きずられない調査・実装・レビューを可能にする機構。",
                "input": "親セッションの作業、役割ごとの責務",
                "output": "Subagentの完了報告、独立した中間成果物",
            },
            {
                "name": "Reviewer Agent（独立コンテキストの評価者）",
                "summary": "成果物だけを渡して評価させ、迎合バイアスを排した指摘を得るための専任エージェント。",
                "input": "成果物、評価観点（要件/安全/保守性）",
                "output": "独立コンテキストからの指摘リストと優先度",
            },
            {
                "name": "Research Agent",
                "summary": "調査専任で出典・確度・反証を分けて整理するエージェント。実装者と分離して情報収集の質を確保する。",
                "input": "調査テーマ、検索範囲、評価軸",
                "output": "出典付き調査結果と未確認項目リスト",
            },
            {
                "name": "Agent View と並列実行",
                "summary": "複数Agentの動きを俯瞰し、独立した仕事へ分担させる運用画面。同じファイルへの同時編集は避ける指針付き。",
                "input": "並列化したいタスク群、各Agent責務",
                "output": "Agent View上の並列実行ログと統合結果",
            },
        ],
        "scene": "自分で作った資料を自分でレビューすると、どうしても甘くなります。蓮は、実装を担当したセッションを閉じ、背景を知らないReviewer Agentへ成果物だけを渡しました。初めて見える欠点が、いくつも出てきます。",
        "essay": "Subagentは単なる並列化ではなく、文脈を分ける仕組みです。調査、実装、レビューなど役割を限定し、必要な入力と期待する出力を明示します。作成者と評価者を分けると、過去の会話に引きずられない評価ができます。\n\nAgent Viewや並列実行は、互いに独立した仕事へ使います。同じファイルを複数Agentへ同時編集させるのではなく、調査観点やレビュー観点を分担させます。",
        "mission": "現在の成果物を、新しいセッションまたはReviewer Agentへ渡し、要件充足・安全・保守性の三観点で評価させてください。",
        "takeaway": "複数Agentの最大の価値は人数ではなく、独立した文脈と役割分担です。",
        "image_concept": "A small expert team with separate researcher, builder, and independent reviewer desks coordinated by one project lead",
        "image_kind": "team editorial illustration",
        "usecases": [
            {
                "situation": "ある個人開発者（架空）が、自分のコードを自分でレビューさせるとAIが甘く採点し、毎回バグを見落としている。",
                "action": "実装セッションを閉じ、背景を知らない独立コンテキストのReviewer Agentへ成果物だけ渡す。",
                "benefit": "迎合バイアスが消え、要件・安全・保守性の三観点で本当の指摘が返ってくる。",
            },
            {
                "situation": "中堅企業のリサーチチーム（架空）が、調査・検証・統合を一人のAIに任せ、結論が初期仮説に引きずられる傾向が抜けない。",
                "action": "Research・Verify・Synthesizeを別Agentに分け、各役割の入力と期待出力を明示する。",
                "benefit": "仮説バイアスが分離され、反証も合わせて統合できる。結論の信頼度が説明可能になる。",
            },
        ],
    },
    "14": {
        "intro_human": """『rm -rf 禁止』とCLAUDE.mdに書いても、繁忙期に事故は起きます。
人が読み飛ばすことを、AIも引きずる。文章のお願いには限界があります。

そこで出てくるのが、特定イベントで必ず動く強制装置（Hooks）。
危険コマンドの実行直前で物理的に止める（PreToolUse）。編集直後にtsc型チェックを自動で走らせる（PostToolUse）。セッション開始時に必要な前提を勝手にロードする（SessionStart）。
3つだけで、暴走と見落としが激減します。

ついでに、SkillとHookをまとめて配るための『Plugin』という束ね方も学びます。
この章を読み終わる頃には、『気をつけて』を『気をつけなくても止まる』に書き換えられるようになります。""",
        "features": [
            {
                "name": "PreToolUse Guard（危険操作の物理拒否）",
                "summary": "rm -rfや本番DB操作など、文章のお願いでは止められない操作を実行直前に拒否するHook。",
                "input": "実行されようとしたコマンド、対象Path",
                "output": "ブロック判定とログ、許可された操作のみの実行",
            },
            {
                "name": "PostToolUse Validation",
                "summary": "Edit/Write直後にtsc・lint・テスト等を自動実行し、編集の瞬間にエラーを検出する検証Hook。",
                "input": "編集したファイル、プロジェクトの検証コマンド",
                "output": "検証結果、エラー時のブロックと修正指示",
            },
            {
                "name": "SessionStart Hook",
                "summary": "セッション開始時に必要な前提・ルール・現在地ファイルを自動注入し、毎回ゼロから説明させない仕掛け。",
                "input": "セッション起動イベント、注入したい文脈ファイル",
                "output": "起動時自動ロードされた前提情報",
            },
            {
                "name": "Plugins（配布単位）",
                "summary": "Skills・Hooks・設定をまとめて配布する束ね単位。導入範囲と更新を組織的に管理する。",
                "input": "配布したいSkill群、Hook群",
                "output": "インストール可能なPluginパッケージ",
            },
            {
                "name": "Hook Test（Fixture検証）",
                "summary": "安全な入力と危険な入力のFixtureで、Hook自体の動作を単体テストする仕組み。Hookコードの品質を担保する。",
                "input": "安全/危険のFixture、想定動作",
                "output": "Fixture通過/拒否の検証結果",
            },
        ],
        "scene": "安全ルールを文書に書いても、忙しい日に見落とされることがあります。美咲は、危険なコマンドの直前で止め、編集後に型チェックを走らせ、終了時に保存を促す仕組みを作ります。注意を、決定的な動作へ変える章です。",
        "essay": "HooksはAIへ『気をつけて』と頼む代わりに、特定イベントで必ず処理を実行します。PreToolUseで危険操作を拒否し、PostToolUseで検証し、SessionStartで必要な文脈を注入します。/goalの停止判定にもHookの考え方が使われます。\n\nHook自体もコードであり、入力検証、Timeout、ログ、失敗時の扱い、単体テストが必要です。PluginはSkillsやHooksなどの配布単位として扱い、導入範囲を管理します。",
        "mission": "危険な削除コマンドを拒否する最小PreToolUse Hookを作り、安全な入力と危険な入力のFixtureでテストしてください。",
        "takeaway": "絶対に守らせたいことは文章ではなく、HookとPolicyで実行時に強制します。",
        "image_concept": "A software factory with deterministic quality gates before commands, after edits, at session start, and at completion",
        "image_kind": "isometric quality-control illustration",
        "usecases": [
            {
                "situation": "情シス（架空）が、CLAUDE.mdに『rm -rf禁止』と書いても、繁忙期にAIが破壊的コマンドを生成して事故が起きる。",
                "action": "PreToolUseでrm -rf・本番DB操作・外部送信を物理的に拒否するHookを書き、Fixtureテストを通す。",
                "benefit": "AIがどんなに賢くてもHookで止まる。文章のお願いから決定論的な強制へ昇格できる。",
            },
            {
                "situation": "ある制作チーム（架空）が、編集後のTypeScript型エラーを翌朝まで気づかず、毎週の月曜に手戻りが発生している。",
                "action": "PostToolUseでEdit/Write後にtsc --noEmitを自動実行するHookを入れる。",
                "benefit": "型エラーが編集の瞬間に検出され、月曜の手戻り会議が消える。",
            },
        ],
    },
    "15": {
        "intro_human": """『APIキー、チャットに貼っちゃえ』。
これ、世界中の人が今日もやってる、最も危険な10秒です。動画キャプチャ・スクショ・他人への画面共有、どこかで漏れます。

ほとんどの人は、外部サービス連携を『繋げば便利』としか見てません。
でも、繋ぐ瞬間に信頼境界も広がります。読める範囲（Read）・書ける範囲（Write）・鍵の置き場所、この3つは必ず先に決めてから繋ぐ。

この章では、用意済みのサービス連携（Connector）・標準規格で接続するMCP・自由実装のAPIという3方式の使い分けと、外部から取得した文書をうっかり命令として実行させない対策（Prompt Injection対策）まで揃えます。

外部連携は、能力を増やす前に、境界を引くことから始まります。""",
        "features": [
            {
                "name": "Connector / MCP / API（3方式）",
                "summary": "用意されたサービス連携、標準化された接続規格、自由実装のAPIという3つの外部接続方式の使い分け。",
                "input": "繋ぎたい外部サービス、必要な操作",
                "output": "方式別の接続設定と権限境界",
            },
            {
                "name": ".mcp.json 雛形と Scope設計",
                "summary": "MCPサーバー定義ファイルにScopeを絞り、Read権限とWrite権限を分離して書く標準テンプレート。",
                "input": "外部サービス、必要なScope一覧",
                "output": "最小権限の.mcp.json設定",
            },
            {
                "name": "Read/Write分離 と Human Gate",
                "summary": "情報取得は自動でよいが、書き込みは明示承認を介する設計。書き込み事故を構造的に防ぐ。",
                "input": "業務フロー、Write操作の頻度と重要度",
                "output": "Read自動・Write承認のフロー設計",
            },
            {
                "name": "Prompt Injection対策",
                "summary": "取得した外部文書を命令として実行せずデータとして扱うルール。Web/Doc経由の攻撃を無効化する。",
                "input": "外部から取得する文書、Webコンテンツ",
                "output": "データ扱い徹底ルール、書き込みの明示承認設計",
            },
            {
                "name": "Secrets保存と導入Check",
                "summary": "鍵をチャットや会話履歴に露出させず、環境変数・専用ファイル・SecretManagerへ置く導入手順チェックリスト。",
                "input": "必要なAPIキー、トークン",
                "output": "Secret保存場所と導入時チェックリスト",
            },
        ],
        "scene": "会議アシスタントをGoogle Driveとつなげたい遥は、APIキーをチャットへ貼ろうとします。美咲が止め、鍵は会話ではなく環境変数と秘密管理へ置きます。外部連携は能力を広げる一方、信頼境界も広げます。",
        "essay": "Connectorは用意されたサービス連携、MCPはツールを標準的に接続する仕組み、APIはより自由な実装窓口です。どの方式でも、Scopeを絞り、ReadとWriteを分け、Secretsをファイルやチャットへ露出させません。\n\n外部データにはPrompt Injectionが混ざる可能性があります。取得した文書を命令として実行せず、データとして扱い、書き込み操作は明示的な承認と検証を通します。",
        "mission": "使いたい外部サービスを一つ選び、必要なRead権限と不要なWrite権限を分け、Secretの保存場所を決めてください。",
        "takeaway": "外部連携では、できることより先に、読める範囲・書ける範囲・鍵の置き場所を決めます。",
        "image_concept": "A secure bridge from a local AI workspace to cloud services, with a locked key vault, read-only lanes, and guarded write lanes",
        "image_kind": "security integration illustration",
        "usecases": [
            {
                "situation": "ABC商事の総務（架空）が、Drive連携Skillで毎日のレポート取得を自動化したいが、AIに書き込み権限まで渡すのが怖くて導入が止まっている。",
                "action": "MCP/Connectorの権限をRead Only Scopeに絞り、書き込みはHuman Gateを介する設計にする。",
                "benefit": "情報収集の自動化は走り、書き込み事故は構造的に起きない安全な業務基盤になる。",
            },
            {
                "situation": "個人ライター（架空）が、外部記事を要約させたら本文に紛れ込んだ命令でAIが意図しない動作をした（Prompt Injection）。",
                "action": "取得文書はデータとして扱い実行しないルール＋書き込みは明示承認のみ、というRuleを書く。",
                "benefit": "外部データに混入した悪意ある命令が動作にならず、調査用途として安全に使い続けられる。",
            },
        ],
    },
    "16": {
        "intro_human": """『長い報告書、また読まれてないな』。
資料を作る側からすると、これが一番虚しい瞬間です。

ほとんどの人は、報告は『Markdown か Word で長文を書くもの』と思ってます。
でも、結論到達時間はフォーマットで2倍変わります。同じ内容でも、カード・グラフ・強調された結論が並ぶ単一HTMLにすると、会議の冒頭で『見ました』前提で議論が始まる。

この章で扱うのは、Markdownと単一HTMLの使い分け、CSVを1ページHTMLに変える標準プロンプト、それから印刷・スマホ・アクセシビリティの公開前チェック。
外部CSSに頼らず、1ファイルだけで開けるHTMLを正本にする運用です。

HTMLを選ぶ理由は『見栄え』じゃなく『理解の速度』。
これが分かると、報告の通り方が変わります。""",
        "features": [
            {
                "name": "形式選択（Markdown vs 単一HTML）",
                "summary": "執筆・差分管理が強いMarkdownと、視認性・操作性が強いHTMLを目的別に使い分ける判定基準。",
                "input": "成果物の用途、読み手、共有経路",
                "output": "形式選択の根拠と最終出力フォーマット",
            },
            {
                "name": "単一HTML標準（自己完結レポート）",
                "summary": "外部CSS/JSに依存せず、1ファイルだけで開ける標準フォーマット。共有・印刷・スマホ表示も担保する。",
                "input": "Markdown原稿、データ、画像",
                "output": "外部依存なし1ファイルHTMLレポート",
            },
            {
                "name": "CSV分析Prompt",
                "summary": "CSVを読み込んで集計結果と図解を含むHTMLにする標準プロンプト。経営共有しやすい1枚物に変換する。",
                "input": "CSVデータ、注目したい軸",
                "output": "集計表・グラフ・要点カード入りHTML",
            },
            {
                "name": "HTML Slide / Discussion Board",
                "summary": "Markdownから1ページHTMLでスライド風や議論用ボードを作る派生形式。同じ正本から複数表現を出す。",
                "input": "発表用骨子または議題リスト",
                "output": "HTML Slide、Discussion Board",
            },
            {
                "name": "品質Check（A11y/印刷/スマホ）",
                "summary": "公開前にアクセシビリティ・印刷・スマホ表示・装飾依存度を確認する標準チェック項目。",
                "input": "完成したHTML",
                "output": "A11y/印刷/スマホでの動作確認結果",
            },
        ],
        "scene": "同じ分析結果をMarkdownとHTMLで見せると、会議室の反応が変わりました。長い文章では見落とされた傾向が、カード、グラフ、強調された結論によって一目で伝わります。HTMLは装飾ではなく、理解の速度を設計する形式でした。",
        "essay": "Markdownは執筆と差分管理に強く、HTMLは情報密度、視認性、操作性、共有性に強みがあります。CSV分析、スライド風資料、ディスカッションボードのように、見る人が比較・操作する仕事ではHTMLが向きます。\n\nただし生成画像や派手な装飾に重要情報を閉じ込めません。本文、Alt、Captionだけでも意味が通り、単一HTMLで開け、印刷・スマホ・アクセシビリティを確認します。",
        "mission": "同じ小さなレポートをMarkdownと単一HTMLで作り、読み手が結論へ到達する時間を比べてください。",
        "takeaway": "HTMLを選ぶ理由は見栄えではなく、理解・比較・操作を助けることです。",
        "image_concept": "A split-screen comparison of a dense markdown document and a clear editorial HTML report with cards, charts, and interactive controls",
        "image_kind": "editorial comparison illustration",
        "usecases": [
            {
                "situation": "ある経営企画（架空）が、毎月の予実報告をMarkdownで提出するが、役員が目を通さず会議で同じ説明を繰り返している。",
                "action": "同内容を単一HTMLレポートへ変換し、結論カード・グラフ・強調点を1ページに集約する。",
                "benefit": "結論到達時間が短くなり、会議の冒頭で『見ました』前提で議論が始まる。",
            },
            {
                "situation": "中堅メーカーの開発者（架空）が、テストレポートをスクリーンショットで貼り、後日参照しても何が壊れていたか追えない。",
                "action": "テスト結果を単一HTMLで保存し、印刷・スマホ・Alt textで読める形式に揃える。",
                "benefit": "障害後の振り返り会議で誰でも開けて確認でき、Markdown原本との二重管理にしなくて済む。",
            },
        ],
    },
    "17": {
        "intro_human": """『AIに「LP作って」って頼んだら、毎回ゼロからやり直し』。
これ、AIが悪いんじゃありません。情報設計・見た目・実装を同時に決めようとしてるからです。

ほとんどの人は、いきなりコードから作り始めます。
プロは違います。まず白黒のワイヤーフレーム（Wireframe）で情報の順序を固定し、色・フォント・余白の共通ルール（Design System）を当て、動きを確認するプロトタイプ、最後に実装。
段階を分けると、修正コストがその段階内で閉じます。

この章を読み終わる頃には、ブランド資産として再利用できるDesign Systemを別プロジェクトに持っておき、複数LPで一貫性を保つ運用が組めるようになります。

情報・見た目・動作を分けて決める。これが生成AIの速度を、手戻りに変えない秘訣です。""",
        "features": [
            {
                "name": "Wireframe / Design System / Prototype / Code 分離",
                "summary": "情報・見た目・動作・実装を別段階で確定する4分離設計。修正コストを段階で閉じ込める。",
                "input": "作りたい画面の目的と利用者",
                "output": "段階ごとに確定した情報設計・スタイル・プロトタイプ・コード",
            },
            {
                "name": "Design SystemとProject分離",
                "summary": "色・タイポ・余白の共通システムを別Projectに固定し、各画面はそれを参照する形に揃える運用。",
                "input": "ブランドカラー、フォント、共通余白ルール",
                "output": "再利用可能なDesign System Projectと参照Path",
            },
            {
                "name": "Claude Design 標準Flow",
                "summary": "白黒WireframeからDesign System適用、実装まで進める標準的な制作フロー。各段階の決定事項を記録する。",
                "input": "ラフ案、要件、対象ユーザー",
                "output": "段階別の決定記録と実装ドラフト",
            },
            {
                "name": "Codeへ渡すPromptとSync Rule",
                "summary": "Designの決定をコード側へ漏れなく伝える受け渡しプロンプトと、後で齟齬を起こさない同期ルール。",
                "input": "Designでの確定事項、参照コンポーネント",
                "output": "実装プロンプトとSync用ルール",
            },
            {
                "name": "公開前チェック",
                "summary": "レスポンシブ・アクセシビリティ・リンク・秘密情報・ブランド整合をCode側で再検証する公開前ゲート。",
                "input": "実装済みページ、公開予定",
                "output": "5項目のチェック結果と公開可否判定",
            },
        ],
        "scene": "いきなりコードからLPを作ると、情報構造と見た目と実装が同時に揺れました。遥はClaude Designで白黒のワイヤーフレームを作り、内容の順序を固めてから、Design Systemを適用してCodeへ渡します。",
        "essay": "Designでは、情報構造を決めるWireframe、見た目のルールを持つDesign System、動作を確かめるPrototype、実装を担うCodeを分けます。各段階で何を確定したかが分かると、修正コストが下がります。\n\n同期機能やUI名は変化しやすいため、公式の現行入口を確認しながら使います。公開前にはレスポンシブ、アクセシビリティ、リンク、秘密情報、ブランド整合性をCode側で再検証します。",
        "mission": "一つのページを、情報だけのWireframe、Design System適用版、実装版の三段階で作り、各段階の決定事項を記録してください。",
        "takeaway": "情報、見た目、動作を分けて決めると、生成AIの速度を手戻りに変えずに済みます。",
        "image_concept": "A clean progression from grayscale wireframe to branded design system components to a functioning responsive web application",
        "image_kind": "design process illustration",
        "usecases": [
            {
                "situation": "ある中小Web会社（架空）が、AIに『LPを作って』と頼むたびに情報構造とビジュアルが同時に揺れて、毎回ゼロからやり直している。",
                "action": "白黒Wireframe→Design System適用→実装の三段階に分け、各段階の決定事項を記録する。",
                "benefit": "情報・見た目・動作の修正コストが分離され、出戻りが特定段階だけで済む。",
            },
            {
                "situation": "個人事業主（架空）が、複数LPで色・フォント・余白がバラバラになり、ブランドの一貫性が失われている。",
                "action": "Design Systemを別Projectとして固定し、各LPはそれを参照する形に揃える。",
                "benefit": "1箇所直せば全LPに反映され、ブランド資産として再利用できる。",
            },
        ],
    },
    "18": {
        "intro_human": """週報、毎週ゼロから書いてませんか。
あれ、本当は『書く資料』じゃなくて『開いたら最新になってる画面』が正解です。

ほとんどの人は、レポートを『静的な成果物』として作ります。
でも、開くたびにDriveの会議ファイルを読み込んで・要約して・キャッシュする仕組み（Live Artifact）にすると、書く時間がゼロになります。
データ取得・整形・表示・AI要約・キャッシュの5層に分けて設計するのがコツ。毎回高価な処理を繰り返さず、更新時刻と出典を画面に出して、失敗時は『古いデータ』と明示する。

書く資料から、更新される業務画面へ。
この章で、AI活用の発想が一段階ジャンプします。""",
        "features": [
            {
                "name": "Cowork（非開発業務の複数ステップ）",
                "summary": "Projectで文脈を固定し、複数ステップの業務処理を継続実行する作業形態。Codeとは別の入口として扱う。",
                "input": "繰り返し発生する業務、参照する文脈ファイル",
                "output": "継続実行可能なCowork Project",
            },
            {
                "name": "Live Artifact 5層構造",
                "summary": "データ取得・整形・表示・AI要約・キャッシュの5層に分けて設計する、開くたびに最新化する業務インターフェース。",
                "input": "対象データソース、表示したい指標",
                "output": "5層分離されたLive Artifact実装",
            },
            {
                "name": "会議Dashboard Prompt",
                "summary": "Driveの会議ファイルを開くたびに取り込み・要約・キャッシュするダッシュボード用プロンプトのテンプレ。",
                "input": "Drive上の会議ファイル群、要約観点",
                "output": "リロード時に最新化される会議Dashboard",
            },
            {
                "name": "Scheduled設計",
                "summary": "定期実行で重複防止・ロック・ログ・通知・再試行を持たせる業務スケジュール設計。",
                "input": "実行頻度、失敗時の挙動、通知先",
                "output": "Scheduledジョブ設定と運用ログ",
            },
            {
                "name": "Acceptance（更新/キャッシュ/出典）",
                "summary": "Live Artifactの完成判定。更新時刻・キャッシュ振る舞い・出典表示の3点をAcceptance基準にする。",
                "input": "完成したArtifact、運用シナリオ",
                "output": "3点Acceptance通過記録、Stale時の挙動確認",
            },
        ],
        "scene": "週報を毎回作るのではなく、開くたびに最新のDrive情報を読み込むDashboardにできないか。遥の問いから、CoworkとLive Artifactsの実験が始まりました。作る資料から、更新される業務画面へ発想が変わります。",
        "essay": "Coworkは非開発業務の複数ステップに向きます。Projectで文脈を固定し、Scheduledで定期実行し、Artifactsで結果を操作可能な画面へし、ConnectorやMCPから最新情報を取り込みます。\n\nLive Artifactでは、データ取得、整形、表示、AI要約、キャッシュを分けて設計します。読み込みのたびに高価な処理を繰り返さず、更新時刻と出典を表示し、失敗時には古いデータであることを明示します。",
        "mission": "ローカルの会議データを表示する小さなDashboardを作り、更新・キャッシュ・出典表示の三点を確認してください。",
        "takeaway": "Artifactsは静的な成果物ではなく、データ更新とAI処理を持つ業務インターフェースです。",
        "image_concept": "A live operations dashboard pulling current meeting files from cloud storage, summarizing them, caching results, and showing update status",
        "image_kind": "dashboard concept illustration",
        "usecases": [
            {
                "situation": "ある営業マネージャー（架空）が、週報を毎週手動更新しており、開くたびに最新化されないため週末まで状況が見えない。",
                "action": "Driveの会議ファイルを開くたびに取り込み・要約・キャッシュするLive Artifact Dashboardを作る。",
                "benefit": "開いた瞬間に最新の進捗が見え、週次更新作業そのものが不要になる。",
            },
            {
                "situation": "中小オペレーター（架空）が、外部APIを毎リロードで叩く実装にして請求金額がはねた。",
                "action": "Cache・更新時刻・出典・失敗時のStale表示を分離して設計する。",
                "benefit": "コストとUXのバランスが取れ、データ取得失敗時にも古い情報と明示できる。",
            },
        ],
    },
    "19": {
        "intro_human": """『AIに全会話履歴を渡せば、自分専用になる』。
これ、便利そうに見えて、顧客の個人情報まで学習素材に紛れ込ませる地雷です。

ほとんどの人は、パーソナライズを『大量に覚えさせること』だと思ってます。
正解は逆。『何を保存しないか』を最初に決めることです。秘密・個人情報・顧客データ・雑談は除外し、関心・学習課題・好む形式の3つだけ抽出して INTERESTS.md に書く。本人がいつでも編集・削除できる状態を保つ。

新しさと深掘り回数で重み付け（Recency Score）して『現在の関心』を反映する、毎回全ログ読まずに差分処理する、そのProfileから復習問題まで作る、というところまでこの章で組みます。

自分専用化は、大量記憶じゃなく、信号の選別と本人の制御で作ります。""",
        "features": [
            {
                "name": "Privacy by Design（保存しないものを決める）",
                "summary": "秘密・個人情報・顧客データ・雑談を除外し、保存対象を関心・学習課題・好む形式に限定するパーソナライズ設計。",
                "input": "会話ログ、扱う情報のセンシティビティ",
                "output": "保存対象/除外対象を分けた抽出ルール",
            },
            {
                "name": "Interest Profile Skill",
                "summary": "未分析ログから関心・学習課題・好む形式だけを抽出してINTERESTS.mdへまとめるSkill。本人が編集可能。",
                "input": "セッションログ、過去会話",
                "output": "編集可能なINTERESTS.mdプロファイル",
            },
            {
                "name": "Recency Score（重み付け）",
                "summary": "新しさと深掘り回数で重み付けし、現在の関心を反映するスコアリング。古い関心と現在を混ぜない。",
                "input": "抽出済み関心信号、時間軸",
                "output": "現在優先のスコア順関心リスト",
            },
            {
                "name": "差分処理（処理済み位置の管理）",
                "summary": "処理済み位置を保持し、毎回全ログを再走査しない実装パターン。処理時間と費用を構造的に抑える。",
                "input": "新規ログと前回処理位置",
                "output": "差分のみ処理した抽出結果",
            },
            {
                "name": "学習問題生成",
                "summary": "Profileを元に調査テーマや復習問題を作る出力機能。学んだことを定着させるための再利用。",
                "input": "INTERESTS.md、苦手分野",
                "output": "復習問題、深掘り調査テーマ",
            },
        ],
        "scene": "数週間使うと、遥の質問には興味や苦手分野が表れ始めました。ナビゲーターは会話を丸ごと記憶するのではなく、未分析ログから必要な信号だけを抽出し、INTERESTS.mdへまとめます。自分専用化を、プライバシーと一緒に設計します。",
        "essay": "パーソナライズでは、何を保存しないかが重要です。秘密、個人情報、顧客データ、単なる雑談を除外し、関心、学習課題、好む形式のような再利用価値のある信号だけを抽出します。処理済み位置を持ち、毎回全ログを読み直しません。\n\n新しさと深掘り回数を重み付けすると、現在の関心を反映できます。そのProfileから調査テーマや復習問題を作り、学習者自身が編集・削除できるようにします。",
        "mission": "保存してよい学習信号と保存してはいけない情報を定義し、少量の会話ログからINTERESTS.mdの試作を作ってください。",
        "takeaway": "自分専用化は大量記憶ではなく、目的を限定した信号抽出と本人の制御で作ります。",
        "image_concept": "A private personal knowledge garden growing from carefully filtered conversation signals, with sensitive data kept outside a protected boundary",
        "image_kind": "editorial privacy illustration",
        "usecases": [
            {
                "situation": "ある個人ライター（架空）が、AIに『自分専用化したい』と全会話履歴を渡し、結果として顧客個人情報まで学習対象に紛れて怖くなった。",
                "action": "保存対象を関心・学習課題・好む形式の三つに限定し、秘密情報・顧客データ・雑談は除外定義を書く。",
                "benefit": "個人化の便益は得つつ、プライバシーリスクが構造的にゼロへ近づく。",
            },
            {
                "situation": "学習担当（架空）が、社員ごとのスキルレベルを把握したいが、毎回全ログを再走査して処理時間が爆発している。",
                "action": "処理済み位置と新しさ重みを持つINTERESTS.md抽出Skillを作る。",
                "benefit": "差分処理になり、関心の最新動向だけ追える。本人が編集・削除できる透明な仕組みになる。",
            },
        ],
    },
    "20": {
        "intro_human": """朝起きたら、もう昨日の続きが終わってる。
これ、ちょっとズルしてる気分になります。

ほとんどの人は、AIを『チャット欄を開いて話しかける』対象だと思ってます。
でも実はAIには、自分で動く方法が3つあります。
ゴールを渡して走らせる（/goal）。画面を開かずに動かす（Headless）。決まった時間に勝手に動かす（定期実行）。

ただし、自律化の本当の難所は『始め方』じゃなく『止め方』です。成功条件・最大ターン・Timeout・許可範囲・失敗時停止を仕様にしてから走らせる。公開・送信・課金・削除は完全自動化せず、最後の一歩は人間承認に残す。

設定は10分。一度入れたら、コーヒーを淹れる前にレポートが手元にある生活が普通になります。""",
        "features": [
            {
                "name": "/goal（成功条件と停止条件）",
                "summary": "成功条件・最大ターン・Timeout・許可範囲・失敗時停止を仕様化し、自律実行が安全に終わるよう設計するコマンド。",
                "input": "自動化したい仕事、成功判定の機械条件",
                "output": "完了 or 安全停止のどちらかで終わる自律実行",
            },
            {
                "name": "Headless実行",
                "summary": "対話画面なしで定型タスクを走らせる実行形態。CI・夜間バッチ・サーバー常駐に組み込む。",
                "input": "実行内容、引数、許可範囲",
                "output": "Headlessジョブの実行ログとExitステータス",
            },
            {
                "name": "安全なWrapper（重複防止・ロック・ログ）",
                "summary": "/goalやHeadlessを実運用に乗せるための重複防止・ロック・ログ・通知・再試行を包んだラッパースクリプト。",
                "input": "ベース実行コマンド、運用要件",
                "output": "Wrapperスクリプトと運用ログ",
            },
            {
                "name": "Scheduled必須要件",
                "summary": "定期実行で必ず満たすべき重複防止・冪等性・通知の要件チェック。配信時刻のブレも管理する。",
                "input": "スケジュール対象ジョブ、頻度",
                "output": "必須要件チェック通過記録",
            },
            {
                "name": "LaunchAgent例",
                "summary": "macOS LaunchAgentによる定期実行設定の具体例。個人Mac〜開発機での自動化導入に使う。",
                "input": "実行コマンド、頻度、ログ出力先",
                "output": "動作するLaunchAgent plist例",
            },
            {
                "name": "自動化しない領域の明示",
                "summary": "公開・送信・課金・削除など、最後の一歩を必ず人間に残す領域を明確化するルール。",
                "input": "自動化候補リスト、副作用の有無",
                "output": "自動化可/人間承認必須の振り分け表",
            },
        ],
        "scene": "『テストが通るまで直して』は便利ですが、条件が曖昧だと永遠に動き続けます。蓮は、終了条件、最大回数、許可範囲、ログ、失敗時の停止を先に書きます。自律化は、始め方より止め方を設計する仕事でした。",
        "essay": "/goalやHeadless実行は、検証可能な条件がある仕事に向きます。成功条件を機械で確かめられ、最大ターンやTimeoutがあり、副作用が限定されていることが前提です。定期実行では重複防止、ロック、ログ、通知、再試行を持たせます。\n\n人の承認が必要な公開、送信、課金、削除は完全自動化しません。自動化の境界を明示し、最後の一歩を人間へ残します。",
        "mission": "自動化したい仕事を一つ選び、成功条件・最大回数・Timeout・禁止する副作用・人間の承認地点を書いてください。",
        "takeaway": "良い自律化は、達成条件と停止条件の両方を検証可能にします。",
        "image_concept": "A bounded autonomous loop with measurable goals, a turn counter, timeout clock, logs, and a clear human approval gate before external effects",
        "image_kind": "automation control illustration",
        "usecases": [
            {
                "situation": "ある社内開発者（架空）が、AIに『テストが通るまで直して』と頼み、無限ループで朝までCPUが回り続けて停止条件もなく止まれない。",
                "action": "成功条件・最大ターン・Timeout・許可範囲・失敗時停止を/goal仕様として先に書き出す。",
                "benefit": "夜間自動実行が安全に走り、達成 or 安全停止の二状態で終わる。",
            },
            {
                "situation": "情シス（架空）が、毎日のレポート自動配信を構築したいが、誤送信時の責任の所在が決まらず承認が出ない。",
                "action": "公開・送信・課金・削除は完全自動化せず、最後の一歩を人間承認に残す設計にする。",
                "benefit": "副作用のある操作だけ責任者が承認し、それ以外は自動で進む構造になり、承認が下りる。",
            },
        ],
    },
    "21": {
        "intro_human": """『調査・検証・統合をひとりのAIに任せたら、最初の仮説に最後まで引きずられた』。
これ、結構ありがちな失敗です。

ほとんどの人は、AIを増やせば品質が上がると思ってます。
でも複数Agentの本質は、人数じゃなく『仮説バイアスの分離』。情報源を探す（Research）・主張を検証する（Verify）・矛盾と重複を整理して統合する（Synthesize）の3役を別の文脈で動かすと、初期仮説の磁場から抜けられます。

ただし、Agentを増やせば検索量と料金も急増します。Agent数・最大トークン・再試行回数の上限を必ず設ける。単純な仕事では Dynamic を使わず、手動Workflowで済ませる判断軸もこの章で学びます。

複数Agentは、品質を自動保証する魔法じゃありません。難しい仕事を分解する道具です。""",
        "features": [
            {
                "name": "Dynamic Workflows",
                "summary": "入力に応じて複数Agentの流れを組み替える可変Workflow。仮説バイアスを分離した調査・統合に向く。",
                "input": "調査テーマ、必要な情報源、品質基準",
                "output": "Agent構成と各Agentの中間成果物",
            },
            {
                "name": "Research → Verify → Synthesize",
                "summary": "情報源を探す・主張を検証する・矛盾と重複を整理して統合する三役分業の代表構成。",
                "input": "調査依頼、複数情報源",
                "output": "出典付き検証済み統合レポート",
            },
            {
                "name": "Cost Control（Agent数/トークン/再試行）",
                "summary": "Agent数・検索範囲・最大トークン・再試行回数を制限し、料金暴走を構造的に防ぐ運用設定。",
                "input": "想定予算、現状のAgent構成",
                "output": "上限つきCost設定とアラート閾値",
            },
            {
                "name": "手動Workflow（Dynamic不要の判定）",
                "summary": "単純な仕事ではDynamicを使わず、手動の小さなWorkflowで済ませる判断軸。複雑度とコストを天秤にかける。",
                "input": "タスク内容、必要な分業度合い",
                "output": "Dynamic採用/手動採用の判定理由",
            },
            {
                "name": "Acceptance（中間成果物の保存）",
                "summary": "各段階の中間成果物を保存し、最終出力だけで判断しない受け入れ基準。再現と監査を可能にする。",
                "input": "Workflow実行ログ、中間成果物",
                "output": "段階別保存ファイルとAcceptance結果",
            },
        ],
        "scene": "一つのAgentに調査、検証、執筆を全部任せると、最初の思い込みが最後まで残ることがあります。そこで調査者、検証者、統合者を分けます。ただし人数を増やせばよいわけではなく、費用と情報量も急増します。",
        "essay": "Dynamic Workflowsは入力に応じて複数Agentの流れを組みます。代表的な形はResearch、Verify、Synthesizeです。異なる情報源を探し、主張を検証し、重複と矛盾を整理して最終成果物へ統合します。\n\n単純な仕事では手動の小さなWorkflowの方が速く安価です。Agent数、検索範囲、最大トークン、再試行を制限し、各段階の中間成果物を保存します。",
        "mission": "一つの調査テーマをResearch・Verify・Synthesizeへ分け、各担当へ渡す入力と受け取る出力を定義してください。",
        "takeaway": "複数Agentは難しい仕事を分解する手段であり、品質を自動保証するものではありません。",
        "image_concept": "Three coordinated specialist agents researching, verifying, and synthesizing evidence, with visible cost and scope controls",
        "image_kind": "multi-agent workflow illustration",
        "usecases": [
            {
                "situation": "中堅リサーチ会社（架空）が、新市場調査をひとりのAIに任せたら初期仮説に引きずられて、後で重大な事実を見逃したと判明した。",
                "action": "Research・Verify・Synthesizeの三役を独立Agentに分け、Cost上限と再試行回数も決める。",
                "benefit": "仮説バイアスが分離され、結論への反証も統合される。意思決定の質が説明可能になる。",
            },
            {
                "situation": "ある個人投資家（架空）が、複数Agent構成にしたら検索量が爆発し、月のAPI料金が想定の5倍になった。",
                "action": "Agent数・検索範囲・最大トークンを段階的に制限し、各段階の中間成果物を保存する。",
                "benefit": "暴走しないCost構造になり、シンプルな調査は手動Workflowへ戻す判断もできる。",
            },
        ],
    },
    "22": {
        "intro_human": """『この数字、どこから持ってきたの？』
役員プレゼンで詰められて、答えられず黙る。
これ、AIに調査させた時の代表的な事故です。

ほとんどの人は、AIの調査結果を『そのまま貼って終わり』にしてます。
だから根拠不明の数字・古い情報・SNSの噂が混ざっていても気づけない。

この章で導入するのは、主張・根拠・日付・確度・反証を1行ずつ記録する『Claim Ledger』という台帳。情報源の重みは公式→一次→実測→解説→SNSの順で固定し、変動情報には確認日を付ける。
ついでに、動画やSNSから情報を取る時の重複統合と、発言と事実の区別もここで仕込みます。

調査品質は、文章の滑らかさじゃなく、主張と証拠の追跡可能性で決まります。""",
        "features": [
            {
                "name": "Source優先度（公式→一次→実測→解説→SNS）",
                "summary": "情報源の重みを序列化し、変動情報には確認日を付ける調査品質の土台。SNSの勢いと事実を分ける。",
                "input": "集めた情報源、それぞれの種別",
                "output": "重み付き情報源リストと確認日メタ",
            },
            {
                "name": "Claim Ledger",
                "summary": "主張・根拠・日付・確度・反証を1行ずつ記録する追跡可能な台帳。後で『この数字の出所は？』に即答できる。",
                "input": "レポート上の主張、対応する出典",
                "output": "5列構造のClaim Ledger",
            },
            {
                "name": "Research Skill",
                "summary": "対象・期間・除外条件・評価軸を内蔵した調査Skill。テーマを渡すと出典付き調査結果を返す。",
                "input": "調査テーマ、期間、除外条件",
                "output": "Research Skillによる出典付きレポート",
            },
            {
                "name": "動画/SNS統合（発言と事実の区別）",
                "summary": "同じ内容を重複カウントせず、発言と事実を区別して統合する処理。SNS発の話題を業務情報に変える。",
                "input": "動画・SNS投稿の集合",
                "output": "重複統合済みの発言/事実分離レポート",
            },
            {
                "name": "完了条件（未確認事項の明示）",
                "summary": "未確認事項と次に検証すべき点を明示してレポートを閉じる完了基準。隠れた不確実性を残さない。",
                "input": "調査ドラフト",
                "output": "未確認事項リストと次の検証アクション",
            },
        ],
        "scene": "最新機能のレポートを読んだ美咲は、結論より先に『どの主張が、どの一次情報に支えられているか』を尋ねました。SNSの勢いを、会社の判断材料へ変えるには、出典と不確実性を分ける必要があります。",
        "essay": "信頼できる調査では、公式文書、一次資料、実測、信頼できる解説、SNSの順に重みを変えます。Claim Ledgerへ、主張、根拠、日付、確度、反証を記録し、変動情報には確認日を付けます。\n\n動画やSNSを統合するときは、同じ内容を重複カウントせず、発言と事実を区別します。最後に、未確認事項と次に検証すべき点を明示します。",
        "mission": "一つの最新機能について三つの主張を選び、Claim Ledgerへ一次情報・確認日・確度・反証を書いてください。",
        "takeaway": "調査品質は文章の滑らかさではなく、主張と証拠の追跡可能性で判断します。",
        "image_concept": "An evidence board linking claims to official sources, dates, confidence levels, and counterevidence, arranged like an investigative newsroom",
        "image_kind": "editorial evidence illustration",
        "usecases": [
            {
                "situation": "経営企画（架空）が、AIに業界レポートを作らせたが、根拠不明の数字や古い情報が混じり、役員プレゼンで矛盾を指摘された。",
                "action": "Claim Ledgerに主張・根拠・日付・確度・反証を必須項目で記録するSkillを作る。",
                "benefit": "プレゼン前に根拠を逆引きでき、『この数字の出所は？』に即答できる。",
            },
            {
                "situation": "ある個人ブロガー（架空）が、最新機能の解説を書こうとして、SNSの噂と公式情報が混在し、結果として誤情報を発信して訂正に追われた。",
                "action": "出典の優先度を公式→一次→解説→SNSの順で重み付けし、変動情報には確認日を付ける。",
                "benefit": "発信前にSNS情報を切り分けでき、訂正リスクが大幅に減る。",
            },
        ],
    },
    "23": {
        "intro_human": """『自分のMacで動くSkill、ZIPで全社に配布したら阿鼻叫喚』。
配布の失敗、ほとんどがこのパターンです。

ほとんどの人は、便利なファイルを配ることを『全社化』だと思ってます。
でも、個人の便利ツールが組織のインフラに変わる境目では、正本・配布先・個人差分・強制Policy・Release段階を別物として設計する必要があります。

この章で扱うのが、ハーネスの4面構造（Guidance＝お願い／Enforcement＝強制／Content＝中身／Delivery＝配布）。
正本（skill-src）と生成物を分離し、Claude Code とCodex両方へ同じ正本から展開する。配布は段階的（Canary→Pilot→Stable）。個人カスタマイズは ~/.claude/local/ で保護する。

全社化は『コピーして送る』じゃなく、製品として設計する仕事です。""",
        "features": [
            {
                "name": "ハーネス4面（Guidance/Enforcement/Content/Delivery）",
                "summary": "全社配布基盤を案内・強制・コンテンツ・配布の4面に分け、各面の正本と更新方法を設計する全体図。",
                "input": "現在の共通資産、配布手段",
                "output": "4面に分類された正本と更新フロー",
            },
            {
                "name": "推奨Repository（正本と生成物の分離）",
                "summary": "skill-srcを正本、配布用パッケージを生成物として分離し、Claude/Codex両Runtimeへ同じ正本から展開する構造。",
                "input": "Skill群、Hook群、Plugin群",
                "output": "正本と生成物が分かれたGit Repository",
            },
            {
                "name": "Release Flow（Canary→Pilot→Stable）",
                "summary": "PR→Test→Evaluator→Canary→Pilot→Stableの順で段階配布し、失敗を小さく発見できるリリース設計。",
                "input": "配布候補の更新セット",
                "output": "段階通過ごとのリリースタグと配布対象",
            },
            {
                "name": "Guidance/Enforcement Mapping",
                "summary": "どのルールが文章のお願いで、どれがHookやPolicyで物理強制かを表に揃えるマッピング作業。",
                "input": "現状の全ルール一覧",
                "output": "Guidance/Enforcement分類表",
            },
            {
                "name": "個人Layer（私物設定の保護）",
                "summary": "~/.claude/local/ など、配布で上書きされない個人カスタマイズ層を分離し、私物設定を守る仕組み。",
                "input": "個人カスタマイズ、私物Skill",
                "output": "上書き保護されたLocal Layer",
            },
        ],
        "scene": "遥のSkillが好評になり、『全員へ配ろう』という話が出ます。美咲はZIPを送る代わりに、正本、配布先、個人差分、強制Policy、Release段階を図にします。個人の便利ツールが、組織のインフラへ変わる境目です。",
        "essay": "トレプロハーネスは、CLAUDE.md、Commands、Hooks、Skills、Codex資産をGitで一元管理し、各Macへ自動同期する基盤です。Guidance、Enforcement、Content、Deliveryを別の面として設計し、個人カスタマイズ層を保護します。\n\nRepositoryでは正本と生成物を分け、PR、Test、Evaluator、Canary、Pilot、Stableの順で配布します。即時全社反映より、失敗を小さく発見できるRelease Flowを優先します。",
        "mission": "現在の共通資産をGuidance・Enforcement・Content・Deliveryの四面へ分類し、正本をどこに置くか決めてください。",
        "takeaway": "全社化では、便利なファイルを配るのではなく、正本・強制・配布・復旧を一つの製品として設計します。",
        "image_concept": "An enterprise harness architecture with four planes—guidance, enforcement, content, and delivery—feeding staged release rings across employee laptops",
        "image_kind": "enterprise architecture illustration",
        "usecases": [
            {
                "situation": "ある中堅企業（架空）が、AIで成果を出した社員のSkill群をZIPで全社配布した結果、人によって設定が壊れ、サポートが回らなくなった。",
                "action": "Guidance・Enforcement・Content・Deliveryの四面に分け、各面の正本と更新方法を定義する。",
                "benefit": "個別調整がDelivery層で吸収され、共通層は壊れない。サポート問い合わせの種類が分類できる。",
            },
            {
                "situation": "情シス（架空）が、全社一斉配布したSkillにバグが見つかった時、誰がどこから戻せるのか分からず深夜対応になった。",
                "action": "Canary→Pilot→StableのRelease Flowを設け、各段階のExit Criteriaを書く。",
                "benefit": "事故は小さい範囲で止まり、Stable到達前にロールバックできる構造になる。",
            },
        ],
    },
    "24": {
        "intro_human": """『毎朝の自動更新が、ネット不安定な端末で半端な状態で止まった』。
これ、配布基盤の本当の品質が試される瞬間です。

ほとんどの人は、自動更新を『コピーすればOK』と思ってます。
でも本番では、何度実行しても壊れない（冪等な）Bootstrap、追加・変更・削除まで追従する同期（Convergent Sync）、配布直後のVerify、事故時に一手で戻せるRollbackまでがセットでないと、ある朝突然崩壊します。

この章では、個人カスタマイズLayerに触れずに共通Skillだけ更新する update.sh、Manifest比較で差分を計算する仕組み、署名済みの旧版へ即座に戻すRollback運用までを設計します。

配布の完成条件は『コピー成功』じゃなく、収束・検証・復旧が繰り返し成立することです。""",
        "features": [
            {
                "name": "Bootstrap（冪等な初回セットアップ）",
                "summary": "何度実行しても壊れない初回セットアップ。ネット障害時に安全に持ち越し、同時実行をロックで防ぐ。",
                "input": "新規端末、認証情報、対象Repository",
                "output": "冪等に走るBootstrap実行ログと最終状態",
            },
            {
                "name": "Convergent Sync（追加/変更/削除追従）",
                "summary": "前回Manifestと今回正本を比較し、追加・変更・削除を最終状態へ収束させる同期処理。",
                "input": "Manifest差分、現端末状態",
                "output": "収束済み最新状態と差分ログ",
            },
            {
                "name": "Skill Merge と update.sh",
                "summary": "個人Layerに触れずに共通Skillだけ更新する定期マージ処理と、それを呼ぶupdate.shの標準実装。",
                "input": "更新対象Skill群、個人Layerパス",
                "output": "個人保護つき更新完了ログ",
            },
            {
                "name": "Verify（存在/Version/Hook動作）",
                "summary": "配布直後に存在・Version・Hook動作を構造化チェックし、配布の成功を客観的に確認する検証層。",
                "input": "配布対象、想定Version",
                "output": "Verify結果レポートと不一致リスト",
            },
            {
                "name": "Rollback（既知Releaseへ一手戻し）",
                "summary": "署名済みの以前のReleaseへ一操作で戻せる仕組み。事故時の復旧時間を分単位に短縮する。",
                "input": "現在版、戻り先Releaseタグ",
                "output": "Rollback実行ログと復旧後Verify",
            },
        ],
        "scene": "翌朝の自動更新で一部端末だけ失敗したとき、配布基盤の本当の品質が試されます。美咲は、何度実行しても壊れないBootstrap、削除まで追従するSync、検証、Rollbackを一つの流れにします。",
        "essay": "BootstrapとUpdateは冪等で、ネットワーク障害時には安全に次回へ持ち越し、同時実行をロックで防ぎます。Syncは前回Manifestと今回の正本を比較し、追加・変更・削除へ収束させながら、個人Layerへ触れません。\n\n配布後はVerifyで存在、Version、Hook動作を確認し、問題があれば署名済みの以前のReleaseへ一操作で戻します。ログと端末Inventoryがなければ、配布の成功は判断できません。",
        "mission": "小さなサンプル構成でdry-run、同期、削除追従、個人フォルダ保護、Rollbackを順にテストしてください。",
        "takeaway": "配布の完成条件はコピー成功ではなく、収束・検証・復旧が繰り返し成立することです。",
        "image_concept": "A reliable software distribution conveyor showing bootstrap, manifest sync, verification, staged rollout, and one-click rollback",
        "image_kind": "isometric delivery pipeline illustration",
        "usecases": [
            {
                "situation": "情シス（架空）が、毎朝の自動更新スクリプトがネット不安定の社員端末で半端な状態で止まり、AIの動作が日替わりで変わる現象に悩んでいる。",
                "action": "Bootstrap・Updateを冪等に作り直し、Manifest比較で追加・変更・削除を最終状態へ収束させる。",
                "benefit": "ネットワーク失敗時も次回で復旧でき、端末ごとの設定差が物理的に解消する。",
            },
            {
                "situation": "ある中堅IT部門（架空）が、配布事故の際に『誰の端末がどの版か』を集計できず、対応に半日かかった。",
                "action": "配布後Verify＋端末Inventoryを構造化ログで持ち、Rollbackは署名済み旧版へ一操作で戻せるようにする。",
                "benefit": "事故時の影響範囲が即座に見え、復旧が分単位になる。",
            },
        ],
    },
    "25": {
        "intro_human": """『気づいたら社内にSkillが200個』。
似た名前・古い手順・誰が責任者か分からない資産が混ざる。
これ、Skill運用の中盤で必ず起きる詰まりです。

ほとんどの人は、Skill運用を『数を増やすこと』と勘違いします。
本当に効くのは、提案→生成→評価→Canary→Stable→廃止までの一生（Lifecycle）を全部のSkillに付けること。Canonical Name・Category・Owner・Version・Fixture・評価点を持たせ、Generator（作る）とEvaluator（採点する）を分けて自作自演バイアスをなくす。

正常・不足・巨大・危険・対象外の5ケースFixtureで機械的に判定し、合格点未満は本番配布しない。
Skillの価値は数じゃなく、再現性・責任者・評価・廃止まで追えること。製品台帳として運用する章です。""",
        "features": [
            {
                "name": "5 Prefix命名規約",
                "summary": "Skillの分類prefixを揃え、用途と所有者をひと目で分かるようにする命名統一ルール。",
                "input": "既存Skill名群、分類カテゴリ",
                "output": "5 Prefix適用後の正規Skill名一覧",
            },
            {
                "name": "Skill Lifecycle（提案→廃止）",
                "summary": "提案・Source・Generator・Fixture・Evaluator・Canary・Stable・Deprecation・Archiveのライフサイクル管理。",
                "input": "Skill提案、評価結果",
                "output": "段階情報を持つSkill台帳",
            },
            {
                "name": "Generator / Evaluator分離",
                "summary": "Skillを作るスキルと採点するスキルを分け、自作自演バイアスを排除する設計。",
                "input": "新Skill仕様、評価Fixture",
                "output": "Generator出力＋Evaluatorによる4軸スコア",
            },
            {
                "name": "Fixture-driven開発",
                "summary": "正常・不足・巨大・危険・対象外の5ケースFixtureでSkillを開発し、評価器が機械的に判定する開発フロー。",
                "input": "Skill仕様、5ケースFixture",
                "output": "Fixture通過率と改善ポイント",
            },
            {
                "name": "Build / Validator / 重複統合",
                "summary": "skill-srcを正本としてClaude Code/Codex両方へBuild展開し、Validatorで構造検証、重複候補は統合提案する。",
                "input": "skill-src、複数Runtime対象",
                "output": "両Runtime用ビルド成果と統合候補リスト",
            },
            {
                "name": "Deprecation（廃止予告と代替先）",
                "summary": "古いSkillには代替先と終了日を示して安全に閉じる手順。利用者の移行コストを下げる。",
                "input": "廃止対象Skill、代替Skill",
                "output": "Deprecation通知、移行ガイド、終了日",
            },
        ],
        "scene": "Skillが増えると、似た名前、古い手順、評価されていない資産が混ざり始めます。美咲は数を成果にせず、提案、生成、評価、Canary、Stable、廃止というLifecycleを導入します。",
        "essay": "Skill Governanceでは、Canonical Name、Category、Owner、Version、対象Runtime、依存、Fixture、評価点を持たせます。GeneratorとEvaluatorを分離し、明確性、実用性、保守性、整合性の四軸で採点します。\n\n同じSkillをClaude Code用とCodex用に手で二重編集せず、skill-srcを正本にしてBuildします。重複は統合し、非推奨には代替先と終了日を示します。",
        "mission": "既存Skillを三つ選び、Owner・Version・Fixture・評価点・重複候補を棚卸ししてください。",
        "takeaway": "Skillの価値は数ではなく、再現性、責任者、評価、廃止まで追えることです。",
        "image_concept": "A governed skill lifecycle from proposal to generator, evaluator, canary, stable release, deprecation, and archive",
        "image_kind": "lifecycle infographic illustration",
        "usecases": [
            {
                "situation": "ある制作会社（架空）が、200個のSkillが乱立し、似た名前と古い手順が混ざって誰も全体像を把握できなくなった。",
                "action": "Canonical Name・Category・Owner・Version・Fixture・評価点を持たせ、4軸の評価器で採点する。",
                "benefit": "Skill群が製品台帳として管理でき、廃止予告も移行先付きで安全に出せる。",
            },
            {
                "situation": "ある中規模IT会社（架空）が、Claude Code用とCodex用のSkillを二重管理して、片方だけ修正された結果、社員間で動作が違う事態が起きた。",
                "action": "skill-srcを正本にしてBuildで両Runtimeへ展開する構造に変える。",
                "benefit": "二重編集の手間がなくなり、Runtime差での挙動ズレが消える。",
            },
        ],
    },
    "26": {
        "intro_human": """『CLAUDE.mdに削除禁止って書いたから安全』。
これ、攻撃や誤操作の前では1秒で破れる紙の盾です。

ほとんどの組織は、安全策を『文章で書けば守れる』と思ってます。
でも、外部社員の端末では文書が書き換えられる。Bypassは便利だから常用される。CLAUDE.mdは読み飛ばされる。
だから、強制したいことは Managed Settings / Managed MCP で個人端末から触れない場所に置き、HookのBlock Eventを構造化ログに残す。文書ではなく実行時の強制で安全を成立させる。

想定脅威は6つ（秘密漏えい・危険コマンド・Prompt Injection・誤配布・設定改変・Supply Chain）。それぞれを予防・検知・復旧の3列で守る。
KPIはBlock件数だけじゃなく誤検知率・更新成功率・復旧時間まで測る。

『守りすぎ』も『緩すぎ』も数字で見えるようにする章です。""",
        "features": [
            {
                "name": "Threat Model（6想定脅威）",
                "summary": "秘密漏えい・危険コマンド・Prompt Injection・誤配布・設定改変・Supply Chainを想定脅威として並べる出発点。",
                "input": "組織の運用構造、扱うデータ",
                "output": "6脅威それぞれの予防/検知/復旧マトリクス",
            },
            {
                "name": "Managed Settings / Managed MCP",
                "summary": "個人端末で改変できない組織Policyを固定し、文書ではなく実行時の強制で安全を成立させる仕組み。",
                "input": "強制したい設定、許可するMCP",
                "output": "Managed Settings/MCP定義ファイル",
            },
            {
                "name": "Hook Block Event のログ化",
                "summary": "HookのBlock判定を構造化ログへ落とし、誰がいつ何を止めたかを追跡可能にする観測機構。",
                "input": "Hookブロック発生、対象操作",
                "output": "構造化ログとブロック傾向の集計",
            },
            {
                "name": "KPI / 指標群",
                "summary": "Block件数だけでなく誤検知率・更新成功率・Skill失敗率・Cost・復旧時間を測る安全KPI。",
                "input": "運用ログ群",
                "output": "ダッシュボード化された安全指標",
            },
            {
                "name": "Incident運用とRunbook",
                "summary": "事故発生時の隔離・Rollback・通知・振り返りを標準化するRunbook。属人化させず素早く復旧する。",
                "input": "発生したインシデント、影響範囲",
                "output": "Runbook手順、復旧ログ、振り返り記録",
            },
            {
                "name": "Retention（ログ保持と権限）",
                "summary": "ログの保持期間と閲覧権限を決める方針。長すぎる保持と広すぎる閲覧の両方を避ける。",
                "input": "扱うログ種別、コンプラ要件",
                "output": "保持期間/閲覧権限マトリクス",
            },
        ],
        "scene": "『CLAUDE.mdに削除禁止と書いたから安全』という説明に、美咲は首を振ります。攻撃や誤操作が起きたとき、文書を無視しても止まる仕組みが必要です。Managed Policyと観測性が、組織の最後の防波堤になります。",
        "essay": "Threat Modelでは、秘密漏えい、危険コマンド、Prompt Injection、誤配布、設定改変、Supply Chainを想定します。Managed SettingsとManaged MCPで組織Policyを固定し、HookのBlock Eventを構造化ログへ残します。\n\n安全指標はBlock件数だけではありません。誤検知率、更新成功率、Skill失敗率、Incident、Cost、復旧時間を測ります。Retentionと権限を決め、Incident時の隔離、Rollback、通知、振り返りをRunbook化します。",
        "mission": "自組織のThreat Modelを五項目書き、各項目を予防・検知・復旧の三列へ割り当ててください。",
        "takeaway": "組織の安全は、強制Policy、観測、Incident対応が一体になって初めて成立します。",
        "image_concept": "An enterprise security operations room with managed policy, guarded tool access, structured event logs, metrics, and incident rollback controls",
        "image_kind": "security operations illustration",
        "usecases": [
            {
                "situation": "ある金融系IT部門（架空）が、AI導入の安全策をCLAUDE.mdで案内したが、外部社員の端末で簡単に書き換えられて事故が起きた。",
                "action": "Managed SettingsとManaged MCPで組織Policyを固定し、HookのBlock Eventを構造化ログへ残す。",
                "benefit": "文書ではなく実行時の強制で安全が成立し、誰の端末でも改変できない。",
            },
            {
                "situation": "情シス（架空）が、Block件数だけ報告しているが、誤検知が多すぎて社員から信頼を失っている。",
                "action": "誤検知率・更新成功率・Skill失敗率・Cost・復旧時間を含む指標を一緒に測る。",
                "benefit": "数字で『守りすぎ』『緩すぎ』のバランスが見え、Policy調整に根拠が持てる。",
            },
        ],
    },
    "27": {
        "intro_human": """新人にAI研修動画を渡しても、初日のセットアップでつまずいて消える。
これ、定着率が伸びない一番の原因です。

ほとんどの組織は、新人向けに『大量の資料』を渡します。
でも、知識量で勝負しても定着しません。初日に『安全なLabで・実際に成果物を作って・証拠を示して・翌日もそこから再開できる』状態まで持っていくのが正解。

この章は、それを30分で終える導入フロー（環境診断→Lab作成→成果物→証拠→再開）の設計図です。
初日Safety、Plan/Verify/Git/Skill化を実演させるBronze認定、つまずきポイントを切り分ける障害表まで揃えます。
運用開始後も、月次診断・更新確認・Incident演習を続けて知識の劣化を防ぐ。

Onboardingのゴールは『入った』じゃなく『安全に一人で一周できた』です。""",
        "features": [
            {
                "name": "30分Onboarding Flow",
                "summary": "環境診断→Lab作成→成果物→証拠→再開の5段で、新人が30分でBronze相当の最初の一周を終える導入フロー。",
                "input": "新人の端末、所属ロール",
                "output": "初日成果物と再開可能State",
            },
            {
                "name": "初日Safety",
                "summary": "初日に必ず適用する権限・削除禁止・本番遮断のセットアップ。事故ゼロでスタートさせるための最小防御。",
                "input": "新人Project、本番資源の所在",
                "output": "初日Safetyが効いたLab環境",
            },
            {
                "name": "Bronze認定",
                "summary": "Plan/Verify/Git/Skill化を実演させて合否判定する、知識クイズではなく実演ベースの初期認定。",
                "input": "実演課題、観察観点",
                "output": "Bronze合否判定と次のレベル課題",
            },
            {
                "name": "運用Cadence（月次診断/演習）",
                "summary": "Onboarding後も月次診断・更新確認・Incident演習を続け、知識と環境の劣化を防ぐ運用サイクル。",
                "input": "現職社員、運用カレンダー",
                "output": "月次診断結果、演習レポート",
            },
            {
                "name": "障害表 / Diagnostics",
                "summary": "認証・権限・Path・Versionなどつまずきやすい箇所を切り分け診断するチェック表とスクリプト。",
                "input": "詰まり報告、エラー内容",
                "output": "症状→対応の対照表と自動診断ログ",
            },
        ],
        "scene": "新人へ大量の資料を渡しても、最初の一歩で止まれば定着しません。遥が体験した会議アシスタントを、30分の導入、初日のSafety、Bronze認定、障害時Runbookへ変えます。",
        "essay": "Onboardingはインストール完了ではなく、本人が安全なLabで成果物を作り、証拠を示し、再開できる状態までを含みます。自動診断で環境を確認し、つまずきやすい認証、権限、Path、Versionを切り分けます。\n\n認定は知識問題だけでなく、Plan、Verify、Git、Skill化を実演させます。運用開始後も、月次診断、更新確認、Incident演習をCadenceへ入れます。",
        "mission": "新人が30分で終える導入手順を、環境診断・Lab作成・成果物・証拠・再開の五段階で書いてください。",
        "takeaway": "Onboardingのゴールは『入った』ではなく、『安全に一人で一周できた』です。",
        "image_concept": "A clear onboarding journey from a new laptop through setup, safety lab, first artifact, verification badge, and support runbook",
        "image_kind": "journey illustration",
        "usecases": [
            {
                "situation": "ABC人事（架空）が、新人配属時にAIガイドを渡しても初日のセットアップで詰まり、本人のやる気が消える事例が続いている。",
                "action": "30分の導入Flow（環境診断→Lab→成果物→証拠→再開）を作り、つまずきポイントを切り分け診断する。",
                "benefit": "初日にBronze相当の成果物が完成し、本人のAI導入感が一気に立ち上がる。",
            },
            {
                "situation": "情シス（架空）が、新人サポート問い合わせが配属直後に集中し、月初の業務が回らない。",
                "action": "Runbookで認証・権限・Path・Versionの障害分類と対応手順を整える。",
                "benefit": "新人が自分でRunbookを引いて解決でき、情シスの負荷が分散する。",
            },
        ],
    },
    "28": {
        "intro_human": """請求書・契約書・会議メモ・整理されてない『なんとなくフォルダ』。
派手じゃないけど、毎日の時間を一番奪うのはここです。

ほとんどの人は、こういう文書業務を『いきなりAIに加工させて』失敗します。
件数も例外も把握せず実行した結果、稟議添付のExcelが消える事故が起きる。

この章で扱うのは、文書業務の正しい順序。
まずRead-onlyで一覧と分類案を作る。次に抽出項目と例外パターンを定義する。それからDry-runで件数を確認してから本番に進む。
契約書は『法的結論』ではなく『論点整理』としてAIに任せ、最終判断は人。

整理・削除は元データを残し、移動先を明示し、結果一覧を出す可逆的な手順で。
派手じゃないけど、ここから自動化できる業務が一気に広がります。""",
        "features": [
            {
                "name": "請求書Folder棚卸し",
                "summary": "Read-onlyで請求書フォルダを一覧化し、抽出項目と例外パターンを定義してから自動化に進む業務型。",
                "input": "請求書PDF/画像フォルダ、台帳の現状",
                "output": "抽出項目定義、例外一覧、Dry-run結果",
            },
            {
                "name": "Folder整理（可逆な分類）",
                "summary": "元データを残し、移動先を明示し、結果一覧を出す可逆的な整理手順。削除ではなく分類から始める。",
                "input": "整理対象フォルダ、分類ルール",
                "output": "分類後フォルダと整理結果レポート",
            },
            {
                "name": "契約書論点整理",
                "summary": "法的結論ではなく、契約書から論点を抽出して人の判断に渡すワークフロー。AIに最終判断をさせない型。",
                "input": "契約書PDF、確認したい観点",
                "output": "論点一覧と人が判断すべき箇所のハイライト",
            },
            {
                "name": "会議Assistant本番化",
                "summary": "第4章で作った会議アシスタントを実業務で運用するための例外対応・テンプレ整備・配布手順。",
                "input": "本番議事録依頼、社内テンプレ",
                "output": "実業務で回る会議AssistantとSkill群",
            },
            {
                "name": "週報生成",
                "summary": "会議データを連結し、週報・タスク・連絡文へ展開する定期業務化。書く時間ではなく見る時間に変える。",
                "input": "週内の会議メモ、タスクログ",
                "output": "週報Markdown/HTMLと未対応タスクリスト",
            },
        ],
        "scene": "ここから四人は現場へ戻ります。最初の机には請求書、契約書、会議メモ、整理されていないフォルダが積まれていました。どれも派手ではありませんが、時間を奪う仕事です。",
        "essay": "文書・ファイル業務では、まずRead-onlyで一覧と分類案を作り、変更前に対象と件数を確認します。請求書は抽出項目と例外を定義し、契約書は法的結論ではなく論点整理として扱い、会議データは議事録・タスク・週報へ連結します。\n\n整理や削除は、元データを残し、移動先を明示し、結果一覧を出す可逆的な手順から始めます。",
        "mission": "一つの実務フォルダをRead-onlyで棚卸しし、変更せずに分類案と例外一覧を作ってください。",
        "takeaway": "文書業務は、いきなり加工せず、抽出項目・例外・可逆性を先に決めます。",
        "image_concept": "An AI-assisted office desk organizing invoices, contracts, meeting notes, and messy folders into structured, reviewable outputs",
        "image_kind": "practical editorial illustration",
        "usecases": [
            {
                "situation": "ABC商事の経理（架空）が、毎月100枚の請求書PDFを手動で台帳入力し、毎月末に残業4時間を発生させている。",
                "action": "Read-onlyで請求書フォルダの一覧と分類案を作り、抽出項目・例外を定義してから自動化する。",
                "benefit": "例外検出を残しつつ標準項目は自動入力でき、残業時間が大幅に減る。",
            },
            {
                "situation": "中小法務（架空）が、契約書PDFをAIに『この契約問題ない？』と聞き、誤った法的結論を得て社内へ展開しかけた。",
                "action": "契約書は法的結論ではなく論点整理として扱い、最終判断は人が行う運用ルールを書く。",
                "benefit": "AIは負荷の高い論点抽出を担い、人は判断に集中できる。誤断のリスクが消える。",
            },
        ],
    },
    "29": {
        "intro_human": """『毎週末、YouTubeとSNS見て終わる』。
情報収集だけで時間が消えて、教材や記事が作れない。

ほとんどの人は、調査を『集める量』で評価します。
でも本当に効くのは『目的に沿った選別』。一般的な人気じゃなく、自分の番組コンセプトや学習目的にとっての価値で素材を選ぶ仕組みを作ります。

この章で組むのは、対象・期間・除外条件・評価軸を内蔵した動画調査Skill。番組Profileを参照して『その人にとっての価値』だけ残す。発言と事実を区別し、重複は統合する。
最後は News Dashboard で、更新時刻・出典・未確認情報を表示する1ページHTMLに変換する。

良い調査は情報量じゃなく、選別と出典の透明性で決まります。
情報収集が10分に収まる生活がここから始まります。""",
        "features": [
            {
                "name": "YouTube Research Skill",
                "summary": "対象・期間・除外条件・評価軸を持つ動画調査Skill。検索→転記→分析→要約を一連で回す。",
                "input": "テーマ、対象期間、除外したい動画種別",
                "output": "出典付き動画要約と評価軸スコア",
            },
            {
                "name": "番組Profile",
                "summary": "自分の番組・学習目的を定義したProfile。一般的な人気ではなく自分にとっての価値で素材を選ぶための基準。",
                "input": "番組コンセプト、視聴者像、避けたい話題",
                "output": "Profileファイルと選別基準",
            },
            {
                "name": "SNS/動画から教材化",
                "summary": "発言を重複統合し、事実確認が必要な箇所を分離して教材に組み立てる加工パイプ。",
                "input": "SNS投稿・動画文字起こし",
                "output": "重複統合済み教材ドラフトと要検証リスト",
            },
            {
                "name": "個人学習Loop",
                "summary": "INTERESTS.mdと連動し、個人の苦手・関心に沿って復習問題・調査テーマを生成する学習ループ。",
                "input": "個人Profile、最近のログ",
                "output": "復習問題、調査テーマ、進捗状態",
            },
            {
                "name": "News Dashboard",
                "summary": "更新時刻・出典・未確認情報を表示する1ページHTMLニュースダッシュボード。重複統合で巡回時間を短縮。",
                "input": "RSS/API/Web情報源、更新間隔",
                "output": "単一HTMLのNews Dashboard",
            },
        ],
        "scene": "次の机には、YouTube、SNS、論文、ニュースが並んでいます。遥は情報を集めるだけで満足せず、自分の番組や学習目的に合う形へ変えたいと考えます。",
        "essay": "調査・Content業務では、対象、期間、一次情報、除外条件、評価軸をSkillへ持たせます。番組ProfileやINTERESTS.mdを参照すると、一般的な人気ではなく、その人にとって価値のあるテーマを選べます。\n\n動画やSNSから教材を作るときは、発言を重複統合し、事実確認が必要な箇所を分離します。News Dashboardは更新時刻、出典、未確認を表示します。",
        "mission": "一つの調査テーマで、公式情報・解説・SNSを分けて集め、重複を統合した一ページのHTMLレポートを作ってください。",
        "takeaway": "良い調査は情報量ではなく、目的に沿った選別と出典の透明性で決まります。",
        "image_concept": "A research studio combining videos, social posts, papers, and news into a personalized evidence-based learning report",
        "image_kind": "editorial research illustration",
        "usecases": [
            {
                "situation": "ある教育系YouTuber（架空）が、教材作成のために動画とSNSを大量視聴し、毎週末が情報収集だけで終わっている。",
                "action": "Skillに対象・期間・一次情報・除外条件・評価軸を持たせ、INTERESTS.mdを参照させる。",
                "benefit": "自分にとって価値のある素材だけが残り、教材作成の時間が情報整理から本質的な構成へ移る。",
            },
            {
                "situation": "個人投資家（架空）が、毎朝のニュースサイトを巡回しているが、重複情報で時間を浪費している。",
                "action": "News Dashboardで更新時刻・出典・未確認情報を表示する単一HTMLを作る。",
                "benefit": "重複が統合され、未確認情報だけが目立つ。情報収集が10分に収まる。",
            },
        ],
    },
    "30": {
        "intro_human": """『AIで作ったアプリ、動いたから公開した』。
1日後、エッジケースで毎日エラーが出てユーザーが離脱。
これ、ほとんどの個人開発で起きてる事故です。

ほとんどの人は、『画面が出たら完成』だと思ってます。
でも、デモと製品の間には品質の橋が必要です。エラー時の挙動、データ保存、テスト、変更履歴、戻し方。最低でもこれが揃わないと、他人に渡せません。

この章では、Localで価値を確かめる最小アプリの作り方、Bug修正は必ず再現テストから始める運用、大規模Migrationは段階移行＋Rollback条件、独立コンテキストで最終チェックするFresh Reviewまで扱います。
健康・投資のような高リスク領域では、意思決定を自動化せず情報整理に限定する設計指針も。

アプリの完成は『画面が出ること』じゃなく、失敗を再現し検証し戻せること。""",
        "features": [
            {
                "name": "Local Task Manager（最小アプリ）",
                "summary": "Localで価値を確かめ、要件・データ境界・Test・Schemaを揃える最小Webアプリの作り方。",
                "input": "タスク管理の要件、データスキーマ",
                "output": "Local起動するTask Managerと検証ログ",
            },
            {
                "name": "Bug修正（再現手順から）",
                "summary": "Bug報告を必ず再現手順から扱い、修正前に再現テストを書く品質運用。直したつもりを防ぐ。",
                "input": "Bug報告、現状の挙動",
                "output": "再現テストと修正Patch、Diff",
            },
            {
                "name": "大規模Migration",
                "summary": "調査・段階移行・互換性・Rollbackを持たせる大規模移行の運用設計。一気に切り替えない。",
                "input": "旧仕様、新仕様、影響範囲",
                "output": "段階移行計画とRollback条件",
            },
            {
                "name": "Fresh Review",
                "summary": "実装と切り離した独立コンテキストで成果物を見直す最終チェック。迎合バイアスのない指摘を得る。",
                "input": "実装済み機能、レビュー観点",
                "output": "独立レビュー指摘と修正アクション",
            },
            {
                "name": "Diet App / 投資支援App / 世界Dashboard",
                "summary": "健康・投資・グローバル情報のような高リスク領域で、意思決定を自動化せず情報整理と注意喚起に機能を限定する設計例。",
                "input": "扱うリスク領域、ユーザー像",
                "output": "意思決定支援に限定した安全アプリ仕様",
            },
        ],
        "scene": "遥はタスク管理アプリを作り、蓮は『動いた』の次に、エラー時、データ保存、テスト、変更履歴を確認します。個人用デモと、他人が使うApplicationの間には、品質の橋が必要です。",
        "essay": "Application開発では、Localで価値を確かめ、要件とデータ境界を固定し、TestとSchemaで動作を検証します。Bug修正は再現手順から始め、大規模Migrationは調査、段階移行、互換性、Rollbackを持たせます。\n\n健康や投資のような高リスク領域は、意思決定を自動化せず、情報整理と注意喚起へ限定します。リアルタイムDashboardも、出典、更新失敗、誤差を表示します。",
        "mission": "小さなLocal Appへ一つ機能を追加し、再現テスト、正常系、異常系、Diff、Rollbackを記録してください。",
        "takeaway": "アプリの完成は画面が出ることではなく、失敗を再現し、検証し、戻せることです。",
        "image_concept": "A local web application evolving from prototype to tested product with data schema, automated tests, bug reproduction, and rollback",
        "image_kind": "application lifecycle illustration",
        "usecases": [
            {
                "situation": "ある個人開発者（架空）が、AIで作ったタスク管理アプリが『動いた』と思って公開したら、エッジケースで毎日エラーが出てユーザー離脱が始まった。",
                "action": "再現テスト・正常系・異常系・Diff・Rollback手順を実装と同時に作る運用に変える。",
                "benefit": "公開後の事故時も再現と巻き戻しが両方できる。ユーザー信頼が壊れない。",
            },
            {
                "situation": "中小ヘルスケア事業者（架空）が、健康Dashboardに自動アドバイス機能を入れたら誤情報のリスクで弁護士からNGが出た。",
                "action": "意思決定を自動化せず、情報整理と注意喚起へ機能を限定する。出典・更新失敗・誤差は明示する。",
                "benefit": "法的リスクが下がり、機能を成立させながら世に出せる。",
            },
        ],
    },
    "31": {
        "intro_human": """『AIで作ったLP、そのまま本番に出した』。
あとから見たら、テスト用Analytics IDと本番APIキーがソースに残ってた。
これ、毎週どこかの組織で起きてます。

ほとんどの人は、公開を『最後のボタンを押す作業』だと思ってます。
でも公開は、情報・ブランド・権限・リンク・戻し方を確認する別の工程です。
Preview公開→秘密情報・リンク・公開範囲・スマホ表示・A11yチェック→本番、というQuality Gateを通す。

この章では、LP・スライド・レポートで同じDesign Systemを再利用する運用、HTMLを正本にしてPPT/PDFをExportする標準手順、フォント崩れの直し方の順序まで揃えます。

公開は生成の続きじゃなく、独立した品質・安全ゲート。
事故をなくす一番効くスイッチが、ここに入ります。""",
        "features": [
            {
                "name": "LP制作Flow",
                "summary": "Wireframe→Design System→Codeで作ったLPを、公開を見据えて整える章末仕上げの制作ライン。",
                "input": "LP目的、Design System、コンテンツ素材",
                "output": "公開直前のLP実装と確認用Preview",
            },
            {
                "name": "Design System再利用",
                "summary": "LP・スライド・レポートで同じDesign Systemを参照し、ブランド一貫性を維持する再利用ルール。",
                "input": "既存Design System、新規制作物",
                "output": "システム参照済みの新規制作物",
            },
            {
                "name": "PPT / PDF Export",
                "summary": "HTML正本からPPT/PDFへExportする標準手順。フォント崩れ・ページ分割を事前にチェックする。",
                "input": "HTML正本、Export設定",
                "output": "崩れ確認済みのPPTX/PDF",
            },
            {
                "name": "Deploy / Preview Gate",
                "summary": "Deploy前にSecret・環境変数・公開範囲・Analytics・Rollbackを確認し、Previewレビューを通す公開ゲート。",
                "input": "公開予定ビルド、本番設定",
                "output": "Preview承認ログと本番Deploy可否判定",
            },
        ],
        "scene": "資料やLPが完成すると、次に『共有したい』『公開したい』という欲求が生まれます。公開は最後のボタンではなく、情報、ブランド、権限、リンク、戻し方を確認する別の工程です。",
        "essay": "Design Systemを再利用すると、LP、スライド、レポートに一貫性が出ます。PPTやPDFへExportする場合も、元のHTMLを正本にし、崩れ、フォント、ページ分割を確認します。\n\nDeploy前にはSecret、環境変数、公開範囲、Analytics、Rollbackを確認し、Previewでレビューしてから本番へ進めます。",
        "mission": "既存HTMLをPreview公開し、スマホ表示・リンク・秘密情報・Rollback手順を確認してから、本番可否を判断してください。",
        "takeaway": "公開は生成の続きではなく、独立した品質・安全Gateです。",
        "image_concept": "A design system flowing into a landing page, slide deck, PDF export, preview environment, and carefully gated production release",
        "image_kind": "publishing workflow illustration",
        "usecases": [
            {
                "situation": "中小マーケ会社（架空）が、AIで作ったLPを即本番公開した結果、テスト用Analytics IDや本番用APIキーが残ったまま外に出てしまった。",
                "action": "Preview公開→秘密情報・リンク・公開範囲・スマホ表示・A11yチェック→本番、というQuality Gateを設ける。",
                "benefit": "公開前事故が体系的に防げ、本番公開を安心して進められる。",
            },
            {
                "situation": "ある提案チーム（架空）が、HTMLからPPT/PDFをExportするたびにフォントが崩れ、毎回手動修正に数時間を奪われている。",
                "action": "Export時にレイアウト・フォント・ページ分割を確認する標準Checkを書く。",
                "benefit": "崩れ箇所だけを集中修正でき、Export成果物の品質が安定する。",
            },
        ],
        "expansion": {
            "title": "実務に落とすときの補足",
            "points": [
                {
                    "label": "公開前に最低限揃えるもの",
                    "body": "Preview URL、スマホ表示確認、内部リンクと外部リンクの到達確認、Analytics・APIキー等の秘密情報の有無、Rollback手順の5点を1枚の事前チェックに固定します。ここを言語化していない組織では、毎回担当者の記憶頼みで公開され、必ずいつか事故が起きます。",
                },
                {
                    "label": "Export崩れの直し方の順序",
                    "body": "PPT/PDFへExportして崩れた時、HTML側を直すかExport設定を直すかで悩む前に、まず正本はHTMLだと宣言します。崩れの再現箇所を1ページだけ抜き出して原因を見極め、フォント置換・ページ分割・余白の3観点で順に潰すと最短で安定します。",
                },
                {
                    "label": "測ると効く指標",
                    "body": "公開回数、公開前事故件数、Rollback回数、Export修正に費やした時間を月単位で記録します。事故ゼロを目指すのではなく、Rollback回数が一定範囲内に収まっているかを健全性の指標にすると、過剰な慎重さで止まらなくなります。",
                },
                {
                    "label": "次の章への接続",
                    "body": "公開Gateの感覚が掴めると、次章の毎日業務の自動化でも『失敗時の戻し方』を最初に決められるようになります。公開とは独立した品質ゲートだという意識が、自動化全体の安全装置として効いてきます。",
                },
            ],
        },
    },
    "32": {
        "intro_human": """『毎朝のニュース整理と、会議後のタスク登録と、月次のSkill評価』。
全部、自分が手動でやってませんか。

ほとんどの人は、繰り返しが見えても『自分で頑張る』を選びます。
でも、人を速くする努力には上限があります。仕組みへ移すのが正解。

この章で扱うのは、毎朝Brief（予定・未返信・締切を1枚に圧縮）、会議からTask Boardへ流し込む橋渡し、Skill改善Loop（実行ログ・失敗Fixture・評価点を集めてCanary更新）。
そして自動化成熟度モデル（個人手作業→再利用→半自動→監視付き自動の4段）で、業務ごとに今どこにいるかを月次で記録する。

自動化は頻度だけで決めません。入力の安定性・検証可能性・失敗時の人への戻しやすさで選ぶ。
休んでも止まらない情報基盤が、ここで生まれます。""",
        "features": [
            {
                "name": "毎朝Brief",
                "summary": "朝一に予定・未返信・締切・重要連絡を1枚に圧縮し、今日の動き方を10秒で把握できるようにする補佐機能。",
                "input": "Calendar・メール未返信・締切Task・Slack/メンション履歴",
                "output": "今日の予定リスト・準備が必要な会議・返信下書き・リスクメモ",
            },
            {
                "name": "会議→Task Board",
                "summary": "議事録からタスクを抽出してTask Boardへ流し込み、重複登録と担当者確認を持たせる橋渡し機能。",
                "input": "会議文字起こし、現Task Board",
                "output": "重複統合済みのTaskエントリと担当者割り当て",
            },
            {
                "name": "Skill改善Loop",
                "summary": "実行ログ・失敗Fixture・評価点を集めてSkillを更新し、Canary経由で再配布する継続改善ループ。",
                "input": "Skill実行ログ、失敗Fixture、評価スコア",
                "output": "改善されたSkillとCanary配布結果",
            },
            {
                "name": "自動化成熟度モデル",
                "summary": "個人手作業→再利用→半自動→監視付き自動の4段で、業務ごとの自動化レベルを段階的に上げる尺度。",
                "input": "対象業務、入力安定性、副作用の有無",
                "output": "業務別の現在レベルと次のターゲット段階",
            },
        ],
        "scene": "毎朝のニュース、会議後のTask Board、月次のSkill評価。繰り返しが見えたとき、四人は人を速くするのではなく、仕組みへ移すことを考えます。",
        "essay": "継続業務は、入力が安定し、完了条件が検証でき、失敗時に人へ戻せるものから自動化します。毎朝Briefは情報源と更新時刻を固定し、会議からTask Boardへの流れは重複登録と担当者確認を持たせます。\n\nSkill改善Loopでは、実行ログ、失敗Fixture、評価点を集め、Canaryで更新します。成熟度は、個人の手作業から再利用、半自動、監視付き自動へ段階的に上げます。",
        "mission": "週一回以上繰り返す仕事を一つ選び、入力の安定性・検証可能性・副作用・失敗時対応を採点してください。",
        "takeaway": "自動化は頻度だけで決めず、安定した入力と安全な失敗経路がある仕事から始めます。",
        "image_concept": "A calm operations rhythm showing morning brief, meeting-to-task flow, scheduled skill evaluation, and monitored automation maturity stages",
        "image_kind": "operations illustration",
        "usecases": [
            {
                "situation": "ある営業企画（架空）が、毎日のニュースとTask Boardを手動更新しており、休む日は誰も状況を把握できない。",
                "action": "情報源と更新時刻を固定したMorning Brief Skillを作り、毎朝Scheduledで配信する。",
                "benefit": "休んでも止まらない情報基盤になり、属人化と業務継続性のリスクが消える。",
            },
            {
                "situation": "中堅人事（架空）が、毎月のSkill評価を手作業で集計し、月初の3日間を奪われている。",
                "action": "実行ログ・失敗Fixture・評価点を集めるSkill改善LoopをCanary更新と組む。",
                "benefit": "評価が自動化され、人は問題のあるSkillだけ集中的に直せる。",
            },
        ],
        "expansion": {
            "title": "実務に落とすときの補足",
            "points": [
                {
                    "label": "自動化候補の優先順位",
                    "body": "週1回以上の頻度・入力フォーマットが安定・完了条件が機械検証できる・失敗しても人へ戻せる、の4条件を満たす業務だけを最初の自動化対象にします。条件を満たさない業務を強引にSkill化すると、最初の数週間は動いても運用フェーズで誤動作が出てきます。",
                },
                {
                    "label": "Morning Brief の入力源を固定する",
                    "body": "Calendar・メール・Slackメンション・締切Taskなど、毎朝の情報源を毎回違う方法で取りに行くと、ある日急に空欄になります。情報源と更新時刻を仕様として書き、対象が増えた時はSkillを直すのではなくRegistryへ追記する設計にします。",
                },
                {
                    "label": "成熟度を測る尺度",
                    "body": "個人手作業→再利用→半自動→監視付き自動の4段階で、対象業務がいまどこにいるかを月次で記録します。一気に最終段階を目指さず、半自動で1ヶ月動かしてから監視付き自動へ進めると、運用事故がほぼ起きません。",
                },
                {
                    "label": "次の章への接続",
                    "body": "自動化を増やすほど、過去の失敗を学習資産へ変換する次章のテーマが重要になります。動くものが増えるほど、止まったときの原因分析と再発防止の仕組みが品質を決めるからです。",
                },
            ],
        },
    },
    "33": {
        "intro_human": """『同じ事故、また起きた』。
振り返りメモを書いて満足して、半年後また同じパターンで詰まる。
これ、ほとんどの組織で延々と繰り返されてます。

ほとんどの人は、失敗を『反省で終わらせて』ます。
でも反省は、人の記憶に依存する仕組み。次に同じ条件が来た時、誰も覚えてません。
正解は、失敗をRule・Skill・Hook・Runbookのどれかに必ず変換して、二度と人の注意力に頼らないこと。

この章で扱うのは、巨大CLAUDE.md・無検証完了・Bypass常用・全社即時配布など、繰り返し起きる失敗を表にする台帳。人・手順・権限・検証・配布の5観点で根を分け、対策の置き場所を1つに絞る判断軸。

失敗は記録するだけじゃ意味がない。次回のRule・Skill・Hookへ変換して初めて学習資産になります。""",
        "features": [
            {
                "name": "失敗Pattern台帳",
                "summary": "巨大CLAUDE.md・無検証完了・Bypass常用・全社即時配布など、繰り返し起きる失敗を表にして再発防止へ変換する一覧。",
                "input": "発生したトラブル、関係者の証言",
                "output": "失敗→対策が対になった共有可能なPattern表",
            },
            {
                "name": "失敗の5観点分解",
                "summary": "人・手順・権限・検証・配布の5軸で失敗の根を分け、どこに防御を置くかを決める分析フレーム。",
                "input": "発生インシデント、状況メモ",
                "output": "5観点で分解した原因と対策設置先",
            },
            {
                "name": "Rule/Skill/Hook/Runbookへの落とし込み",
                "summary": "失敗を反省で終わらせず、Rule・Skill・Hook・Runbookのどれに変換するかを必ず決める運用ルール。",
                "input": "5観点分解結果",
                "output": "再発防止のための新規ルール/スキル/フック/Runbook",
            },
        ],
        "scene": "最後に四人は、うまくいった話ではなく、何度も起きた失敗を壁へ貼りました。巨大なCLAUDE.md、無検証の完了、Bypass常用、同じ会話の引き延ばし、全社即時配布。失敗Patternは、最も実用的な教材です。",
        "essay": "失敗には共通する構造があります。目的が曖昧、境界が広すぎる、証拠がない、正本が二つある、戻せない、変動情報を固定知識として扱う。個別のトラブルとして終わらせず、Rule、Skill、Hook、Runbookへ改善を戻します。\n\n失敗を責めるのではなく、次に同じ条件が来たとき自動で気づける仕組みへ変えることが、ハーネスの成長です。",
        "mission": "最近の失敗を一つ選び、原因を人・手順・権限・検証・配布の観点で分解し、再発防止の置き場所を決めてください。",
        "takeaway": "失敗を記録するだけでなく、次回のRule・Skill・Hookへ変換して初めて学習になります。",
        "image_concept": "A wall of common AI workflow pitfalls being converted into safeguards, checklists, tests, and reusable lessons",
        "image_kind": "editorial lessons-learned illustration",
        "usecases": [
            {
                "situation": "ある制作チーム（架空）が、AIが古い情報のまま動く事故を毎月起こすが、振り返りメモを書くだけで終わって再発を防げていない。",
                "action": "失敗を人・手順・権限・検証・配布で分解し、Rule/Skill/Hook/Runbookのどこへ落とすか決める。",
                "benefit": "失敗が組織の改善資産となり、同じ条件が来たら自動で気づける仕組みへ変換できる。",
            },
            {
                "situation": "情シス（架空）が、社員がBypass常用したことによる事故をたびたび経験し、注意喚起では止まらないと判明した。",
                "action": "BypassをHookで物理ブロックし、Runbookで例外申請の手順を書く。",
                "benefit": "便利さの誘惑が物理的に断たれ、必要時だけ手続きを経て解除できる。",
            },
        ],
        "expansion": {
            "title": "実務に落とすときの補足",
            "points": [
                {
                    "label": "失敗台帳を続けるための仕組み",
                    "body": "失敗Patternは『書こうと思った時に書く』運用では絶対に続きません。インシデント発生時に必ず1行残すRunbookと、月末に台帳を読み返す15分の枠を予定として固定します。書く労力をゼロに近づけることが、最大の継続要因です。",
                },
                {
                    "label": "5観点分解の使い方",
                    "body": "人・手順・権限・検証・配布のうち、対策を置く場所は必ず1つに絞ります。複数に分散すると責任の所在がぼやけ、結局どれも実装されません。最も影響の大きい1観点へ置き、他観点は『今回は対象外』と明示することで、対策の実装率が劇的に上がります。",
                },
                {
                    "label": "対策の落とし先の選び方",
                    "body": "Rule（CLAUDE.md）は読み返さないと効きません。Skillは呼ばれて初めて動きます。Hookは無条件に動きます。Runbookは事故時に開きます。失敗の性質を見て『無条件に止めるべきか／その瞬間だけ呼べばいいか』を分けると、過剰防御も穴も出にくくなります。",
                },
                {
                    "label": "次の章への接続",
                    "body": "失敗をHook/Skill/Rule/Runbookへ変換する設計が身につくと、次の組織展開フェーズで『全社員に同じ防御を物理配布する』思想がそのまま使えます。失敗対策は個人の記憶ではなく配布物として育てる、というのが組織展開の核心です。",
                },
            ],
        },
    },
    "34": {
        "intro_human": """『要件定義、毎回項目を思い出しながら書いてる』。
そして毎回、何かが抜けてクライアント手戻り。

ほとんどの人は、テンプレートを『手抜きの道具』だと誤解してます。
本当のテンプレートは、思考を省くためじゃなく、抜けを減らし会話の前提を揃えるための道具です。

この章では、全社共通の基盤Baseline・案件用のProject CLAUDE.md・Requirements/Implementation Plan/Completion Reportの3点セット・Quality Gate Skill・Fresh Reviewer Agent・Definition of Doneを揃えます。
正本とVersionを持たせ、古いコピーが残らない配布方法とセットで運用。

テンプレートは答えじゃなく、考えるべき問いを再現可能にする道具。
これが揃うと、新しい案件でも『最初の30分』で前提が揃います。""",
        "features": [
            {
                "name": "全社共通CLAUDE.md（Baseline）",
                "summary": "通信・標準ワークフロー・安全・品質・Gitなどを揃えた、全プロジェクト共通の基盤Baseline。",
                "input": "組織共通方針、必須安全項目",
                "output": "全社共通CLAUDE.md Baselineテンプレ",
            },
            {
                "name": "Project CLAUDE.md テンプレ",
                "summary": "Purpose・Architecture・Commands・Required workflow・Constraints・Do notを揃えた案件単位のテンプレ。",
                "input": "案件の目的、技術スタック、禁止事項",
                "output": "案件用CLAUDE.md初版",
            },
            {
                "name": "Requirements / Implementation Plan / Completion Report",
                "summary": "要件定義・実装計画・完了報告の3点セットを揃え、案件横断で抜けを減らす標準テンプレ群。",
                "input": "新案件、進行中のタスク",
                "output": "3テンプレに沿った各フェーズ成果物",
            },
            {
                "name": "Quality Gate Skill",
                "summary": "テンプレ通過を自動チェックし、空欄や曖昧な完了主張を弾く品質ゲートSkill。",
                "input": "テンプレ提出物",
                "output": "Gate判定とブロック理由レポート",
            },
            {
                "name": "Fresh Reviewer Agent",
                "summary": "実装者と別文脈の独立Reviewer Agent。要件・安全・保守性で成果物を採点する。",
                "input": "完了報告、関連ファイル",
                "output": "独立コンテキストからの指摘リスト",
            },
            {
                "name": "Definition of Done",
                "summary": "PJ開始時に合意し書面化する『完成』の共通定義。納品時の認識ズレを未然に防ぐカード。",
                "input": "PJ目的、納品物、検証条件",
                "output": "PJごとに合意されたDoD",
            },
        ],
        "scene": "理解した内容を毎回白紙から書く必要はありません。四人は、全社共通、Project、要件定義、実装計画、完了報告、Quality Gate、Reviewer、Definition of Doneを道具箱へまとめます。",
        "essay": "テンプレートは思考を省くためではなく、抜けを減らし、会話の前提を揃えるために使います。すべての項目を機械的に埋めるのではなく、不要な項目は理由を持って外します。\n\nコピー後にProject固有の制約へ調整し、実際の失敗を反映して更新します。正本とVersionを持たせ、古いコピーが残らない配布方法と組み合わせます。",
        "mission": "Requirements TemplateとCompletion Reportを自分の案件へコピーし、実際の内容で一度完成させてください。",
        "takeaway": "テンプレートは答えではなく、考えるべき問いを再現可能にする道具です。",
        "image_concept": "A professional toolkit containing reusable project guidance, requirements, plans, quality gates, reviewer briefs, and definition-of-done cards",
        "image_kind": "editorial toolkit illustration",
        "usecases": [
            {
                "situation": "ABCコンサルのプロジェクトマネージャ（架空）が、要件定義のたびに項目を思い出しながら書き、毎回抜けが出てクライアント手戻りが発生している。",
                "action": "Requirements・Implementation Plan・Completion Reportのテンプレを揃え、案件ごとにコピーして埋める。",
                "benefit": "考えるべき項目が抜けなくなり、レビュー時の追加質問が減って初稿の合格率が上がる。",
            },
            {
                "situation": "新人マネージャ（架空）が、Definition of Doneを定義できず、毎回『完成』の認識ズレで揉めている。",
                "action": "Definition of Doneカードをテンプレ化し、PJ開始時に必ず合意して書面化する。",
                "benefit": "『完成』の定義が共通化され、納品時の認識ズレが激減する。",
            },
        ],
    },
    "35": {
        "intro_human": """『教材をHTMLにしたから完成』。
でも受講者がどこで止まったか、何を実践したかは分からないまま。
これ、社内研修の8割が抱える詰まりです。

ほとんどの組織は、教材を『PDFやHTMLで配るだけ』で終わってます。
でも本当に必要なのは、本人の現在地・次の一操作・期待結果・証拠・再開地点が常に見える学習アプリ。
本文をLesson JSONに分解し、進捗をseen/practiced/verified/appliedの4段階で持つ。変動するモデル名やUIはFeature Registryで動的差し替え。ブラウザから任意Shellを実行させず、許可コマンドだけ動かすLocal Companionで連携する。

学習アプリの中心は本文表示じゃありません。行動・証拠・状態・再開です。
ここを設計すると、修了判定が客観的になります。""",
        "features": [
            {
                "name": "教科書アプリ Content Model",
                "summary": "Role別Path・Lesson・前提・成果物・Check・Feature Registry・進捗・質問履歴を構造化した学習データモデル。",
                "input": "本文テキスト、章構成、進捗ステータス案",
                "output": "Content Modelに沿ったJSONデータ",
            },
            {
                "name": "Lesson JSON Schema",
                "summary": "1Lessonの前提・成果物・チェック・所要時間・版情報を機械検証可能にするJSON Schema。",
                "input": "Lesson原稿、検証ルール",
                "output": "Schema検証通過済みLesson JSON",
            },
            {
                "name": "Feature Registry連携",
                "summary": "変動するモデル名・コマンド・UIをLesson本文に埋め込まず、Registry参照で動的差し替えする仕組み。",
                "input": "変動情報のキー、Registryデータ",
                "output": "Registry参照で差し替えされたLesson表示",
            },
            {
                "name": "Progress State",
                "summary": "seen/practiced/verified/applied の4段階進捗を保存し、本人と管理者の両方から見える学習State。",
                "input": "Lesson完了イベント、証拠提出",
                "output": "保存された進捗Stateと修了判定",
            },
            {
                "name": "Allowlist付き Local Companion",
                "summary": "ブラウザから任意Shellを実行せず、Local Companionが許可コマンドだけ動かす安全な実行連携。",
                "input": "ブラウザからの実行要求、Allowlist定義",
                "output": "許可コマンドの実行結果、拒否ログ",
            },
        ],
        "scene": "教科書をHTMLへしただけでは、遥が途中で止まった場所も、何を実践したかも分かりません。そこで本文をLesson Dataへ分け、ナビゲーターが状態を読みながら次の一操作を案内する学習アプリを設計します。",
        "essay": "最適な教科書アプリはPDF Viewerではありません。Role別Path、Lesson、前提、成果物、Check、Feature Registry、進捗、質問履歴を構造化します。進捗はseen、practiced、verified、appliedの段階で持ちます。\n\nブラウザから任意Shellを直接実行せず、将来はAllowlist付きLocal Companionと連携します。画面は現在地、次の一操作、期待結果、証拠、保存・再開を中心に設計します。",
        "mission": "一章をLesson JSONへ変換し、前提・成果物・チェック・所要時間・版情報をSchemaで検証してください。",
        "takeaway": "学習アプリの中心は本文表示ではなく、行動・証拠・状態・再開です。",
        "image_concept": "A browser-based learning navigator with role paths, lesson cards, progress states, next action, evidence checks, and save-resume controls",
        "image_kind": "product concept illustration",
        "usecases": [
            {
                "situation": "ある教育担当（架空）が、HTML教材をPDFビューアで配り、受講者の進捗が分からず修了判定もできない状況に詰まっている。",
                "action": "本文をLesson JSONへ分解し、前提・成果物・チェック・進捗（seen/practiced/verified/applied）をSchema検証する。",
                "benefit": "誰がどこまでできたかが本人にも管理者にも見え、修了判定が客観的にできる。",
            },
            {
                "situation": "オンラインスクール（架空）が、ブラウザから任意Shellを実行する設計で監査NGを受けた。",
                "action": "ブラウザ実行はAllowlist付きLocal Companionへ任せ、画面側は次の一操作・期待結果・証拠提示に専念する。",
                "benefit": "監査要件を満たしつつ、学習者は手元で安全に実行できる設計に置き換わる。",
            },
        ],
    },
    "36": {
        "intro_human": """『AI全社展開、半年計画でスタートしたら3ヶ月目で停滞』。
これ、大きな構想を一気に動かそうとした時の典型パターンです。

ほとんどの組織は、AI導入を『プロジェクト』として組みます。
でも、検証可能な一週間の積み重ねで進めないと、必ず途中で疲弊します。

この章で扱うのは、最初の30日を4週間に割る具体ロードマップ。
1週目はInventoryとPolicy（動かさない作業）、2週目はBuildとTest、3週目はCanary配布とBronze研修を並走、4週目はPilot拡大とStable Release。各週にExit条件とRollback地点を置く。
30日後は、導入時間・更新率・認定完了・Rollback Drill・Critical Gap・Skill二重編集を経営報告用に測る。

変革は『大きな完成図』じゃなく、検証可能な一週間の積み重ねで進めます。""",
        "features": [
            {
                "name": "Week 1: Inventory & Policy",
                "summary": "現有資産の棚卸しとPolicy策定。動かす前に正本と禁止事項を決める1週目の作業塊。",
                "input": "現状のSkill群・Hook群・運用ルール",
                "output": "Inventory表、初期Policyドラフト",
            },
            {
                "name": "Week 2: Build & Test",
                "summary": "正本Buildと評価Fixture整備を行う2週目。Canaryへ流す前に品質基準を満たす土台作り。",
                "input": "正本ソース、Fixture",
                "output": "Buildパイプラインと初期テスト通過状態",
            },
            {
                "name": "Week 3: Canary & Bronze研修",
                "summary": "限定範囲のCanary配布と新人Bronze研修を並走させる3週目。小さく失敗を発見する段階。",
                "input": "Canary対象、研修対象社員",
                "output": "Canary実績ログとBronze認定者リスト",
            },
            {
                "name": "Week 4: Pilot & Stable Release",
                "summary": "Pilot範囲拡大とStable Releaseを行う4週目。Exit条件とRollback条件を持って全社展開へ進む。",
                "input": "Canary通過状態、Pilot対象部署",
                "output": "Stable Releaseと配布完了レポート",
            },
            {
                "name": "30日後指標",
                "summary": "導入時間・更新率・認定完了・Rollback Drill・Critical Gap・Skill二重編集を測る経営報告用指標群。",
                "input": "30日後の運用ログ",
                "output": "KPIダッシュボードと経営報告書ドラフト",
            },
        ],
        "scene": "大きな構想は、最初の一か月へ落とさなければ動きません。美咲は、棚卸し、正本化、Canary、研修、Pilot、全社展開を四週間へ分けます。",
        "essay": "最初の週はInventoryとPolicy、二週目はBuildとTest、三週目はCanaryとBronze研修、四週目はPilotとStable Releaseへ進みます。各週に完了条件とRollback地点を置き、未完成の基盤を全社員へ広げません。\n\n30日後は、導入時間、更新率、認定完了、Rollback Drill、Critical Gap、Skill正本の二重編集を測ります。",
        "mission": "自組織向けに四週間の導入表を作り、各週のOwner、成果物、合格条件、Rollback条件を記入してください。",
        "takeaway": "変革は大きな完成図ではなく、検証可能な一週間の積み重ねで進めます。",
        "image_concept": "A four-week implementation roadmap with inventory, build and test, canary training, pilot, stable rollout, and measurable outcomes",
        "image_kind": "roadmap illustration",
        "usecases": [
            {
                "situation": "ある中堅企業（架空）の経営者が、半年計画でAI全社展開を始めたが、3ヶ月目で社内疲れて停滞している。",
                "action": "1週目Inventory/Policy→2週目Build/Test→3週目Canary/Bronze研修→4週目Pilot/Stableに分け、各週Exit条件を置く。",
                "benefit": "一気に動かさず、検証単位で前進するため疲弊せず、未完成基盤の全社展開も防げる。",
            },
            {
                "situation": "情シス（架空）が、AI導入のKPIをCEOから求められたが、何を測ればよいか答えられない。",
                "action": "導入時間・更新率・認定完了・Rollback Drill・Critical Gapを30日後測定指標として宣言する。",
                "benefit": "経営報告に使える数字が揃い、AI推進の費用対効果を定量で説明できる。",
            },
        ],
        "expansion": {
            "title": "実務に落とすときの補足",
            "points": [
                {
                    "label": "4週間で詰めすぎないコツ",
                    "body": "1週目のInventoryは最低でも3営業日、Policyドラフトに2営業日確保しないと、後半のCanaryで必ず差し戻しが発生します。最初の週は『動かさない作業しかしない』ことを宣言し、その分2週目以降のテンポを上げる設計にすると失敗が減ります。",
                },
                {
                    "label": "Canary対象の選び方",
                    "body": "Canary対象は『AI習熟度が高い人』ではなく、『業務頻度が高く、失敗を口頭で言ってくれる人』を3〜5名選びます。習熟度の高い人は自分で迂回路を作ってしまうため、設計上の問題が検出されにくくなります。",
                },
                {
                    "label": "30日後指標の運用",
                    "body": "指標は5〜7個に絞り、毎週月曜にダッシュボードへ自動転記します。指標を10個以上並べると誰も見なくなり、結果として導入の費用対効果がCEOに伝わりません。指標を絞り切る判断が、組織展開の成否を分けます。",
                },
                {
                    "label": "次の章への接続",
                    "body": "4週間ロードマップが回り始めると、次章のFeature/原則分離が真価を発揮します。配布物が増えれば増えるほど、長く使える原則と頻繁に変わる製品情報を別々の更新周期で管理する必要が高まるからです。",
                },
            ],
        },
    },
    "37": {
        "intro_human": """『半年前のテキスト、モデル名が違って総ツッコミ』。
これ、教材を作る人なら必ず通る恥ずかしい瞬間です。

ほとんどの人は、教科書本文に『現行のモデル名・料金・UI』をそのまま書きます。
でもAI製品の機能は数週間で変わる。本文に書いた瞬間、その教科書は腐り始めます。

正解は、長く使える原則と、頻繁に変わるFeatureを別レイヤーで管理すること。
Plan/Verifyの重要性は何年も使えるけど、モデル名・料金・利用上限・UI・Beta状態は確認日と公式Sourceを持つFeature Registryへ。素材の動画にモデル名が出てきても本文を書き換えず、補正表で『現行ではこう扱う』と上書きする。

長く使える原則と、頻繁に変わる製品情報を別の更新周期で管理する。
これが、配布物を時間経過で腐らせない核心です。""",
        "features": [
            {
                "name": "原則とFeatureの分離",
                "summary": "長く使える原則と、モデル名・料金・UIなど頻繁に変わるFeatureを別レイヤーで扱う設計方針。",
                "input": "教材本文、変動情報の候補",
                "output": "原則本文とRegistry分離後の構成",
            },
            {
                "name": "Feature Registry更新",
                "summary": "名前・状態・確認日・公式Source・代替手順をRegistryへ書き、本文を直さずに新仕様へ追随できる仕組み。",
                "input": "現行Featureの最新情報、公式Source",
                "output": "Registryに追加された確認日付きエントリ",
            },
            {
                "name": "Suspended / Deprecated 表示",
                "summary": "停止・非推奨を明示し、古い手順から新仕様への移行ガイドを必ず添えるバージョン管理。",
                "input": "停止対象、代替Feature",
                "output": "Suspended/Deprecatedラベルと移行ガイド",
            },
            {
                "name": "素材→現行仕様補正表",
                "summary": "動画・記事など素材上の主張と、本書での現行扱いを対応付ける補正表。素材を否定せず使い続ける運用。",
                "input": "素材の主張、現行仕様",
                "output": "素材→現行扱いの対照表",
            },
        ],
        "scene": "動画で見たモデル名やコマンドが、数週間後には変わっていることがあります。遥は『教科書が間違った』のではなく、変動情報を本文へ固定した設計が間違いだと学びます。",
        "essay": "原則とFeatureを分けます。PlanとVerifyの重要性は長く使えますが、モデル名、料金、利用上限、UI、Beta状態は確認日と公式Sourceを持つRegistryへ置きます。動画の主張は素材として活かし、現行仕様で補正します。\n\n更新時は差分を記録し、SuspendedやDeprecatedを明示し、古い手順から安全に移行できる案内を付けます。",
        "mission": "本文にある変動情報を三つ見つけ、Feature Registryへ名前・状態・確認日・公式Source・代替手順として移してください。",
        "takeaway": "長く使える原則と、頻繁に変わる製品情報を別の更新周期で管理します。",
        "image_concept": "A stable stone foundation of principles beneath changing signboards for models, commands, pricing, beta features, and versions",
        "image_kind": "editorial metaphor illustration",
        "usecases": [
            {
                "situation": "ある社内研修担当（架空）が、半年前のテキストでモデル名・料金・UIが現行と違い、受講者から『間違っている』と総ツッコミを受けた。",
                "action": "変動情報をFeature Registryへ抜き出し、確認日・公式Source・代替手順を持たせる。",
                "benefit": "テキスト本体は更新せずRegistryだけ差し替えればよくなり、改訂コストが下がる。",
            },
            {
                "situation": "個人技術ブロガー（架空）が、過去記事のモデル仕様が古くなり、SEO的にも信頼を失っている。",
                "action": "原則とFeatureを分離して書き、Featureには確認日とDeprecated移行案内を入れる。",
                "benefit": "原則は長く使え、Featureだけ更新すれば記事全体の信頼が保てる。",
            },
        ],
        "expansion": {
            "title": "実務に落とすときの補足",
            "points": [
                {
                    "label": "Registryに最低限書くべき項目",
                    "body": "名前・状態（Active/Suspended/Deprecated）・確認日・公式Sourceの4項目は必須です。代替手順は任意ですが、Deprecated項目には必ず入れます。確認日のない項目はRegistryに置く意味がないため、新規追加時の必須欄として強制する仕組みにします。",
                },
                {
                    "label": "本文とRegistryの境界線",
                    "body": "『3ヶ月以内に変わりそうか』を判断基準にすると、本文へ書くか、Registryへ書くかが迷わず決まります。モデル名・料金・利用上限・UI・Beta状態はほぼ全てRegistry側です。本文に書いてよいのは、変わっても古びない設計思想と原則のみと割り切ります。",
                },
                {
                    "label": "確認日の運用",
                    "body": "確認日は『前回見たから動くと推定する有効期限』であり、過ぎたら必ず再確認します。3ヶ月を上限とし、過ぎたものはダッシュボードに赤で出します。確認日が形骸化したRegistryは、ない方がマシです。",
                },
                {
                    "label": "終章への接続",
                    "body": "原則とFeatureを分けて運用すると、配布物が時間経過で腐らなくなります。次の終章では、ここまでの全章を通じて作ってきた配布物群を、長く続くハーネスとして組み立て直す視点が問われます。",
                },
            ],
        },
    },
    "38": {
        "intro_human": """『全部の機能、解説したつもり』。
でもレビューに出したら重要トピックの抜けが大量発見。
これ、章数を増やしただけで網羅性を作った気になるとよく起きる事故です。

ほとんどの人は、網羅性を『印象』で判断します。
でも本当に必要なのは、各動画・公式補正・ハーネス要件を章へ対応付けた『Coverage Map』。
1つのSource Topicが、説明・実習・Template・管理者運用のどこで扱われているかを表で証明する。

この章で組むのは、動画別Coverage Map、Harness要件Coverage Map、Source Topic追跡軸の3つ。
すでに統合した話題も、出典とのつながりを残すことで将来の改訂時に追跡できる。

網羅性は『全部入れたつもり』じゃなく、Sourceと章の対応関係で証明します。""",
        "features": [
            {
                "name": "動画別 Coverage Map",
                "summary": "各動画の主内容と本書のどの章に配置したかを対応付ける表。素材ベースの抜け漏れ検出に使う。",
                "input": "素材動画群、章構成",
                "output": "動画→章 配置マッピング表",
            },
            {
                "name": "Harness要件 Coverage Map",
                "summary": "配布・同期・Hook・Skill・Safety・観測性などの要件が、どの章で扱われているかを確認する要件側マップ。",
                "input": "ハーネス要件一覧",
                "output": "要件→章 マッピング表と未充足要件",
            },
            {
                "name": "Source Topic追跡",
                "summary": "各Source Topicが説明・実習・Template・管理者運用のどこで扱われたかを確認する追跡軸。網羅性の証明手段。",
                "input": "Source Topic一覧、章別取扱い",
                "output": "Topic×取扱い種別のマトリクス",
            },
        ],
        "scene": "最後の確認で、美咲は『読みやすくなったか』だけでなく、『素材のどの話題が、どこへ入ったか』を尋ねます。網羅性は印象ではなく、Coverage Mapで証明します。",
        "essay": "Coverage Mapは、各動画、公式補正、ハーネス要件を章へ対応付け、未収録と重複を見つける表です。すでに統合した話題も、出典とのつながりを残すことで、将来の改訂時に追跡できます。\n\n章数が多いことを網羅性としません。各Source Topicが、説明、実習、Template、管理者運用のどこで扱われるかを確認します。",
        "mission": "新しく追加した素材を一つ選び、既存章への統合先、重複、追加すべき実習、更新日をCoverage Mapへ記録してください。",
        "takeaway": "網羅性は『全部入れたつもり』ではなく、Sourceと章の対応関係で証明します。",
        "image_concept": "A comprehensive coverage map connecting source videos, official documentation, requirements, chapters, exercises, and templates without gaps",
        "image_kind": "information map illustration",
        "usecases": [
            {
                "situation": "ある教科書編集者（架空）が、『全部の機能を解説した』と思って入稿したら、レビューで重要トピックの抜けが多数発見され大改修になった。",
                "action": "Coverage Mapで各Source Topicが説明・実習・Template・運用のどこで扱われるかを表にする。",
                "benefit": "抜けと重複が事前に検出でき、レビュー時に『どの章に入っているか』を即答できる。",
            },
            {
                "situation": "中堅IT企業（架空）が、AI研修テキストの追加教材を入れるたびに既存章と矛盾し、整合性チェックに毎回数日かかる。",
                "action": "追加素材を統合する際に既存章への対応・重複・追加実習をCoverage Mapへ記録する。",
                "benefit": "整合性チェックが表の更新で済み、改訂サイクルが大幅に短縮される。",
            },
        ],
    },
    "final": {
        "intro_human": """『一度完成させた環境、半年後に劣化してたことに気づかなかった』。
これ、AI推進担当が一番怖い瞬間です。

ほとんどの人は、最強の環境を『一度完成させて固定するもの』だと思ってます。
でも実は、最強の条件は『更新し続けられること』。
変化を観測し、小さく試し、独立した文脈で評価し、安全に配布し、必要なら戻す。このLoopが続く限り、教科書も組織も古びません。

この終章でまとめるのは、個人の学びと組織のハーネスを同じLoopで成長させる設計。
原則と変動情報は別の更新周期で管理する。月次で1つLesson/Skillを選んで改善する。個人の成功手順は組織のハーネスに昇格させ、組織の更新は個人の学習に戻す。

完成より、検証可能に更新し続けられること。
それが『最強』の条件です。""",
        "features": [
            {
                "name": "更新Loop（観測→試行→評価→配布→復旧）",
                "summary": "変化を観測し、小さく試し、独立評価し、安全に配布し、必要なら戻すサイクル。完成形ではなく更新可能性を最強の条件にする運用骨格。",
                "input": "現在の運用状態、改善候補",
                "output": "1サイクル分の更新ログとRollback地点",
            },
            {
                "name": "Lesson/Skill 月次改善",
                "summary": "Owner・Fixture・評価日・Release段階を持つLessonまたはSkillを月次で1つ選び改善する継続活動。",
                "input": "現Lesson/Skill台帳、評価スコア",
                "output": "改善対象1件と次月の改善ログ",
            },
            {
                "name": "原則と変動情報の継続分離",
                "summary": "長く使える原則と、頻繁に変わるFeatureを別更新周期で管理し続ける運用習慣。教材と現実のズレを構造的に防ぐ。",
                "input": "本文の表現、現行仕様の変化",
                "output": "原則本文の安定維持とRegistryの定期更新",
            },
            {
                "name": "個人学習 × 組織ハーネス同期",
                "summary": "個人が成功した手順を組織のハーネスへ昇格させ、組織の更新を個人の学習に戻す双方向の連結機構。",
                "input": "個人の成功事例、ハーネスの最新版",
                "output": "ハーネス側Skill追加と個人環境の更新",
            },
        ],
        "scene": "教科書を書き終えた日、遥はもう『分からなくなったら最初からやり直す』とは考えませんでした。現在地を保存し、証拠を見て、必要なLessonへ戻り、成功した手順をSkillへ直せるからです。",
        "essay": "最強の環境は、一度完成した環境ではありません。変化を観測し、小さく試し、独立して評価し、安全に配布し、必要なら戻せる環境です。個人の学びと組織のハーネスは同じLoopで成長します。\n\n読む、作る、確かめる、保存する、共有する。その循環が続く限り、教科書は古びた説明書ではなく、現場と一緒に育つ実行システムであり続けます。",
        "mission": "次の30日で改善するLessonまたはSkillを一つ選び、Owner、Fixture、評価日、Release段階を決めてください。",
        "takeaway": "完成よりも、検証可能に更新し続けられることが『最強』の条件です。",
        "image_concept": "A lighthouse guiding an evolving network of learners, tools, and safe release loops, symbolizing continuous improvement rather than a fixed finish line",
        "image_kind": "cinematic editorial illustration",
        "usecases": [
            {
                "situation": "ABC社のAI推進リーダー（架空）が、AI環境を一度完成させたあと、半年後に劣化したことに気づかず競合に追い抜かれた。",
                "action": "Owner・Fixture・評価日・Release段階を持つLessonまたはSkillを月次で改善し続ける。",
                "benefit": "完成形ではなく更新可能性が組織能力となり、競合変化に追随できる。",
            },
            {
                "situation": "個人開発者（架空）が、最初に作ったSkillを使い回し続けて陳腐化に気づかず、ある日突然動かなくなった。",
                "action": "30日ごとに次に改善するLessonまたはSkillを選び、検証可能なRelease段階で更新する。",
                "benefit": "個人レベルでも更新Loopが回り、陳腐化や急停止のリスクが低くなる。",
            },
        ],
    },
}

EXTRA_VISUALS = [
    {
        "id": "diagram-ch04-meeting-flow",
        "chapter": "04",
        "tier": "core",
        "placement": "第4章の要件定義直後。入力から四つの成果物へ分岐する流れを示す。",
        "kind": "process diagram background",
        "concept": "A clean left-to-right process diagram background showing meeting transcript input branching into minutes, task JSON, HTML report, and reusable skill, no text labels",
        "alt": "文字起こしから議事録、タスク、HTML、Skillへ展開する処理の概念図",
        "caption": "一つの入力を、人が読む成果物・機械が読む成果物・再利用手順へ分けます。",
    },
    {
        "id": "diagram-ch06-standard-loop",
        "chapter": "06",
        "tier": "core",
        "placement": "第6章6.1の直後。七段階の標準Loopを俯瞰する。",
        "kind": "circular workflow diagram background",
        "concept": "A precise seven-step circular workflow background with seven empty labeled zones and a central human quality decision point, no text",
        "alt": "探索からCommitまでの七段階標準Loop",
        "caption": "どの仕事も同じLoopへ入れると、抜けと手戻りを発見しやすくなります。",
    },
    {
        "id": "diagram-ch11-knowledge-layers",
        "chapter": "11",
        "tier": "core",
        "placement": "第11章11.1の直後。CLAUDE.md、Rules、Skills、Memoryの責務分離。",
        "kind": "layered architecture background",
        "concept": "A four-layer architecture background with a small always-on guidance layer, path-specific rules, on-demand manuals, and compact discovered memory, no text",
        "alt": "CLAUDE.md、Rules、Skills、Auto Memoryの責務レイヤー",
        "caption": "常時読む情報ほど短くし、詳細手順は必要時だけ読み込みます。",
    },
    {
        "id": "diagram-ch12-skill-anatomy",
        "chapter": "12",
        "tier": "core",
        "placement": "第12章12.4の直後。Skillの構成要素を示す。",
        "kind": "anatomy diagram background",
        "concept": "A reusable skill manual opened to show input, trigger, steps, output, checks, failure handling, and references as distinct visual compartments, no text",
        "alt": "Skillを構成する入力、手順、出力、検証、参照資料",
        "caption": "Skillは短い呪文ではなく、検証可能な業務パッケージです。",
    },
    {
        "id": "diagram-ch15-trust-boundary",
        "chapter": "15",
        "tier": "core",
        "placement": "第15章15.5の直後。ReadとWrite、Secret、外部データの境界。",
        "kind": "security architecture background",
        "concept": "A trust-boundary diagram background with local workspace, secret vault, read-only external lane, approval-gated write lane, and untrusted content quarantine, no text",
        "alt": "外部連携におけるRead、Write、Secret、未信頼データの境界",
        "caption": "外部能力を増やすほど、信頼境界と承認地点を明示します。",
    },
    {
        "id": "diagram-ch16-format-choice",
        "chapter": "16",
        "tier": "core",
        "placement": "第16章16.1の直後。MarkdownとHTMLの適性比較。",
        "kind": "comparison infographic background",
        "concept": "A balanced comparison background: a structured text document for drafting and version control on one side, an interactive visual web report for presentation and exploration on the other, no text",
        "alt": "MarkdownとHTMLの用途比較",
        "caption": "正本の書きやすさと、読み手の理解しやすさを分けて選びます。",
    },
    {
        "id": "diagram-ch17-design-to-code",
        "chapter": "17",
        "tier": "core",
        "placement": "第17章17.4の直後。Wireframeから実装・検証まで。",
        "kind": "design pipeline background",
        "concept": "A four-stage design pipeline background from grayscale wireframe to design system components, interactive prototype, and tested responsive code, no text",
        "alt": "Wireframe、Design System、Prototype、Codeの流れ",
        "caption": "情報・見た目・動作を段階的に確定します。",
    },
    {
        "id": "diagram-ch18-live-artifact-layers",
        "chapter": "18",
        "tier": "core",
        "placement": "第18章18.3の直後。Live Artifactの五層。",
        "kind": "stack diagram background",
        "concept": "A five-layer live dashboard stack background for external data retrieval, normalization, display, AI summary, and local cache with freshness indicator, no text",
        "alt": "Live Artifactのデータ取得、整形、表示、AI要約、キャッシュ",
        "caption": "更新される画面は、表示だけでなく取得・AI処理・キャッシュまで分離します。",
    },
    {
        "id": "diagram-ch23-harness-architecture",
        "chapter": "23",
        "tier": "core",
        "placement": "第23章23.4の直後。推奨Repositoryと四つの面。",
        "kind": "enterprise architecture background",
        "concept": "A repository-centered enterprise architecture background separating source assets, generated runtime packages, managed policy, distribution pipeline, personal local layer, and monitoring, no text",
        "alt": "トレプロハーネスの正本、生成物、Policy、配布、個人Layer、監視",
        "caption": "正本と生成物、共通層と個人層、GuidanceとEnforcementを分離します。",
    },
    {
        "id": "diagram-ch24-sync-rollback",
        "chapter": "24",
        "tier": "core",
        "placement": "第24章24.4の直後。Manifest同期とRollback。",
        "kind": "delivery sequence background",
        "concept": "A sequence diagram background for remote release, local update lock, manifest comparison, safe copy and deletion, verification, inventory update, and rollback path, no text",
        "alt": "Manifest方式の同期、検証、Rollbackの流れ",
        "caption": "配布は毎回、同じ正しい状態へ収束し、失敗時には既知のReleaseへ戻します。",
    },
    {
        "id": "diagram-ch25-skill-lifecycle",
        "chapter": "25",
        "tier": "core",
        "placement": "第25章25.2の直後。Skill Lifecycle。",
        "kind": "lifecycle diagram background",
        "concept": "A controlled lifecycle ring background from proposal, source authoring, generator, fixtures, evaluator, canary, stable, deprecation, and archive, no text",
        "alt": "Skillの提案から廃止までのLifecycle",
        "caption": "Skillを増やすだけでなく、評価・段階配布・廃止まで管理します。",
    },
    {
        "id": "diagram-ch26-threat-model",
        "chapter": "26",
        "tier": "core",
        "placement": "第26章26.1の直後。Threatと予防・検知・復旧。",
        "kind": "threat model background",
        "concept": "A defensive architecture background showing threats entering from secrets, commands, external content, configuration changes, and supply chain, each met by prevention, detection, and recovery controls, no text",
        "alt": "主要Threatに対する予防、検知、復旧の三層",
        "caption": "事故をゼロと仮定せず、予防・検知・復旧を重ねます。",
    },
    {
        "id": "diagram-ch35-learning-system",
        "chapter": "35",
        "tier": "core",
        "placement": "第35章35.2の直後。教材アプリのContent Model。",
        "kind": "product architecture background",
        "concept": "A learning system architecture background connecting role-based paths, structured lessons, artifacts, evidence checks, feature registry, progress state, and local companion, no text",
        "alt": "教科書アプリのLearning Path、Lesson、証拠、Feature Registry、進捗、Local Companion",
        "caption": "本文、行動、証拠、状態、Version差分を一つの学習Systemとして扱います。",
    },
]


# 14レッスン体験コース（claude-code-handson-navigator v3 と同期）
# 各レッスンの textbook_chapters は本書の章番号（'final' は終章）。
LESSON_COURSE = [
    {
        "id": "F00",
        "title": "体験学習を開始する",
        "minutes": 10,
        "chapters": [0, 1],
        "objective": "学習専用ワークスペースと保存可能な学習状態を作り、操作方法を理解する。",
        "note": "教科書の使い方／Claude Code は何が違うのか",
    },
    {
        "id": "F01",
        "title": "安全を最初に設計する",
        "minutes": 20,
        "chapters": [2, 3],
        "objective": "プロジェクト、作業範囲、承認、最小権限の意味を体験する。",
        "note": "Sandbox・Project Folder の作り方",
    },
    {
        "id": "F02",
        "title": "最初の90分実習：会議アシスタント",
        "minutes": 20,
        "chapters": [4],
        "objective": "Explorer・Editor・Agent・Terminalの役割を区別し、ファイルを自分で編集する。",
        "note": "ハンズオン入門・名物章",
    },
    {
        "id": "F03",
        "title": "強い指示の書き方",
        "minutes": 30,
        "chapters": [5],
        "objective": "目的・背景・入力・出力・制約・完了条件で曖昧でない依頼を作る。",
        "note": "依頼の構造化",
    },
    {
        "id": "F04",
        "title": "ESPIVRC の型",
        "minutes": 25,
        "chapters": [6],
        "objective": "AIの変更を承認前に読み、意図しない変更を戻せる。",
        "note": "Explore→Specify→Plan→Implement→Verify→Review→Commit",
    },
    {
        "id": "F05",
        "title": "Permission Mode と危険操作",
        "minutes": 25,
        "chapters": [7],
        "objective": "現在地確認・一覧・ファイル内容確認という安全な読み取りを使いこなす。",
        "note": "権限境界と Sandbox",
    },
    {
        "id": "F06",
        "title": "Model と Effort、Session と Context",
        "minutes": 30,
        "chapters": [8, 9],
        "objective": "小さな制作課題を計画だけさせ、人がレビューしてから実装へ進める。",
        "note": "深さと文脈の管理",
    },
    {
        "id": "F07",
        "title": "Git と Checkpoint で戻れる安心",
        "minutes": 45,
        "chapters": [10],
        "objective": "承認済みPlanからHTML成果物を実装し、目視とファイルで検証する。",
        "note": "戻る勇気",
    },
    {
        "id": "F08",
        "title": "CLAUDE.md・Rules・Auto Memory",
        "minutes": 30,
        "chapters": [11],
        "objective": "同じworkspaceを異なるエージェントで開き、状態を失わず使い分ける。",
        "note": "Claude Code の覚えさせ方",
    },
    {
        "id": "F09",
        "title": "Skills 設計（自分専用 Skill）",
        "minutes": 45,
        "chapters": [12, 13],
        "objective": "既存Skillを魔法として使うのではなく、入力・骨子・生成・検証に分解する。",
        "note": "Skill 設計と Subagent 活用",
    },
    {
        "id": "F10",
        "title": "Hooks・Plugins・MCP",
        "minutes": 45,
        "chapters": [14, 15],
        "objective": "小さな成功手順を標準準拠のSkillへ変換する。",
        "note": "拡張機構と外部接続",
    },
    {
        "id": "F11",
        "title": "HTMLレポート／Claude Design／成果物制作",
        "minutes": 45,
        "chapters": [16, 17, 18],
        "objective": "発火と出力品質を分け、正常・不足・巨大・危険・対象外の5ケースで評価する。",
        "note": "ライブ成果物・Cowork",
    },
    {
        "id": "F12",
        "title": "自分専用に育てる ／ /goal・Headless・定期実行",
        "minutes": 15,
        "chapters": [19, 20],
        "objective": "意図的にセッションを切り、新しいチャットで同じ地点から復帰する。",
        "note": "発展編",
    },
    {
        "id": "F13",
        "title": "0→1卒業制作（応用＋終章）",
        "minutes": 90,
        "chapters": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, "final"],
        "objective": "実務に近い小成果物を、要件・Plan・実装・検証・Skill候補化まで自走する。",
        "note": "終章までの全章を自分の課題で適用する",
    },
]
