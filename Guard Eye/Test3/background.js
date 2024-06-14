chrome.action.onClicked.addListener(async (tab) => {
    const input = prompt('Enter a string:');
    console.log("HIIII");
    const response = await fetch('http://localhost:8000/hello', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({input})
    });
    const data = await response.json();
    chrome.action.setBadgeText({text: data.output});
  });
  
  