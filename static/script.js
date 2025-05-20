const alertBox = document.getElementById('alert');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const alarm = document.getElementById('alarm');

// تشغيل كاميرا المتصفح
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    alertBox.textContent = 'لا يمكن الوصول للكاميرا';
    alertBox.style.display = 'block';
  });

let isAlarmPlaying = false;

async function sendFrame() {
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(async function(blob) {
    const formData = new FormData();
    formData.append('file', blob, 'frame.jpg');
    try {
      const res = await fetch('/detect', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data.drowsy) {
        alertBox.textContent = 'الشخص نائم!';
        alertBox.style.display = 'block';
        if (!isAlarmPlaying) {
          alarm.currentTime = 0;
          alarm.play();
          isAlarmPlaying = true;
        }
      } else {
        alertBox.textContent = '';
        alertBox.style.display = 'none';
        if (isAlarmPlaying) {
          alarm.pause();
          alarm.currentTime = 0;
          isAlarmPlaying = false;
        }
      }
    } catch (e) {
      alertBox.textContent = 'خطأ في الاتصال بالسيرفر';
      alertBox.style.display = 'block';
      if (isAlarmPlaying) {
        alarm.pause();
        alarm.currentTime = 0;
        isAlarmPlaying = false;
      }
    }
  }, 'image/jpeg');
}

setInterval(sendFrame, 1000);
