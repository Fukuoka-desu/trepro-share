/* ============================================================================
 * TrePro AI ポータルモック v2 — 架空データ（fictional, fixed / no random）
 * ----------------------------------------------------------------------------
 * スキーマは Salesforce 設計に合わせる:
 *   Account            : id / name / industry / employeeSize / owner / mrr / sfLink
 *   更新ジャッジ__c     : continuityAngle / prevAngle / judgeResult / paused
 *                        renewalMonth / nextAction / dueDate / drop
 *   （Opportunity, 議事録タイムライン等は下部に別途）
 * 単位: 千円 / 日付: JST YYYY-MM-DD / クライアント名は様付け
 * ========================================================================== */

const OWNERS = ["高木", "西村", "大川", "藤沢"];

/* -- KPI 目標（千円 / 社 / %） ------------------------------------------- */
const TARGETS = {
  mrr: 20000,        // 稼働MRR目標（千円）
  churnRate: 8.0,    // 解約率目標（%以下）低いほど良い
  renewalRate: 92.0, // 更新率目標（%以上）
  newMrr: 1800       // 今月新規MRR目標（千円）
};

/* -- Account + 更新ジャッジ__c（40社・固定） ---------------------------- */
/* renewalMonth は 2026-07〜2026-12 に分散。continuityAngle=継続角度(0-100)
 * prevAngle=先週の角度（↑↓算出用）。judgeResult: null|renew|churn。
 * paused: 一時停止。drop: 確度低下アラート。                              */
