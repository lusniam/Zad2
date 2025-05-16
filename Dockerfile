# syntax=docker/dockerfile:1.5.2

# Etap 1: Budowanie aplikacji
FROM python:3.13-alpine AS builder

LABEL org.opencontainers.image.authors="Maciej Luśnia"

# Instalacja zależności
RUN --mount=type=cache,target=/root/.cache apk add binutils gcc musl-dev linux-headers libffi-dev libxml2-dev libxslt-dev curl git openssh

COPY simple-weather-app/ /app

WORKDIR /app

# Instalacja zależności aplikacji
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt pyinstaller

# Użycie sekretu do przekazania klucza API
RUN --mount=type=secret,id=api_key,dst=/app/api_key.txt \
    sed -i "s/API_KEY/$(cat /app/api_key.txt)/g" app.py

# Kompilacja aplikacji do pliku binarnego
RUN pyinstaller --noconfirm --clean --onefile \
    --add-data="templates/index.html:templates" \
    --add-data="templates/weather.html:templates" \
    app.py

# Etap 2: Tworzenie minimalnego obrazu
FROM scratch

# Kopiowanie zasobów aplikacji
ADD alpine-minirootfs-3.21.3-x86_64.tar.gz /
COPY --from=builder /app/dist/app /

# Ustawienie punktu wejścia
ENTRYPOINT ["/app"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost:8080/ || exit 1