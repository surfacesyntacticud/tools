doc:
	@echo "make install  upload server code on grew.lchn.fr"
	@echo "make start    run server on grew.lchn.fr"
	@echo "make stop     fill server on grew.lchn.fr"
	@echo "make curl     test sendind a request to the server"

install:
	scp sud2ud_server.py guillaum@grew.lchn.fr:/home/guillaum/webservice

stop:
	ssh guillaum@grew.lchn.fr "killall -r sud2ud_server"

start:
	ssh guillaum@grew.lchn.fr 'nohup webservice/sud2ud_server.py > /home/guillaum/webservice/std.out 2> /home/guillaum/webservice/std.err < /dev/null &'

curl:
	curl -X POST --data-binary @./one.conll http://sud2ud.grew.fr

