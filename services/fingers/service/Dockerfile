FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -yyq
RUN apt-get install socat -yyq
RUN apt-get install expect -yyq
 
ADD --chown=root ./run.sh /run.sh
RUN chmod 777 /run.sh
ADD --chown=root ./velkomtuzeklabbaddi.kod ./velkomtuzeklabbaddi.kod
ADD --chown=root ./kumir2-run ./kumir2-run
RUN chmod 777 /kumir2-run

WORKDIR /

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork,keepalive", "EXEC:./run.sh"]