const ACCOUNTS = [
  {id:1,  name:"株式会社青葉製作所様",             industry:"製造", employeeSize:"B(60名)",  owner:"高木", mrr:500, continuityAngle:85, prevAngle:83, renewalMonth:"2026-07", judgeResult:null, paused:false, drop:false, nextAction:"月次レポート持参のうえ更新面談", dueDate:"2026-07-25", sfLink:true},
  {id:2,  name:"ひまわり介護ホールディングス様",   industry:"介護", employeeSize:"A(180名)", owner:"西村", mrr:800, continuityAngle:52, prevAngle:61, renewalMonth:"2026-07", judgeResult:null, paused:false, drop:true,  nextAction:"採用数値の乖離説明＋改善提案書", dueDate:"2026-07-24", sfLink:true},
  {id:3,  name:"株式会社山彦建設様",               industry:"建設", employeeSize:"B(45名)",  owner:"大川", mrr:500, continuityAngle:71, prevAngle:70, renewalMonth:"2026-07", judgeResult:null, paused:false, drop:false, nextAction:"次期キャンペーン企画の提示", dueDate:"2026-07-28", sfLink:true},
  {id:4,  name:"グリーンリーフ物流株式会社様",     industry:"物流", employeeSize:"A(320名)", owner:"高木", mrr:900, continuityAngle:90, prevAngle:88, renewalMonth:"2026-07", judgeResult:null, paused:false, drop:false, nextAction:"契約書更新版の締結", dueDate:"2026-07-31", sfLink:true},
  {id:5,  name:"株式会社北斗ソフトウェア様",       industry:"IT",   employeeSize:"C(18名)",  owner:"西村", mrr:300, continuityAngle:41, prevAngle:48, renewalMonth:"2026-07", judgeResult:null, paused:true,  drop:true,  nextAction:"停止理由ヒアリング（予算凍結）", dueDate:"2026-07-23", sfLink:true},
  {id:6,  name:"株式会社flowaフラワー様",          industry:"小売", employeeSize:"C(28名)",  owner:"藤沢", mrr:300, continuityAngle:78, prevAngle:75, renewalMonth:"2026-07", judgeResult:null, paused:false, drop:false, nextAction:"EC連携の追加提案", dueDate:"2026-07-29", sfLink:true},
  {id:7,  name:"株式会社ルミエールビューティー様", industry:"美容", employeeSize:"C(25名)",  owner:"大川", mrr:300, continuityAngle:75, prevAngle:72, renewalMonth:"2026-08", judgeResult:null, paused:false, drop:false, nextAction:"新店舗向け追加提案", dueDate:"2026-08-08", sfLink:true},
  {id:8,  name:"株式会社おおぞら福祉会様",         industry:"福祉", employeeSize:"B(90名)",  owner:"高木", mrr:500, continuityAngle:88, prevAngle:86, renewalMonth:"2026-08", judgeResult:null, paused:false, drop:false, nextAction:"満足度ヒアリング（定例内）", dueDate:"2026-08-15", sfLink:true},
  {id:9,  name:"株式会社すばる自動車販売様",       industry:"小売", employeeSize:"B(70名)",  owner:"西村", mrr:500, continuityAngle:49, prevAngle:57, renewalMonth:"2026-08", judgeResult:null, paused:false, drop:true,  nextAction:"応募単価改善レポートの提出", dueDate:"2026-08-05", sfLink:true},
  {id:10, name:"株式会社もみじフーズ様",           industry:"食品", employeeSize:"A(150名)", owner:"大川", mrr:800, continuityAngle:64, prevAngle:66, renewalMonth:"2026-08", judgeResult:null, paused:true,  drop:false, nextAction:"再開条件（新工場稼働）の確認", dueDate:"2026-08-20", sfLink:true},
  {id:11, name:"株式会社こまち商事様",             industry:"卸売", employeeSize:"B(52名)",  owner:"藤沢", mrr:500, continuityAngle:82, prevAngle:80, renewalMonth:"2026-08", judgeResult:null, paused:false, drop:false, nextAction:"更新見積の事前送付", dueDate:"2026-08-22", sfLink:true},
  {id:12, name:"株式会社しらかば歯科グループ様",   industry:"医療", employeeSize:"C(30名)",  owner:"高木", mrr:300, continuityAngle:80, prevAngle:79, renewalMonth:"2026-09", judgeResult:null, paused:false, drop:false, nextAction:"更新見積の事前送付", dueDate:"2026-09-10", sfLink:true},
  {id:13, name:"株式会社あかつき電設様",           industry:"建設", employeeSize:"C(22名)",  owner:"西村", mrr:300, continuityAngle:92, prevAngle:90, renewalMonth:"2026-09", judgeResult:null, paused:false, drop:false, nextAction:"事例記事化の許諾取得", dueDate:"2026-09-12", sfLink:true},
  {id:14, name:"株式会社みなと海運様",             industry:"物流", employeeSize:"B(85名)",  owner:"大川", mrr:500, continuityAngle:56, prevAngle:63, renewalMonth:"2026-09", judgeResult:null, paused:false, drop:true,  nextAction:"競合比較資料＋役員同席打診", dueDate:"2026-09-05", sfLink:true},
  {id:15, name:"株式会社こだま印刷様",             industry:"製造", employeeSize:"C(15名)",  owner:"藤沢", mrr:300, continuityAngle:72, prevAngle:72, renewalMonth:"2026-09", judgeResult:null, paused:false, drop:false, nextAction:"通常更新（定例で確認）", dueDate:"2026-09-18", sfLink:true},
  {id:16, name:"株式会社つばさ人材サービス様",     industry:"人材", employeeSize:"B(55名)",  owner:"高木", mrr:500, continuityAngle:35, prevAngle:44, renewalMonth:"2026-09", judgeResult:null, paused:true,  drop:true,  nextAction:"解約回避: 運用体制の再設計提案", dueDate:"2026-09-01", sfLink:true},
  {id:17, name:"株式会社大和ハウジング様",         industry:"不動産", employeeSize:"A(140名)", owner:"西村", mrr:800, continuityAngle:87, prevAngle:85, renewalMonth:"2026-09", judgeResult:null, paused:false, drop:false, nextAction:"賃貸部門への横展開提案", dueDate:"2026-09-20", sfLink:true},
  {id:18, name:"株式会社こもれびクリニック様",     industry:"医療", employeeSize:"C(24名)",  owner:"大川", mrr:300, continuityAngle:68, prevAngle:65, renewalMonth:"2026-10", judgeResult:null, paused:false, drop:false, nextAction:"看護師採用の成果共有", dueDate:"2026-10-06", sfLink:true},
  {id:19, name:"株式会社はやて運輸様",             industry:"物流", employeeSize:"B(78名)",  owner:"藤沢", mrr:500, continuityAngle:59, prevAngle:58, renewalMonth:"2026-10", judgeResult:null, paused:false, drop:true,  nextAction:"ドライバー応募数の週次モニタリング", dueDate:"2026-10-10", sfLink:true},
  {id:20, name:"株式会社みらい教育社様",           industry:"教育", employeeSize:"B(66名)",  owner:"高木", mrr:500, continuityAngle:84, prevAngle:82, renewalMonth:"2026-10", judgeResult:null, paused:false, drop:false, nextAction:"講師採用キャンペーンの設計", dueDate:"2026-10-14", sfLink:true},
  {id:21, name:"株式会社さくら食品工業様",         industry:"食品", employeeSize:"A(210名)", owner:"西村", mrr:900, continuityAngle:91, prevAngle:89, renewalMonth:"2026-10", judgeResult:null, paused:false, drop:false, nextAction:"複数拠点への展開見積", dueDate:"2026-10-18", sfLink:true},
  {id:22, name:"株式会社なでしこ介護様",           industry:"介護", employeeSize:"B(95名)",  owner:"大川", mrr:500, continuityAngle:47, prevAngle:55, renewalMonth:"2026-10", judgeResult:null, paused:false, drop:true,  nextAction:"離職率と採用数の相関レポート提出", dueDate:"2026-10-08", sfLink:true},
  {id:23, name:"株式会社こはく建材様",             industry:"建設", employeeSize:"C(19名)",  owner:"藤沢", mrr:300, continuityAngle:73, prevAngle:71, renewalMonth:"2026-10", judgeResult:null, paused:false, drop:false, nextAction:"通常更新（定例で確認）", dueDate:"2026-10-22", sfLink:true},
  {id:24, name:"株式会社きらめきデンタル様",       industry:"医療", employeeSize:"C(26名)",  owner:"高木", mrr:300, continuityAngle:79, prevAngle:77, renewalMonth:"2026-11", judgeResult:null, paused:false, drop:false, nextAction:"衛生士採用の追加枠提案", dueDate:"2026-11-05", sfLink:true},
  {id:25, name:"株式会社アルタイル製造様",         industry:"製造", employeeSize:"A(260名)", owner:"西村", mrr:900, continuityAngle:86, prevAngle:84, renewalMonth:"2026-11", judgeResult:null, paused:false, drop:false, nextAction:"技能職向け動画パックの提案", dueDate:"2026-11-10", sfLink:true},
  {id:26, name:"株式会社ひなたリテール様",         industry:"小売", employeeSize:"B(72名)",  owner:"大川", mrr:500, continuityAngle:62, prevAngle:64, renewalMonth:"2026-11", judgeResult:null, paused:false, drop:false, nextAction:"店舗スタッフ採用の再設計", dueDate:"2026-11-14", sfLink:true},
  {id:27, name:"株式会社くすのき運送様",           industry:"物流", employeeSize:"B(88名)",  owner:"藤沢", mrr:500, continuityAngle:44, prevAngle:53, renewalMonth:"2026-11", judgeResult:null, paused:true,  drop:true,  nextAction:"停止理由ヒアリング（繁忙期都合）", dueDate:"2026-11-03", sfLink:true},
  {id:28, name:"株式会社ソレイユ美容室様",         industry:"美容", employeeSize:"C(20名)",  owner:"高木", mrr:300, continuityAngle:81, prevAngle:80, renewalMonth:"2026-11", judgeResult:null, paused:false, drop:false, nextAction:"スタイリスト採用の事例化", dueDate:"2026-11-18", sfLink:true},
  {id:29, name:"株式会社みどり建設様",             industry:"建設", employeeSize:"A(160名)", owner:"西村", mrr:800, continuityAngle:69, prevAngle:67, renewalMonth:"2026-11", judgeResult:null, paused:false, drop:false, nextAction:"施工管理職の採用強化提案", dueDate:"2026-11-22", sfLink:true},
  {id:30, name:"株式会社こうめ保育園グループ様",   industry:"福祉", employeeSize:"B(58名)",  owner:"大川", mrr:500, continuityAngle:83, prevAngle:81, renewalMonth:"2026-12", judgeResult:null, paused:false, drop:false, nextAction:"保育士採用の年間計画提案", dueDate:"2026-12-04", sfLink:true},
  {id:31, name:"株式会社テクノスター様",           industry:"IT",   employeeSize:"B(64名)",  owner:"藤沢", mrr:500, continuityAngle:76, prevAngle:74, renewalMonth:"2026-12", judgeResult:null, paused:false, drop:false, nextAction:"エンジニア採用ブランディング提案", dueDate:"2026-12-08", sfLink:true},
  {id:32, name:"株式会社あおぞら薬局様",           industry:"医療", employeeSize:"B(50名)",  owner:"高木", mrr:500, continuityAngle:58, prevAngle:60, renewalMonth:"2026-12", judgeResult:null, paused:false, drop:true,  nextAction:"薬剤師採用の媒体見直し提案", dueDate:"2026-12-12", sfLink:true},
  {id:33, name:"株式会社まつり食品様",             industry:"食品", employeeSize:"B(76名)",  owner:"西村", mrr:500, continuityAngle:80, prevAngle:78, renewalMonth:"2026-12", judgeResult:null, paused:false, drop:false, nextAction:"季節採用キャンペーンの設計", dueDate:"2026-12-16", sfLink:true},
  {id:34, name:"株式会社さざなみ観光様",           industry:"観光", employeeSize:"B(62名)",  owner:"大川", mrr:500, continuityAngle:66, prevAngle:63, renewalMonth:"2026-12", judgeResult:null, paused:false, drop:false, nextAction:"繁忙期スタッフ採用の前倒し提案", dueDate:"2026-12-20", sfLink:true},
  /* 判定済みサンプル（更新率・解約率のKPIを成立させるため） */
  {id:35, name:"株式会社ときわ商会様",             industry:"卸売", employeeSize:"B(54名)",  owner:"藤沢", mrr:500, continuityAngle:88, prevAngle:86, renewalMonth:"2026-06", judgeResult:"renew", paused:false, drop:false, nextAction:"更新完了（次回は2026-12）", dueDate:"2026-06-28", sfLink:true},
  {id:36, name:"株式会社ひばり工業様",             industry:"製造", employeeSize:"A(190名)", owner:"高木", mrr:800, continuityAngle:85, prevAngle:83, renewalMonth:"2026-06", judgeResult:"renew", paused:false, drop:false, nextAction:"更新完了（横展開を継続提案）", dueDate:"2026-06-25", sfLink:true},
  {id:37, name:"株式会社ゆうなぎ物流様",           industry:"物流", employeeSize:"B(68名)",  owner:"西村", mrr:500, continuityAngle:38, prevAngle:42, renewalMonth:"2026-06", judgeResult:"churn", paused:false, drop:true,  nextAction:"解約確定（撤退理由をナレッジ化）", dueDate:"2026-06-30", sfLink:true},
  {id:38, name:"株式会社こもり印刷様",             industry:"製造", employeeSize:"C(16名)",  owner:"大川", mrr:300, continuityAngle:82, prevAngle:80, renewalMonth:"2026-06", judgeResult:"renew", paused:false, drop:false, nextAction:"更新完了", dueDate:"2026-06-27", sfLink:true},
  {id:39, name:"株式会社ほたる化成様",             industry:"製造", employeeSize:"B(74名)",  owner:"藤沢", mrr:500, continuityAngle:90, prevAngle:88, renewalMonth:"2026-06", judgeResult:"renew", paused:false, drop:false, nextAction:"更新完了", dueDate:"2026-06-26", sfLink:true},
  {id:40, name:"株式会社なごみ介護サービス様",     industry:"介護", employeeSize:"B(82名)",  owner:"高木", mrr:500, continuityAngle:45, prevAngle:50, renewalMonth:"2026-06", judgeResult:"churn", paused:false, drop:true,  nextAction:"解約確定（サービス設計の反省点整理）", dueDate:"2026-06-29", sfLink:true}
];

