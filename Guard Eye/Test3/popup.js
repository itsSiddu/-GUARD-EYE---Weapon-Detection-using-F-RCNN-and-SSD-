chrome.action.getBadgeText({}, (text) => {
    const resultElement = document.getElementById('result');
    resultElement.textContent = text;
  });
  