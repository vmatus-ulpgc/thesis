name=capture_18042022
ss=333

raspistill -t 1000 -ss $ss -o ${name}_ss${ss}.jpeg
raspistill -t 1000 -ss 3333 -o ss3333.jpeg
raspistill -t 1000 -ss 33333 -o ss33333.jpeg
