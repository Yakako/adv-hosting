function checkHealth() {
  fetch("/api/health")
    .then(res => res.json())
    .then(data => {
      document.getElementById("health").innerText =
        JSON.stringify(data, null, 2);
    })
    .catch(err => alert("API not reachable"));
}

function addCar() {
  const brand = document.getElementById("brand").value;
  const model = document.getElementById("model").value;

  if (!brand || !model) {
    alert("Please enter brand and model");
    return;
  }

  fetch("/api/cars", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ brand, model })
  })
    .then(res => res.json())
    .then(() => {
      document.getElementById("brand").value = "";
      document.getElementById("model").value = "";
      loadCars();
    });
}

function loadCars() {
  fetch("/api/cars")
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("cars");
      list.innerHTML = "";

      data.forEach(car => {
        const li = document.createElement("li");
        li.innerText = `${car.id}. ${car.brand} - ${car.model}`;
        list.appendChild(li);
      });
    });
}