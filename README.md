


# Steps to Run


# 1. Start the Backend

a. Start a localhost server

In the `Backend/` directory/folder run:

```
uvicorn main:app
```

This will create a server locally. By default the link is `localhost:8000`

You can test to see if it worked by going into the browser and typing in `localhost:8000/health`

b. Expose the localhost server to the internet. Currently using a temporary Cloudflared tunnel

In the `Backend/` directory/folder in a seperate terminal from the previous one:

```
cloudflared tunnel --url localhost:8000
```

# 2. Start the Frontend

In the `Frontend/` directory/folder

`npm run dev`

This requires Node.js to be installed.

https://nodejs.org/en/download

# 3. Upload the code to the ESP32

a. Make sure the connections are correct according to the code

## TFT + Touch Wiring

### TFT Display (SPI)

| TFT Pin | Microcontroller Pin |
|--------|---------------------|
| CS     | 10                  |
| DC     | 9                   |
| RST    | 8                   |
| MOSI   | 17                  |
| SCLK   | 18                  |
| MISO   | 16                  |
| VCC    | 3.3V / 5V           |
| GND    | GND                 |

---

### Touch Controller (SPI)

| Touch Pin | Microcontroller Pin |
|-----------|---------------------|
| CS        | 7                   |
| CLK       | 5                   |
| DIN       | 4                   |
| DO        | 11                  |
| VCC       | 3.3V / 5V           |
| GND       | GND                 |

b. open in arduino IDE and click run.