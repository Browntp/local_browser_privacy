navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    alert("Get ready! The photo will be taken in 3 seconds.");
    
    setTimeout(() => {
      const video = document.createElement('video');
      video.srcObject = stream;
      video.play();
      
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      
      video.addEventListener('loadeddata', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        canvas.toBlob(blob => {
          const blobUrl = URL.createObjectURL(blob);
          
          // Send the blob URL to the background script
          chrome.runtime.sendMessage({ blobUrl: blobUrl });
          
          // Stop the webcam
          stream.getTracks().forEach(track => track.stop());
        }, 'image/png');
      });
    }, 3000);
  })
  .catch(err => {
    console.error("Error accessing webcam: ", err);
  });

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "showAlert") {
    alert(message.message);
  }
});