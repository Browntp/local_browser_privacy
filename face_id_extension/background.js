chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Message received in background script');
  if (message.blobUrl) {
    console.log("Blob URL received:", message.blobUrl);
    
    fetch(message.blobUrl)
      .then(response => response.blob())
      .then(blob => {
        console.log("Blob fetched successfully");
        let formData = new FormData();
        formData.append('image', blob, `youtube_selfie_${Date.now()}.png`);
        
        return fetch('http://127.0.0.1:5000/upload-image', {
          method: 'POST',
          body: formData
        });
      })
      .then(response => response.json())
      .then(data => {
        console.log('Server response:', data);
        if (data.success && data.faces_detected > 0) {
          let message = `Detected ${data.faces_detected} face(s) in the picture!\n`;
          if (data.match_found) {
            message += `Match found! Recognized: ${data.recognized_faces.join(', ')}`;
          } else {
            message += "No match found. The face was not recognized.";
          }
          
          // Send a message to the content script to show an alert
          chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: "showAlert", message: message});
          });
        } else {
          console.log('No face detected');
          // Optionally, you can send a message to show an alert for this case too
          chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: "showAlert", message: "No face detected in the picture."});
          });
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        // Optionally, show an alert for errors
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {action: "showAlert", message: "An error occurred while processing the image."});
        });
      });
  }
});