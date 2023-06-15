
var dropzone = document.getElementById('dropzone');

dropzone.addEventListener('dragenter', handleDragEnter, false);
dropzone.addEventListener('dragover', handleDragOver, false);
dropzone.addEventListener('dragleave', handleDragLeave, false);
dropzone.addEventListener('drop', handleDrop, false);

function handleDragEnter(e) {
  e.preventDefault();
  dropzone.classList.add('hover');
}

function handleDragOver(e) {
  e.preventDefault();
}

function handleDragLeave(e) {
  e.preventDefault();
  dropzone.classList.remove('hover');
}

function handleDrop(e) {
  e.preventDefault();
  dropzone.classList.remove('hover');

  var files = e.dataTransfer.files;
  if (files.length > 0) {
    var file = files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
      var img = document.createElement('img');
      img.src = e.target.result;
      img.classList.add('dropped-image');

      // Remove existing dropped images, if any
      var existingImages = dropzone.querySelectorAll('.dropped-image');
      for (var i = 0; i < existingImages.length; i++) {
        dropzone.removeChild(existingImages[i]);
      }

      dropzone.appendChild(img);
      dropzone.querySelector('.dropzone-text').style.display = 'none';
    };

    reader.readAsDataURL(file);
  }
}
