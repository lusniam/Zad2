# Zadanie 2

1. W folderze simple-weather-app znajdują się pliki aplikacji, które są wykorzystywane w budowie obrazu.
2. Po nowym pushu z tagiem "v*" oznaczającym wersję aplikacji lub pullu na plikach plikach aplikacji zostanie zbudowany obraz kontenera, który zostanie wypchnięty do ghcr.io/lusniam/pawcho-zad2
3. Obraz jest sprawdzany w Trivy przed wypchnięciem, jeśli skan zakończy się niepowodzeniem, to obraz nie zostaje wypchnięty
4. Dla ułatwienia pobierania tworzony jest tag "latest", jednak analiza jest opierana na tagu "sha"
5. Dla ujednolicenia nazewnictwa zastosowana została zmienna "github.repository", która zawiera użytkownika i repozytorium, do którego został wypchnięty kod aplikacji
6. Wykorzystane są dwa buildery o różnych architekturach, aby pierwsze budowanie obrazu było jak najszybsze przez zminimalizowanie emulacji
7. Cache z pierwszego budowania jest przesyłany do oddzielnego taga, który zostanie wykorzystany przy budowaniu obrazu multi-architekturowego, gdzie emulacja będzie konieczna, jednak cały gotowy obraz z każdej architektury będzie już w cachu