zwaailicht Service
==================

De zwaailicht service is een REST API die op basis van de BAG+ en de WKPB pand-informatie verzamelt. 


Requirements
------------

* [docker-compose](https://docs.docker.com/compose/)


Developing
----------

	docker-compose up --build -d

De development server is nu beschikbaar op http://${DOCKER_HOST}:8000/


Mapping
-------

Voor het bijwerken van de mapping tussen BAG/WKPB/etc codes en de daadwerkelijke resultaten, wordt een mapping file aangeleverd in json.

De huidige mapping file is altijd te zien op /zwaailicht/mapping/

Vervangen door een nieuwe mapping is een kwestie van overschrijven van `web/zwaailicht/mapping.json`


Voorbeelden
-----------

Status pand: /zwaailicht/status_pand/0363010000941193/

Gebruik: /zwaailicht/gebruik/0363010000998532/

Bouwlagen: /zwaailicht/bouwlagen/0363010000747356/


