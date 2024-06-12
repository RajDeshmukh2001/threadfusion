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