/* -- Opportunity（案件） ------------------------------------------------- */
const DEALS = [
  {name:"青葉製作所様 SNS採用運用 更新",       account:"株式会社青葉製作所様",           recordType:"トレプロ新規",   stage:"更新交渉",   amount:6000, closeDate:"2026-07-31", owner:"高木"},
  {name:"ひまわり介護HD様 運用継続",           account:"ひまわり介護ホールディングス様", recordType:"トレプロ新規",   stage:"更新交渉",   amount:9600, closeDate:"2026-07-31", owner:"西村"},
  {name:"わかば商事様 新規SNS運用",            account:"株式会社わかば商事様",           recordType:"トレプロ新規",   stage:"提案",       amount:6000, closeDate:"2026-08-15", owner:"大川"},
  {name:"あさひ機工様 AI研修（DXリスキリング）",account:"株式会社あさひ機工様",           recordType:"トレプロショット", stage:"見積提示",   amount:1800, closeDate:"2026-08-29", owner:"高木"},
  {name:"みなと海運様 動画制作パック",         account:"株式会社みなと海運様",           recordType:"トレプロショット", stage:"ヒアリング", amount:900,  closeDate:"2026-09-12", owner:"大川"},
  {name:"つばさ人材様 継続（回避提案）",       account:"株式会社つばさ人材サービス様",   recordType:"トレプロ新規",   stage:"更新交渉",   amount:6000, closeDate:"2026-09-01", owner:"高木"},
  {name:"大和ハウジング様 賃貸部門 新規",      account:"株式会社大和ハウジング様",       recordType:"トレプロ新規",   stage:"提案",       amount:9600, closeDate:"2026-09-20", owner:"西村"},
  {name:"アルタイル製造様 技能職動画パック",    account:"株式会社アルタイル製造様",       recordType:"トレプロショット", stage:"見積提示",   amount:1200, closeDate:"2026-11-10", owner:"西村"},
  {name:"テクノスター様 採用ブランディング",    account:"株式会社テクノスター様",         recordType:"トレプロ新規",   stage:"ヒアリング", amount:6000, closeDate:"2026-12-08", owner:"藤沢"},
  {name:"みらい教育社様 講師採用キャンペーン",  account:"株式会社みらい教育社様",         recordType:"トレプロショット", stage:"提案",       amount:1500, closeDate:"2026-10-14", owner:"高木"}
];

