document.addEventListener('DOMContentLoaded', () => {
    let close_toast = document.querySelector('#close-toast');
    let toast = document.querySelector('.toast-box');
    
    if (close_toast && toast) {
        close_toast.onclick = () => {
            toast.classList.add('hide');
            const redirectURL = close_toast.getAttribute('data-redirect');
            if (redirectURL) {
                window.location.href = redirectURL;
            }
        }
    }
})

Quill.register("modules/imageCompressor", imageCompressor);
Quill.register("modules/resize", window.QuillResizeModule);

class QuillWrapper {
    constructor(targetDivId, targetInputId, quillOptions) {
        this.targetDiv = document.getElementById(targetDivId);
        if (!this.targetDiv) throw 'Target div(' + targetDivId + ') id was invalid';

        this.targetInput = document.getElementById(targetInputId);
        if (!this.targetInput) throw 'Target Input id was invalid';

        this.quill = new Quill('#' + targetDivId, quillOptions);
        this.quill.on('text-change', () => {
            var delta = JSON.stringify(this.quill.getContents());
            var html = this.targetDiv.getElementsByClassName('ql-editor')[0].innerHTML;
            var data = {delta: delta, html: html};
            this.targetInput.value = JSON.stringify(data);
        });
    }
}
