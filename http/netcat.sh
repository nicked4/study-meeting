# nc で TCP が確立できていることを確認する
nc -l 8000         # Terminal:1
nc localhost 8000  # Terminal:2
# 標準入力が接続先に渡されることを確認（双方向）

# port:8000 で立てて simple200.txt を返す
# Chrome からもアクセスできる（現状なぜかアクセスしようとした後に立てると接続に成功する（？））
nc -lk 8000 < simple200.txt