/* -- MRR 推移（千円・6ヶ月） -------------------------------------------- */
const MRR_TREND = [["2月",17800],["3月",18100],["4月",18400],["5月",19000],["6月",19300],["7月",19800]];

/* -- My Day: 今日の会議（架空・2026-07-22） ---------------------------- */
const MEETINGS = [
  {time:"10:00", title:"ひまわり介護HD様 更新面談", type:"更新", accountId:2, place:"オンライン"},
  {time:"13:30", title:"青葉製作所様 月次レポート報告", type:"定例", accountId:1, place:"先方訪問"},
  {time:"16:00", title:"社内: 継続ジャッジ 朝会振り返り", type:"社内", accountId:null, place:"会議室A"}
];

/* -- My Day: 期限タスク（今日〜近日） ---------------------------------- */
const TASKS = [
  {id:"t1", title:"北斗ソフトウェア様 停止理由ヒアリング準備", due:"2026-07-23", accountId:5, priority:"high"},
  {id:"t2", title:"ひまわり介護HD様 改善提案書ドラフト作成", due:"2026-07-24", accountId:2, priority:"high"},
  {id:"t3", title:"青葉製作所様 更新見積の社内承認申請", due:"2026-07-25", accountId:1, priority:"mid"},
  {id:"t4", title:"山彦建設様 次期キャンペーン企画たたき", due:"2026-07-28", accountId:3, priority:"mid"},
  {id:"t5", title:"flowaフラワー様 EC連携の要件整理", due:"2026-07-29", accountId:6, priority:"low"}
];

