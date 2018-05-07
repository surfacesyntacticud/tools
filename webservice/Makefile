doc:
	@echo "make install  upload server code on grew.lchn.fr"
	@echo "make start    run server on grew.lchn.fr"
	@echo "make stop     fill server on grew.lchn.fr"
	@echo "make curl     test sendind a request to the server"

install:
	scp sud2ud_server.py ud2sud_server.py guillaum@grew.lchn.fr:/home/guillaum/webservice

stop:
	ssh guillaum@grew.lchn.fr "killall -r sud2ud_server && killall -r ud2sud_server"

start:
	ssh guillaum@grew.lchn.fr 'nohup webservice/sud2ud_server.py > /home/guillaum/webservice/sud2ud_std.out 2> /home/guillaum/webservice/sud2ud_std.err < /dev/null &'
	ssh guillaum@grew.lchn.fr 'nohup webservice/ud2sud_server.py > /home/guillaum/webservice/ud2sud_std.out 2> /home/guillaum/webservice/ud2sud_std.err < /dev/null &'

curl:
	curl -X POST --data-binary @./one.conll http://sud2ud.grew.fr

