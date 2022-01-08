# sensor_tower_dom (DOM version)

Web scraper that collects game information from SensorTower.com. This version scrapes data from DOM.

Spider scrapes for each game and platform the following metrics:

- Game name,
- Platform,
- Date scrapped,
- Sensor score,
- Visibility score,
- Internationalization score,
- Downloads,
- Revenue,
- List of keywords,
- Review breakdown (including Date, # of positive and # of negative reviews).

Run command: `scrapy crawl sensor_tower -a game_names='["Candy Crush Saga", "Star Trek Timelines"]'`

Output is stored in `output.jl` JSON Line file