/* -- My Day: AI提案「次にやること」 ------------------------------------ */
const AI_SUGGESTIONS = [
  {id:"a1", accountId:2, text:"ひまわり介護HD様は先週から継続角度が9pt低下。面談前に『採用数の乖離要因3点』をAIが下書き済み。カルテで承認すると議事メモに反映されます。", cta:"カルテで確認"},
  {id:"a2", accountId:5, text:"北斗ソフトウェア様は予算凍結で一時停止中。再開トリガー（次期予算確定月）をAIが10月と推定。10月頭のリマインド設定を提案します。", cta:"リマインド設定"}
];

/* -- 顧客カルテ: 議事録タイムライン（架空・accountIdごと） -------------- */
const MINUTES = {
  1: [
    {date:"2026-07-01", title:"月次定例", summary:"応募数は前月比+18%。採用単価も改善傾向。更新は前向き。", angle:83, aiDraft:false},
    {date:"2026-06-03", title:"月次定例", summary:"求人原稿のABテスト開始。母集団の質に課題感の共有。", angle:80, aiDraft:false},
    {date:"2026-05-07", title:"キックオフ振り返り", summary:"運用開始3ヶ月。トレタン運用に社内の理解が進む。", angle:78, aiDraft:false}
  ],
  2: [
    {date:"2026-07-15", title:"臨時MTG（温度感低下）", summary:"採用計画に対し実績が未達。先方役員から費用対効果への疑問。要改善提案。", angle:52, aiDraft:true, aiText:"AI下書き: ①媒体別の応募単価を並べ、閾値超過媒体を特定 ②改善済み施策の効果を数値で提示 ③次月の打ち手を2案提示（動画強化 / エリア拡大）"},
    {date:"2026-06-18", title:"月次定例", summary:"応募数は横ばい。介護職の母集団形成に苦戦。", angle:61, aiDraft:false},
    {date:"2026-05-20", title:"月次定例", summary:"運用体制の見直しを実施。担当を西村へ変更。", angle:64, aiDraft:false}
  ],
  5: [
    {date:"2026-07-10", title:"一時停止の連絡", summary:"下期予算の凍結により一時停止の申し出。関係性は良好。再開意向あり。", angle:41, aiDraft:true, aiText:"AI下書き: 再開条件を『次期予算確定（10月見込み）』と記録。停止中も四半期に1回の情報提供で接点維持を提案。"},
    {date:"2026-06-12", title:"月次定例", summary:"エンジニア採用は難航。単価の見直しを相談。", angle:48, aiDraft:false}
  ]
};

