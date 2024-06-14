const input = prompt("Enter some data:");
fetch('/input', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({data: input})
})
