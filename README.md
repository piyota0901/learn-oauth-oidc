# APIの認証と認可

- 認可
    
    ユーザーが特定のリソースにアクセス・操作できるかどうかを決定するプロセス

- 認証
    
    ユーザーの身元を検証するプロセス

## OAuth

OAuthはアクセス委任の標準プロトコル

![](./image.drawio.svg)

| 番号 | 説明                                                   | 操作のイメージ                                                 |
|----|------------------------------------------------------|---------------------------------------------------------|
| ①  | リソースオーナーがOauthフローを開始する。                              | ユーザーがアプリケーションの「Facebookから連絡先リストを取得する」ボタンを押すこと。          |
| ②  | アプリ（クライアント）は、認可サーバー（Facebook）に対して「リソースへのアクセス権」を要求する。 | アプリがFacebookに対して、Facebookの連絡先リストへのアクセス権を要求すること。         |
| ③  | 認可サーバーは「クライアントへのアクセス権の委譲」にういてリソースオーナーの意思を確認する。       | Facebookが「連絡先リストへのアクセス権をアプリに委譲すること」について、ユーザーの意思を確認すること。 |
| ④  | リソースオーナーはアクセス権の委譲について同意する。                           | 意思の確認についてOKボタンを押すこと。                                    |
| ⑤  | 認可サーバーはアクセス権が付与された証（アクセストークン）をアプリに発行する。              | Facebookがアプリにアクセストークンを発行すること。                           |
| ⑥  | アプリはアクセストークンをもってリソースへのアクセスが可能になる。                    | アプリがアクセストークンによってFacebookの連絡先リストにアクセスすること。               |

### 定義

OAuthは、ユーザーが他のWebサイトにある自分の情報へのアクセスをサードパーティーアプリケーションに許可できるオープン規格である。一般に、アクセスはトークンを発行することによって許可される。サードパーティーアプリケーションはそのトークンを使ってユーザー情報にアクセスする。

### フロー

アクセス条件に応じてユーザーに許可を与えるフローが4種類に分かれている。

- 認可コードフロー
- PKCEフロー
- クライアントクレデンシャルフロー
- 更新トークンフロー

#### 認可コードフロー

クライアントサーバーがシークレットを認可サーバーと交換することで署名URLを生成する。  
署名URLを使用してユーザーがログインすると、クライアントサーバーがアクセストークンと交換できるワンタイムコードを手に入れる。

**バックエンドでレンダリングされる従来のWebアプリケーションなど、コードが公開されないアプリケーションにのみ適している。**  
OAuth2.1では、PKCEフローとの組み合わせで使うことが推奨されている。

#### PKCEフロー

Proof of Key for Code Exchangeの略。  
モバイルアプリケーションやSPAなどコードが公開されるアプリケーションを保護するために設計された認可コードフローの拡張。

**ソースコードが公開される場合はシークレットも公開されるため、クライアントがシークレットを使うことはできない。**

1. クライアントが**コードベリファイア**と**コードチャレンジ**をリクエストに追加して認可サーバーに送信する。

    - コードベリファイア（シークレット）
    - コードチャレンジ（コードベリファイアをエンコードしたもの）

1. 認可サーバーは、クライアントがアクセストークンと交換できる**認可コード**を生成する。
アクセストークンを取得するには、クライアントが認可コードとコードチャレンジの両方を送信しなければならない。


PKCEフローでは、コードチャレンジのおかげで、認可コードインジェクション攻撃も阻止される。この攻撃では、悪意のあるユーザーが認可コードをインターセプトし、それを使ってアクセストークンを窃取する。PKCEフローにはセキュリティの利点があるため、サーバー側のアプリケーションでも推奨される。

#### クライアントクレデンシャルズフロー

サーバー間の通信を目的としている。アクセストークンを手に入れるためにシークレットが交換される。  
クライアントクレデンシャルズフローは、セキュアなネットワークを介してマイクロサービス間の通信を実現するのに適している。

#### 更新トークンフロー

クライアントが更新トークンを新しいアクセストークンと交換することができる。セキュリティ上の理由により、アクセストークンの有効期間は限られている。アクセストークンが期限切れになった後も、APIクライアントはAPIサーバーと通信出来なければならないことが多い。そこで新しいトークンを取得するために更新トークンフローを使う。

## OpenID Connect