/* -- 統合受信箱 --------------------------------------------------------- */
const INBOX = [
  {id:"i1", kind:"承認", priority:"high", title:"ひまわり介護HD様 改善提案書の社内レビュー依頼", source:"Slack #cs-継続", due:"2026-07-24", accountId:2},
  {id:"i2", kind:"アラート", priority:"high", title:"北斗ソフトウェア様 継続角度が48→41に低下", source:"継続ジャッジ Flow", due:"2026-07-23", accountId:5},
  {id:"i3", kind:"タスク", priority:"mid", title:"青葉製作所様 更新見積の承認申請を提出", source:"My Day", due:"2026-07-25", accountId:1},
  {id:"i4", kind:"メンション", priority:"mid", title:"@高木 山彦建設様のキャンペーン、7月内に初稿ほしい", source:"Slack #sales", due:"2026-07-28", accountId:3},
  {id:"i5", kind:"アラート", priority:"mid", title:"すばる自動車販売様 応募単価が目標比+32%", source:"広告連携 bridge", due:"2026-08-05", accountId:9},
  {id:"i6", kind:"承認", priority:"low", title:"flowaフラワー様 EC連携見積の確認", source:"Slack #cs-継続", due:"2026-07-29", accountId:6},
  {id:"i7", kind:"タスク", priority:"low", title:"みなと海運様 競合比較資料の作成", source:"My Day", due:"2026-09-05", accountId:14},
  {id:"i8", kind:"メンション", priority:"low", title:"@高木 事例記事化、あかつき電設様の許諾状況は？", source:"Slack #marketing", due:"2026-09-12", accountId:13}
];

/* -- データソース台帳（KPIポップオーバー用） --------------------------- */
const KPI_META = {
  mrr:        {source:"Salesforce 更新ジャッジ__c / Account.mrr", updated:"2026-07-22 08:00 JST", def:"解約・一時停止を除く稼働中クライアントの月額合計（千円）。正本=Salesforce。"},
  pending:    {source:"Salesforce 更新ジャッジ__c", updated:"2026-07-22 08:00 JST", def:"当月が更新月で judgeResult 未入力のクライアント数。"},
  paused:     {source:"Salesforce 更新ジャッジ__c.paused", updated:"2026-07-22 08:00 JST", def:"一時停止中のクライアント数。翌月も自動でヒアリング対象に計上。"},
  danger:     {source:"Salesforce 更新ジャッジ__c.continuityAngle", updated:"2026-07-22 08:00 JST", def:"継続角度60未満のクライアント数（解約確定を除く）。"},
  churnRate:  {source:"Salesforce（直近3ヶ月の判定実績）", updated:"2026-07-22 08:00 JST", def:"直近判定のうち churn の比率（%）。低いほど良い。正本=Salesforce。"},
  renewalRate:{source:"Salesforce（直近3ヶ月の判定実績）", updated:"2026-07-22 08:00 JST", def:"直近判定のうち renew の比率（%）。高いほど良い。"}
};

/* ====================== MATERAS相当の会社機能（すべて架空） ====================== */

/* -- ニュース・お知らせ -------------------------------------------------- */
const NEWS = [
  {date:"2026-07-22", cat:"事例",    title:"株式会社青葉製作所様 採用成功事例を公開しました", body:"SNS採用運用6ヶ月で応募数+180%。事例記事を営業資料ライブラリに追加しました。提案時にご活用ください。", target:"全社"},
  {date:"2026-07-20", cat:"重要",    title:"セキュリティポリシー更新のお知らせ", body:"クライアントデータの取り扱い規程を改定しました。全員、今週中に一読のうえ確認ボタンを押してください。", target:"全社", mustRead:true},
  {date:"2026-07-18", cat:"新着",    title:"社内表彰制度「挑戦アワード」エントリー受付開始", body:"今期の挑戦事例を募集します。締切は8/8。自薦・他薦どちらも歓迎です。", target:"全社"},
  {date:"2026-07-15", cat:"人事",    title:"新メンバー入社のお知らせ（CS部）", body:"8月1日付でCS部に1名が入社します。オンボーディング担当は山田です。", target:"全社"},
  {date:"2026-07-12", cat:"イベント", title:"8月 全社AIキャンプ開催（8/22 終日）", body:"今期のAI活用テーマの共有と実践ワークショップ。会場は本社+オンライン併用です。", target:"全社"},
  {date:"2026-07-10", cat:"業務",    title:"継続ジャッジ運用フロー v2 を公開", body:"一時停止の扱いと確度低下アラートの運用を明文化しました。継続カレンダーのヘルプから参照できます。", target:"CS"}
];

/* -- 年間スケジュール（FY26: 2025-09〜2026-08） -------------------------- */
const YEAR_EVENTS = [
  {m:"2025-09", t:"期首キックオフ",        kind:"イベント"},
  {m:"2025-12", t:"忘年会・年末休暇",      kind:"休暇"},
  {m:"2026-01", t:"下期中間レビュー",      kind:"評価"},
  {m:"2026-03", t:"期末評価（下期）",      kind:"評価"},
  {m:"2026-04", t:"新体制スタート",        kind:"イベント"},
  {m:"2026-07", t:"上期 自己評価入力",     kind:"評価", now:true},
  {m:"2026-08", t:"期末・全社AIキャンプ",  kind:"イベント"}
];

