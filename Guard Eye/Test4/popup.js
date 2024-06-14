function sendInput() {
    const input = document.getElementById("input").value;
    const url = "http://localhost:5000/hello";
    const data = { name: input };
    
    fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(response => response.json())
    .then(data => {
      const message = data.message;
      const result = document.getElementById("result");
      result.innerHTML = message;
    })
    .catch(error => console.error(error));
  }
  
  document.getElementById("submit").addEventListener("click", sendInput);
  