OIDCは、OAuthをベースとして構築された本人確認のオープン規格。  
サードパーティーのIDプロバイダーを使用して、ユーザーがWebサイトに対して認証を行うことができる。  

OAuthをベースとしているため、前項の認可フローをどれでも使用することができる。  

OpenID Connectプロトコルを使用して認証を行うときには、IDトークンとアクセストークンの2種類のトークンを区別する。どちらもJWT形式で提供されるが目的が異なる。

| 項目       | 説明                                                                                            |
|----------|-----------------------------------------------------------------------------------------------|
| IDトークン   | ユーザーを識別するトークンであり、ユーザーの名前、電子メール、その他の個人情報を含む。IDトークンは身元確認にのみ使用され、ユーザーがAPIにアクセスできるかどうかの判断には使われない。 |
| アクセストークン | APIアクセスの検証に使用される。ユーザー情報は含まれておらず、ユーザーのアクセス権限に関する一連のクレームが含まれている。                                |

OpenID Connectの統合をサポートしているIDプロバイダーは、`/.well-known/openid-configuration`というエンドポイントを公開する。  
このエンドポイントは、APIコンシューマーに認証を行う方法とアクセストークンを取得する方法を伝えるもので、ディスカバリエンドポイントとも呼ばれる。

※ID トークンは何のためにあるのか？   
ユーザーが認証されたという事実とそのユーザーの属性情報を、捏造されていないことを確認可能な方法で、様々なアプリで利用するため。

## JWTの作り方

JWTの署名アルゴリズム

- RSA256

    秘密鍵と公開鍵のペアを使用してトークンに署名する

- HS256

    シークレットを使用してトークンを暗号化する

### RSA256

1. 秘密鍵と公開鍵を作成する
    ```bash
    $ openssl req -x509 -nodes -newkey rsa:2048 -keyout private_key.pem -out public_key.pem -subj "/CN=MyApp"
    $ ls
    ・・・ private_key.pem  public_key.pem ・・・
    ```

1. `jwt_generator.py`を実行する
    ```bash
    $ python jwt_generator.py
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgubXlhcHAuaW8vIiwic3ViIjoiYjU2N2RkOGYtNmJiNS00ZDJjLWI2NmYtYjE4MTZiNWQ0ZGMxIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDAwLyIsImlhdCI6MTczMDAyNDUyNi44NjYzMjQsImV4cCI6MTczMDAyNDgyNi44NjYzMjQsInNjb3BlIjoib3BlbmlkIn0.pu9qZoLS2SajYT2cbkain8BnVzFIA4T5NECfz6SM9doP6xoRiChxIqDEI71sMoTR8j5v_v-q9GA1vC0q3oiT2xhTPvVKu4-eJKn6cZjs3gY833OPBkDbhZtf2PTED-ny5irAskInJR6mxkB6Nu_O9_4J01EqXGLU9kAURpDsWhC2c8ZOaJgomQIeglXYp1gPoujELSYKQTFzUcgg7tG4-Xxe_pDZBeJxyR3Y94G-6zz8e0h2a-KHV-BBbwBV_DzWltt_6IO-Z36tWhRVtD5iARwJdnBcgnRB6DfBKr0qNBA1FQeaSAfUocMTQ-LeiNgFy7Xv_OAiMLXcf6cOqd6Exg
    ```

## JWTを検証する

- [jwt.io](https://jwt.io/)

1. 公開鍵を抽出する
    ```bash
    $ openssl x509 -pubkey -noout < public_key.pem > pubkey.pem
    ```

1. JWTを検証する
    ```bash
    $ python src/jwt_verification.py
    Please enter the JWT token: eyJhbGciOiJSUzI1・・・
    {'iss': 'https://auth.myapp.io/', 'sub': 'b567dd8f-6bb5-4d2c-b66f-b1816b5d4dc1', 'aud': 'my_audience', 'iat': 1730025445.803477, 'exp': 1730025745.803477, 'scope': 'openid'}
    ```

トークンが無効であれば例外が発生する
```bash
$ python src/jwt_verification.py 
Please enter the JWT token: XXXXX・・・
・
・
・
jwt.exceptions.InvalidAudienceError: Invalid audience
```

## Referece

- [OAuth Community Site](https://oauth.net/)

    OAuthの使用を詳しく理解するためのリソースが揃っている