/* -- ピープル（架空メンバー12名） ---------------------------------------- */
const MEMBERS = [
  {id:1,  name:"火村 誠",     dept:"経営",       role:"代表取締役",         skills:["経営戦略","アライアンス"],           loc:"東京",   boss:null},
  {id:2,  name:"山田 花子",   dept:"CS",         role:"CS部 マネージャー",   skills:["継続運用","カスタマーサクセス"],     loc:"東京",   boss:1},
  {id:3,  name:"高木 蓮",     dept:"セールス",   role:"フィールドセールス",  skills:["提案","クロージング"],               loc:"東京",   boss:1},
  {id:4,  name:"藤沢 迅",     dept:"セールス",   role:"インサイドセールス",  skills:["アポイント","リード育成"],           loc:"大阪",   boss:3},
  {id:5,  name:"西村 栞",     dept:"CS",         role:"カスタマーサクセス",  skills:["介護・医療業界","レポーティング"],   loc:"東京",   boss:2},
  {id:6,  name:"大川 湊",     dept:"CS",         role:"カスタマーサクセス",  skills:["建設・物流業界","更新交渉"],         loc:"東京",   boss:2},
  {id:7,  name:"三浦 このみ", dept:"マーケ",     role:"マーケティング",      skills:["広告運用","LP改善"],                 loc:"東京",   boss:1},
  {id:8,  name:"望月 るい",   dept:"マーケ",     role:"SNS運用",             skills:["ショート動画","企画"],               loc:"リモート", boss:7},
  {id:9,  name:"春日 陽向",   dept:"制作",       role:"動画クリエイター",    skills:["編集","撮影ディレクション"],         loc:"東京",   boss:1},
  {id:10, name:"白鳥 圭",     dept:"開発",       role:"AIエンジニア",        skills:["LLM活用","業務自動化"],              loc:"リモート", boss:1},
  {id:11, name:"東雲 咲",     dept:"コーポレート", role:"人事・採用",        skills:["採用","オンボーディング"],           loc:"東京",   boss:1},
  {id:12, name:"桐生 悠真",   dept:"コーポレート", role:"経理・管理",        skills:["経理","契約管理"],                   loc:"東京",   boss:1}
];

/* -- 評価・育成（架空） --------------------------------------------------- */
const EVAL_SELF = {period:"2026年上期", window:"2026-07-15 〜 2026-07-31", status:"未提出", due:"2026-07-31"};
const EVALS = [
  {period:"2025年下期", biz:82, bizRank:"A",  abil:76, abilRank:"B+", value:88, valueRank:"A", total:81, totalRank:"A",  by:"山田 花子", status:"確定"},
  {period:"2025年上期", biz:74, bizRank:"B+", abil:71, abilRank:"B",  value:80, valueRank:"A-", total:74, totalRank:"B+", by:"山田 花子", status:"確定"}
];
const MBO = [
  {goal:"担当クライアントの継続率 92% 達成",   weight:40, prog:78},
  {goal:"AI活用施策を月2件 実運用に載せる",     weight:30, prog:100},
  {goal:"顧客カルテ運用の定着（記入率90%）",    weight:30, prog:55}
];
const ANGLE_CHECKS = [
  {date:"2026-07-08", with:"山田 花子", memo:"継続ジャッジの精度が向上。次月は解約回避提案の型化に挑戦。"},
  {date:"2026-06-10", with:"山田 花子", memo:"介護業界の知見が強み。ナレッジ共有会での登壇を設定。"},
  {date:"2026-05-13", with:"山田 花子", memo:"業務量がやや過多。案件の一部を大川へ移管して調整。"}
];
const DEV_SHEETS = [
  {period:"FY26", template:"CSキャリア開発シート", status:"記入中", updated:"2026-07-15"},
  {period:"FY25", template:"CSキャリア開発シート", status:"確定",   updated:"2026-03-28"}
];

