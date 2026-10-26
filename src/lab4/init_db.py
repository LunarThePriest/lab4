import psycopg

DSN = "postgresql://postgres:postgres@localhost:5432/lab4_db"


def init_database() -> None:
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS beers;
                DROP TABLE IF EXISTS breweries;

                CREATE TABLE breweries (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    country VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                );

                CREATE TABLE beers (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(150) NOT NULL,
                    style VARCHAR(50) NOT NULL,
                    abv NUMERIC(3, 1) NOT NULL,
                    sku VARCHAR(20) UNIQUE NOT NULL,
                    brewery_id INT NOT NULL REFERENCES breweries(id) ON DELETE CASCADE
                );
            """)

            breweries_data = [
                ("Pravda Beer Theatre", "Ukraine", "info@pravda.beer"),
                ("Varvar Brew", "Ukraine", "contact@varvarbrew.com"),
                ("Underwood Brewery", "Ukraine", "hello@underwood.beer"),
                ("Guinness Brewery", "Ireland", "support@guinness.com"),
                ("BrewDog", "Scotland", "hello@brewdog.com"),
                ("Paulaner Brauerei", "Germany", "info@paulaner.de"),
                ("Pilsner Urquell", "Czech Republic", "info@pilsnerurquell.cz"),
                ("Chimay Brewery", "Belgium", "contact@chimay.be"),
            ]

            cur.executemany(
                "INSERT INTO breweries (name, country, email) VALUES (%s, %s, %s);",
                breweries_data,
            )

            styles = ["IPA", "Stout", "Pilsner", "Lager", "Sour", "Porter", "Wheat"]
            beers_data = []
            sku_counter = 1001

            for b_id in range(1, len(breweries_data) + 1):
                for idx, style in enumerate(styles, start=1):
                    title = f"Beer Special {style} #{b_id}-{idx}"
                    abv = 4.0 + (idx * 0.7)
                    sku = f"BEER-{sku_counter}"
                    beers_data.append((title, style, round(abv, 1), sku, b_id))
                    sku_counter += 1

            cur.executemany(
                "INSERT INTO beers (title, style, abv, sku, brewery_id) VALUES (%s, %s, %s, %s, %s);",
                beers_data,
            )

        conn.commit()
    print(
        f"База успішно ініціалізована: додано {len(breweries_data)} броварень та {len(beers_data)} сортів пива."
    )


if __name__ == "__main__":
    init_database()
