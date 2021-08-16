# timelapse
a timelapse machine build in raspberry 

Uma máquina de gerar imagens para time-lapse. Há dois modos de funcionamento:

Uma detecta movimentos, e então começa a tirar fotos com intervalo periodíco.
Quanto não detecta mais movimentos para ded tirar fotos, renderiza o filme em uma thread nova e sobe o filme para o GoogleDrive.

No segundo caso, tira fotos apenas se detectar luz atravẽs da GPIO16, e tira fotos no perĩodo que estiver ligado.
Então com intervalo de tempo programado ele sobe as imagens para o GoogleDrive, e em outro PC ẽ possĩvel fazer o download e renderizar o vĩdeo
