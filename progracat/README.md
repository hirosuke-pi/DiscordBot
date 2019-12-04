# progracat
+ Python, Ruby, PHP, node.js, Perlの実行結果を返してくれるプログラムのネコです

## コマンド一覧

### Python

/py:
```py
print('hello')
```
> Pythonの実行結果をユーザー宛に返す。

/pyw:
```py
print('hello')
```
> Pythonの実行結果をそのまま返す。

### Ruby

/rb:
```rb
puts 'hello'
```
> Rubyの実行結果をユーザー宛に返す。

/rbw:
```rb
puts 'hello'
```
> Rubyの実行結果をそのまま返す。

### PHP

/php:
```php
echo 'hello';
```
> PHPの実行結果をユーザー宛に返す。

/phpw:
```php
echo 'hello';
```
> PHPの実行結果をそのまま返す。

### JavaScript

/js:
```js
console.log('hello');
```
> Node.jsの実行結果をユーザー宛に返す。

/jsw:
```js
console.log('hello');
```
> Node.jsの実行結果をそのまま返す。

### Perl

/pl:
```pl
print 'hello';
```
> Perlの実行結果をユーザー宛に返す。

/plw:
```pl
console.log('hello');
```
> Perlの実行結果をそのまま返す。

### トークコマンド(仮)

* /talk[:(文字数)]
> なにかしゃべる。30～600文字まで設定可能。

* /comp[:(ステートサイズ)]
> 言語データを再コンパイルする。1～9まで設定可能。

### その他コマンド

* /help
> ヘルプを表示。

* /timeout:<TIMEOUT_SECOND>
> 制限時間(秒)の設定。 10 ~ 600秒まで設定可能。

### コマンド注意事項
> :との間にスペースを入れると反応できない。


## 注意
+ サーバー内で実行するので、プログラムによってはサーバー内で悪影響を及ぼすかもしれません!
+ 実行制限するプログラムは入れてないので、実行するサーバーを考えてから実行してください!
