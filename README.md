# ラインボット

## Setup

### 1. Line Bot Message API 環境の作成

まず LINE Developers コンソールで、Line Bot の Message API 環境を作成します。

Line Bot のアクセストークンは「Messaging API 設定」の "チャンネルアクセストークン（長期）" という欄にある "発行" というボタンを押すと発行されます。
Line Bot のシークレットは「チャネル基本設定」の画面にあります。
これらの値は、"3. デプロイ" で利用します。

### 2. Dialogflow の設定

#### 2.1 Dialogflow プロジェクト・エージェントの作成

Google Cloud Platform (GCP) のコンソールで、Dialogflow プロジェクトを作成します。
エージェントも 1 つ以上、作成します。

Dialogflow プロジェクトのプロジェクト ID を "3. デプロイ" で利用します。

#### 2.2 GCP 認証情報

Dialogflow の呼び出しに必要な認証情報をダウンロードして、src/lambda1/gcp-auth.json として置いてください。

このファイルがない場合、デプロイがエラーになります。

### 3. デプロイ

```bash
make make-venv
source venv/bin/activate
make
```

と入力してください。

その後、いくつかの質問がでます。

- `Stack Name [sam-app]:` 適当な名前を入力。
- `Parameter LineChannelAccessToken []:` 上で作成した Line Bot のアクセストークンを入力
- `Parameter LineChannelSecret []:` 上で作成した Line Bot のシークレットを入力
- `DialogflowProjectId []:` 上で作成した Dialogflow プロジェクトのプロジェクトIDを入力
- `EndPointFunction may not have authorization defined, Is this okay? [y/N]:` Y と入力

上記以外は、そのまま Enter で OK です。

また、うち間違えた場合は、後から手動で samconfig.toml を書き換えて修正することも可能です。

出力例
```bash
% make samconfig.toml
sam build
Building function 'EndPointFunction'
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Invoke Function: sam local invoke
[*] Deploy: sam deploy --guided

sam deploy --region ap-northeast-1 -g --no-execute-changeset

Configuring SAM deploy
======================

	Looking for samconfig.toml :  Not found

	Setting default arguments for 'sam deploy'
	=========================================
	Stack Name [sam-app]: linebot-test-stack-001
	AWS Region [ap-northeast-1]:
	Parameter StageTag [Prod]:
	Parameter LineChannelAccessToken []: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	Parameter LineChannelSecret []: xxxxxxxxxxxxxxxxxxxxx
	Parameter DialogflowProjectId []: xxxxxxxxxxxxxxx
	#Shows you resources changes to be deployed and require a 'Y' to initiate deploy
	Confirm changes before deploy [y/N]:
	#SAM needs permission to be able to create roles to connect to the resources in your template
	Allow SAM CLI IAM role creation [Y/n]:
	EndPointFunction may not have authorization defined, Is this okay? [y/N]: Y
	Save arguments to samconfig.toml [Y/n]:
```

### 4. Line Bot の WebHook 設定

ふたたび LINE Developers コンソールに行き、"Messaging API 設定" の画面で Webhook を設定します。

- "Webhokk URL" にデプロイ後に出てくる URL を設定
- "Webhokk の利用" を有効に切り替え
- "応答メッセージ", "あいさつメッセージ" を無効に設定 (ここが有効だとLine提供のデフォルトの応答になり、WebHook が呼び出されない)

以上で、Line Bot が動作するようになります。

### 更新時

更新時は

```bash
make
```

を実行してください。