/* -- 採用（架空求人） ----------------------------------------------------- */
const JOBS = [
  {id:1, title:"カスタマーサクセス（採用SNS運用）", type:"正社員",     dept:"CS",      loc:"東京（リモート併用）", salary:"月給 30万〜45万円",
   desc:"採用SNS運用クライアントの継続支援・更新提案を担当。継続カレンダーとAIカルテを使った次世代のCS体制を一緒に作るポジションです。",
   points:["AIツールを全社員が日常利用","継続率を軸にした明確な評価","業界特化の深い知見が身につく"],
   reqs:["法人向け折衝経験 2年以上","採用・HR領域への興味","AIツールへの抵抗がないこと"]},
  {id:2, title:"フィールドセールス", type:"正社員", dept:"セールス", loc:"東京", salary:"月給 32万〜50万円＋インセンティブ",
   desc:"中小企業の経営者・人事責任者への採用ブランディング提案。リードはマーケが供給、クロージングに集中できます。",
   points:["商談はすべて録画・AI要約で振り返り","提案資料はAIが下書き","成果に応じた明確な報酬"],
   reqs:["無形商材の営業経験","経営者との折衝経験は歓迎"]},
  {id:3, title:"動画クリエイター（採用ショート動画）", type:"正社員／業務委託", dept:"制作", loc:"東京 or リモート", salary:"月給 28万〜42万円（委託は応相談）",
   desc:"採用向けショート動画の企画・撮影・編集。月間数十本の制作ラインをAI編集ツールと一緒に回します。",
   points:["AI編集パイプラインで単純作業を削減","企画から関われる","撮影機材・環境完備"],
   reqs:["動画編集の実務経験","ショート動画のトレンド理解"]},
  {id:4, title:"AIエンジニア（社内AI基盤）", type:"正社員", dept:"開発", loc:"リモート", salary:"月給 45万〜70万円",
   desc:"トレプロ社内のAI基盤（ポータル・自動化・エージェント）の開発。Salesforce連携やLLMパイプラインの設計から実装まで。",
   points:["全社員がユーザーの社内プロダクト","最新モデルを業務で常用","小さく作って早く出す文化"],
   reqs:["Web開発の実務経験 3年以上","LLM API活用の経験"]},
  {id:5, title:"人事・採用アシスタント", type:"アルバイト・パート", dept:"コーポレート", loc:"東京", salary:"時給 1,400円〜",
   desc:"面接日程の調整、候補者対応、入社準備のサポート。自社でも採用SNSを実践しているので、採用の最前線が学べます。",
   points:["週3日〜OK","採用実務の経験が積める"],
   reqs:["基本的なPC操作","丁寧なコミュニケーション"]}
];

/* -- 会議室（架空・トレプロ本社） ----------------------------------------- */
const ROOMS = [
  {id:"A", name:"会議室A", cap:6, sched:[{s:10,e:11.5,t:"営業定例",o:"高木 蓮"},{s:13,e:14.5,t:"ひまわり介護HD様 更新面談",o:"西村 栞"},{s:16,e:17,t:"継続ジャッジ 朝会振り返り",o:"山田 花子"}]},
  {id:"B", name:"会議室B", cap:4, sched:[{s:11,e:12,t:"採用面接（CS）",o:"東雲 咲"}]},
  {id:"C", name:"会議室C", cap:8, sched:[{s:10,e:13,t:"AIキャンプ準備WS",o:"白鳥 圭"},{s:15,e:16,t:"制作レビュー",o:"春日 陽向"}]},
  {id:"P1", name:"フォンブース1", cap:1, sched:[{s:14,e:15,t:"クライアント電話",o:"大川 湊"}]},
  {id:"P2", name:"フォンブース2", cap:1, sched:[]}
];
const ROOMS_NOW = 13.5; /* モック上の現在時刻 13:30 */

/* -- FAQ ------------------------------------------------------------------ */
const FAQS = [
  {q:"「保存する」ボタンが見当たらない", a:"継続カレンダーとカルテの操作は押した瞬間に保存されます（保存ボタンはありません）。判定の取り消しはカード内の「判定取消」から行えます。"},
  {q:"継続角度は何を基準に入力する？", a:"80以上=更新にポジティブな発言あり／60〜79=懸念はあるが対話継続中／60未満=明確なリスクあり。詳細は継続ジャッジ運用フローv2を参照してください。"},
  {q:"一時停止と解約の違いは？", a:"一時停止は請求を止めて関係を維持する状態で、翌月以降も自動でヒアリング対象に載ります。解約は契約終了の確定です。迷ったら独断にせず、担当マネージャーに相談してください。"},
  {q:"AI提案の根拠はどこで確認できる？", a:"カルテのAI提案カードに元になった議事録・数値へのリンクが表示されます。承認する前に必ず根拠を確認してください。"},
  {q:"表示している期が違う", a:"画面右上のユーザーメニューから対象期を切り替えられます（モックでは2026年上期固定です）。"},
  {q:"評価の確定ボタンが押せない", a:"自己評価がすべて入力済みで、1on1（アングルチェック）が今期1回以上記録されていることが確定の条件です。"}
];
