# chatsovellus
Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

**Sovelluksen ominaisuudet**

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

**Sovelluksen nykyinen tilanne**

Sovelluksesta puuttuvat vielä seuraavat toiminnot:
- <s>Viimeksi lähetetyn viestin ajankohta</s>
- <s>Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.<s>
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- <s>Ylläpitäjä voi lisätä ja poistaa keskustelualueita.</s>
- <s>Ylläpitäjä voi luoda salaisen alueen</s> ja määrittää, keillä käyttäjillä on pääsy alueelle. (Toteutukselle luotu pohja tietokantaan)

HUOMIOITAVAA:
Sovelluksen ulkoasu on kesken. Tähän palautukseen keskityin saamaan toiminnallisuuksia eteenpäin. Jos sovelluksen tietokannan tyhjentää silloin kun olet kirjautunut sisään verkkosivulla, niin sovellus voi mennä sekaisin. Jos poistelet tietokantaa testaamisen aikana, niin kannattaa kirjautua ensin ulos.

**Käynnistysohjeet** **TÄRKEÄÄ SUORITTAA NÄMÄ OIKEASSA JÄRJESTYKSESSÄ!**

1. Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL="tietokannan-paikallinen-osoite"

SECRET_KEY="salainen-avain"

2. Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:

$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r ./requirements.txt

3. Määritä vielä tietokannan skeema komennolla:
$ psql < schema.sql

**HUOM!!!!! Tämä komento alustaa tietokannan tyhjillä tauluilla ja poistaa saman nimiset taulut, joten ole varovainen ettet tyhjennä omaa tietokantaasi. Ohjeet tämän estämiseksi https://hy-tsoha.github.io/materiaali/vertaisarviointi/**

4. Nyt voit käynnistää sovelluksen komennolla:
$ flask run

5. Avaa sovellus osoitteessa http://127.0.0.1:5000/

6. Sovellus tarjoaa mahdollisuuden kirjautua sisään. Painamalla linkkiä sovellus tarjoaa mahdollisuuden luoda uusi tunnus. **Voit luoda käyttäjän ylläpitäjän oikeuksilla testaamista varten antamalla käyttäjänimeksi "admin".** Luo uusi tunnus, jonka jälkeen palaat etusivulle.

**Jos haluat tietokantaan valmiiksi keskustelualueita ja ketjuja:**

7. Uuden tunnuksen luomisen jälkeen voit lisätä halutessasi tietokantaan valmiiksi muutaman keskustelualueen ja ketjun:
$ psql < test.sql

**HUOM!!!!! Tämä komento luo tietokantaan valmiiksi muutaman keskustelualueen ja ketjun. Tällä hetkellä koodi olettaa, että sovelluksessa on ainakin yksi käyttäjä ennen alueiden ja ketjujen luomista, joten on tärkeää tehdä tämä juuri tässä järjestyksessä. Jos teet kohdat 3-7 väärässä järjestyksessä, niin voit aina aloittaa uudestaan kohdasta 3.**

8. Päivitä tämän jälkeen nettisivu.

