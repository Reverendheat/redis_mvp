# Trigger data refresh for Redis via FastAPI route.

FROM alpine:latest

RUN apk add --no-cache curl

RUN echo '0 * * * * curl -X POST http://api:8000/start' >> /etc/crontabs/root

CMD ["/usr/sbin/crond", "-f"]