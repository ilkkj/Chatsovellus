# chatsovellus
Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Sovelluksen ominaisuudet

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki alueet, ketjut ja viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

HUOMIOITAVAA:
Jos sovelluksen tietokannan tyhjentää silloin kun olet kirjautunut sisään verkkosivulla, niin sovellus voi mennä sekaisin. Jos poistelet tietokantaa testaamisen aikana, niin kannattaa kirjautua ensin ulos.

# Käynnistysohjeet

## VAROITUS! seuraa näitä ohjeita tarkasti tietokannan alustamisessa tai voit vahingossa alustaa omaa tietokantaasi!

1\. Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
~~~
DATABASE_URL="tietokannan-paikallinen-osoite"
SECRET_KEY="salainen-avain"
~~~
2\. Seuraavaksi avaa terminaali, aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
~~~
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
~~~
3\. Avaa uusi terminaali ja käynnistä siellä tietokanta:
```
start-pg.sh
```
4\. Mene takaisin toiseen terminaali-ikkunaan ja kirjoita seuraavat komennot jotta oma tietokantasi ei vahingossa mene sekaisin:
```
psql
CREATE DATABASE <tietokannan-nimi>;
```
5\. Voit nyt määrittää projektin tietokantaskeeman omasta tietokannastasi erilliseen tietokantaan komennoilla:
```
\q
psql -d <tietokannan-nimi> < schema.sql
```
Määritä vielä tietokannan osoite projektille siten, että osoite päättyy luomasi tietokannan nimeen. Esimerkiksi, jos omalla sovelluksellasi osoite on muotoa postgresql:///user ja loit äsken uuden tietokannan nimeltä testi, tulisi uudeksi tietokannan osoitteeksi postgresql:///testi.

6\. Nyt voit käynnistää sovelluksen komennolla (samassa terminaalissa, jossa aktivoit virtuaaliympäristön):
~~~
flask run
~~~
Avaa sovellus osoitteessa http://127.0.0.1:5000/

7\. Sovellus tarjoaa mahdollisuuden kirjautua sisään. Painamalla linkkiä sovellus tarjoaa mahdollisuuden luoda uusi tunnus. **Voit luoda käyttäjän ylläpitäjän oikeuksilla testaamista varten antamalla käyttäjänimeksi "admin".** Luo uusi tunnus, jonka jälkeen palaat etusivulle.

## Jos haluat tietokantaan valmiiksi keskustelualueita ja ketjuja:
**Koodi olettaa, että sovelluksessa on ainakin yksi käyttäjä ennen alueiden ja ketjujen luomista, joten on tärkeää luoda käyttäjä ennen tämän ajamista**

8\. Uuden tunnuksen luomisen jälkeen voit lisätä halutessasi tietokantaan valmiiksi muutaman keskustelualueen ja ketjun:
~~~
psql -d <tietokannan-nimi> < test.sql
~~~
Jos teet kohdat 5-8 väärässä järjestyksessä, niin voit aina aloittaa uudestaan kohdasta 5.

9\. Päivitä tämän jälkeen nettisivu.

