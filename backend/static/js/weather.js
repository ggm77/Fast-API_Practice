const API_KEY = "3bee41529d3cc0ca8ebd5360f6825b7e";
function onGeoOk(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  console.log("You live in", lat, lon);
  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const weather = document.querySelector("#weather span:first-child");
      const city = document.querySelector("#weather span:last-child");
      const degree = Math.floor(data.main.temp);
      city.innerText = data.name;
      weather.innerText = `${data.weather[0].main} ${degree}°C`;
    });
}
function onGeoError() {
  alert("can`t find you. No weather for you. ");
}

navigator.geolocation.getCurrentPosition(onGeoOk, onGeoError);
