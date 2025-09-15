const API_KEY = "3597b64f37581e5dabd6fc08902ae36e"; // Replace with your OpenWeatherMap API key

async function getWeather() {
    const city = document.getElementById("city").value.trim();
    const weatherDiv = document.getElementById("weather");

    if (!city) {
        weatherDiv.innerHTML = "⚠️ Please enter a city name!";
        return;
    }

    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.cod != 200) {
            weatherDiv.innerHTML = `❌ City not found!`;
            return;
        }

        const temp = data.main.temp;
        const desc = data.weather[0].description;
        const humidity = data.main.humidity;
        const wind = data.wind.speed;
        const mainWeather = data.weather[0].main.toLowerCase();

        const icons = {
            "clear": "☀️",
            "clouds": "☁️",
            "rain": "🌧️",
            "drizzle": "🌦️",
            "thunderstorm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️",
            "fog": "🌫️"
        };

        const icon = icons[mainWeather] || "🌍";

        weatherDiv.innerHTML = `
            <h2>${icon} Weather in ${city}</h2>
            <p><b>Description:</b> ${desc}</p>
            <p><b>Temperature:</b> ${temp}°C</p>
            <p><b>Humidity:</b> ${humidity}%</p>
            <p><b>Wind Speed:</b> ${wind} m/s</p>
        `;

    } catch (err) {
        weatherDiv.innerHTML = "⚠️ Error fetching data!";
        console.error(err);
    }
}

